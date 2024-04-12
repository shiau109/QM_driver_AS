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

w1_idle = 4.39 * 2*pi
w2_idle = 4.46 * 2*pi
wc_idle = 5.605 * 2*pi

w1_CZ = 4.30764959732671 *2*pi
w2_CZ = 4.5 * 2*pi
wc_CZ = 4.77 * 2*pi #[GHz]
########## calculate g_eff at CZ
d1c_CZ = w1_CZ-wc_CZ
d2c_CZ = w2_CZ-wc_CZ
siga1c_CZ = w1_CZ+wc_CZ
siga2c_CZ = w2_CZ+wc_CZ
g12_CZ = g12_max*sqrt(w1_CZ*w2_CZ)/sqrt(w1_max*w2_max)
g1c_CZ = g1c_max*sqrt(w1_CZ*wc_CZ)/sqrt(w1_max*wc_max)
g2c_CZ = g2c_max*sqrt(w2_CZ*wc_CZ)/sqrt(w2_max*wc_max)
g_eff_CZ = g12_CZ + 0.5*g1c_CZ*g2c_CZ*(1/d1c_CZ+1/d2c_CZ-1/siga1c_CZ-1/siga2c_CZ)

T_CZ_sudden = 2*pi/(2*sqrt(2)*abs(g_eff_CZ))


############### tr and tg : plug in the optimized t_ramp and t_gate
tr_q = 0.01
tr_c = 7.41140874345618#9.478772269211621#2.64
tg = 69.60676003160523#75.11200943143764#64.81713538126096#2.2*T_CZ_sudden

##############################################################
 
Nt = 400
Nt_eig = 1000
tlist =  linspace(0,tg,Nt)   
tlist_eig =  linspace(0,tg,Nt_eig) 
############################################


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
idx_000 = 0*dim_qc*dim_q2 + 0*dim_q2 + (0+1)*1 -1
idx_100 = 1*dim_qc*dim_q2 + 0*dim_q2 + (0+1)*1 -1
idx_010 = 0*dim_qc*dim_q2 + 1*dim_q2 + (0+1)*1 -1
idx_001 = 0*dim_qc*dim_q2 + 0*dim_q2 + (1+1)*1 -1
idx_110 = 1*dim_qc*dim_q2 + 1*dim_q2 + (0+1)*1 -1
idx_101 = 1*dim_qc*dim_q2 + 0*dim_q2 + (1+1)*1 -1
idx_011 = 0*dim_qc*dim_q2 + 1*dim_q2 + (1+1)*1 -1
idx_200 = 2*dim_qc*dim_q2 + 0*dim_q2 + (0+1)*1 -1
idx_020 = 0*dim_qc*dim_q2 + 2*dim_q2 + (0+1)*1 -1
idx_002 = 0*dim_qc*dim_q2 + 0*dim_q2 + (2+1)*1 -1
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

################  plot w1 or g  #########################
fig, axes = plt.subplots(1, 1, figsize=(8, 2))
axes.plot(tlist, [wc_t(t)/2/pi for t in tlist], "k")
axes.set_xlabel("Time (ns)", fontsize=16)
axes.set_ylabel(r'$\omega_c(t)$', fontsize=16)
# axes.set_ylim(0, 2)
fig.tight_layout()
#################################################

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
################ plot time evolution #################################
Us101t0 = U*s101_
 
c000_t = zeros(Nt) + 1j*zeros(Nt) #000_
c001_t = zeros(Nt) + 1j*zeros(Nt) #001_
c002_t = zeros(Nt) + 1j*zeros(Nt) #002_
c100_t = zeros(Nt) + 1j*zeros(Nt) #100_
c101_t = zeros(Nt) + 1j*zeros(Nt) #101_
c110_t = zeros(Nt) + 1j*zeros(Nt) #110_
c011_t = zeros(Nt) + 1j*zeros(Nt) #011_
c200_t = zeros(Nt) + 1j*zeros(Nt) #200_



for ii in range(Nt):
    c000_t[ii] = (s000_.dag()*Us101t0[ii]).full() 
    c001_t[ii] = (s001_.dag()*Us101t0[ii]).full() 
    c002_t[ii] = (s002_.dag()*Us101t0[ii]).full() 
    c100_t[ii] = (s100_.dag()*Us101t0[ii]).full() 
    c101_t[ii] = (s101_.dag()*Us101t0[ii]).full() 
    c110_t[ii] = (s110_.dag()*Us101t0[ii]).full() 
    c011_t[ii] = (s011_.dag()*Us101t0[ii]).full() 
    c200_t[ii] = (s200_.dag()*Us101t0[ii]).full() 
   

plt.rcParams.update({'font.size': 24})
fig, axes = plt.subplots(1, 1, sharex=True, figsize=(12, 8))

axes.plot(tlist,  abs(c101_t)**2, "b",
              linewidth=2, label="|101_>")

axes.plot(tlist,  abs(c002_t)**2, "r",
              linewidth=2, label="|002_>")

axes.plot(tlist,  abs(c001_t)**2, "g",
              linewidth=2, label="|001_>")

axes.plot(tlist,  abs(c100_t)**2, "k",
              linewidth=2, label="|100_>")

axes.plot(tlist,  abs(c110_t)**2, "g--",
              linewidth=2, label="|110_>")

axes.plot(tlist,  abs(c011_t)**2, "b--",
              linewidth=2, label="|011_>")

axes.plot(tlist,  abs(c200_t)**2, "r--",
              linewidth=2, label="|200_>")


# axes.plot(tlist,  abs(c002_t)**2+abs(c101_t)**2, "g",
#              linewidth=2, label="101 + 002") 
# axes[0].set_ylim(-0.08, 0.08)
axes.set_xlabel("Time (ns)", fontsize=28)
axes.set_ylabel("Population", fontsize=28)
axes.legend()
fig.tight_layout()
    
# ########### Calculate the instantaneous eigenstates |s101_(t)> and |s002_(t)>      
# ########### Also calculate <s101_(t)|state(t)> and  <s002_(t)|state(t)>
##### 101-002 Rabi in CZ 
s101t_Us101t0 = zeros(Nt) + 1j*zeros(Nt) #101_
s002t_Us101t0 = zeros(Nt) + 1j*zeros(Nt) #002_

##### other unwanted 2-excitation states 
s200t_Us101t0 = zeros(Nt) + 1j*zeros(Nt) #200_
s110t_Us101t0 = zeros(Nt) + 1j*zeros(Nt) #110_
s011t_Us101t0 = zeros(Nt) + 1j*zeros(Nt) #011_

################  eigenfreq
w101t = zeros(Nt)
w002t = zeros(Nt)
w001t = zeros(Nt)
w100t = zeros(Nt)

for ii in range(Nt):
    t = tlist[ii]
    w1 = w1_t(t)
    wj_q1 = (w1+EC1)*(j1+0.5)-EC1*(6*j1**2+6*j1+3)/12 #q1的eigen angular frequency
    wj_q1 = wj_q1-wj_q1[0]  #Noramlied so that the ground state energy is 0
    
    
    w2 = w2_t(t)
    wj_q2 = (w2+EC2)*(j2+0.5)-EC2*(6*j2**2+6*j2+3)/12 #q1的eigen angular frequency
    wj_q2 = wj_q2-wj_q2[0]
    
    
    wc = wc_t(t)
    wj_qc = (wc+ECc)*(jc+0.5)-ECc*(6*jc**2+6*jc+3)/12 #qc的eigen angular frequency
    wj_qc = wj_qc-wj_qc[0] #Noramlied so that the ground state energy is 0
    
    g12 = g12_t(t)
    g1c = g1c_t(t)
    g2c = g2c_t(t)
   
    ########## time-dependent H #######################
    Hq1_t = qdiags(wj_q1, 0) # q1 Hamiltonian in q1's H-space
    Hq1_t_ = tensor(Hq1_t, Iqc, Iq2) #Extended Hq1 in in the whole H-space
    
    ########## time-dependent H #######################
    Hq2_t = qdiags(wj_q2, 0) # q1 Hamiltonian in q1's H-space
    Hq2_t_ = tensor(Iq1, Iqc, Hq2_t) #Extended Hq1 in in the whole H-space
    
    ########## time-dependent H #######################
    Hqc_t = qdiags(wj_qc, 0) # q1 Hamiltonian in q1's H-space
    Hqc_t_ = tensor(Iq1, Hqc_t, Iq2) #Extended Hq1 in in the whole H-space
    
    ####################################################################
    Hi12_t_ = g12*Y1Y2_
    Hi1c_t_ = g1c*Y1Yc_
    Hi2c_t_ = g2c*Y2Yc_

    
    ########### calculate the the instantaneous eigenstates 
    Ht = Hq1_t_ + Hqc_t_+ Hq2_t_ + Hi12_t_ + Hi1c_t_ + Hi2c_t_
    evals_t, eket_t = Ht.eigenstates()
    
    ##### 101-002 Rabi in CZ
    s101_t = eket_t[idx_101_]
    s002_t = eket_t[idx_002_]
    s101t_Us101t0[ii] = (s101_t.dag()*Us101t0[ii]).full() #101_
    s002t_Us101t0[ii] = (s002_t.dag()*Us101t0[ii]).full() #002_
    
    ##### other unwanted 2-excitation states 
    s200_t = eket_t[idx_200_]
    s110_t = eket_t[idx_110_]
    s011_t = eket_t[idx_011_]
    s200t_Us101t0[ii] = (s200_t.dag()*Us101t0[ii]).full() #200_
    s110t_Us101t0[ii] = (s110_t.dag()*Us101t0[ii]).full() #110_
    s011t_Us101t0[ii] = (s011_t.dag()*Us101t0[ii]).full() #011_
    w101t[ii]=evals_t[idx_101_]
    w002t[ii]=evals_t[idx_002_]
    w100t[ii]=evals_t[idx_100_]
    w001t[ii]=evals_t[idx_001_]
    
##################   plot w101t w002t
fig, axes = plt.subplots(1, 1, sharex=True, figsize=(12, 8))

axes.plot(tlist,  w101t/2/pi, "b",
              linewidth=2, label=r'$\omega_{101}(t)$')

axes.plot(tlist,  w002t/2/pi, "r",
              linewidth=2, label=r'$\omega_{002}(t)$')

axes.plot(tlist,  (w001t+w100t)/2/pi, "--g",
              linewidth=2, label=r'$\omega_{100}(t)+\omega_{001}(t)$')

# axes[0].set_ylim(-0.08, 0.08)
axes.set_xlabel("Time (ns)", fontsize=24)
axes.set_ylabel("Frequency (GHz)", fontsize=24)
axes.legend()
fig.tight_layout()  

CZ_splitting = abs(w101t[200]-w002t[200])/2/pi

################  plot s11t_Us11t0 and s20t_Us11t0   #########################
fig, axes = plt.subplots(1, 1, sharex=True, figsize=(12, 8))

##### 101-002 Rabi in CZ
axes.plot(tlist,  abs(s101t_Us101t0)**2, "b",
              linewidth=2, label="|101_(t)>")

axes.plot(tlist,  abs(s002t_Us101t0)**2, "r",
              linewidth=2, label="|002_(t)>")

##### other unwanted 2-excitation states 
axes.plot(tlist,  abs(s200t_Us101t0)**2, "--b",
              linewidth=2, label="|200_(t)>")

axes.plot(tlist,  abs(s110t_Us101t0)**2, "--r",
              linewidth=2, label="|110_(t)>")

axes.plot(tlist,  abs(s011t_Us101t0)**2, "--g",
              linewidth=2, label="|011_(t)>")

# axes[0].set_ylim(-0.08, 0.08)

axes.set_xlabel("Time (ns)", fontsize=16)
axes.set_ylabel("Population", fontsize=16)
axes.legend()
fig.tight_layout()  
#########################################################



# ########### Double check the gamma1 and gamma2      
# ########### and calculate them in two-qubit rotating frame 
w_000_ = []
w_001_ = []
w_100_ = []

dt =   tlist_eig[1]-tlist_eig[0]
for ii in range(Nt_eig):
    t = tlist_eig[ii]
    w1 = w1_t(t)
    wj_q1 = (w1+EC1)*(j1+0.5)-EC1*(6*j1**2+6*j1+3)/12 #q1的eigen angular frequency
    wj_q1 = wj_q1-wj_q1[0]  #Noramlied so that the ground state energy is 0
    
    
    w2 = w2_t(t)
    wj_q2 = (w2+EC2)*(j2+0.5)-EC2*(6*j2**2+6*j2+3)/12 #q1的eigen angular frequency
    wj_q2 = wj_q2-wj_q2[0]
    
    
    wc = wc_t(t)
    wj_qc = (wc+ECc)*(jc+0.5)-ECc*(6*jc**2+6*jc+3)/12 #qc的eigen angular frequency
    wj_qc = wj_qc-wj_qc[0] #Noramlied so that the ground state energy is 0
    
    g12 = g12_t(t)
    g1c = g1c_t(t)
    g2c = g2c_t(t)
   
    ########## time-dependent H #######################
    Hq1_t = qdiags(wj_q1, 0) # q1 Hamiltonian in q1's H-space
    Hq1_t_ = tensor(Hq1_t, Iqc, Iq2) #Extended Hq1 in in the whole H-space
    
    ########## time-dependent H #######################
    Hq2_t = qdiags(wj_q2, 0) # q1 Hamiltonian in q1's H-space
    Hq2_t_ = tensor(Iq1, Iqc, Hq2_t) #Extended Hq1 in in the whole H-space
    
    ########## time-dependent H #######################
    Hqc_t = qdiags(wj_qc, 0) # q1 Hamiltonian in q1's H-space
    Hqc_t_ = tensor(Iq1, Hqc_t, Iq2) #Extended Hq1 in in the whole H-space
    
    ####################################################################
    Hi12_t_ = g12*Y1Y2_
    Hi1c_t_ = g1c*Y1Yc_
    Hi2c_t_ = g2c*Y2Yc_

    
    ########### calculate the the instantaneous eigenstates 
    Ht = Hq1_t_ + Hqc_t_+ Hq2_t_ + Hi12_t_ + Hi1c_t_ + Hi2c_t_
    evals_t, eket_t = Ht.eigenstates()
    
    
    
    w_000_.append(evals_t[idx_000_])
    w_001_.append(evals_t[idx_001_])
    w_100_.append(evals_t[idx_100_])
    
w_000_ = array(w_000_)
w_001_ = array(w_001_)
w_100_ = array(w_100_)


w_000_nor = w_000_-w_000_
w_001_nor = w_001_-w_000_
w_100_nor = w_100_-w_000_


cumulated_phase1 = sum(w_100_nor[0:-1]*dt)
cumalated_phase1_nor = cumulated_phase1-round(cumulated_phase1/2/pi)*2*pi


cumulated_phase2 = sum(w_001_nor[0:-1]*dt)
cumalated_phase2_nor = cumulated_phase2-round(cumulated_phase2/2/pi)*2*pi




# gamma1_in_q1_frame = sum((w_100_nor[0:-1]-w_100_nor[0])*dt)
# gamma1_in_q1_frame_nor = gamma1_in_q1_frame-round(gamma1_in_q1_frame/2/pi)*2*pi

# gamma2_in_q2_frame = sum((w_001_nor[0:-1]-w_001_nor[0])*dt)
# gamma2_in_q2_frame_nor = gamma2_in_q2_frame-round(gamma2_in_q2_frame/2/pi)*2*pi


idle_phase1 = w_100_nor[0]*tg
idle_phase1_nor = idle_phase1-round(idle_phase1/2/pi)*2*pi
gamma1_in_q1_frame_nor = gamma1-idle_phase1_nor

idle_phase2 = w_001_nor[0]*tg
idle_phase2_nor = idle_phase2-round(idle_phase2/2/pi)*2*pi
gamma2_in_q2_frame_nor = gamma2-idle_phase2_nor


# ################  plot w_01_nor   w_10_nor#########################
# fig, axes = plt.subplots(1, 1, sharex=True, figsize=(12, 8))
# axes.plot(tlist_eig,  w_01_nor/2/pi, "b",
#              linewidth=2, label="w_s01_t")

# # axes[0].set_ylim(-0.08, 0.08)
# axes.set_xlabel("Time (ns)", fontsize=16)
# axes.set_ylabel("Frequency", fontsize=16)
# axes.legend()
# fig.tight_layout()


# fig, axes = plt.subplots(1, 1, sharex=True, figsize=(12, 8))
# axes.plot(tlist_eig,  w_10_nor/2/pi, "r",
#              linewidth=2, label="w_s10_t")
# # axes[0].set_ylim(-0.08, 0.08)
# axes.set_xlabel("Time (ns)", fontsize=16)
# axes.set_ylabel("Frequency", fontsize=16)
# axes.legend()
# fig.tight_layout()

# #########################################################





print('cumulated phase 1 =', cumalated_phase1_nor,'(rad)')
print('cumulated phase 2 =', cumalated_phase2_nor,'(rad)')
print('gamma1=', gamma1,'(rad)')
print('gamma2=', gamma2,'(rad)')
print('gamma1 in q1 idle frame =', gamma1_in_q1_frame_nor,'(rad)')
print('gamma2 in q2 idle frame =', gamma2_in_q2_frame_nor,'(rad)')
print('Conditional phase=', (phase_control_1-phase_control_0),'(rad)')
print('Gate fidelity=', abs(F_ave_pc))
