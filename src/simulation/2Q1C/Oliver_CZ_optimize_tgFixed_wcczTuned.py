# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 11:02:08 2021

@author: JYW
"""
import matplotlib.pyplot as plt
#import numpy as np
from numpy import *
from qutip import *
from math import *
from scipy.optimize import minimize

qutip.settings.has_mkl=False

h_bar = 1.05457180013e-34	#[J·s]
kb = 1.3806485279e-23 	#[J/K]


dim_qc = 3
dim_q1 = 3              # number of levels of q1
dim_q2 = 3              # number of levels of q2




w1_max = 4.5 * 2*pi  #[GHz] zero flux w01 of q1
w2_max = 4.5 * 2*pi #[GHz] zero flux w01 of q2
wc_max = 6.3 * 2*pi #[GHz] zero flux w01 of q2
EC1 = 0.2 * 2*pi  #[GHz] EC of q1 (ECP = 4EC)
EC2 = 0.2 * 2*pi  #[GHz] EC of q2 (ECP = 4EC)
ECc = 0.15 * 2*pi
g12_max = 0.0062 *2*pi #q1(e-g)_q2(e-g) coupling strength
g1c_max = 0.085 *2*pi
g2c_max = 0.085 *2*pi

w1_idle = 4.43 * 2*pi
w2_idle = 4.48 * 2*pi
wc_idle = 5.6662 * 2*pi


w2_CZ = 4.5 * 2*pi
w1_CZ_pre = w2_CZ-EC2
wc_CZ_pre = 4.8 * 2*pi #[GHz]

########## calculate g_eff at w1_CZ_pre
d1c_CZ = w1_CZ_pre-wc_CZ_pre
d2c_CZ = w2_CZ-wc_CZ_pre
siga1c_CZ = w1_CZ_pre+wc_CZ_pre
siga2c_CZ = w2_CZ+wc_CZ_pre
g12_CZ = g12_max*sqrt(w1_CZ_pre*w2_CZ)/sqrt(w1_max*w2_max)
g1c_CZ = g1c_max*sqrt(w1_CZ_pre*wc_CZ_pre)/sqrt(w1_max*wc_max)
g2c_CZ = g2c_max*sqrt(w2_CZ*wc_CZ_pre)/sqrt(w2_max*wc_max)
g_eff_CZ = g12_CZ + 0.5*g1c_CZ*g2c_CZ*(1/d1c_CZ+1/d2c_CZ-1/siga1c_CZ-1/siga2c_CZ)

T_CZ_sudden = 2*pi/(2*sqrt(2)*abs(g_eff_CZ))

####### initial guess of t_ramp q1 and qc, and t_gate
# fixed parameters
r_cp = 0
tr_q = 0.01
tg = 70#2*T_CZ_sudden

#initial guess of parameters to be optimized
w1_CZ0 = w1_CZ_pre#(3.94+0.006865) * 2*pi
wc_CZ0 = wc_CZ_pre
tr0_c = 7

############################################

############################################

Nt = 400

###################################################
g12_idle = g12_max*sqrt(w1_idle*w2_idle)/sqrt(w1_max*w2_max)
g1c_idle = g1c_max*sqrt(w1_idle*wc_idle)/sqrt(w1_max*wc_max)
g2c_idle = g2c_max*sqrt(w2_idle*wc_idle)/sqrt(w2_max*wc_max)


####################################################
#################   Tuning parameter (filling factor) independet code
########  initial states #######
j1 = arange(0,dim_q1) #level indices of q1
j2 = arange(0,dim_q2) #level indices of q2
jc = arange(0,dim_qc) #level indices of q2
dim_tot = dim_q1*dim_q2*dim_qc #total dimension

    
############# operators in individual H-space  ###############
Iq1 = qeye(dim_q1)    # Identity matrix in q1's H-space 
Iq2 = qeye(dim_q2)    # Identity matrix in q2's H-space 
Iqc = qeye(dim_qc)    # Identity matrix in qc's H-space
sm1 = destroy(dim_q1) # c operator in q1's H-space
sm2 = destroy(dim_q2) # c operator in q2's H-space
smc = destroy(dim_qc) # c operator in q2's H-space
n1 = qdiags(j1, 0)
n2 = qdiags(j2, 0)
nc = qdiags(jc, 0)
Y1 = -1j*sm1+1j*sm1.dag()
Y2 = -1j*sm2+1j*sm2.dag()
Yc = -1j*smc+1j*smc.dag()
############# Extended operators in the whole H-space  ###############
sm1_ = tensor(sm1, Iqc ,Iq2)
sm2_ = tensor(Iq1, Iqc, sm2)
smc_ = tensor(Iq1, smc, Iq2)
n1_ = tensor(n1, Iqc, Iq2)
n2_ = tensor(Iq1, Iqc, n2)
nc_ = tensor(Iq1, nc, Iq2)
Y1_ = tensor(Y1, Iqc, Iq2)
Y2_ = tensor(Iq1, Iqc, Y2)
Yc_ = tensor(Iq1, Yc, Iq2)
Y1Y2_ = Y1_*Y2_
Y1Yc_ = Y1_*Yc_
Y2Yc_ = Y2_*Yc_

    
# q1的eigen frequency at idle
w1 = w1_idle
wj_q1 = (w1+EC1)*(j1+0.5)-EC1*(6*j1**2+6*j1+3)/12 #q1的eigen angular frequency
wj_q1 = wj_q1-wj_q1[0]  #Noramlied so that the ground state energy is 0


# q2的eigen frequency at idle
w2 = w2_idle
wj_q2 = (w2+EC2)*(j2+0.5)-EC2*(6*j2**2+6*j2+3)/12 #q2的eigen angular frequency
wj_q2 = wj_q2-wj_q2[0] #Noramlied so that the ground state energy is 0


# qc的eigen frequency at idle
wc = wc_idle
wj_qc = (wc+ECc)*(jc+0.5)-ECc*(6*jc**2+6*jc+3)/12 #qc的eigen angular frequency
wj_qc = wj_qc-wj_qc[0] #Noramlied so that the ground state energy is 0




########## time-independent part #######################
Hq1_idle = qdiags(wj_q1, 0) 
Hq2_idle = qdiags(wj_q2, 0) 
Hqc_idle = qdiags(wj_qc, 0) 
Hq1_idle_ = tensor(Hq1_idle, Iqc, Iq2) 
Hq2_idle_ = tensor(Iq1, Iqc, Hq2_idle) 
Hqc_idle_ = tensor(Iq1, Hqc_idle, Iq2) 
Hi12_idle_ = g12_idle*Y1Y2_
Hi1c_idle_ = g1c_idle*Y1Yc_
Hi2c_idle_ = g2c_idle*Y2Yc_
 

################ computational and + states ###################
s0_q1 = basis(dim_q1,0)
s1_q1 = basis(dim_q1,1)
sp_q1 = (basis(dim_q1,0) + basis(dim_q1,1))/sqrt(2)
s2_q1 = basis(dim_q1,2)

s0_q2 = basis(dim_q2,0)
s1_q2 = basis(dim_q2,1)
sp_q2 = (basis(dim_q2,0) + basis(dim_q2,1))/sqrt(2)
s2_q2 = basis(dim_q2,2)

s0_qc = basis(dim_qc,0)
s1_qc = basis(dim_qc,1)
sp_qc = (basis(dim_qc,0) + basis(dim_qc,1))/sqrt(2)
s2_qc = basis(dim_qc,2)


s000 = tensor(s0_q1,s0_qc,s0_q2) # 0 occupation
s001 = tensor(s0_q1,s0_qc,s1_q2) # 1 occupation
s100 = tensor(s1_q1,s0_qc,s0_q2) # 1 occupation
s010 = tensor(s0_q1,s1_qc,s0_q2) # 1 occupation  'leakage'
s101 = tensor(s1_q1,s0_qc,s1_q2) # 2 occupation
s110 = tensor(s1_q1,s1_qc,s0_q2) # 2 occupation  'leakage'  
s011 = tensor(s0_q1,s1_qc,s1_q2)# 2 occupation  'leakage'
s200 = tensor(s2_q1,s0_qc,s0_q2)# 2 occupation  'leakage'
s020 = tensor(s0_q1,s2_qc,s0_q2)# 2 occupation  'leakage'
s002 = tensor(s0_q1,s0_qc,s2_q2)# 2 occupation  'leakage'

########## Identity of 2q #########################
I44 = array(qeye(4))  


#################   solve the eigenstates of the idling 2q
H_idle = Hq1_idle_ + Hq2_idle_ + Hqc_idle_ + Hi12_idle_ + Hi1c_idle_ + Hi2c_idle_
evals, eket = H_idle.eigenstates()
    
############### Search dressed omputational states (eigenatets)
overlap_000 = []
overlap_001 = []
overlap_100 = []
overlap_010 = []
overlap_101 = []
overlap_110 = []
overlap_011 = []
overlap_200 = []
overlap_020 = []
overlap_002 = []
for ii in range(dim_tot):
    overlap_000.append(abs((s000.dag()*eket[ii]).full())) 
    overlap_001.append(abs((s001.dag()*eket[ii]).full()))
    overlap_100.append(abs((s100.dag()*eket[ii]).full()))
    overlap_010.append(abs((s010.dag()*eket[ii]).full()))
    overlap_101.append(abs((s101.dag()*eket[ii]).full()))
    overlap_110.append(abs((s110.dag()*eket[ii]).full()))
    overlap_011.append(abs((s011.dag()*eket[ii]).full()))
    overlap_200.append(abs((s200.dag()*eket[ii]).full()))
    overlap_020.append(abs((s020.dag()*eket[ii]).full()))
    overlap_002.append(abs((s002.dag()*eket[ii]).full()))
     
idx_000_ = overlap_000.index(max(overlap_000))
idx_001_ = overlap_001.index(max(overlap_001))
idx_100_ = overlap_100.index(max(overlap_100))
idx_010_ = overlap_010.index(max(overlap_010))
idx_101_ = overlap_101.index(max(overlap_101))
idx_110_ = overlap_110.index(max(overlap_110))
idx_011_ = overlap_011.index(max(overlap_011))
idx_200_ = overlap_200.index(max(overlap_200))
idx_020_ = overlap_020.index(max(overlap_020))
idx_002_ = overlap_002.index(max(overlap_002))

s000_ = eket[idx_000_]
s100_ = eket[idx_100_]
s010_ = eket[idx_010_]
s001_ = eket[idx_001_]
s110_ = eket[idx_110_]
s101_ = eket[idx_101_]
s011_ = eket[idx_011_]
s200_ = eket[idx_200_]
s020_ = eket[idx_020_]
s002_ = eket[idx_002_]
################################  Cost funtion ##################
def costfunc(x):
    tr_c = x[0]
    w1_CZ = x[1]
    wc_CZ = x[2]
    def w1_t(t,args=None):
        return w1_idle + 0.5*(w1_CZ-w1_idle)*(erf((t-0.5*tr_q)/(0.25*tr_q))-erf((t-tg+0.5*tr_q)/(0.25*tr_q)))
    
    
    def dw1_t(t, args=None):
        return w1_t(t)-w1_idle
    
    def w2_t(t,args=None):
        return w2_idle + 0.5*(w2_CZ-w2_idle)*(erf((t-0.5*tr_q)/(0.25*tr_q))-erf((t-tg+0.5*tr_q)/(0.25*tr_q)))
    
    
    def dw2_t(t, args=None):
        return w2_t(t)-w2_idle
    
    def wc_t(t,args=None):
        return wc_idle + 0.5*(wc_CZ-wc_idle)*(erf((t-0.5*tr_c)/(0.25*tr_c))-erf((t-tg+0.5*tr_c)/(0.25*tr_c)))
    
    
    def dwc_t(t, args=None):
        return wc_t(t)-wc_idle
    
          
    def g12_t(t, args=None):
        return g12_max*sqrt(w1_t(t)*w2_t(t))/sqrt(w1_max*w2_max)
    
    def dg12_t(t, args=None):
        return g12_t(t)-g12_idle
    
    
          
    def g1c_t(t, args=None):
        return g1c_max*sqrt(w1_t(t)*wc_t(t))/sqrt(w1_max*wc_max)
    
    def dg1c_t(t, args=None):
        return g1c_t(t)-g1c_idle
    
    def g2c_t(t, args=None):
        return g2c_max*sqrt(w2_t(t)*wc_t(t))/sqrt(w2_max*wc_max)
    
    def dg2c_t(t, args=None):
        return g2c_t(t)-g2c_idle
    
    tlist =  linspace(0,tg,Nt)  
    H_t = [[n1_, dw1_t], [nc_, dwc_t], [n2_, dw2_t], [Y1Y2_, dg12_t], [Y1Yc_, dg1c_t], [Y2Yc_, dg2c_t], Hq1_idle_, Hq2_idle_, Hqc_idle_, Hi12_idle_, Hi1c_idle_, Hi2c_idle_]
    # H_t = [[n1_, dw1_t], Hq1_idle_, Hq2_idle_, Hi_idle_]
    # res = sesolve(H_t, psi0, tlist)      
    U = propagator(H_t, tlist, c_op_list=[])
    Uf = U[-1]  # in computational bases
    Uf_in_eket = Uf.transform(eket) # in eket bases
    
    ###################### calculate additional single-qubit phases of 10 and 01
    gamma1 = -float(angle(s100_.dag()*Uf*s100_)-angle(s000_.dag()*Uf*s000_))
    gamma2 = -float(angle(s001_.dag()*Uf*s001_)-angle(s000_.dag()*Uf*s000_))
    
    
    ######### calculate conditional phase
    phase_control_0 = -float(angle(s100_.dag()*Uf*s100_)-angle(s000_.dag()*Uf*s000_))
    phase_control_1 = -float(angle(s101_.dag()*Uf*s101_)-angle(s001_.dag()*Uf*s001_))
    
    #################################################
    ##### projection of Uf onto 00 01 10 11 [0,1,3,4] subspace
    # Uf_array = array(Uf)
    # U44 = Uf_array[ix_([0,1,dim,dim+1],[0,1,dim,dim+1])]
    
    
    ##### projection of Uf onto 00_ 01_ 10_ 11_  dressed state subspace
    Uf_in_eket_array = array(Uf_in_eket)
    U44_in_eket = Uf_in_eket_array[ix_([idx_000_,idx_001_,idx_100_,idx_101_],[idx_000_,idx_001_,idx_100_,idx_101_])]
    
    
    
    I44 = array(qeye(4))
    cost_abs = sum(abs(abs(U44_in_eket)-abs(I44)))
    cost_phase = abs(e**(-1j*(phase_control_1-phase_control_0))-e**(-1j*(pi)))
        
    U_singleQ_z_rotation = diag([1,e**(-1j*gamma2),e**(-1j*gamma1),e**(-1j*(gamma1+gamma2))],0)
    U_singleQ_z_rotation_dag = U_singleQ_z_rotation.conj().T
    
    
    U44_in_eket_dag = U44_in_eket.conj().T
    U44_in_eket_pc = U_singleQ_z_rotation_dag@U44_in_eket
    U44_in_eket_pc_dag = U44_in_eket_pc.conj().T
    U_CZ = diag([1,1,1,-1],0)
    U_CZ_dag = U_CZ.conj().T
    F_ave_upc = (trace(U44_in_eket_dag@U44_in_eket)+abs(trace(U_CZ_dag@U44_in_eket))**2)/(4*(4+1))
    F_ave_pc = (trace(U44_in_eket_pc_dag@U44_in_eket_pc)+abs(trace(U_CZ_dag@U44_in_eket_pc))**2)/(4*(4+1))
    #########################################################################
    # return  float((1-r_cp)*cost_abs+r_cp*cost_phase)
    return abs(1-F_ave_pc)
    
    
      
######################################################



x0 = [tr0_c,w1_CZ0, wc_CZ0]
# bnds = ((tr_min,tr_max),(tg_min,tg_max))
Sol = minimize(costfunc, x0, method='Nelder-Mead')
# Sol = minimize(costfunc, x0, method='Powell')
print('(t_ramp_q,t_ramp_c,t_gate)=', [tr_q,Sol.x[0],tg],'(ns)')
print('wq1_CZ=', Sol.x[1]/2/pi,'(GHz)')
print('wqc_CZ=', Sol.x[2]/2/pi,'(GHz)')

# Sol = minimize(costfunc, x0, method='Nelder-Mead', bounds=bnds)
