import matplotlib.pyplot as plt
from pandas import DataFrame
from numpy import array, cos, random, max, min, arange, where, pi, inf, hstack, unique
from scipy.optimize import curve_fit

def cosine(x,k,b,A,c):
    '''
        return Acos(kx+b)
    '''
    return A*cos(2*pi*k*(array(x)+b))+c

def fake(x,f):
    
    # random parameters
    A = random.randint(1,10)*(-1)**(random.randint(2))/10
    k = random.randint(500,1800)/16000 
    b = (max(x)+min(x))/2
    c = random.randint(-100,100)/1000
    # noise scale
    noise = (1/40) * (max(f(x,k,b,A,c))-min(f(x,k,b,A,c)))

    noised = []
    for i in x:
        noised.append(f(i,k,b,A,c) + (random.randint(0,60)/10)*noise*(-1)**(random.randint(2)))
    return array(noised)

def theJudge(x,fit_paras):
    candi = hstack([where(cosine(x,*fit_paras) == min(cosine(x,*fit_paras)))[0],where(cosine(x,*fit_paras) == max(cosine(x,*fit_paras)))[0]])
    peak = []
    for i in candi:
        if i != x.shape[0]-1 and i != 0:
            peak.append(i)
    peak = unique(array(peak))
    peaks = []
    for i in peak:
        peaks.append(round(x[i],4))

    if array(peaks).shape[0] == 0:
        peaks = hstack([array(peaks),array([0])])
    
    return peaks

def extendX(x,ratio=1.5):
    """ extend +-1.5 range of X axis to get the extreme values"""
    extension = ratio*(max(x)-min(x))
    steps = (max(x)-min(x))/x.shape[0]
    new_x = arange(min(x)-extension,max(x)+extension,steps)
    return new_x


# initialize with 0.7*amp to 1.3*amp, range ~ 0.16π*amp. when k < 10, probabily can't fit cosine wave well.


if __name__ == '__main__':
    for i in range(20):
        x = arange(start=0.95, stop=1.105, step=0.005)
        y = fake(x,cosine)
        plt.plot(x,y,label='Fake')
        popt,_ = curve_fit(cosine,x,y,maxfev=1000000)
        if abs(popt[0]) < 10 :
            print("Yes")
        plt.plot(x,cosine(x,*popt),label='fitted',c='green')
        print(popt)
        peaks_loca = theJudge(x,popt)
        while 0 in peaks_loca:
            x = extendX(x)
            peaks_loca = theJudge(x,popt)
        plt.title(f"figure_{i},peaks={peaks_loca}")
        if abs(popt[0])>=1:
            for j in peaks_loca:
                plt.scatter(j,cosine(j,*popt),c='red',marker='x',s=100)
        plt.xlabel('XYL ratio (π)')
        plt.legend()
        plt.show()
    
    

