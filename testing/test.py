# import xarray as xr

# # Assume ds1, ds2, and ds3 are xarray.Dataset objects you have previously created or loaded
# ds1 = xr.Dataset()
# datasets = [ds1, ds2, ds3]

# # Merging the datasets
# merged_dataset = xr.merge(datasets)
# # Concatenating datasets along a new dimension (e.g., 'time')
# concatenated_dataset = xr.concat(datasets, dim='time')
# # Now, merged_dataset is a single xarray.Dataset containing all the data from ds1, ds2, and ds3
# print(merged_dataset)

import os
import xarray as xr
from numpy import array, std, average, round, max, min, transpose, abs, sqrt, cos, sin, pi, linspace, arange
import matplotlib.pyplot as plt 
from matplotlib.ticker import FuncFormatter
from src.exp.relaxation_time import fit_T1

def zgate_T1_fitting(dataset:xr.Dataset):
    
    time = dataset.coords["time"].values
    flux = dataset.coords["z_voltage"].values

    T1s = []
    
    for ro_name, data in dataset.data_vars.items():
        signals = data.values[0]
        
        for zDepData in data.values[0]:
            
            try:
                T1s.append(round(fit_T1(time,zDepData)[0]*1e-3,1))
            except:
                T1s.append(1e-6)
            
    return time/1000, flux, T1s, signals

def inver(lis:list):
    return 1/array(lis)

def FqEqn(x,Ec,coefA,d):
    """
    a ~ period, b ~ offset, 
    """
    a = pi/0.175
    b = 0.08
    return sqrt(8*coefA*Ec*sqrt(cos(a*(x-b))**2+d**2*sin(a*(x-b))**2))-Ec


dir_path = r"/Users/ratiswu/Downloads/Send Anywhere (2024-04-18 11-06-13)"

# list to store files
res = []

# Iterate directory
for path in os.listdir(dir_path):
    # check if current path is a file
    if os.path.isfile(os.path.join(dir_path, path)):
        res.append(os.path.join(dir_path,path))



sets = []
for file in res:
    sets.append(xr.open_dataset(file))








ref_z = 0.08

T1 = []
I_chennel = []
for dataset in sets:
    
    # for dataset in sub_set:
    time, bias, T1s, Isignal = zgate_T1_fitting(dataset)
    T1.append(T1s)
    I_chennel.append(Isignal)


avg_I_data = average(array(I_chennel),axis=0)
z = bias+ref_z


# Fit t1 with the whole averaging I signal
T1_1 = []
for zDepData in avg_I_data:
    T1_1.append(round(fit_T1(time*1e3,zDepData)[0]*1e-3,1))


avg_T1 = average(array(T1),axis=0)
std_T1_percent = round(std(array(T1),axis=0)*100/avg_T1,1)
fig, ax = plt.subplots(5,1,figsize=(12.5,22))

ax[0].pcolormesh(z,time,transpose(avg_I_data),cmap='RdBu')
ax[0].scatter(z,avg_T1,s=3,label='$T_{1}$',c='#0000FF')
ax[0].scatter(z,T1_1,s=3,label='$T_{1}$',c='#FF00FF')
ax[0].vlines([0.035],0,50,colors='black',linestyles="--",label='Fq=4.4GHz')
ax[0].vlines([0.08],0,50,colors='orange',linestyles="--",label='Fq=5.3GHz')
 
# ax[0].set_xlabel("bias (V)")
ax[0].set_ylabel("Free Evolution time(µs)") 
ax[0].set_ylim(0,50)
ax[0].set_title("$T_{1}$ vs Z-bias, in 10 average")
ax[0].legend(loc='lower left')

rate = inver(avg_T1)
ax[1].scatter(z,rate,s=3)
ax[1].vlines([0.035],0,max(rate),colors='black',linestyles="--")
ax[1].vlines([0.08],0,max(rate),colors='orange',linestyles="--")

# ax[1].set_xlabel("bias (V)")
ax[1].set_ylabel("$\Gamma_{1}$ (MHz)") 
ax[1].set_ylim(1/50,1/5)
ax[1].set_xlim(min(z),max(z))
ax[1].set_title("$\Gamma_{1}$ vs Z-bias, in 10 average")

ax[2].plot(z,std_T1_percent)
# ax[2].set_xlabel("bias (V)")
ax[2].set_ylabel("STD Percentage (%)")
ax[2].set_title("STD vs Z-bias, in 10 average")
ax[2].vlines([0.035],0,100,colors='black',linestyles="--")
ax[2].vlines([0.08],0,100,colors='orange',linestyles="--")
ax[2].set_ylim(0,100)
ax[2].set_xlim(min(z),max(z))




dataset = xr.open_dataset(r"/Users/ratiswu/Downloads/Send Anywhere (2024-04-18 15-20-12)/flux_resonator_q1_z_20240415_1538.nc")
for ro, data in dataset.data_vars.items():

    amp = data[0] + 1j*data[1]
    freq = (dataset.coords["frequency"].values+5762)/1000
    flux = dataset.coords["flux"].values
    ax[3].pcolormesh(flux,freq,abs(amp),cmap='RdBu')
    ax[3].set_xlim(min(z),max(z))
    ax[3].set_ylim(5.7525,5.765)
    ax[3].set_ylabel("Frequency (GHz)")
    ax[3].set_title("Flux dependent Cavity")
    ax[3].vlines([0.035],min(freq),max(freq),colors='black',linestyles="--")
    ax[3].vlines([0.08],min(freq),max(freq),colors='orange',linestyles="--")




from scipy.optimize import curve_fit 


d = 0.6
Ec = 0.3 #GHz
Ej_sum = 25
init = (Ec,Ej_sum,d)
up_b = (0.31,50,1)
lo_b = (0.29,15,0)
dataset = xr.open_dataset(r"/Users/ratiswu/Downloads/Send Anywhere (2024-04-18 15-20-12)/flux_resonator_q1_z_20240415_1538.nc")
for ro, data in dataset.data_vars.items():

    amp = data[0] + 1j*data[1]
    flux = dataset.coords["flux"].values
    flux = linspace(min(flux),max(flux),10000)

    p, e = curve_fit(FqEqn,[0.035,0.08],[4.4,5.3],p0=init,bounds=(lo_b,up_b))

    fq = FqEqn(flux,*p)
    ax[4].plot(flux,fq)
    ax[4].set_title(f"Ec={round(p[0],3)} GHz, Ej={round(p[1],1)} GHz, d={round(p[2],2)}")
    ax[4].vlines([0.035],min(fq),max(FqEqn(array([0.035]),*p)),colors='black',linestyles="--")
    ax[4].vlines([0.08],min(fq),max(FqEqn(array([0.08]),*p)),colors='orange',linestyles="--")
    ax[4].set_xlim(min(z),max(z))
    ax[4].set_xlabel("bias (V)")
    ax[4].set_ylabel("$f_{q}$ (GHz)")
    ax[4].set_title("Flux dependent Transition Frequency")


  

plt.tight_layout()
# plt.savefig("/Users/ratiswu/Downloads/ZgateT1_welldone_part2.png")
# plt.show()
plt.close()


min_fq = min(fq)
max_fq = max(fq)
a = FqEqn(array([0.035]),*p)
b = FqEqn(array([0.08]),*p)

x_value = FqEqn(z,*p)

fq1 = []
fq12 = []
fq2 = []
for i in range(z.shape[0]):
    if z[i] < 0.08:
        fq1.append(i)
    elif z[i] > 0.08:
        fq2.append(i)
    else:
        fq12.append(i)

fq = []
gamma = []
sd = []
if len(fq1)>=len(fq2):
    fq1_ = fq1[(len(fq1)-len(fq2)):]
    fq1_.reverse()
    fq2 = fq2[1:]
    a = []
    for idx in range(len(fq2)):
        fq_l = FqEqn(array([z[fq1_[idx]]]),*p)[0]
        fq_r = FqEqn(array([z[fq2[idx]]]),*p)[0]
        a = (fq_l-fq_r)*100/((fq_l+fq_r)/2)
        if abs(a) < 1e-9: # 1Hz
            fq.append(fq_l)
            
            sd.append((std_T1_percent[fq1_[idx]]+std_T1_percent[fq2[idx]])/2)








# fq = x_value
gamma = rate
# sd = std_T1_percent


fig ,ax = plt.subplots(2,1,)
ax[0].scatter(x_value,gamma,s=3)

ax[0].set_ylabel("$\Gamma_{1}$ (MHz)") 
ax[0].set_ylim(1/50,1/5)
ax[0].set_title("$\Gamma_{1}$ vs Transition frequency, in 10 average")
ax[0].set_xlabel("Transition Frequency (GHz)")
ax[0].vlines([4.4],0,max(gamma),colors='black',linestyles="--",label='Fq=4.4GHz')
ax[0].vlines([5.3],0,max(gamma),colors='orange',linestyles="--",label='Fq=5.3GHz')
ax[0].legend(loc='upper left')

ax[1].plot(fq,sd)
ax[1].set_ylabel("STD Percentage (%)")
ax[1].set_title("STD vs Transition frequency, in 10 average")
ax[1].vlines([4.4],0,100,colors='black',linestyles="--")
ax[1].vlines([5.3],0,100,colors='orange',linestyles="--")
ax[1].set_ylim(0,100)
ax[1].set_xlabel("Transition Frequency (GHz)")




plt.tight_layout()
# plt.savefig("/Users/ratiswu/Downloads/ZgateT1_welldone_part3.png")
plt.close()


from numpy import ndarray, asarray

def find_nearest_idx(array, value):
    array = asarray(array)
    idx = (abs(array - value)).argmin()
    return idx

def give_Z_plotT1(z:list,flux_ary:ndarray,time:ndarray,Isignals:ndarray):
    """
    z is a list contains what bias T1 you want to see,\n
    Isignals.shape = (flux, evoTime)
    """
    fig, ax = plt.subplots(len(z),1)
    for idx in range(len(z)):
        z_idx = find_nearest_idx(flux_ary, z[idx])
        target_data = Isignals[z_idx]
        T1, func = fit_T1(time,target_data)
        ax[idx].scatter(time,target_data)
        ax[idx].plot( time, func(time), label=f"{z[idx]}: T1={round(T1,1)}µs")
        ax[idx].legend(loc='upper right')
    plt.xlabel("Evolution time (µs)")
    plt.ylabel("I chennel (mV)")
    plt.show()


give_Z_plotT1([0.08,0.06,-0.02],z,time,avg_I_data)