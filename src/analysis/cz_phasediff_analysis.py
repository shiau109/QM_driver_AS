import numpy as np
import matplotlib.pyplot as plt
import xarray as xr

filename = r"C:\Users\quant\SynologyDrive\09 Data\Fridge Data\Qubit\20240905_DR3_5Q4C_0430#7\raw_data\20240925_202902_CZ_diff\q3q4_cz_phasediff_shot.nc"
dataset = xr.open_dataset(filename,engine='netcdf4', format='NETCDF4')
#cz_amp = dataset.coords["cz_amp"].values
#c_amp = dataset.coords["c_amp"].values
#cz_time = dataset.coords["cz_time"].values

threhold_q3 = 4.657e-05#2.615e-5#6.097e-5
threhold_q4 = 1.350e-04#8.246e-7
ro_element = "q4_ro" # target qubit readout
shot_num = 500
data = dataset[ro_element].values[0]
print(data.shape)

# population_gy = np.zeros((len(c_amp),len(cz_amp))) # ground state y-basis
# population_gx = np.zeros((len(c_amp),len(cz_amp))) # ground state x-basis
# population_ey = np.zeros((len(c_amp),len(cz_amp))) # excited state y-basis
# population_ex = np.zeros((len(c_amp),len(cz_amp))) # excited state x-basis

# phase_map = np.zeros((len(c_amp),len(cz_amp)))

# for i in range(shot_num):
#     for j in range(len(c_amp)):
#         for k in range(len(cz_amp)):
#             if data[i,j,k,0,0] >= threhold_q4:
#                 population_gy[j,k] += 1
#             if data[i,j,k,0,1] >= threhold_q4:
#                 population_gx[j,k] += 1
#             if data[i,j,k,1,0] >= threhold_q4:
#                 population_ey[j,k] += 1
#             if data[i,j,k,1,1] >= threhold_q4:
#                 population_ex[j,k] += 1

# population_gy = population_gy/shot_num
# population_gx = population_gx/shot_num
# population_ey = population_ey/shot_num
# population_ex = population_ex/shot_num

# for i in range(len(c_amp)):
#     for j in range(len(cz_amp)):
#         gy = -np.cos(2*np.arcsin(population_gy[i,j]**0.5))
#         gx = -np.cos(2*np.arcsin(population_gx[i,j]**0.5)) 
#         g_phi = np.arctan2(gx,gy)

#         ey = -np.cos(2*np.arcsin(population_ey[i,j]**0.5)) 
#         ex = -np.cos(2*np.arcsin(population_ex[i,j]**0.5)) 
#         e_phi = np.arctan2(ex,ey)

#         if abs((abs(g_phi-e_phi)-np.pi))<=0.1:
#             phase_map[i,j] = (abs(g_phi-e_phi)-np.pi)
#         else:
#            phase_map[i,j] = 0.1
#         if abs(abs(g_phi-e_phi)-np.pi) <0.1:
#             print(c_amp[i],cz_amp[j])
#             print((g_phi-e_phi))
#             print(g_phi,e_phi)
#             print(gy,gx)
#             print(gy**2+gx**2)
#             print(ey,ex)
#             print(ey**2+ex**2)
#             print(population_gy[i,j])
#             print("------------")
#         #print((g_phi-e_phi))



gy = (data[0]-threhold_q4)
gx = (data[1]-threhold_q4)
g_phi = np.arctan2(gx,gy)
print(g_phi)

"""
z_offset = 0.05
z = 0.22
period = 0.65
Ec = 200
fc = 6.13 + (-221+0.75+5-1.25-0.5-10.89-0.264+1.255-0.48+1.03-0.06-0.23-1.1-0.8+0.63-1.76)/1000
phi = np.pi/period*(z-z_offset)
J_max = (fc*1000 +Ec)**2/(8*Ec*np.cos(phi))
zc = np.arange(0.2-0.17, 0.2+0.05, 0.001)
fq = (8*Ec*J_max*np.cos(np.pi/period*(c_amp-z_offset)))**0.5 - Ec
z_offset2 = 0.07
z2 = 0.148
period2 = 0.78
Ec2 = 200
fc2 = 4.7648+1.205e-3-0.073e-3
phi2 = np.pi/period2*(z2-z_offset2)
J_max2 = (fc2*1000 +Ec)**2/(8*Ec*(np.cos(phi2)**2+0.3**2*np.sin(phi2)**2)**0.5)
zc2 = np.arange(0.2-0.17, 0.2+0.05, 0.001)
fq2 = (8*Ec*J_max2*(np.cos(np.pi/period2*(cz_amp-z_offset2))**2+0.3**2*np.sin(np.pi/period2*(cz_amp-z_offset2))**2)**0.5)**0.5 - Ec
"""

# fig,ax = plt.subplots()
# a1 = ax.pcolormesh(cz_amp,c_amp,phase_map,cmap='RdBu')
# ax.set_xlabel("q2 freq (MHz)")
# ax.set_ylabel("coupler freq (MHz)")
# plt.colorbar(a1, ax=ax,label="phase difference - pi")
# plt.show()