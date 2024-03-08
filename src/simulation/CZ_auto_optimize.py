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

dim = 4
dim_q1 = dim              # number of levels of q1
dim_q2 = dim              # number of levels of q2


w1_max = 4.458 * 2*pi  #[GHz] zero flux w01 of q1
w2_max = 3.591 * 2*pi #[GHz] zero flux w01 of q2
EC1 = 0.21 * 2*pi  #[GHz] EC of q1 (ECP = 4EC)
EC2 = 0.21 * 2*pi  #[GHz] EC of q2 (ECP = 4EC)
g_max  = 0.020 * 2 * pi  #q1(e-g)_q2(e-g) coupling strength
T_CZ_sudden = 2*pi/(2*sqrt(2)*g_max)
d_q112_q201 = 0.0 # 2*pi*0.001 [GHz]*2*pi

####### initial guess of t_ramp and t_gate
tr0 = 12
tg0 = 1.2*T_CZ_sudden + 2*tr0
############################################


Nt = 400
 
###################################################
ita1 = -EC1
w1_idle = w1_max
w2_idle = w2_max
g_idle = g_max*sqrt(w1_idle*w2_idle)/sqrt(w1_max*w2_max)


####################################################
#################   Tuning parameter (filling factor) independet code
########  initial states #######
j1 = arange(0,dim_q1) #level indices of q1
j2 = arange(0,dim_q2) #level indices of q2
dim_tot = dim_q1*dim_q2 #total dimension

    
############# operators in individual H-space  ###############
Iq1 = qeye(dim_q1)    # Identity matrix in q1's H-space 
Iq2 = qeye(dim_q2)    # Identity matrix in q2's H-space 
sm1 = destroy(dim_q1) # c operator in q1's H-space
sm2 = destroy(dim_q2) # c operator in q2's H-space
n1 = qdiags(j1, 0)
n2 = qdiags(j2, 0)
Y1 = -1j*sm1+1j*sm1.dag()
Y2 = -1j*sm2+1j*sm2.dag()
############# Extended operators in the whole H-space  ###############
sm1_ = tensor(sm1, Iq2)
sm2_ = tensor(Iq1, sm2)
n1_ = tensor(n1, Iq2)
n2_ = tensor(Iq1, n2)
Y1_ = tensor(Y1, Iq2)
Y2_ = tensor(Iq1, Y2)
Y1Y2_ = Y1_*Y2_
############### Individual parts of the total Hamiltonian in the whole H-space #########
# fr_max = 2*(w1_max+w2_max)/(2*pi)
# dt = (1/fr_max)/5
# N_time_step = 400
# t_list = arange(N_time_step+1)*dt


    
# q1的eigen frequency at flux filling factor=f1
w1 = w1_idle
wj_q1 = (w1+EC1)*(j1+0.5)-EC1*(6*j1**2+6*j1+3)/12 #q1的eigen angular frequency
wj_q1 = wj_q1-wj_q1[0]  #Noramlied so that the ground state energy is 0


# q2的eigen frequency at flux filling factor=f2
w2 = w2_idle
wj_q2 = (w2+EC2)*(j2+0.5)-EC2*(6*j2**2+6*j2+3)/12 #q2的eigen angular frequency
wj_q2 = wj_q2-wj_q2[0] #Noramlied so that the ground state energy is 0


########## time-independent part #######################
Hq1_idle = qdiags(wj_q1, 0) # q1 Hamiltonian in q1's H-space
Hq2_idle = qdiags(wj_q2, 0) # q2 Hamiltonian in q2's H-space
Hq1_idle_ = tensor(Hq1_idle, Iq2) #Extended Hq1 in in the whole H-space
Hq2_idle_ = tensor(Iq1, Hq2_idle) #Extended driving Hamiltonian of q1
Hi_idle_ = g_idle*Y1Y2_
####### define func   ######################
    
    


def costfunc(x):
    tr = x[0]
    tg = x[1]
    def w1_t(t, tr, tg, args=None):
        return w1_idle + 0.5*((w2_idle-ita1+d_q112_q201)-w1_idle)*(erf((t-0.5*tr)/(0.25*tr))-erf((t-tg+0.5*tr)/(0.25*tr)))
    
    
    def dw1_t(t, args=None):
        return w1_t(t, tr, tg)-w1_idle
          
    def g_t(t, args=None):
        return g_max*sqrt(w1_t(t, tr, tg)*w2_idle)/sqrt(w1_max*w2_max)
    
    def dg_t(t, args=None):
        return g_t(t)-g_idle
    tlist =  linspace(0,tg,Nt)  
    H_t = [[n1_, dw1_t], [Y1Y2_, dg_t], Hq1_idle_, Hq2_idle_, Hi_idle_]
    # H_t = [[n1_, dw1_t], Hq1_idle_, Hq2_idle_, Hi_idle_]
    # res = sesolve(H_t, psi0, tlist)      
    U = propagator(H_t, tlist, c_op_list=[])
    
    
    
    ###################### calculate additional single-qubit phases of 10 and 01
    Uf = U[-1]
    s0_q1 = basis(dim_q1,0)
    s1_q1 = basis(dim_q1,1)
    sp_q1 = (basis(dim_q1,0) + basis(dim_q1,1))/sqrt(2)
    
    s0_q2 = basis(dim_q2,0)
    s1_q2 = basis(dim_q2,1)
    sp_q2 = (basis(dim_q2,0) + basis(dim_q2,1))/sqrt(2)
    
    s00 = tensor(s0_q1,s0_q2)
    s01 = tensor(s0_q1,s1_q2)
    s10 = tensor(s1_q1,s0_q2)
    s11 = tensor(s1_q1,s1_q2)
    sp0 = tensor(sp_q1,s0_q2) #q1 in +state, q2(qc) in 0
    s0p = tensor(s0_q1,sp_q2) #q1 in 0, q2(qc) in + state
    sp1 = tensor(sp_q1,s1_q2) #q1 in +state, q2(qc) in 1
    s1p = tensor(s1_q1,sp_q2) #q1 in 1, q2(qc) in + state
    
    gamma1 = -float(angle(s10.dag()*Uf*s10)-angle(s00.dag()*Uf*s00))
    gamma2 = -float(angle(s01.dag()*Uf*s01)-angle(s00.dag()*Uf*s00))
    

    
    ### This also yeald the same results 
    # gamma1 = -float(angle(s10.dag()*Uf*sp0)-angle(s00.dag()*Uf*sp0))
    # gamma2 = -float(angle(s01.dag()*Uf*s0p)-angle(s00.dag()*Uf*s0p))
    
    
    ######### calculate conditional phase
    phase_control_0 = -float(angle(s10.dag()*Uf*sp0)-angle(s00.dag()*Uf*sp0))
    phase_control_1 = -float(angle(s11.dag()*Uf*sp1)-angle(s01.dag()*Uf*sp1))
    
    #################################################
    ##### projection of Uf onto 00 01 10 11 [0,1,3,4] subspace
    Uf_array = array(Uf)
    U44 = Uf_array[ix_([0,1,dim,dim+1],[0,1,dim,dim+1])]
    # U44 = Qobj(U44_)
    
    I44 = array(qeye(4))
    cost_abs = sum(abs(abs(U44)-abs(I44)))
    cost_phase = abs(e**(-1j*(phase_control_1-phase_control_0))-e**(-1j*(pi)))
    ##############################################################
    U_singleQ_z_rotation = diag([1,e**(-1j*gamma2),e**(-1j*gamma1),e**(-1j*(gamma1+gamma2))],0)
    U_singleQ_z_rotation_dag = U_singleQ_z_rotation.conj().T
    
    U44_dag = U44.conj().T
    U44_pc = U_singleQ_z_rotation_dag@U44
    U44_pc_dag = U44_pc.conj().T
    U_CZ = diag([1,1,1,-1],0)
    U_CZ_dag = U_CZ.conj().T
    F_ave_upc = (trace(U44_dag@U44)+abs(trace(U_CZ_dag@U44))**2)/(dim*(dim+1))
    F_ave_pc = (trace(U44_pc_dag@U44_pc)+abs(trace(U_CZ_dag@U44_pc))**2)/(dim*(dim+1))
    #########################################################################
    return  float(cost_abs+cost_phase)
    # return abs(1-F_ave_pc)
    
    
      
######################################################



x0 = [tr0, tg0]
# bnds = ((tr_min,tr_max),(tg_min,tg_max))
Sol = minimize(costfunc, x0, method='Nelder-Mead')
print('(t_ramp,t_gate)=', (Sol.x[0],Sol.x[1]),'(ns)')
# Sol = minimize(costfunc, x0, method='Nelder-Mead', bounds=bnds)
