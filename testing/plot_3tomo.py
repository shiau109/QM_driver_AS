"""
# import numpy as np
# import matplotlib.pyplot as plt
# tomo_raw_data = np.load(r'testing/5Q_GHZ_5_4_3.npz', allow_pickle=True)# ["arr_0"].item()
# # tomo_data =
# for k, v in tomo_raw_data.items():
#     print(k, v.shape)
# # threshold = [2.007e-04, -5.748e-06, 1.421e-04]
# threshold = [-5.748e-06, 2.007e-04, 1.421e-04]

# q_names = ["rr5","rr4","rr3"]
# q_order = [5,4,3]


# tomo_data = {}

# for q_o, q_name in zip(q_order, q_names):
#     print(q_o, q_name, tomo_raw_data[q_name].shape)
#     tomo_data[q_name] = np.moveaxis(tomo_raw_data[q_name],1,-1)[q_o*2-2:q_o*2]


# bit_string = np.zeros(tomo_data[q_names[0]].shape[1:],dtype=int)

# total_count = tomo_data[q_names[0]].shape[-1]
# # plt.plot( r1_data[0][0][0],r1_data[1][0][0],'o')
# # plt.show()
# # plt.plot( r2_data[2][0][0],r2_data[3][0][0],'o')
# # plt.show()

# print( bit_string.shape )
# for q_i, label in enumerate(q_names):
#     q_address = len(q_names)-q_i-1
#     print( label, 2**q_address, tomo_data[label].shape, threshold[q_address] )
#     # ar_data = np.moveaxis(tomo_data[label],1,-1)
#     bit_string += (tomo_data[label][0] > threshold[q_i]).astype(int)*(2**q_address)
#     print(bit_string.shape)

# probability_tomo = np.zeros(tomo_data[q_names[0]].shape[1:-1]+(2**len(q_names),))
# print(probability_tomo.shape)
# for i in range(3):
#     ii = i-1
#     if ii<0:
#         ii=2
#     for j in range(3):
#         jj = j-1
#         if jj<0:
#             jj=2
#         for k in range(3):
#             kk = k-1
#             if kk<0:
#                 kk=2
#         # count_arr = np.unique(bit_string[i][j],return_counts=True)
#             count_arr = np.bincount(bit_string[i][j][k])
#             # print(count_arr, total_count, np.sum(count_arr))
#             probability_tomo[ii][jj][kk] = count_arr/float(total_count)
# print(probability_tomo.shape)


# from scipy.io import savemat
# savemat('3Q_tomo.mat',{"data":probability_tomo})
"""



import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat

# Load data from the mat file
data = loadmat('3Q_tomo.mat')

QSTd = data['data']

# QSTd = np.ones((3, 3, 3, 8)) / 8  # Uncomment if needed

# Initialize QSTd_ext
QSTd_ext = np.zeros((4, 4, 4, 8))
# Copy values from QSTd to QSTd_ext
QSTd_ext[0:3, 0:3, 0:3, :] = QSTd

# Generate additional data
QSTd_ext[3, 0:3, 0:3, :] = QSTd[0, 0:3, 0:3, :]
QSTd_ext[0:3, 3, 0:3, :] = QSTd[0:3, 0, 0:3, :]
QSTd_ext[0:3, 0:3, 3, :] = QSTd[0:3, 0:3, 0, :]
QSTd_ext[3, 3, 0:3, :] = QSTd[0, 0, 0:3, :]
QSTd_ext[3, 0:3, 3, :] = QSTd[0, 0:3, 0, :]
QSTd_ext[0:3, 3, 3, :] = QSTd[0:3, 0, 0, :]
QSTd_ext[3, 3, 3, :] = QSTd[0, 0, 0, :]

# Bit stream and tables
bit_stream = np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1],
                       [1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1]])

XYZ_table = np.zeros((2, 2, 3), dtype=complex)
XYZ_table[:, :, 0] = [[0, 1], [1, 0]]  # X
XYZ_table[:, :, 1] = [[0, 1j], [-1j, 0]]  # Y
XYZ_table[:, :, 2] = [[-1, 0], [0, 1]]  # Z

I = np.array([[1, 0], [0, 1]], dtype=complex)

# Initialize density matrix
lo = np.zeros((8, 8), dtype=complex)

# Loop over q1, q2, q3, and bs
for q1 in range(4):
    for q2 in range(4):
        for q3 in range(4):
            for bs in range(8):
                # Measurement matrices and eigenvalues
                if q1 == 3:
                    q1_M = I 
                    eig_q1_M = 1
                else:
                    q1_M = XYZ_table[:, :, q1]
                    eig_q1_M = (-1) ** (1 - bit_stream[bs, 0])

                if q2 == 3:
                    q2_M = I 
                    eig_q2_M = 1
                else:
                    q2_M = XYZ_table[:, :, q2]
                    eig_q2_M = (-1) ** (1 - bit_stream[bs, 1])

                if q3 == 3:
                    q3_M = I
                    eig_q3_M = 1 
                else:
                    q3_M = XYZ_table[:, :, q3]
                    eig_q3_M = (-1) ** (1 - bit_stream[bs, 2])

                # Tensor product and update density matrix
                q1q2q3_M = np.kron(q1_M, np.kron(q2_M, q3_M))
                eig_q1q2q3_M = eig_q1_M * eig_q2_M * eig_q3_M
                lo += eig_q1q2q3_M * QSTd_ext[q1, q2, q3, bs] * q1q2q3_M

# Normalize density matrix
lo /= 2**3

# Plot the result

from qutip.visualization import matrix_histogram_complex
matrix_histogram_complex( lo, ["|0>","|1>","|2>","|3>","|4>","|5>","|6>","|7>"],["|0>","|1>","|2>","|3>","|4>","|5>","|6>","|7>"], limits=[0,0.5] )

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# _x = np.arange(8)
# _y = np.arange(8)
# _xx, _yy = np.meshgrid(_x, _y)
# x, y = _xx.ravel(), _yy.ravel()
# top = x + y
# print(top.shape)
# print(lo.shape)
# ax.bar3d(x, y, np.zeros(64), 0.8, 0.8, np.abs(lo).ravel())


plt.show()






