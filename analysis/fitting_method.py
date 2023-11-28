import matplotlib.pyplot as plt
from pandas import DataFrame
from numpy import array, cos, random, max, min, arange, where, pi, inf, hstack, unique, ndarray, mean
from scipy.optimize import curve_fit
from sympy.solvers import solve
from sympy import Symbol, sympify

class math_eqns:

    def __init__(self):
        pass

    def cosine(x,A,c,k,b):
        '''
            return Acos(kx+b)
        '''
        return A*cos(2*pi*(k*array(x)+b))+c

    def linear(x,a,b,*args):
        '''
            return ax+b
        '''
        return a*x+b

def fake(x,f):
    
    # random parameters
    A = random.randint(70)*(-1)**(random.randint(2))/1000 # -0.07~0.07
    k = random.randint(10,40)/10 
    b = random.randint(0.8*min(x)*100,0.8*max(x)*100)/100
    c = random.randint(-100,100)/1000
    # noise scale
    noise = (1/40) * (max(f(x,A,c,k,b))-min(f(x,A,c,k,b)))

    noised = []
    for i in x:
        noised.append(f(i,A,c,k,b) + (random.randint(0,60)/10)*noise*(-1)**(random.randint(2)))
    return array(noised)

def theJudge(x,fit_paras):
    '''
        return the x value which has the minimal y.
    '''
    candi = where(math_eqns.cosine(x,*fit_paras) == min(math_eqns.cosine(x,*fit_paras)))[0][0]
    peaks = round(x[candi],3)

    return peaks

def sympyExpGener(popt,symbol,mode='linear'):
    """
        convert to sympy expression from a given fit parameters popt with a symbol 'x' or 'y' or 'z'. 
    """
    match mode:
        case "linear":
            return sympify(f"{popt[0]}*{symbol}+{popt[1]}")
        case _:
            return ""

def crossPoint_solver(popt1,popt2):
    '''
        expect 2 linear equations in function,\n
        return the cross point x value.
    '''
    x = Symbol('x')
    expre1 = sympyExpGener(popt1,'x')
    expre2 = sympyExpGener(popt2,'x')
    ans = solve(expre1-expre2,x)
    
    return float(ans[0])


def find_amp_minima(x:ndarray,amp_array:ndarray,mode:str='continuous'):
    """
        expect an amp exp result array with a amp x axis array to fit cosine function.\n
        return peak amp ratio in float.
    """
    match mode.lower():
        case 'continuous':
            boundaries = ((-0.1,-0.1,1,min(x)),(0.1,0.1,4,max(x)))
        case 'oneshot':
            boundaries = ()
        case _:
            boundaries = ()
    popt,_ = curve_fit(math_eqns.cosine,x,amp_array,maxfev=10000000)#
    peaks_loca = theJudge(x,popt)
    
    return peaks_loca, popt

# Call this to analyze amp exp data
def analysis_amp(x:ndarray,y1:ndarray,y2:ndarray):
    '''
        give 2 amp result arrays and x axis,\n return the avg amp ratio.
    '''
    minima1,_ = find_amp_minima(x,y1)
    minima2,_ = find_amp_minima(x,y2)

    return round(mean(array([minima1,minima2])),3)


# Call this to analyze DRAG ratio alpha exp data
def analysis_drag_a(x:ndarray,y1:ndarray,y2:ndarray,*args):
    popt1,_ = curve_fit(math_eqns.linear,x,y1,maxfev=1000000)
    popt2,_ = curve_fit(math_eqns.linear,x,y2,maxfev=1000000)
    ans = crossPoint_solver(popt1,popt2)

    if len(args) != 0:
        plt.plot(x,y1)
        plt.plot(x,math_eqns.linear(x,*popt1))
        plt.plot(x,y2)
        plt.plot(x,math_eqns.linear(x,*popt2))
        plt.scatter(ans,math_eqns.linear(ans,*popt1),marker='X',s=80)
        plt.title(f"alpha = {round(ans,3)}")
        plt.show()

    return ans


if __name__ == '__main__':
    test = input("test for: ")

    if test.lower() in ['amp','amplitude']:
        ### amp test
        for i in range(20):
            x = arange(start=0.95, stop=1.105, step=0.005)
            y = fake(x,math_eqns.cosine)
            plt.plot(x,y,label='Fake')
            peaks_loca, popt = find_amp_minima(x,y)

            plt.plot(x,math_eqns.cosine(x,*popt),label='fitted',c='green')
            
            plt.title(f"figure_{i},peaks={peaks_loca}")
            plt.scatter(peaks_loca,math_eqns.cosine(peaks_loca,*popt),c='red',marker='x',s=100)
            plt.xlabel('XYL ratio (π)')
            plt.legend()
            plt.show()
    else:
        ### drag alpha test
        for i in range(20):
            x = arange(start=-1.5, stop=1.5, step=0.1)
            y1 = fake(x,math_eqns.linear)
            y2 = fake(x,math_eqns.linear)
            analysis_drag_a(x,y1,y2,'plot')
    
    
    

