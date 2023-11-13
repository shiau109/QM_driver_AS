
### Symbolic approximations for error###
from sympy import symbols, Matrix, N, refine, Q, expand, simplify, series,re, collect, nsimplify, solve
from sympy.physics.quantum.dagger import Dagger
from sympy.matrices.expressions import Trace
import matplotlib.pyplot as plt
from numpy import array, sqrt, matrix, pi, absolute,mean
from numpy.random import randint as R
# define the error evaluation symbol, 'a' for amplitude, 'd' for detuning 
identity = array([[1,0],[0,1]])
pauli_x = array([[0,1],[1,0]])
pauli_y = array([[0,-1j],[1j,0]])
pauli_z = array([[1,0],[0,-1]])

allXY_seq = [
    "I,I",
    "X,X",
    "Y,Y",
    "X,Y",
    "Y,X",
    "X/2,I",
    "Y/2,I",
    "X/2,Y/2",
    "Y/2,X/2",
    "X/2,Y",
    "Y/2,X",
    "X,Y/2",
    "Y,X/2",
    "X/2,X",
    "X,X/2",
    "Y/2,Y",
    "Y,Y/2",
    "X,I",
    "Y,I",
    "X/2,X/2",
    "Y/2,Y/2",
]

def chop(x):
    if abs(x)<1e-10:
        return 0
    else:
        return x

def U_sym(theta,op):
    u = -1j*theta*Matrix(op)*0.5
    return u.exp()

def give_rho_sym():
    rho = Matrix(identity+pauli_z)*0.5
    operation = U_sym(0,Matrix(identity))
    return Dagger(operation)*rho*operation

def tr(mtx):
    return Trace(mtx).simplify()

def ZProjector_sym(operation):
    return N(Trace(operation*give_rho_sym()*Dagger(operation)*Matrix(pauli_z)).doit())




def allXY_operator_sym(A,f,tg,xscale):
    """A:amplitude, f:detuning, tg:gate time"""
    operation_delta = -2*pi*f*tg*Matrix(pauli_z)
    z_projection = {}
    for pulse_1 in ["X","Y","X/2","Y/2"]:
        for pulse_2 in ["I","X","Y","X/2","Y/2"]:
            if len(pulse_1) == 1:
                if pulse_1 == "X":
                    operation_1 = U_sym(pi,A*xscale*pauli_x+operation_delta/pi)
                else:
                    operation_1 = U_sym(pi,A*pauli_y+operation_delta/pi)
            else:
                if pulse_1 == "X/2":
                    operation_1 = U_sym(pi/2,A*xscale*pauli_x+operation_delta/(pi/2))
                else:
                    operation_1 = U_sym(pi/2,A*pauli_y+operation_delta/(pi/2))
            
            if len(pulse_2) == 1:
                if pulse_2 == "X":
                    operation_2 = U_sym(pi,A*xscale*pauli_x+operation_delta/pi)
                elif pulse_2 == "Y":
                    operation_2 = U_sym(pi,A*pauli_y+operation_delta/pi)
                else:
                    operation_2 = U_sym(pi,identity+operation_delta/pi)
            else:
                if pulse_2 == "X/2":
                    operation_2 = U_sym(pi/2,A*xscale*pauli_x+operation_delta/(pi/2))
                else:
                    operation_2 = U_sym(pi/2,A*pauli_y+operation_delta/(pi/2))
            z_projection[pulse_1+","+pulse_2] = ZProjector_sym(operation_1*operation_2)
        
    z_projection["I,I"] =  ZProjector_sym(U_sym(pi,identity+operation_delta/pi)*U_sym(pi,identity+operation_delta/pi))
    
    sorted_proj = {}
    
    try: #numerical
        for OP in allXY_seq:
            sorted_proj[OP] = N(z_projection[OP],chop=True)
    except: #symbolic
        sorted_proj = z_projection # doing...
    
    return sorted_proj

# define give the cost function, doing...
def cos_func(expre_dict,symbol):
    a = symbols("a", real=True)
    d = symbols("d", real=True)
    if symbol == 'a':
        amp_dep = expre_dict["X/2,Y"] # so far good
        
        amp_expre = 0.8*nsimplify(series(refine(re(amp_dep),Q.real(a)).expand(),n=2).removeO().evalf(),tolerance=1e-10,rational=True)
        return amp_expre
    elif symbol == 'd':
        detune_dep = expre_dict["Y/2,X/2"]
        detune_expre = 0.8*nsimplify(re(collect(series(refine(refine(detune_dep,Q.positive(d)),Q.real(d)).expand().simplify(),n=2),d).removeO()),tolerance=1e-10,rational=True)
        return detune_expre
    else:
        raise ValueError("Check the symbol in the expressions! 'a' for amplitude, 'd' for detuning.")

# def extract the features from allXY experiment and calc the next step
def detuning_optimizer(detune_expre,detune_feat):
    d = symbols("d", real=True) # detuning error
    ans = solve(N(detune_expre)-detune_feat, d, dict=True)
    if "re(d)" in array(list(ans[0])).astype(str):
        if absolute(ans[0][re(d)]) < 10: # absolute detune error should < 10MHz
            next_detune = float(ans[0][re(d)])
        else:
            print(f"detuning solutions={ans}")
            next_detune = "no solutions!"
        return next_detune
    elif "d" in array(list(ans[0])).astype(str):
        if absolute(ans[0][d]) < 15: # absolute detune error should < 10MHz
            next_detune = float(ans[0][d])
        else:
            print(f"detuning solutions={ans}")
            next_detune = "no solutions!"
        return next_detune
    else:
        print(f"detuning solutions={ans}")
        raise ValueError("No real solution in detuning dependences searching!")

def amplitude_optimizer(amp_expre,amp_feat):
    a = symbols("a", real=True) # amplitude error
    ans = solve(N(amp_expre)-amp_feat, a, dict=False)
    try:
        ans_idx = list(absolute(ans)).index(min(absolute(ans)))
        if absolute(ans[ans_idx]) <= 0.26: # absolute amplitude error should < 2dB
            amp_modify = -float(ans[ans_idx])
        else:
            print(f"Amplitude solutions={ans}")
            amp_modify = "no solutions in boundaries!"
        return amp_modify
    except:
        print(f"Amplitude solutions={ans}")
        raise ValueError("Error when search a solution in amplitude dependences.")
        
# allXY simulations with optimizer        
# def AllXY_optimizer_simula(amp_error,detuning,exp_1st,amp_feat,detune_feat):
#     print("Strat Optimizing AllXY: ")
#     exp_record = {"0":exp_1st}
#     amp_record = [amp_error]
#     a_error = amp_error
#     next_detune = detuning
#     detune_record = [detuning]
#     i = 1
#     while abs(a_error)>1e-2 or abs(next_detune)>2e-2:
#         print(f"Now the {i} iteration...")
#         try:
#             amp_modify =  chop(amplitude_optimizer(amp_expre,amp_feat))  
#             a_error += amp_modify
#         except:
#             raise ValueError("Amplitude no solution!")
#         try:
#             next_detune = chop(detuning_optimizer(detune_expre,detune_feat))
#         except:
#             raise ValueError("Detuning no solution!")

#         experimental = allXY_operator_sym(A=1+a_error,f=next_detune*1e6,tg=gateTime,xscale=1)
#         amp_record.append(a_error)
#         detune_record.append(next_detune)
#         exp_record[str(i)] = experimental
#         amp_feat = (experimental["Y,X/2"]+experimental["X/2,Y"])/2
#         detune_feat = (experimental["Y/2,X/2"]-experimental["X/2,Y/2"])/2
#         if i > 9:
#             print("Ierations maximum reached!")
#             break
#         i += 1
#     return exp_record, amp_record, detune_record, i-1

'''On machine'''
def get_costfuncs(gateTime_ns):
    """get the cost functions for amp and detune based on a given gate time"""
    a = symbols("a", real=True)
    d = symbols("d", real=True)
    gateTime = gateTime_ns * 1e-9 
    amp_expre = cos_func(expre_dict=allXY_operator_sym(A=1+a,f=0,tg=gateTime,xscale=1),symbol='a')
    print(f"amp expre = {amp_expre}")
    detune_expre = cos_func(expre_dict=allXY_operator_sym(A=1,f=d*1e6,tg=gateTime,xscale=1),symbol='d')
    print(f"detune expre = {detune_expre}")
    theoretical = allXY_operator_sym(A=1,f=0,tg=gateTime,xscale=1)
    return {"amp":amp_expre,"detune":detune_expre}, theoretical



def result_arranger(exp_results):
    allXY_seq = [
    "I,I",
    "X,X",
    "Y,Y",
    "X,Y",
    "Y,X",
    "X/2,I",
    "Y/2,I",
    "X/2,Y/2",
    "Y/2,X/2",
    "X/2,Y",
    "Y/2,X",
    "X,Y/2",
    "Y,X/2",
    "X/2,X",
    "X,X/2",
    "Y/2,Y",
    "Y,Y/2",
    "X,I",
    "Y,I",
    "X/2,X/2",
    "Y/2,Y/2",
    ]
    # change the unit from continuous Voltage to probability normalize to [-1,1]
    norm = []

    for i in exp_results:
        norm.append(2*(i-min(exp_results))/(max(exp_results)-min(exp_results))-1)


    res = {}
    for op_idx in range(len(allXY_seq)):
        res[allXY_seq[op_idx]] = norm[op_idx]
    return res

# AllXY optimizer on QM
def AllXY_nextstep_teller(res,cost_funcs):
    """res is a array ordered by the AllXY_seq ordering\n
       cost_funcs is a dict with key: 'amp', 'detune'
    """
    
    # calc the experimental error
    amp_feat = (res["Y,X/2"]+res["X/2,Y"])/2
    detune_feat = (res["Y/2,X/2"]-res["X/2,Y/2"])/2
    amp_modify_ratio =  chop(amplitude_optimizer(cost_funcs['amp'],amp_feat))
    detune_modify = -chop(detuning_optimizer(cost_funcs['detune'],detune_feat)) #MHz
    
    return amp_modify_ratio, detune_modify





