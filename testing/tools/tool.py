from os import stat
from numpy import prod,array,ndarray,append,floor, int64,delete,dstack,sqrt, argmax,std,mean,pi,sin, diff, unwrap, arctan2
from json import loads
from ast import literal_eval
from re import split
from numpy import linspace, prod, stack, quantile
from pandas import DataFrame,concat
from sqlite3 import connect
from pandas import read_sql_query
from plotly import graph_objects
from plotly.offline import plot
from tools.circuit import notch_port
from sklearn.cluster import KMeans
from numpy.fft import fft, fftfreq
from scipy.optimize import curve_fit
from os import makedirs,listdir,remove
from os.path import exists
from tools.Load_PYQUM import Load_pyqum

class waveform:
    '''Guidelines for Command writing:\n
        1. All characters will be converted to lower case.\n
        2. Use comma separated string to represent string list.\n
        3. Inner-Repeat is ONLY used for CW_SWEEP: MUST use EXACTLY ' r ' (in order to differentiate from r inside word-string).\n
        4. waveform.inner_repeat: the repeat-counts indicated after the ' r ' or '^', determining how every .data's element will be repeated.\n
        5. Option to let waveform be 'function-ized' using f: <base/power/log..> at the end of the command/ order:
            a. Base: data points from dense to sparse.
            b. Power: 0-1: same with Log, >1: same with Base, but slower.
            c: Log: data points from sparse to dense.
        NOTE: '^' is equivalent to ' r ' without any spacing restrictions.
    '''
    def __init__(self, command):
        # defaulting to lower case
        command = str(command)
        self.command = command.lower()

        # special treatment to inner-repeat command: (to extract 'inner_repeat' for cwsweep averaging)
        self.inner_repeat = 1
        if ' r ' in self.command:
            self.command, self.inner_repeat = self.command.split(' r ')
            while " " in self.inner_repeat: self.inner_repeat = self.inner_repeat.replace(" ","")
            self.inner_repeat = int(self.inner_repeat)
        if '^' in self.command:
            self.command, self.inner_repeat = self.command.split('^')
            while " " in self.inner_repeat: self.inner_repeat = self.inner_repeat.replace(" ","")
            self.inner_repeat = int(self.inner_repeat)

        # correcting back ("auto-purify") the command-string after having retrieved the repeat-count or not:
        # get rid of multiple spacings
        while " "*2 in self.command:
            self.command = self.command.replace(" "*2," ")
        # get rid of spacing around keywords
        while " *" in self.command or "* " in self.command:
            self.command = self.command.replace(" *","*")
            self.command = self.command.replace("* ","*")
        while " to" in self.command or "to " in self.command:
            self.command = self.command.replace(" to","to")
            self.command = self.command.replace("to ","to")
        while " (" in self.command or "( " in self.command:
            self.command = self.command.replace(" (","(")
            self.command = self.command.replace("( ","(")
        while " )" in self.command or ") " in self.command:
            self.command = self.command.replace(" )",")")
            self.command = self.command.replace(") ",")")
        while " f" in self.command or "f " in self.command:
            self.command = self.command.replace(" f","f")
            self.command = self.command.replace("f ","f")
        while " :" in self.command or ": " in self.command:
            self.command = self.command.replace(" :",":")
            self.command = self.command.replace(": ",":")
        while " /" in self.command or "/ " in self.command:
            self.command = self.command.replace(" /","/")
            self.command = self.command.replace("/ ","/")
        # print(Fore.CYAN + "Command: %s" %self.command)
        
        command = self.command.split(" ") + [""]
        
        # 1. building string list:
        if ("," in command[0]) or ("," in command[1]):
            # remove all sole-commas from string list command:
            command = [x for x in command if x != ',']
            # remove all attached-commas from string list command:
            command = [i for x in command for i in x.split(',') if i != '']
            self.data = command
            self.count = len(command)
        # 2. building number list:
        else:
            command = [x for x in command if x != ""]
            self.data, self.count = [], 0
            for cmd in command:
                self.count += 1
                if "*" in cmd and "to" in cmd:
                    C = [j for i in cmd.split("*") for j in i.split('to')]
                    try:
                        start = float(C[0])
                        steps = range(int(len(C[:-1])/2))
                        for i, target, asterisk in zip(steps,C[1::2],C[2::2]):
                            num = asterisk.split("f:")[0]
                            self.count += int(num)
                            # 2a. Simple linear space / function:
                            self.data += list(linspace(start, float(target), int(num), endpoint=False, dtype=float64))
                            if i==steps[-1]: 
                                self.data += [float(target)] # data assembly complete
                                # 2b. Customized space / function for the WHOLE waveform: base, power, log scales
                                if "f:" in asterisk:
                                    func = asterisk.split("f:")[1]
                                    # print(Fore.CYAN + "Function: %s" %func)
                                    if 'base' in func:
                                        if "e" == func.split('/')[1]: self.data = list(exp(self.data))
                                        else: self.data = list(power(float(func.split('/')[1]), self.data))
                                    elif 'power' in func:
                                        self.data = list(power(self.data, float(func.split('/')[1])))
                                    elif 'log10' in func:
                                        self.data = list(log10(self.data))
                                    elif 'log2' in func:
                                        self.data = list(log2(self.data))
                                    elif 'log' in func:
                                        self.data = list(log(self.data))
                                    else: print("Function NOT defined YET. Please consult developers")
                                    print("scaled %s points" %len(self.data))
                            else: 
                                start = float(target)
                    except: # rooting out the wrong command:
                        # raise
                        # print("Invalid command")
                        pass
                else: self.data.append(float(cmd))     

# c-structure, rjson,readoutype
def command_in_dict(command,dic):
    '''
    command_in_dict(command,dic): 
    command is the output dictionary form
    dic is the raw data dictionary
    '''
    for i in dic:
        if i == 'C-Structure':
            continue
        if waveform(dic[i]).count !=1:
            command['change'] = append(command['change'],i)
            command['change_command'] = append(command['change_command'],waveform(dic[i]).command)
            command['change_len'] = append(command['change_len'],waveform(dic[i]).count)
            if waveform(dic[i]).inner_repeat !=1:
                command['repeat'] = append(command['repeat'],i)
                command['repeat_command'] = append(command['repeat_command'],waveform(dic[i]).inner_repeat)
        elif waveform(dic[i]).inner_repeat !=1:
            command['repeat'] = append(command['repeat'],i)
            command['repeat_command'] = append(command['repeat_command'],waveform(dic[i]).inner_repeat)
        else:
            command['parameter'] = append(command['parameter'],i)
    return command

def repeat_mean(data,repeat,repeat_command):return data.reshape((-1,int(repeat_command[0]))).mean(axis=1)
def construct_layer(where,change_command,change_list_len):
    repeat, group = multiply_except_self(where, change_list_len)
    # print(repeat,group)
    out = seperate(where,change_command)*int(repeat)
    out.sort()
    out = out*int(group)
    return out

def seperate(idx,change_command):
    try:
        tmp = split('[to*]',change_command[idx])
        out = list(linspace(float(tmp[0]), float(tmp[2]), int(tmp[3])+1))
    except:
        out = change_command[idx].split()
    return out
def multiply_except_self(where, alist):
    repeat, group = 1,1
    for i in range(len(alist)):
        if i > where:
            repeat*=alist[i]
        elif i < where:
            group*=alist[i]
    return repeat, group

def command_analytic(selectdata,corder, perimeter,datadensity):
    command = {'change':[],'change_command':[], 'repeat':[], 'repeat_command':[], 'parameter':[], 'change_len':[]}

    print("C-order :")
    for key, value in corder.items():
        print('\t',key, ' : ', value)
    command = command_in_dict(command,corder)

    if 'READOUTYPE' in perimeter.keys():
        print("R-JSON :")
        RJSON = literal_eval(perimeter['R-JSON'])
        command =command_in_dict(command,RJSON)
        for key, value in RJSON.items():
            print('\t',key, ' : ', value)
        if perimeter['READOUTYPE'] == 'continuous':
            shot = int(perimeter['RECORD-SUM'])
            print('RECORD-SUM : ',shot)
            time_unit = int(perimeter['TIME_RESOLUTION_NS'])
            time_ns = int(perimeter['RECORD_TIME_NS'])
            print('RECORD_TIME_NS : ',time_ns)
            print('TIME_RESOLUTION_NS : ',time_unit)
            print('RECORD_TIME_dot : ',int(time_ns/time_unit))
            command['change'] = append(command['change'],'RECORD_TIME_NS')
            command['change_command'] = append(command['change_command'],str(1*time_unit)+'to'+str(time_ns)+'*'+str(int(time_ns/time_unit)-1))
            command['change_len'] = append(command['change_len'],int(time_ns/time_unit))
        if perimeter['READOUTYPE'] == 'one-shot':
            shot = int(perimeter['RECORD-SUM'])
            print('RECORD-SUM : ',shot)
            time_ns = int(perimeter['RECORD_TIME_NS'])
            print('RECORD_TIME_NS : ',time_ns)
            command['change'] = append(command['change'],'RECORD-SUM')
            command['change_command'] = append(command['change_command'],'1to'+str(shot)+'*'+str(shot-1))
            command['change_len'] = append(command['change_len'],shot)

    print("Change : \n\t",command['change'])
    print("Change command : \n\t",command['change_command'])
    print("Repeat : \n\t",command['repeat'])
    print("Repeat_command : \n\t",command['repeat_command'])
    # print("Unchange : \n\t",command['parameter'])
    print("\n")

    selectdata_i_data = selectdata[::datadensity]
    selectdata_q_data = selectdata[1::datadensity]
    while len(command['repeat'])!=0:
        selectdata_i_data = repeat_mean(selectdata_i_data,command['repeat'],command['repeat_command'])
        selectdata_q_data = repeat_mean(selectdata_q_data,command['repeat'],command['repeat_command'])
        command['repeat'] = delete(command['repeat'],0)
        command['repeat_command'] = delete(command['repeat_command'],0)

    df = DataFrame()
    for i in range(len(command['change'])):
        df1 = DataFrame(construct_layer(i,command['change_command'],command['change_len']), columns = [command['change'][i]])
        df = concat([df,df1],axis =1)
    df_label = df
    # print(df_label)
    return selectdata_i_data,selectdata_q_data, df_label
        
def jobid_search_pyqum(id):
    # --------------Search Path --------------
    path = 'pyqum.sqlite'
    conn = connect(path)
    job = read_sql_query("SELECT * FROM job", conn)
    user = read_sql_query("SELECT * FROM user", conn)[['id','username']]
    sample = read_sql_query("SELECT * FROM sample", conn)[['id','samplename','author_id']]
    queue = read_sql_query("SELECT * FROM queue", conn)
    sample_id = job[job['id']==id]['sample_id'].iloc[0]
    queue_name = job[job['id']==id]['queue'].iloc[0]
    dateday = job[job['id']==id]['dateday'].iloc[0]
    task = job[job['id']==id]['task'].iloc[0]
    wmoment  = job[job['id']==id]['wmoment'].iloc[0]
    name_id = sample[sample['id']==sample_id]['author_id'].iloc[0]
    name = user[user['id']==name_id]['username'].iloc[0]
    sample_name = sample[sample['id']==sample_id]['samplename'].iloc[0]
    mission = queue[queue['system']==queue_name]['mission'].iloc[0]
    pyqum_path = r"C:\Users\ASQUM\HODOR\CONFIG\USRLOG\%s\%s\%s\%s\%s.pyqum(%d)"%(name,sample_name,mission,dateday,task,wmoment)
    print("Path : ",pyqum_path)
    return pyqum_path,task
def print_comment(pyqum_path):
    filesize = stat(pyqum_path).st_size
    with open(pyqum_path, 'rb') as datapie:
        i = 0
        while i < (filesize):
            datapie.seek(i)
            bite = datapie.read(7)
            if bite == b'\x02' + bytes("ACTS", 'utf-8') + b'\x03\x04': # ACTS
                datalocation = i
                break
            else: i += 1
        datapie.seek(17)
    #     print(datapie.read())
        dict_label = datapie.read(datalocation-18)
    dict_str = dict_label.decode("UTF-8")
    file_label = literal_eval(dict_str)
    print("Comment : \n"+str(file_label['comment']))

def load_corder(pyqum_path):
    filesize = stat(pyqum_path).st_size
    with open(pyqum_path, 'rb') as datapie:
        i = 0
        while i < (filesize):
            datapie.seek(i)
            bite = datapie.read(7)
            if bite == b'\x02' + bytes("ACTS", 'utf-8') + b'\x03\x04': # ACTS
                datalocation = i
                break
            else: i += 1
        datapie.seek(17)
    #     print(datapie.read())
        dict_label = datapie.read(datalocation-18)
    dict_str = dict_label.decode("UTF-8")
    file_label = literal_eval(dict_str)
    corder = file_label['c-order']
    return corder

def load_RJSON(pyqum_path):
    filesize = stat(pyqum_path).st_size
    with open(pyqum_path, 'rb') as datapie:
        i = 0
        while i < (filesize):
            datapie.seek(i)
            bite = datapie.read(7)
            if bite == b'\x02' + bytes("ACTS", 'utf-8') + b'\x03\x04': # ACTS
                datalocation = i
                break
            else: i += 1
        datapie.seek(17)
    #     print(datapie.read())
        dict_label = datapie.read(datalocation-18)
    dict_str = dict_label.decode("UTF-8")
    file_label = literal_eval(dict_str)
    perimeter = file_label['perimeter']
    RJSON = literal_eval(perimeter['R-JSON'])
    return RJSON

def print_parameter(pyqum_path):
    filesize = stat(pyqum_path).st_size
    with open(pyqum_path, 'rb') as datapie:
        i = 0
        while i < (filesize):
            datapie.seek(i)
            bite = datapie.read(7)
            if bite == b'\x02' + bytes("ACTS", 'utf-8') + b'\x03\x04': # ACTS
                datalocation = i
                break
            else: i += 1
        datapie.seek(17)
    #     print(datapie.read())
        dict_label = datapie.read(datalocation-18)
    dict_str = dict_label.decode("UTF-8")
    file_label = literal_eval(dict_str)
    corder = file_label['c-order']
    try: perimeter = file_label['perimeter']
    except(KeyError): perimeter = {}

    print("C-order :")
    for key, value in corder.items():
        print('\t',key, ' : ', value)

    if 'READOUTYPE' in perimeter.keys():
        print("R-JSON :")
        RJSON = literal_eval(perimeter['R-JSON'])
        for key, value in RJSON.items():
            print('\t',key, ' : ', value)
        if perimeter['READOUTYPE'] == 'continuous':
            shot = int(perimeter['RECORD-SUM'])
            print('RECORD-SUM : ',shot)
            time_unit = int(perimeter['TIME_RESOLUTION_NS'])
            time_ns = int(perimeter['RECORD_TIME_NS'])
            print('RECORD_TIME_NS : ',time_ns)
            print('TIME_RESOLUTION_NS : ',time_unit)
            print('RECORD_TIME_dot : ',int(time_ns/time_unit))
            
        if perimeter['READOUTYPE'] == 'one-shot':
            shot = int(perimeter['RECORD-SUM'])
            print('RECORD-SUM : ',shot)
            time_ns = int(perimeter['RECORD_TIME_NS'])
            print('RECORD_TIME_NS : ',time_ns)

def load_rawdata(pyqum_path):
    # --------------load IQdata --------------
    filesize = stat(pyqum_path).st_size
    with open(pyqum_path, 'rb') as datapie:
    #     print(datapie.read())
        i = 0
        while i < (filesize):
            datapie.seek(i)
            bite = datapie.read(7)
            if bite == b'\x02' + bytes("ACTS", 'utf-8') + b'\x03\x04': # ACTS
                datalocation = i
                break
            else: i += 1
        datapie.seek(datalocation+7)
        writtensize = filesize-datalocation-7
        pie = datapie.read(writtensize)
        datacontainer = bite.decode('utf-8')
    selectdata = ndarray(shape=(writtensize//8,), dtype=">d", buffer=pie) # speed up with numpy ndarray, with the ability to do indexing in it.
    # print("Select Data length: %s" %len(selectdata))
    # print(selectdata)
    # --------------load C-order --------------
    with open(pyqum_path, 'rb') as datapie:
        datapie.seek(17)
    #     print(datapie.read())
        dict_label = datapie.read(datalocation-18)
    dict_str = dict_label.decode("UTF-8")
    file_label = literal_eval(dict_str)
    # print(file_label)
    corder = file_label['c-order']
#     print("C-order : \n"+str(corder))
    print("Comment : \n"+str(file_label['comment']))
    # --------------load Perimeter --------------
    try: perimeter = file_label['perimeter']
    except(KeyError): perimeter = {}
#     print("\nperimeter : \n"+str(perimeter))
    try: jobid = perimeter['jobid']
    except(KeyError): jobid = 0
    
    store_shape = array([waveform(corder[x]).count * waveform(corder[x]).inner_repeat for x in corder if x != 'C-Structure' ])
    cdatasize = int(prod(store_shape, dtype='uint64')) * file_label['data-density'] #data density of 2 due to IQ
    
    if 'READOUTYPE' in perimeter.keys():
        RJSON = literal_eval(perimeter['R-JSON'])
        RJSON_shape = array([waveform(x).count * waveform(x).inner_repeat for x in RJSON.values()])
        cdatasize*=int(prod(RJSON_shape, dtype='uint64'))
        if perimeter['READOUTYPE'] == 'continuous':
            time_unit = int(perimeter['TIME_RESOLUTION_NS'])
            time_ns = int(perimeter['RECORD_TIME_NS'])
            cdatasize*=int(time_ns/time_unit)
        if perimeter['READOUTYPE'] == 'one-shot':
            shot = int(perimeter['RECORD-SUM'])
            cdatasize*=shot
            
    print("\nC-order Data size: \n%s" %cdatasize)
    print("Select Data length: \n%s" %len(selectdata))   
    # --------------Check data integrity --------------
    if cdatasize == len(selectdata):
        print("\tChecked!\n")
        print("Start load data....")
    else:
        print("examine pyqum data")
    
    return selectdata, corder,perimeter, jobid, file_label['data-density']

def pyqum_load_data(pyqum_path):
    selectdata, corder, perimeter, jobid, datadensity = load_rawdata(pyqum_path)
    mean_i_data, mean_q_data, df_label = command_analytic(selectdata,corder, perimeter,datadensity)
    df_i = DataFrame(mean_i_data, columns = ['I'])
    df_q = DataFrame(mean_q_data, columns = ['Q'])
    df_data = concat([df_i,df_q],axis =1)
    # print(df_label)
    # print(df_data)
    tidy_data = concat([df_label,df_data],axis =1)
    df_amp =DataFrame(sqrt(tidy_data['I']**2+tidy_data['Q']**2), columns = ['Amp'])
    amp_data = concat([tidy_data,df_amp],axis =1)
    UPhase = diff(unwrap(arctan2(tidy_data['Q'],tidy_data['I'])))
    UPhase = append(UPhase, mean(UPhase))
    df_UPhase =DataFrame(UPhase, columns = ['UPhase'])
    data = concat([amp_data,df_UPhase],axis =1)
    data = data.astype(float)
    return data,jobid

# if __name__ == "__main__":
#     id = int(input("id? : "))
#     # pyqum_path,task = jobid_search_pyqum(id)
#     pyqum_path = 'F_Response.pyqum(2)'
#     amp_data,jobid  = pyqum_load_data(pyqum_path)

class PowerDepend:
    def __init__(self, dataframe):
        self.dataframe = dataframe
        self.data = load_valid(dataframe)
    def do_analysis(self):
        model = KMeans(n_clusters=2, n_init=1, random_state=0)
        label = model.fit_predict(self.data)
        label_new = outlier_detect(self.data,label)
        power_0,power_1 = cloc(label_new)
        print("power : "+"{:.2f}".format(self.data[:, 0][power_0])+"{:<7}".format(' dBm ; ')+
            "fr : "+"{:.2f}".format(self.data[:, 1][power_0])+"{:<7}".format(' MHz ; \n')+
            "power : "+"{:.2f}".format(self.data[:, 0][power_1])+"{:<7}".format(' dBm ; ')+
            "fr : "+"{:.2f}".format(self.data[:, 1][power_1])+"{:<7}".format(' MHz ; '))
        self.low_power = min(self.data[:, 0][power_0],self.data[:, 0][power_1])
        self.high_power = max(self.data[:, 0][power_0],self.data[:, 0][power_1])
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(12, 9))
        plt.scatter(self.data[:, 0], self.data[:, 1], c=label_new, s=40)
        plt.xlabel("Power")
        plt.ylabel("Frequency")
        plt.show()
        return self.low_power, self.high_power
    def give_plot_info(self):
        plot_items  = {
			'Frequency':array(self.dataframe['Frequency']),
			'Power':array(self.dataframe['Power']),
			'Amplitude':array(self.dataframe['Amp'])
		}
        plot_scatter = {
			'Power':array(self.data[:, 0]),
			'Fr':array(self.data[:, 1])/1000
		}
        return {'heatmap':plot_items,'scatter':plot_scatter}
    
def power_load_data(data):
    ''' 
        mat form
        x = Flux-Bias(V/A) ; y = freq(GHz) ;
        I , Q ;
        A = 20*log10(sqrt(I**2 + Q**2)) ;
        P = arctan2(Q, I) # -pi < phase < pi
        
        output  = self.dataframe pandas dataframe
    '''
#     mat = loadmat(path)
    df1=DataFrame()
    fr = []
    for i in data["Power"].unique():
        port1 = notch_port(f_data=data[data["Power"]==i]["Frequency"].values,z_data_raw=data[data["Power"]==i]["I"]+1j*data[data["Power"]==i]["Q"])
        port1.autofit()
        fr.append(port1.fitresults['fr'])
    df1.insert(loc=0, column='fr', value = array(fr))
    df1.insert(loc=0, column='power', value = data["Power"].unique())
#     for j in range(len(mat['x'][0])):
#         power,freq,I,Q,A,P,df= [],[],[],[],[],[],[]
#         for i in range(len(mat['y'][0])):
#                 power.append(mat['x'][0][j]);freq.append(mat['y'][0][i])
#                 I.append(mat['ZZI'][i][j]);Q.append(mat['ZZQ'][i][j])
#                 # A.append(mat['ZZA'][i][j]);P.append(mat['ZZP'][i][j])
#         # df =DataFrame({"Frequency":freq,"Power":power,"p":P,"a":A,"i":I,"q":Q}).sort_values(["Frequency","Power"],ascending=True)
#         df =DataFrame({"Frequency":freq,"Power":power,"i":I,"q":Q}).sort_values(["Frequency","Power"],ascending=True)
#         port1 = notch_port(f_data=df["Frequency"].values,z_data_raw=df["i"]+1j*df["q"])
#         # port1.plotrawdata()
#         port1.autofit()

#         # port1.plotall()
#         # display(DataFrame([port1.fitresults]).applymap(lambda x: "{0:.2e}".format(x)))
#         df1 = df1.append(DataFrame([port1.fitresults]), ignore_index = True)
#     df1.insert(loc=0, column='power', value=mat['x'][0])

    #---------------drop the outward data---------------
    f_min,f_max = min(data['Frequency']),max(data['Frequency'])
    valid = df1[(df1['fr']>= f_min)&(df1['fr']<= f_max)]
    valid.reset_index(inplace=True)
    power = valid['power']
    fr = valid['fr']*1000
    data = stack((power,fr), axis=1)
    return data


def outlier_detect(data,label):
    error_label = 1
    class0_label ,class1_label = 0,2
    label = class1_label* label
    iteration = 3
    threshold = 1.5
    IQR_end = 0.006
    for i in range(iteration):
        Q1_0 = quantile(data[:,1][label==class0_label],.25)
        Q3_0 = quantile(data[:,1][label==class0_label],.75)
        IQR_0 = Q3_0 - Q1_0
        Q1_1 = quantile(data[:,1][label==class1_label],.25)
        Q3_1 = quantile(data[:,1][label==class1_label],.75)
        IQR_1 = Q3_1 - Q1_1
        print("IQR :"+"{:.4f}".format(IQR_0)+" ; "+"{:.4f}".format(IQR_1))
        for i in range(len(label)):
            if label[i]==class0_label:
                if IQR_0 <IQR_end:
                    pass
                elif((data[:,1][i] < (Q1_0 - threshold * IQR_0))| (data[:,1][i] > (Q3_0 + threshold * IQR_0))):
                    label[i]=error_label
            if label[i]==class1_label:
                if IQR_1 <IQR_end:
                    pass
                elif((data[:,1][i] < (Q1_1 - threshold * IQR_1))| (data[:,1][i] > (Q3_1 + threshold * IQR_1))):
                    label[i]=error_label
        if (IQR_0<IQR_end)&(IQR_1<IQR_end):
            print('end')
            break
    return label

def cloc(label_new):
    min_0,min_1, min_2 = -1,-1,-1
    error_label = 1
    class0_label ,class1_label = 0,2
    for i in range(len(label_new)):
        if min_0 != -1 | min_1 != -1| min_2 != -1:
            break
        if label_new[i]==error_label:
            if ((min_0 != -1) | (min_1 != -1))&(min_2== -1):
                min_2 = i
        elif label_new[i]==class0_label:
            if min_0 == -1:
                min_0 = i
        elif label_new[i]==class1_label:
            if min_1 == -1:
                min_1 = i
#     print(min_0,min_1,min_2)
    if min_0<min_1:
        min_0 = min_2-2
    else:
        min_1 = min_2-2
    return min_0,min_1

def flux_load_data(data):
    ''' 
        mat form
        x = Flux-Bias(V/A) ; y = freq(GHz) ;
        I , Q ;
        A = 20*log10(sqrt(I**2 + Q**2)) ;
        P = arctan2(Q, I) # -pi < phase < pi
        
        output  = self.dataframe pandas dataframe
    '''

    #---------------examine the data structure---------------
    # for i in mat.keys():
    #     if i.find('_')==-1:
    #         print(i,' is a ',len(mat[i]),'*',len(mat[i][0]),' matrix')
    # print('x = ',mat['xtitle'][0],'\ny = ',mat['ytitle'][0])

    #---------------prepare data ---------------
    df1=DataFrame()
    fr = []
#     for j in range(len(data)):
#         flux,freq,I,Q,A,P= [],[],[],[],[],[]
#         for i in range(len(mat['y'][0])):
#                 flux.append(mat['x'][0][j]);freq.append(mat['y'][0][i])
#                 I.append(mat['ZZI'][i][j]);Q.append(mat['ZZQ'][i][j])
#         df =DataFrame({"Frequency":freq,"Flux-Bias":flux,"i":I,"q":Q}).sort_values(["Frequency","Flux-Bias"],ascending=True)
#         port1 = notch_port(f_data=df["Frequency"].values,z_data_raw=df["i"]+1j*df["q"])
#         port1.autofit()
#         fr.append(port1.fitresults['fr'])
    for i in data["Flux-Bias"].unique():
        port1 = notch_port(f_data=data[data["Flux-Bias"]==i]["Frequency"].values,z_data_raw=data[data["Flux-Bias"]==i]["I"]+1j*data[data["Flux-Bias"]==i]["Q"])
        port1.autofit()
        fr.append(port1.fitresults['fr'])
    df1.insert(loc=0, column='fr', value = array(fr)*10**3)
    df1.insert(loc=0, column='flux', value = data["Flux-Bias"].unique())
    #---------------drop the outward data---------------
    f_min,f_max = min(data["Frequency"].unique())*1000,max(data["Frequency"].unique())*1000
    valid = df1[(df1['fr']>= f_min)&(df1['fr']<= f_max)]
    valid.reset_index(inplace=True)
    valid = valid.drop(labels=['index'], axis="columns")
    return valid

def fit_sin(tt, yy):
    '''Fit sin to the input time sequence, and return fitting parameters "amp", "omega", "phase", "offset", "freq", "period" and "fitfunc"'''
    tt = np.array(tt)
    yy = np.array(yy)
    ff = np.fft.fftfreq(len(tt), (tt[1]-tt[0]))   # assume uniform spacing
    Fyy = abs(np.fft.fft(yy))
    guess_freq = abs(ff[np.argmax(Fyy[1:])+1])   # excluding the zero frequency "peak", which is related to offset
    guess_amp = np.std(yy) * 2.**0.5
    guess_offset = np.mean(yy)
    guess = np.array([guess_amp, 2.*np.pi*guess_freq, 0., guess_offset])

    def sinfunc(t, A, w, p, c):  return A * np.sin(w*t + p) + c
    popt, pcov = optimize.curve_fit(sinfunc, tt, yy, p0=guess)
    A, w, p, c = popt
    f = w/(2.*np.pi)
    fitfunc = lambda t: A * np.sin(w*t + p) + c
    return {"amp": A, "omega": w, "phase": p,"mean" :c, "offset": np.max(yy), "freq": f, "period": 1./f, "fitfunc": fitfunc, "maxcov": np.max(pcov), "rawres": (guess,popt,pcov)}


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from matplotlib import transforms
def confidence_ellipse(x, y, ax, n_std=3.0, facecolor='none', **kwargs):
    """
    Create a plot of the covariance confidence ellipse of *x* and *y*.

    Parameters
    ----------
    x, y : array-like, shape (n, )
        Input data.

    ax : matplotlib.axes.Axes
        The axes object to draw the ellipse into.

    n_std : float
        The number of standard deviations to determine the ellipse's radiuses.

    **kwargs
        Forwarded to `~matplotlib.patches.Ellipse`

    Returns
    -------
    matplotlib.patches.Ellipse
    """
    if x.size != y.size:
        raise ValueError("x and y must be the same size")

    cov = np.cov(x, y)
    pearson = cov[0, 1]/np.sqrt(cov[0, 0] * cov[1, 1])
    # Using a special case to obtain the eigenvalues of this
    # two-dimensionl dataset.
    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    ellipse = Ellipse((0, 0), width=ell_radius_x * 2, height=ell_radius_y * 2,
                      facecolor=facecolor, **kwargs)

    # Calculating the stdandard deviation of x from
    # the squareroot of the variance and multiplying
    # with the given number of standard deviations.
    scale_x = np.sqrt(cov[0, 0]) * n_std
    mean_x = np.mean(x)

    # calculating the stdandard deviation of y ...
    scale_y = np.sqrt(cov[1, 1]) * n_std
    mean_y = np.mean(y)

    transf = transforms.Affine2D() \
        .rotate_deg(45) \
        .scale(scale_x, scale_y) \
        .translate(mean_x, mean_y)

    ellipse.set_transform(transf + ax.transData)
    return ax.add_patch(ellipse)

def kmean_plot(data,label,kmeans):
    bleed = 10**-3
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.axis('equal')
    data_max = np.max(data,axis =0)
    data_min = np.min(data,axis =0)
    plt.xlim(data_min[0]-bleed, data_max[0]+bleed)
    plt.ylim(data_min[1]-bleed, data_max[1]+bleed)
    diff = kmeans.cluster_centers_[1]-kmeans.cluster_centers_[0]
    k = diff[1]/diff[0]
    b = kmeans.cluster_centers_[0][1]-k*kmeans.cluster_centers_[0][0]
    b1 = kmeans.cluster_centers_[0][1]+1/k*kmeans.cluster_centers_[0][0]
    b2 = kmeans.cluster_centers_[1][1]+1/k*kmeans.cluster_centers_[1][0]
    line = np.linspace(data_min[0], data_max[0], 1000)
    ax.plot(line, k*line+b,color = "k")
    ax.plot(line, -1/k*line+b1,color = "r")
    ax.plot(line, -1/k*line+b2,color = "r")
    #Getting unique labels
    u_labels = np.unique(label)
    # Plot a confidence ellipse of a two-dimensional dataset
    for i in u_labels:
        confidence_ellipse(data[:, 0][label == i], data[:, 1][label == i], ax, n_std=1,
                          facecolor='pink', edgecolor='firebrick',alpha= 0.3)
        confidence_ellipse(data[:, 0][label == i], data[:, 1][label == i], ax, n_std=2,
                          edgecolor='fuchsia', linestyle='--')
        confidence_ellipse(data[:, 0][label == i], data[:, 1][label == i], ax, n_std=3,
                          edgecolor='blue', linestyle=':')
        cov = np.cov(data[:, 0][label == i], data[:, 1][label == i])
        print("{:<10}".format("The I-std div of ")+"{:^3}".format(label[i])+" : {:.4f}".format(np.sqrt(cov[0][0])))
        print("{:<10}".format("The Q-std div of ")+"{:^3}".format(label[i])+" : {:.4f}".format(np.sqrt(cov[1][1])))
    scatter = ax.scatter(data[:, 0], data[:, 1], c=label)
    legend1 = ax.legend(*scatter.legend_elements(), title="Classes")
    ax.add_artist(legend1)
    # plot_svm_decision_function(kmeans)
    for i in range(len(kmeans.cluster_centers_)):
        ax.scatter(kmeans.cluster_centers_[i][0],kmeans.cluster_centers_[i][1],color = "r")
    plt.show()
    
def gmm_plot(data,label,cluster_centers):
    '''
        gmm_plot(data,label,gmm.means_)
    '''
    bleed = 10**-3
    fig, ax = plt.subplots(figsize=(16, 12))
    ax.axis('equal')
    data_max = np.max(data,axis =0)
    data_min = np.min(data,axis =0)
    plt.xlim(data_min[0]-bleed, data_max[0]+bleed)
    plt.ylim(data_min[1]-bleed, data_max[1]+bleed)
    scatter = ax.scatter(data[:, 0], data[:, 1], c=label)
    legend1 = ax.legend(*scatter.legend_elements(), title="Classes")
    ax.add_artist(legend1)
    #Getting unique labels
    u_labels = np.unique(label)
    for i in u_labels1:
        confidence_ellipse_gmm(cluster_centers[i],cov, ax, n_std=1,facecolor='pink', edgecolor='firebrick',alpha= 0.3)
        confidence_ellipse_gmm(cluster_centers[i],cov, ax, n_std=2,edgecolor='fuchsia', linestyle='--')
        confidence_ellipse_gmm(cluster_centers[i],cov, ax, n_std=3,edgecolor='blue', linestyle=':')
    for i in range(len(cluster_centers)):
        ax.scatter(cluster_centers[i][0],cluster_centers[i][1],color = "r")
    plt.xlabel("I")
    plt.ylabel("Q")


def change_label(label):return label^(label&1==label)

def confidence_ellipse_gmm(mean,cov, ax, n_std=3.0, facecolor='none', **kwargs):
    pearson = cov[0, 1]/np.sqrt(cov[0, 0] * cov[1, 1])
    # Using a special case to obtain the eigenvalues of this
    # two-dimensionl dataset.
    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    ellipse = Ellipse((0, 0), width=ell_radius_x * 2, height=ell_radius_y * 2,
                      facecolor=facecolor, **kwargs)

    # Calculating the stdandard deviation of x from
    # the squareroot of the variance and multiplying
    # with the given number of standard deviations.
    scale_x = np.sqrt(cov[0, 0]) * n_std
    mean_x = mean[0]

    # calculating the stdandard deviation of y ...
    scale_y = np.sqrt(cov[1, 1]) * n_std
    mean_y = mean[1]

    transf = transforms.Affine2D() \
        .rotate_deg(45) \
        .scale(scale_x, scale_y) \
        .translate(mean_x, mean_y)

    ellipse.set_transform(transf + ax.transData)
    return ax.add_patch(ellipse)
    
def SNR(gmm):
    S = np.linalg.norm(gmm.means_[0]-gmm.means_[1])**2
    N = 2*np.sqrt(gmm.covariances_[0,0]**2+gmm.covariances_[1,1]**2)
    SNR = S/N
    return S,N,SNR

def cal_SNR(gmm,change_label):
    S = np.linalg.norm(gmm.means_[0]-gmm.means_[1])
    cluster_centers_ = gmm.means_
    if change_label:
        refpoint = cluster_centers_[1]
        diff = cluster_centers_[0]-cluster_centers_[1]
    else:
        refpoint = cluster_centers_[0]
        diff = cluster_centers_[1]-cluster_centers_[0]
    rotation_matrix = np.array([[ diff[0]/S,  -diff[1]/S],[ diff[1]/S,  diff[0]/S]])
    cov = (rotation_matrix @ gmm.covariances_ @ rotation_matrix.T)
    N = 2*cov[0][0]
    snr = S**2/N
    snr_db = 20*np.log10(snr) #電壓增益
    return S,N,snr,snr_db

def cal_Tmk(p0,w_a):
    import scipy
    T = -1/(np.log(1/(-p0+1)*(2*p0-1)+1)*scipy.constants.Boltzmann/scipy.constants.h/w_a/1e9)*1000
    return T

def gmm_plot_class(print_para):
    data1,label1,data2,label2,cluster_centers,cov,samplename,jobid,mark_gmm,XYL,title,w_a = print_para
    if mark_gmm: 
        label1 = change_label(label1)
        label2 = change_label(label2)
    unique1, counts1 = np.unique(label1, return_counts=True)
    unique2, counts2 = np.unique(label2, return_counts=True)
    plt.figure(figsize=(18, 27))
    ax1 = plt.subplot(321)
    ax1.axis('equal')
    ax1.grid()
    scatter1 = ax1.scatter(data1[:, 0],data1[:, 1],c=label1,cmap ='bwr')
    legend1 = ax1.legend(*scatter1.legend_elements(), title="Classes")
    ax1.add_artist(legend1)
    ax1.title.set_text("XYL : "+str(XYL[0])+" with "+str(dict(zip(unique1, counts1))))
    ax1.title.set_size(20)
    for i in range(len(cluster_centers)):
        confidence_ellipse_gmm(cluster_centers[i],cov, ax1, n_std=1,facecolor='pink', edgecolor='firebrick',alpha= 0.3)
        confidence_ellipse_gmm(cluster_centers[i],cov, ax1, n_std=2,edgecolor='fuchsia', linestyle='--')
        confidence_ellipse_gmm(cluster_centers[i],cov, ax1, n_std=3,edgecolor='blue', linestyle=':')
        ax1.scatter(cluster_centers[i][0],cluster_centers[i][1],color = "black")
    ax2 = plt.subplot(322)
    ax2.axis('equal')
    ax2.grid()
    scatter2 = ax2.scatter(data2[:, 0],data2[:, 1],c=label2,cmap ='bwr')
    legend2 = ax2.legend(*scatter2.legend_elements(), title="Classes")
    ax2.add_artist(legend2)
    ax2.title.set_text("XYL : "+str(XYL[-1])+" with "+str(dict(zip(unique2, counts2))))
    ax2.title.set_size(20)
    for i in range(len(cluster_centers)):
        confidence_ellipse_gmm(cluster_centers[i],cov, ax2, n_std=1,facecolor='pink', edgecolor='firebrick',alpha= 0.3)
        confidence_ellipse_gmm(cluster_centers[i],cov, ax2, n_std=2,edgecolor='fuchsia', linestyle='--')
        confidence_ellipse_gmm(cluster_centers[i],cov, ax2, n_std=3,edgecolor='blue', linestyle=':')
        ax2.scatter(cluster_centers[i][0],cluster_centers[i][1],color = "black")
    
    p0_1,p1_1 = counts1[0]/(counts1[0]+counts1[1]),counts1[1]/(counts1[0]+counts1[1])
    p0_2,p1_2 = counts2[0]/(counts2[0]+counts2[1]),counts2[1]/(counts2[0]+counts2[1])
    bins = 500
    if mark_gmm:
        refpoint = cluster_centers[1]
        diff = cluster_centers[0]-cluster_centers[1]
    else:
        refpoint = cluster_centers[0]
        diff = cluster_centers[1]-cluster_centers[0]
    data1_1D = (data1-refpoint)@diff/(scipy.linalg.norm(diff))**2
    data2_1D = (data2-refpoint)@diff/(scipy.linalg.norm(diff))**2
    xlist0 = np.linspace(-1,1,200)
    xlist1 = np.linspace(0,2,200)
    sigma0_1 = std_dev(data1_1D[data1_1D<=0],0)
    sigma1_1= std_dev(data1_1D[data1_1D>=1],1)
    sigma0_2 = std_dev(data2_1D[data2_1D<=0],0)
    sigma1_2= std_dev(data2_1D[data2_1D>=1],1)
    
    ax3 = plt.subplot(312)
    ax3.grid()
    n1,locbin1,patch1 =ax3.hist(data1_1D, bins, density=True,alpha=.1)
    locbin1 = np.delete(locbin1, 0)
    width1 = locbin1[1]-locbin1[0]
    best_fit_line0_1 = scipy.stats.norm.pdf(locbin1, 0, sigma0_1)
    best_fit_line1_1 = scipy.stats.norm.pdf(locbin1, 1, sigma1_1)
    cdf0 = scipy.stats.norm.cdf(locbin1,0, sigma0_1)
    cdf1 = scipy.stats.norm.cdf(locbin1,1, sigma1_1)
    a =DataFrame({'x':locbin1,'y':p0_1*best_fit_line0_1-p1_1*best_fit_line1_1,'pdf0':p0_1*best_fit_line0_1,'pdf1':p1_1*best_fit_line1_1,'cdf0':p0_1*cdf0,'cdf1':p1_1*cdf1})
    df_pdf = a[(a['x']<1)&(a['x']>0)]
    cut = float(df_pdf.iloc[(df_pdf['y']).abs().argsort()[:1]]['x'])
    ax3.bar(locbin1[locbin1<cut]-width1/2,n1[locbin1<cut],width =width1,color='b',alpha =0.5,label=0)
    ax3.bar(locbin1[locbin1>cut]-width1/2,n1[locbin1>cut],width =width1,color='r',alpha =0.5,label=1)
    
    ax3.plot(locbin1, p0_1*best_fit_line0_1,color='b')
    ax3.plot(locbin1, p1_1*best_fit_line1_1,color='r')
    ax3.plot(locbin1, p0_1*best_fit_line0_1+p1_1*best_fit_line1_1,color = 'orange')
    ax3.legend()
    ax3.set_xlabel("X")
    ax3.set_ylabel("Probability")
    ax3.title.set_text("XYL : "+str(XYL[0])+" with "+str(dict(zip(unique1, [round(p0_1,5),round(p1_1,5)])))+", Fidelity_{:.2f}%".format(100*p0_1))
    ax3.title.set_size(20)
    
    ax4 = plt.subplot(313)
    ax4.grid()
    n2,locbin2,patch2 =ax4.hist(data2_1D, bins, density=True,alpha=.1)
    locbin2 = np.delete(locbin2, 0)
    width2 = locbin2[1]-locbin2[0]
    ax4.bar(locbin2[locbin2<cut]-width2/2,n2[locbin2<cut],width =width2,color='b',alpha =0.5,label=0)
    ax4.bar(locbin2[locbin2>cut]-width2/2,n2[locbin2>cut],width =width2,color='r',alpha =0.5,label=1)
    best_fit_line0_2 = scipy.stats.norm.pdf(locbin2, 0, sigma0_2)
    best_fit_line1_2 = scipy.stats.norm.pdf(locbin2, 1, sigma1_2)
    ax4.plot(locbin2, p0_2*best_fit_line0_2,color='b')
    ax4.plot(locbin2, p1_2*best_fit_line1_2,color='r')
    ax4.plot(locbin2, p0_2*best_fit_line0_2+p1_2*best_fit_line1_2,color = 'orange')
    ax4.legend()
    ax4.set_xlabel("X")
    ax4.set_ylabel("Probability")
    ax4.title.set_text("XYL : "+str(XYL[-1])+" with "+str(dict(zip(unique2, [round(p0_2,5),round(p1_2,5)])))+", Fidelity_{:.2f}%".format(100*p1_2))
    ax4.title.set_size(20)
    S = np.linalg.norm(cluster_centers[0]-cluster_centers[1])**2
    N = 2*np.sqrt(cov[0,0]**2+cov[1,1]**2)
    SNR = S/N
    T= cal_Tmk(p1_1,w_a)
    plt.suptitle("#{:d}_{:s} SNR_{:.4f}, T_{:.2f} mk, Fidelity : {:.2f}%".format(jobid,title,SNR,T,100*(1-p1_1-p0_2)),fontsize=28)
    sample_dir = "./"+samplename
    if not exists(sample_dir):
        makedirs(sample_dir)
        print("Sample folder for output created!")
    fig_dir = sample_dir+"/Figure/"
    if not exists(fig_dir):
        makedirs(fig_dir)
    plt.savefig(fig_dir+"#{:d}_{:s}.png".format(jobid,title))
    plt.show()
    plt.clf()
    
import scipy
def GMM_dist(data,label,cluster_centers_):
    '''
        GMM_dist(data,label,gmm.means_)
    '''
    unique, counts = np.unique(label, return_counts=True)
    p0,p1 = counts[0]/(counts[0]+counts[1]),counts[1]/(counts[0]+counts[1])
    plt.figure(figsize=(16, 12))
    bins = 150
    refpoint = cluster_centers_[0]
    diff = cluster_centers_[1]-cluster_centers_[0]
    data_1D = (data-refpoint)@diff/(scipy.linalg.norm(diff))**2
    n,locbin,patch =plt.hist(data_1D, bins, density=True,alpha=.1)
    locbin = np.delete(locbin, 0)
    width = locbin[1]-locbin[0]
    sigma0 = std_dev(data_1D[data_1D<=0],0)
    sigma1 = std_dev(data_1D[data_1D>=1],1)
    best_fit_line0 = scipy.stats.norm.pdf(locbin, 0, sigma0)
    best_fit_line1 = scipy.stats.norm.pdf(locbin, 1, sigma1)
    a =DataFrame({'x':locbin,'y':p0*best_fit_line0-p1*best_fit_line1})
    df_pdf = a[(a['x']<1)&(a['x']>0)]
    cut = float(df_pdf.iloc[(df_pdf['y']).abs().argsort()[:1]]['x'])
    plt.bar(locbin[locbin<cut]-width/2,n[locbin<cut],width =width,color='b',alpha =0.5,label=0)
    plt.bar(locbin[locbin>cut]-width/2,n[locbin>cut],width =width,color='orange',alpha =0.5,label=1)
    xlist0 = np.linspace(-1,1,200)
    xlist1 = np.linspace(0,2,200)
    
    print("sigma0 = ","{:.6f}".format(sigma0)," ; sigma1 = ","{:.6f}".format(sigma1))
    
    plt.plot(locbin, p0*best_fit_line0,color='b')
    plt.plot(locbin, p1*best_fit_line1,color='orange')
    plt.plot(locbin, p0*best_fit_line0+p1*best_fit_line1,color = 'r')
    plt.legend()
    # plt.title(file+".csv")
    plt.xlabel("X")
    plt.ylabel("Probability")
    # plt.savefig(file+'_1D.png')
    plt.show()

def report(unique,counts):
    if 0 not in unique:
        p0 = 0
    else:
        p0= dict(zip(unique, counts))[0]
    if 1 not in unique:
        p1 = 0
    else:
        p1 = dict(zip(unique, counts))[1]
    return p0,p1
    
def text_report(label):
    unique, counts = np.unique(label, return_counts=True)
    print(dict(zip(unique, counts)))
    if 0 not in unique:
        p0 = 0
    else:
        p0= dict(zip(unique, counts))[0]/sum(counts)
    if 1 not in unique:
        p1 = 0
    else:
        p1 = dict(zip(unique, counts))[1]/sum(counts)
    print("\t {:<18}".format("The percentage of ")+"{:^3}".format(0)+" : {:.2f}%".format(100*p0))
    print("\t {:<18}".format("The percentage of ")+"{:^3}".format(1)+" : {:.2f}%".format(100*p1))
    return p0,p1

from sklearn.mixture import GaussianMixture
def gmm_analytic(train,excited,ground):
    training = np.stack((train['I'], train['Q']), axis=1)
    gmm = GaussianMixture(n_components=2, max_iter=8000, n_init=100, random_state=0, covariance_type='tied') 
    gmm.fit(training)
    mark_gmm= False
    data3 = np.stack((ground['I'], ground['Q']), axis=1)
    label3 = gmm.predict(data3)
    data4 = np.stack((excited['I'], excited['Q']), axis=1)
    label4 = gmm.predict(data4)
    unique3, counts3 = np.unique(label3, return_counts=True)
    unique4, counts4 = np.unique(label4, return_counts=True)
    if counts3[0]<counts4[0]:mark_gmm= True
    else:mark_gmm= False
    S,N,SNR,SNR_dB = cal_SNR(gmm,mark_gmm)
    print('S : ',S,' ; N : ',N,' ; SNR : ',SNR)
    return gmm, mark_gmm,data3,label3,data4,label4,S,N,SNR,SNR_dB

def gmm_predict(data1,gmm,mark_gmm):
    data2 = np.stack((data1['I'], data1['Q']), axis=1)
    label2 = gmm.predict(data2)
    if mark_gmm: label2 = change_label(label2)
    p0,p1 = text_report(label2)
    return p0,p1

def std_dev(l,mean):
        if len(l)<10:
            out = 0
        else:
            out = np.lib.scimath.sqrt(sum((i-mean)**2 for i in l) / len(l))
        return out

def show_gmm(show_para):
    data1,label1,data2,label2,cluster_centers,cov,samplename,jobid,mark_gmm,XYL,ROL = show_para
    unique1, counts1 = np.unique(label1, return_counts=True)
    unique2, counts2 = np.unique(label2, return_counts=True)
    plt.figure(figsize=(18, 27))
    ax1 = plt.subplot(321)
    ax1.axis('equal')
    ax1.grid()
    scatter1 = ax1.scatter(data1[:, 0],data1[:, 1],c=label1)
    legend1 = ax1.legend(*scatter1.legend_elements(), title="Classes")
    ax1.add_artist(legend1)
    ax1.title.set_text("XYL : "+str(XYL[0])+" with "+str(dict(zip(unique1, counts1))))
    ax1.title.set_size(20)
    for i in range(len(cluster_centers)):
        confidence_ellipse_gmm(cluster_centers[i],cov, ax1, n_std=1,facecolor='pink', edgecolor='firebrick',alpha= 0.3)
        confidence_ellipse_gmm(cluster_centers[i],cov, ax1, n_std=2,edgecolor='fuchsia', linestyle='--')
        confidence_ellipse_gmm(cluster_centers[i],cov, ax1, n_std=3,edgecolor='blue', linestyle=':')
        ax1.scatter(cluster_centers[i][0],cluster_centers[i][1],color = "r")
    ax2 = plt.subplot(322)
    ax2.axis('equal')
    ax2.grid()
    scatter2 = ax2.scatter(data2[:, 0],data2[:, 1],c=label2)
    legend2 = ax2.legend(*scatter2.legend_elements(), title="Classes")
    ax2.add_artist(legend2)
    ax2.title.set_text("XYL : "+str(XYL[1])+" with "+str(dict(zip(unique2, counts2))))
    ax2.title.set_size(20)
    for i in range(len(cluster_centers)):
        confidence_ellipse_gmm(cluster_centers[i],cov, ax2, n_std=1,facecolor='pink', edgecolor='firebrick',alpha= 0.3)
        confidence_ellipse_gmm(cluster_centers[i],cov, ax2, n_std=2,edgecolor='fuchsia', linestyle='--')
        confidence_ellipse_gmm(cluster_centers[i],cov, ax2, n_std=3,edgecolor='blue', linestyle=':')
        ax2.scatter(cluster_centers[i][0],cluster_centers[i][1],color = "r")
    
    p0_1,p1_1 = counts1[0]/(counts1[0]+counts1[1]),counts1[1]/(counts1[0]+counts1[1])
    p0_2,p1_2 = counts2[0]/(counts2[0]+counts2[1]),counts2[1]/(counts2[0]+counts2[1])
    bins = 750
    if mark_gmm:
        refpoint = cluster_centers[1]
        diff = cluster_centers[0]-cluster_centers[1]
    else:
        refpoint = cluster_centers[0]
        diff = cluster_centers[1]-cluster_centers[0]
    data1_1D = (data1-refpoint)@diff/(scipy.linalg.norm(diff))**2
    data2_1D = (data2-refpoint)@diff/(scipy.linalg.norm(diff))**2
    xlist0 = np.linspace(-1,1,200)
    xlist1 = np.linspace(0,2,200)
    sigma0_1 = std_dev(data1_1D[data1_1D<=0],0)
    sigma1_1= std_dev(data1_1D[data1_1D>=1],1)
    sigma0_2 = std_dev(data2_1D[data2_1D<=0],0)
    sigma1_2= std_dev(data2_1D[data2_1D>=1],1)
    
    ax3 = plt.subplot(312)
    ax3.grid()
    n1,locbin1,patch1 =ax3.hist(data1_1D, bins, density=True,alpha=.1)
    locbin1 = np.delete(locbin1, 0)
    width1 = locbin1[1]-locbin1[0]
    ax3.bar(locbin1[locbin1<0.5]-width1/2,n1[locbin1<0.5],width =width1,color='b',alpha =0.5,label=0)
    ax3.bar(locbin1[locbin1>0.5]-width1/2,n1[locbin1>0.5],width =width1,color='orange',alpha =0.5,label=1)
    best_fit_line0_1 = scipy.stats.norm.pdf(locbin1, 0, sigma0_1)
    best_fit_line1_1 = scipy.stats.norm.pdf(locbin1, 1, sigma1_1)
    ax3.plot(locbin1, p0_1*best_fit_line0_1,color='b')
    ax3.plot(locbin1, p1_1*best_fit_line1_1,color='orange')
    ax3.plot(locbin1, p0_1*best_fit_line0_1+p1_1*best_fit_line1_1,color = 'r')
    ax3.legend()
    ax3.set_xlabel("X")
    ax3.set_ylabel("Probability")
    ax3.title.set_text("XYL : "+str(XYL[0])+" with "+str(dict(zip(unique1, [round(p0_1,5),round(p1_1,5)]))))
    ax3.title.set_size(20)
    
    ax4 = plt.subplot(313)
    ax4.grid()
    n2,locbin2,patch2 =ax4.hist(data2_1D, bins, density=True,alpha=.1)
    locbin2 = np.delete(locbin2, 0)
    width2 = locbin2[1]-locbin2[0]
    ax4.bar(locbin2[locbin2<0.5]-width2/2,n2[locbin2<0.5],width =width2,color='b',alpha =0.5,label=0)
    ax4.bar(locbin2[locbin2>0.5]-width2/2,n2[locbin2>0.5],width =width2,color='orange',alpha =0.5,label=1)
    best_fit_line0_2 = scipy.stats.norm.pdf(locbin2, 0, sigma0_2)
    best_fit_line1_2 = scipy.stats.norm.pdf(locbin2, 1, sigma1_2)
    ax4.plot(locbin2, p0_2*best_fit_line0_2,color='b')
    ax4.plot(locbin2, p1_2*best_fit_line1_2,color='orange')
    ax4.plot(locbin2, p0_2*best_fit_line0_2+p1_2*best_fit_line1_2,color = 'r')
    ax4.legend()
    ax4.set_xlabel("X")
    ax4.set_ylabel("Probability")
    ax4.title.set_text("XYL : "+str(XYL[1])+" with "+str(dict(zip(unique2, [round(p0_2,5),round(p1_2,5)]))))
    ax4.title.set_size(20)
    S = np.linalg.norm(cluster_centers[0]-cluster_centers[1])**2
    N = 2*np.sqrt(cov[0,0]**2+cov[1,1]**2)
    SNR = S/N
    plt.suptitle("ROL : {:s} #{:d} ; SNR : {:.2f}".format(ROL,jobid,SNR),fontsize=28)
    plt.show()

def unpack(index,li):
    l = li.copy()
    out = ['']*len(li)
    for i in range(len(li)):
        l.pop(0)
        if len(l)==0:
            out[i]=index%li[-1]
        else:
            out[i]=(index//np.prod(l))%li[i]
    return out

import time
def gmm_defined_analytic(pyqum_path,samplename,df_local_csv=''):
    pyqum = Load_pyqum(pyqum_path)
    # loaded dataframe
    df = pyqum.dataframe
    # loaded jobid
    jobid = pyqum.jobid
    # Loaded R-JSON
    rjson = pyqum.rjson()
    key = list(df.select_dtypes('number').columns)
    gmm_condition = ['ROF','ROL','XYF']
    gmm_parameter = ['XYL','TOMO', 'TOMOR']
    removable = ['RECORD-SUM','I','Q','Amp','UPhase']
    [key.remove(i) for i in removable if i in key]
    # [print('{:^15} : {:^6} to {:^6} * {:^5}'.format(i,df[i].min(),df[i].max(),df[i].nunique())) for i in key]
    row = np.prod(df[key].nunique())
    result = ['0','1','SNR','T(mk)']
    gmm_condition_count = ['']*len(gmm_condition)
    scroll = 0
    tmp = gmm_condition.copy()
    for index ,value in enumerate(tmp):
        if value not in df:
            if value not in rjson:
                gmm_condition.remove(value)
                scroll += 1
                gmm_condition_count.pop()
            else:
                gmm_condition_count[index-scroll]  = 1
        else:
            gmm_condition_count[index-scroll] = df[value].nunique()
    gmm_parameter_count = ['']*len(gmm_parameter)
    scroll = 0
    tmp = gmm_parameter.copy()
    for index ,value in enumerate(tmp):
        if value not in df:
            if value not in rjson:
                gmm_parameter.remove(value)
                scroll += 1
                gmm_parameter_count.pop()
            else:
                gmm_parameter_count[index-scroll]  = 1
        else:
            gmm_parameter_count[index-scroll] = df[value].nunique()
    df_local_csv = DataFrame({key: [] for key in ['JOBID']+gmm_condition+gmm_parameter+result})
    ground_index, excited_index = 0,-1
    XYL_ground, XYL_excited = df['XYL'].unique()[ground_index],df['XYL'].unique()[excited_index]

    time_start = time.time()
    for i in range(prod(gmm_condition_count)):
        print('\n')
        gmm_status = unpack(i,gmm_condition_count)
        train = df
        status = ['']*len(gmm_condition)
        for pos,label in enumerate(gmm_status):
            if gmm_condition[pos] not in df:
                try:
                    status[pos] = rjson[gmm_condition[pos]]
                except:
                    print("There is no {} in R-JSON.".format(gmm_condition[pos]))
                if label == 'ROL':
                    ROL=str(rjson[gmm_condition[pos]])
            else:
                compare = df[gmm_condition[pos]].unique()[label]
                status[pos] = compare
                train = train[train[gmm_condition[pos]]==compare]
                if label == 'ROL':
                    ROL=str(compare)
        test = train
        # ------- train -------
        # if 'TOMO' in train:
        #     train = train[train['TOMO']==0]
        excited = train[train["XYL"]==XYL_excited]
        ground = train[train["XYL"]==XYL_ground]
        gmm, mark_gmm,data1,label1,data2,label2,SNR = gmm_analytic(train,excited,ground)
        # S,N,SNR,SNR_dB = cal_SNR(gmm,change_label)
        meas_condition = dict(zip(gmm_condition,status))
        print(meas_condition)
        title =''
        for key,value in meas_condition.items():
            title +='{:^3}_{:.4f} , '.format(key,float(value))
        print_para = data1,label1,data2,label2,gmm.means_,gmm.covariances_,samplename,jobid \
                                ,mark_gmm,[XYL_ground,XYL_excited],title,float(meas_condition['XYF'])

        gmm_plot_class(print_para)

        # ------- test -------
        for j in range(np.prod(gmm_parameter_count)):
            data = test
            predict_status = unpack(j,gmm_parameter_count)
            status_index = ['']*len(gmm_parameter)
            for pos,label in enumerate(predict_status): 
                try:
                    compare = df[gmm_parameter[pos]].unique()[label]
                    status_index[pos] = compare
                    data = data[data[gmm_parameter[pos]]==compare]
                except ValueError:
                        print("There is no {} in R-JSON.".format(label))
            print("\t"+str(dict(zip(gmm_parameter,status_index))))
            p0,p1 = gmm_predict(data,gmm,mark_gmm)
            if dict(zip(gmm_parameter,status_index))['XYL'] == XYL_ground:
                T = cal_Tmk(p1,float(meas_condition['XYF']))
            else:
                T = ''
            df_local_csv.loc[len(df_local_csv)] =[jobid]+status+status_index+[p0,p1,SNR,T]
    return df_local_csv,jobid

def find_file(foldername,user_input = -1):
    file_dir = listdir(foldername)
    input_message = "Pick an option:\n"
    for index, item in enumerate(file_dir):
        if index%5!=4:
            input_message += f'{index+1}) {item}\t'
        else:
            input_message += f'{index+1}) {item}\n'
    if int(user_input)== -1:
        user_input = input(input_message+'\nYour Choice is ')
    return foldername+file_dir[int(user_input) - 1]