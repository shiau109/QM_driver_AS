import numpy as np
import 
def fake_ramsey( f_q, f_range, decoherence_time, evo_time, noise_ratio  ):


    data = []
    for f in f_range:
        noise = np.random.rand(evo_time.shape[-1])
        detuning = f -f_q
        data.append( damping_osc(evo_time, detuning, decoherence_time)+noise_ratio*noise)


    return np.array(data)

def damping_osc( x, freq, tau ):
    return np.exp(-x/tau)*np.cos(freq*2*np.pi*x)

if __name__ == '__main__':
    f_points = 50
    f_range = np.linspace( 4.08, 4.11, f_points)
    decoherence_time = 2000 
    evo_time = np.arange( 10, 2000, 4)
    f_q = 4.1

    fake_data = fake_ramsey( f_q, f_range, decoherence_time, evo_time, 0.1)
    print(fake_data.shape)
    import matplotlib.pyplot as plt
    plt.pcolor(f_range, evo_time, fake_data.transpose())
    plt.show()

