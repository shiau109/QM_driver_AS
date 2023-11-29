from tools.tool import gmm_analytic,confidence_ellipse_gmm,cal_Tmk,change_label,text_report
from numpy import array, delete, sqrt, arange, absolute
from numpy import linspace, stack, unique, average, sort
from plotly import graph_objects as go
from plotly.offline import init_notebook_mode, iplot
from scipy.optimize import curve_fit
from scipy.linalg import norm
from scipy import stats
from tools.Load_PYQUM import Load_pyqum
import matplotlib.pyplot as plt
from math import erf
import pandas as pd
'''for continuous'''
def recordTIME_AVGer(df):
    keys = list(df.to_dict().keys())
    df_new = {}
    var_keys = [] # should 1< len <= 3
    for col_name in keys:
        if col_name not in ["RECORD_TIME_NS", "RECORD-SUM"] :
            df_new[col_name] = []
            if col_name not in ["I", "Q"]:
                var_keys.append(col_name)
    # len = 2           
    if len(var_keys) == 2:
        for var_1 in df[var_keys[0]].unique():
            for var_2 in df[var_keys[1]].unique():
                df_2 = df[(df[var_keys[0]]==var_1) & (df[var_keys[1]]==var_2)]
                I_avg = average(df_2["I"])
                Q_avg = average(df_2["Q"])
                df_new[var_keys[0]].append(var_1)
                df_new[var_keys[1]].append(var_2)
                df_new["I"].append(I_avg)
                df_new["Q"].append(Q_avg)
    # len = 3           
    if len(var_keys) == 3:
        for var_1 in df[var_keys[0]].unique():
            for var_2 in df[var_keys[1]].unique():
                for var_3 in df[var_keys[2]].unique():
                    df_2 = df[(df[var_keys[0]]==var_1) & (df[var_keys[1]]==var_2) & (df[var_keys[2]]==var_3)]
                    I_avg = average(df_2["I"])
                    Q_avg = average(df_2["Q"])
                    df_new[var_keys[0]].append(var_1)
                    df_new[var_keys[1]].append(var_2)
                    df_new[var_keys[2]].append(var_3)
                    df_new["I"].append(I_avg)
                    df_new["Q"].append(Q_avg)        
            
            
    df_new = pd.DataFrame.from_dict(df_new)
    return df_new

''' for one shot'''
class GMM_MDs():
    def __init__(self,T1,XYF,XYL,T_ro):
        self.plot_range = ()
        self.overlap_error = 0.1
        self.transit_error = 0.5*T_ro/T1
        self.fq = XYF
        self.XYL = XYL # np.unique(XYL)
    
        
    def give_plotRange(self,g_df=[], e_df=[]):
        """give the iq clouds figure area to plot"""
        xaxis,yaxis = 'I','Q'
        axis0_xrange=array([min(g_df[xaxis].min(),e_df[xaxis].min())-max(g_df[xaxis].var(),e_df[xaxis].var()),\
                            max(g_df[xaxis].max(),e_df[xaxis].max())+max(g_df[xaxis].var(),e_df[xaxis].var())])
        axis0_yrange=array([min(g_df[yaxis].min(),e_df[yaxis].min())-max(g_df[yaxis].var(),e_df[yaxis].var()),\
                            max(g_df[yaxis].max(),e_df[yaxis].max())+max(g_df[yaxis].var(),e_df[yaxis].var())])
        xrange = array([min(axis0_xrange.min(),axis0_xrange.min()),max(axis0_xrange.max(),axis0_xrange.max())])
        yrange = array([min(axis0_yrange.min(),axis0_yrange.min()),max(axis0_yrange.max(),axis0_yrange.max())])
        self.plot_range = [xrange, yrange]
        
    def train_model(self,df=[],Gdf=[],Edf=[],group_num=2):
        """train the gmm model with a ROF and ROL"""
        ground, excited = Gdf, Edf
        ground_index, excited_index = 0,-1
        gmm, mark_gmm,data1,label1,data2,label2,S,N,SNR,self.SNR_dB = gmm_analytic(df,Edf,Gdf,group_num)
        
        if mark_gmm : 
            label1 = change_label(label1)
            label2 = change_label(label2)  
        
        marker_size = Gdf['I'].shape[0]/group_num/1e5
        self.give_plotRange(g_df=Gdf, e_df=Edf)
        self.overlap_error = 1 - (1+erf(((SNR**2)/8)**0.5))/2
        self.RO_error = self.overlap_error + self.transit_error
        self.MD = gmm
        self.mark_gmm = mark_gmm
        self.marker_size = marker_size
        self.DL_1 = {"data":data1,"label":label1}
        self.DL_2 = {"data":data2,"label":label2}
        self.iq_projector()
        
        
        
    def model_predict(self,df=[],mode="label"):
        """input a df return the iq data array and predict labels list"""
        data = stack((df['I'], df['Q']), axis=1)
        label = self.MD.predict(data)
        if self.mark_gmm:
            label = change_label(label)
        if mode == 'label':
            return {"data":data,"label":label} 
        else:
            p0,p1 = text_report(label)
            return {"Pg":p0,"Pe":p1}
    
    def iq_projector(self):
        """project the iq clouds along coaxial axis"""
        lable1, counts1 = unique(self.DL_1["label"], return_counts=True)
        label2, counts2 = unique(self.DL_2["label"], return_counts=True)
        p1b1,p1b2 = counts1[0]/(counts1[0]+counts1[1]),counts1[1]/(counts1[0]+counts1[1])
        p2b1,p2b2 = counts2[0]/(counts2[0]+counts2[1]),counts2[1]/(counts2[0]+counts2[1])
        if self.mark_gmm:
            refpoint = self.MD.means_[1]
            diff = self.MD.means_[0] - self.MD.means_[1]
        else:
            refpoint = self.MD.means_[0]
            diff = self.MD.means_[1] - self.MD.means_[0]
        data1_1D = (self.DL_1["data"]-refpoint)@diff/(norm(diff))**2
        data2_1D = (self.DL_2["data"]-refpoint)@diff/(norm(diff))**2
        d = norm(diff)  # distance between g & e center
        v = self.MD.means_[1]-self.MD.means_[0]
        rotation_matrix = array([[ v[0]/d,  -v[1]/d],[ v[1]/d,  v[0]/d]])
        cov = rotation_matrix @ self.MD.covariances_ @ rotation_matrix.T/(d**2) # normalized rotated conv matrix
        sigma = sqrt(cov[0][0])
        
        x = linspace(-1,2,10000)
        bins = 100
        best_fit_line0 = stats.norm.pdf(x,0, sigma)
        best_fit_line1 = stats.norm.pdf(x,1, sigma)

        cdf0 = stats.norm.cdf(x,0, sigma)   # cumulative distribution function
        cdf1 = stats.norm.cdf(x,1, sigma)

        # y-> 機率相減, pdf0->blue, pedf1->red, cdf0->cumulative blue, cdf1->cumulative red
        a =pd.DataFrame({'x':x,'y':p1b1*best_fit_line0-p1b2*best_fit_line1,'pdf0':p1b1*best_fit_line0,\
                         'pdf1':p1b2*best_fit_line1,'cdf0':p1b1*cdf0,'cdf1':p1b2*cdf1})
        b =pd.DataFrame({'x':x,'y':p2b1*best_fit_line0-p2b2*best_fit_line1,'pdf0':p2b1*best_fit_line0,\
                         'pdf1':p2b2*best_fit_line1,'cdf0':p2b1*cdf0,'cdf1':p2b2*cdf1})

        # 鎖定中間交錯部分，0<x<1
        df_pdf = a[(a['x']<1)&(a['x']>0)]
        df_pdf_2 = b[(b['x']<1)&(b['x']>0)]
        # 藍線紅線最接近的 x, 在鎖定部分
        cut = float(df_pdf.iloc[(df_pdf['y']).abs().argsort()[:1]]['x'])
        cut2 = float(df_pdf_2.iloc[(df_pdf_2['y']).abs().argsort()[:1]]['x'])
        self.histo_parts = {"x":x,"bins":bins,"1D_data":[data1_1D,data2_1D],"cut":[cut,cut2],"best_fit_line":[best_fit_line0,best_fit_line1]}
        self.probas = {"p1b1":p1b1,"p1b2":p1b2,"p2b1":p2b1,"p2b2":p2b2}
        self.T_eff = cal_Tmk(self.probas["p1b2"],self.fq)
    
    def scatterANDsigma(self,ax,dl,**kwargs):
        if kwargs == {}:
            title_appends = ""
        else:
            title_appends = kwargs['title']
        
        """plot IQ clouds scatter"""
        clouds = ax.scatter(dl["data"][:,0],dl["data"][:,1],c=dl["label"],cmap ='bwr',s=self.marker_size)
        legend = ax.legend(*clouds.legend_elements(), title="Classes")
        ax.add_artist(legend)
        for i in range(len(self.MD.means_)):
            confidence_ellipse_gmm(self.MD.means_[i],self.MD.covariances_, ax, n_std=1,edgecolor='pink',alpha= 0.5)
            confidence_ellipse_gmm(self.MD.means_[i],self.MD.covariances_, ax, n_std=2,edgecolor='fuchsia', linestyle='--',alpha= 0.5)
            confidence_ellipse_gmm(self.MD.means_[i],self.MD.covariances_, ax, n_std=3,edgecolor='blue', linestyle=':',alpha= 0.5)
            ax.scatter(self.MD.means_[i][0],self.MD.means_[i][1],color = "black")
        statics = unique(dl["label"], return_counts=True)
            
        ax.title.set_text(title_appends+" IQ clouds with "+str(dict(zip(statics[0],statics[1]))))
        ax.title.set_size(20)
        ax.set_xlim(self.plot_range[0])
        ax.set_ylim(self.plot_range[1])
        
    def plot_iq_scatter(self,prepare_state,mode,**kwargs):
        """give IQ scatter figure. When mode isn't string type, it shows single figure depends on prepare_state (data and label dict). 
           When mode is a list contains few plot axis, it return the scatter plot in the result poster.
        """
        if kwargs == {}:
            title_appends = ""
            saveORnot = False
        else:
            try:
                title_appends = kwargs["title"]
            except:
                title_appends = ""
            try:
                saveORnot = kwargs["saveORnot"]
            except:
                saveORnot = False
        
        if not isinstance(mode,list): # give an arbitrary string to plot a specific figure
            if not isinstance(prepare_state,list): 
                plt.figure(figsize=(9,9))
                ax = plt.subplot(111)
                ax.axis('equal')
                ax.grid()
                self.scatterANDsigma(ax=ax,dl=prepare_state,title=title_appends)
                if saveORnot:
                    plt.savefig(title_appends+" IQ_clouds.png")
                plt.show()
                plt.gcf()
                
            else:
                if isinstance(title_appends,list):
                    if len(title_appends) != 2: title_appends*=2
                else:
                    title_appends = [title_appends]*2
                            
                plt.figure(figsize=(18,9))
                ax1 = plt.subplot(121)
                ax2 = plt.subplot(122)
                ax.axis('equal')
                ax.grid()
                self.scatterANDsigma(ax=ax1,dl=prepare_state[0],title=title_appends[0])
                self.scatterANDsigma(ax=ax2,dl=prepare_state[1],title=title_appends[1])
                if saveORnot:
                    plt.savefig(title_appends+" both_IQ_clouds.png")
                plt.show()
                plt.gcf()
                
        else: # poster mode
            self.scatterANDsigma(ax=mode[0],dl=prepare_state[0])
            self.scatterANDsigma(ax=mode[1],dl=prepare_state[1])
    def iq_projector_histo(self,ax,idx):
        """plot the projection histogram about IQ clouds"""
        
        if idx == 0:
            key_0, key_1 = "p1b1", "p1b2"
            fidelity = 100*self.probas[key_0]
        else:
            key_0, key_1 = "p2b1", "p2b2"
            fidelity = 100*self.probas[key_1]
        n,locbin,patch =ax.hist(self.histo_parts["1D_data"][idx], self.histo_parts["bins"], density=True,alpha=.1)
        locbin = delete(locbin, 0)
        width = locbin[1]-locbin[0]
        ax.bar(locbin[locbin<self.histo_parts["cut"][idx]]-width/2,n[locbin<self.histo_parts["cut"][idx]],\
               width =width,color='b',alpha =0.5,label=0)
        ax.bar(locbin[locbin>self.histo_parts["cut"][idx]]-width/2,n[locbin>self.histo_parts["cut"][idx]],\
               width =width,color='r',alpha =0.5,label=1)
        ax.plot(self.histo_parts["x"], self.probas[key_0]*self.histo_parts["best_fit_line"][0],color='b')
        ax.plot(self.histo_parts["x"], self.probas[key_1]*self.histo_parts["best_fit_line"][1],color='r')
        ax.plot(self.histo_parts["x"], self.probas[key_0]*self.histo_parts["best_fit_line"][0]\
                +self.probas[key_1]*self.histo_parts["best_fit_line"][1],color = 'orange')
        ax.legend()
        ax.set_xlabel("X")
        ax.set_ylabel("probability density")
        statics = unique(self.DL_1["label"])
        ax.title.set_text("XYL : "+str(self.XYL[idx])+" with "+str(dict(zip(statics, [round(self.probas[key_0],5),round(self.probas[key_1],5)])))\
                          +", Fidelity_{:.2f}%".format(fidelity))
        ax.title.set_size(20)
        
        
        
    def results_poster(self,saveORnot,**kwargs):   
        """plot oneshot analysis poster"""
        plt.figure(figsize=(18, 27))
        ax1, ax2 = plt.subplot(321), plt.subplot(322)
        ax1.axis('equal'), ax2.axis('equal')
        ax1.grid(), ax2.grid()
        self.plot_iq_scatter(prepare_state=[self.DL_1, self.DL_2],mode=[ax1, ax2],saveORnot=saveORnot)
        ax3, ax4 = plt.subplot(312), plt.subplot(313)
        ax3.grid(), ax4.grid()
        self.iq_projector_histo(ax=ax3,idx=0)
        self.iq_projector_histo(ax=ax4,idx=1)
        
        try:
            title_append = kwargs["title"] + "_"
        except:
            title_append = ""

        title = title_append + "OneShot results analysis"
        plt.suptitle("{:s} SNR : {:.2f}dB, T : {:.2f} mk, Fidelity : {:.2f}% RO Error : {:.2f}%".format(title,self.SNR_dB,\
                     self.T_eff,100*(1-self.probas["p1b2"]-self.probas["p2b1"]),100*self.RO_error),fontsize=28)
        if saveORnot :
            plt.savefig(title+".png")
        
        plt.show()
        plt.gcf()

    


        
def flip_clouds_recog(df,MDs,XYL_key): 
    """give the trained model class"""
    if XYL_key != "IF_ALIGN_MHz":
        XYLs = df[XYL_key].unique()
        df_1 = df[(df[XYL_key]==XYLs[0])]
        df_2 = df[(df[XYL_key]==XYLs[1])]
        data_1 = stack((df_1['I'], df_1['Q']), axis=1)
        data_2 = stack((df_2['I'], df_2['Q']), axis=1)
        label_1 = MDs.MD.predict(data_1)
        label_2 = MDs.MD.predict(data_2)
    else:
        data_1 = stack((df['I'], df['Q']), axis=1)
        data_2 = stack((df['I'], df['Q']), axis=1)
        label_1 = MDs.MD.predict(data_1)
        label_2 = MDs.MD.predict(data_2)
    
    return data_1, array(label_1), data_2, array(label_2)


def gene_CNOT_truthTable(Cdf,CMDs,CXYL_key,Tdf,TMDs,TXYL_key,saveORnot):
    from sklearn.mixture import GaussianMixture
    
    cXYLs = Tdf[CXYL_key].unique()
    Cg_L = cXYLs[0]
    Ce_L = cXYLs[1]
    tXYLs = Tdf[TXYL_key].unique()
    Tg_L = tXYLs[0]
    Te_L = tXYLs[1]
    
    # Control, Target
    C_GG_df = Cdf[(Cdf[CXYL_key]==Cg_L) & (Cdf[TXYL_key]==Tg_L)]
    C_GE_df = Cdf[(Cdf[CXYL_key]==Cg_L) & (Cdf[TXYL_key]==Te_L)]
    C_EG_df = Cdf[(Cdf[CXYL_key]==Ce_L) & (Cdf[TXYL_key]==Tg_L)]
    C_EE_df = Cdf[(Cdf[CXYL_key]==Ce_L) & (Cdf[TXYL_key]==Te_L)]
    
    # Control, Target
    T_GG_df = Tdf[(Tdf[CXYL_key]==Cg_L) & (Tdf[TXYL_key]==Tg_L)]
    T_GE_df = Tdf[(Tdf[CXYL_key]==Cg_L) & (Tdf[TXYL_key]==Te_L)]
    T_EG_df = Tdf[(Tdf[CXYL_key]==Ce_L) & (Tdf[TXYL_key]==Tg_L)]
    T_EE_df = Tdf[(Tdf[CXYL_key]==Ce_L) & (Tdf[TXYL_key]==Te_L)]
    
    asGG_probas = array(give_probaInfo(CMDs,TMDs,C_GG_df,T_GG_df))
    asGE_probas = array(give_probaInfo(CMDs,TMDs,C_GE_df,T_GE_df))
    asEG_probas = array(give_probaInfo(CMDs,TMDs,C_EG_df,T_EG_df))
    asEE_probas = array(give_probaInfo(CMDs,TMDs,C_EE_df,T_EE_df))
    
    TruthTabel = stack((asGG_probas,asGE_probas,asEG_probas,asEE_probas),axis=0)
    print("When input |00>: ",asGG_probas)
    print("When input |01>: ",asGE_probas)
    print("When input |10>: ",asEG_probas)
    print("When input |11>: ",asEE_probas)
    
    plot2QTOMO3DHist(TruthTabel,"CNOT truth table",saveORnot,"v1","TruthTable")
    
def predict_by_gmm(data1,gmm,mark_gmm,mode):
    data2 = stack((data1['I'], data1['Q']), axis=1)
    
    label2 = gmm.predict(data2)
    if mark_gmm: label2 = change_label(label2)
    if mode == "label":
        return label2
    else:
        p0,p1 = text_report(label2)
        return p0,p1

def give_probaInfo(MD1,MD2,dfQ1,dfQ2,target_state):
    from numpy import char
    Q1_label = array(MD1.model_predict(dfQ1,"label")['label']).astype(str)
    Q2_label = array(MD2.model_predict(dfQ2,"label")['label']).astype(str)
    labels = char.add(Q1_label,Q2_label)
    state, counts = unique(labels, return_counts=True)
    
    if target_state.lower() in ["00","gg"]:
        return dict(zip(state, counts))["00"]/sum(counts)
    elif target_state.lower() in ["01","ge"]:
        return dict(zip(state, counts))["01"]/sum(counts)
    elif target_state.lower() in ["10","eg"]:
        return dict(zip(state, counts))["10"]/sum(counts)
    elif target_state.lower() in ["11","ee"]:
        return dict(zip(state, counts))["11"]/sum(counts)
    else:
        return dict({key: val/sum(counts) for key,val in dict(zip(state, counts)).items()})
        

def plotProb3DHist(Proba,**kwargs):
    if isinstance(Proba,dict):
        Proba = list(Proba.values())
    if kwargs != {}:
        try:
            title = str(kwargs['title'])
        except:
            title = ""
        try:
            saveORnot = kwargs['saveORnot']
        except:
            saveORnot = False
        try:
            version = str(kwargs['version'])
        except:
            version = ""
    else:
        title, version, saveORnot = "", "", False
    
    fig = plt.figure(figsize=(20,20))
    ax = fig.add_subplot(111, projection='3d')
    ax.bar3d([-0.4,-0.4], [-0.4,0.6],[0,0],dx=0.8,dy=0.8,dz=Proba[:2],color=["blue",'orange'],alpha=0.7,edgecolor='black',shade=True)
    ax.bar3d([0.6,0.6], [-0.4,0.6],[0,0],dx=0.8,dy=0.8,dz=Proba[2:],color=["pink","red"],alpha=0.7,edgecolor='black',shade=True)
    ax.set_xlabel('Q1 state',fontsize=30)
    ax.set_ylabel('Q2 state',fontsize=30)
    ax.set_zticks(arange(0,max(list(Proba))+0.1,0.1))
    ax.set_title(title+' Q1Q2 state probability\n\n |00>:%.3f, |01>:%.3f, |10>:%.3f, |11>:%.3f'%tuple(Proba),fontsize=30)
    plt.xticks([0,1],fontsize=20) 
    plt.yticks([0,1],fontsize=20)
    ax.zaxis.set_tick_params(labelsize=20)
    if saveORnot :
        plt.savefig(title+"2QstateProba3DHisto"+version+".png")

    plt.show()
def plot2QTOMO3DHist(DM_2Q,title,saveORnot,version,Meas_type):
    DM_1D = array(DM_2Q).flatten()
    
    c_list = []
    a_list = []
    for i in DM_1D:
        if i < 0 :
            c_list.append("#000080")
        elif i > 0:
            c_list.append("#4682B4")
        else:
            c_list.append("white")
    if Meas_type != "TOMO":
        import matplotlib.colors as colors
        import matplotlib.cm as cm
        offset = DM_1D + absolute(DM_1D.min())
        fracs = offset.astype(float)/offset.max()
        norm = colors.Normalize(fracs.min(), fracs.max())
        c_list = cm.coolwarm(norm(fracs.tolist()))

    fig = plt.figure(figsize=(20,20))
    ax = fig.add_subplot(111, projection='3d')
    ax.bar3d([-0.4,-0.4,-0.4,-0.4,0.6,0.6,0.6,0.6,1.6,1.6,1.6,1.6,2.6,2.6,2.6,2.6], [-0.4,0.6,1.6,2.6,-0.4,0.6,1.6,2.6,-0.4,0.6,1.6,2.6,-0.4,0.6,1.6,2.6],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],dx=0.8,dy=0.8,dz=DM_1D,alpha=0.7,color=c_list,edgecolor='black',shade=True)
#     ax.bar3d([0.6,0.6], [-0.4,0.6],[0,0],dx=0.4,dy=0.4,dz=list(Proba)[2:],color=["pink","red"],alpha=0.7,edgecolor='black',shade=True)
    if Meas_type == 'TOMO':
        ax.set_xlabel('Q1 Direction',fontsize=30, labelpad=30)
        ax.set_ylabel('Q2 Direction',fontsize=30, labelpad=30)
        ax.set_title(title+'Density Matrix',fontsize=30)
    else:
        ax.set_xlabel('Prepare state',fontsize=30, labelpad=30)
        ax.set_ylabel('Measured state',fontsize=30, labelpad=30)
        ax.set_title("CNOT gate Truth Table ",fontsize=30)
    ax.set_zticks(arange(round(min(DM_1D)-0.1,1),round(max(DM_1D)+0.1,1),0.1))#round(np.min(DM_1D)-0.1,1)
    
    plt.xticks([0,1,2,3],["|00>","|01>","|10>","|11>"],fontsize=20) 
    plt.yticks([0,1,2,3],["|00>","|01>","|10>","|11>"],fontsize=20)
    ax.zaxis.set_tick_params(labelsize=20)
    positive = plt.Rectangle((0,0), 10, 10, fc="#4682B4")
    negative = plt.Rectangle((0,0), 10, 10, fc="#000080")
    if 0 not in DM_1D:
        if DM_1D.all() > 0 :
            pass
        else:
            ax.legend([positive,negative],['Positive','Negative'],fontsize=30)
    else:
        zero = plt.Rectangle((0,0), 10, 10, fc="grey")
        ax.legend([positive,negative,zero],['Positive','Negative',"Zero"],fontsize=30)
    if saveORnot :
        if Meas_type == "TOMO":
            plt.savefig("TOMO_fig/"+title+"_2QTOMO_3DHisto_v"+version+".png")
        else:
            plt.savefig("CNOT_popu/"+title+version+".png")

    plt.show()

def PlotRBcloud(df=[],group_num=2,plot=False,saveornot=False,title="None",MDs=[]):
    plotRange = MDs[-1]
    point_number = df['I'].shape[0]/group_num
    marker_size = point_number/1e5
    data, label = gmm_result_gene(df,MDs)
    
    cluster_centers, cov = MDs[0].means_, MDs[0].covariances_
    state, counts = unique(label, return_counts=True)
    
    plt.figure(figsize=(18, 18))
    ax1 = plt.subplot(111)
    ax1.axis('equal')
    ax1.grid()
    scatter = ax1.scatter(data[:, 0],data[:, 1],c=label,cmap ='bwr',s=marker_size)#,cmap ='bwr',s=marker_size
    legend = ax1.legend(*scatter.legend_elements(), title="Classes")
    ax1.add_artist(legend)
    ax1.title.set_text(str(dict(zip(state, counts))))
    ax1.title.set_size(20)
    ax1.set_xlim(plotRange[0])
    ax1.set_ylim(plotRange[1])
    for i in range(len(cluster_centers)):
        confidence_ellipse_gmm(cluster_centers[i],cov, ax1, n_std=1,edgecolor='pink',alpha= 0.5)
        confidence_ellipse_gmm(cluster_centers[i],cov, ax1, n_std=2,edgecolor='fuchsia', linestyle='--',alpha= 0.5)
        confidence_ellipse_gmm(cluster_centers[i],cov, ax1, n_std=3,edgecolor='blue', linestyle=':',alpha= 0.5)
        ax1.scatter(cluster_centers[i][0],cluster_centers[i][1],color = "black")
    plt.suptitle(title,fontsize=28)
    if saveornot :
        plt.savefig(title+"_RB.png")
    if plot:
        plt.show()
        plt.gcf()
    else:
        plt.close()
        
        
# RB related
class RBprocess():
    def __init__(self,qubit_num,group_num,**kwargs):
        """kwargs ROF1 = 666, ROF2 = 777 for 2Q \n
           Q_label='1' for 1Q""" 
        self.q_num = qubit_num
        self.k_num = group_num
         
        
        if self.q_num != 1:
            if kwargs != {}:
                self.ROiF1 = kwargs["Q1ROF"]
                self.ROiF2 = kwargs["Q2ROF"]
                self.mode = kwargs["mode"] # mr or classic
            else:
                raise TypeError("2QRB should input Q1ROF and Q2ROF !")
            self.XYLkey_name = ["Q1XYL","Q2XYL"]
            self.XYFkey_name = ["Q1XYF","Q2XYF"]
        else:
            if kwargs != {}:
                self.q_label = "Q" + str(kwargs['Q_label'])
                self.XYLkey_name = self.q_label+"XYL"
                self.XYFkey_name = self.q_label+"XYF"
            else:
                raise TypeError("1QRB should input the qubit label 'Q_label' !")
        
    def error_calc(self,error_rate):
        self.EPC = (1-error_rate)*(1-1/(2**self.q_num))
        self.EPG = self.EPC/1.875
    
    def calc_CZ_epc(self,SQ_epc):
        """give average SQ epc return CZ gate EPC"""
        SQ_epg = float(SQ_epc) / 1.875
        self.CZ_error = (self.EPC - 33*float(SQ_epg)/4)*2/3
        self.CNOT_error = self.CZ_error + 89*SQ_epg/12
        
    def Basedata_initializer(self,df):
        """A raw datafrme given, return raw dataframe and save the transition frequency.\n
           1Q : {"total_DF":df}\n 
           2Q : {"total_DF":[Q1_df, Q2_df]}
        """
        if self.q_num == 1:
            return {"total_DF":df}
        else:
            try:
                Q1_df = df[(df["IF_ALIGN_MHz"]==self.ROiF1) & (df[self.XYLkey_name[1]]==0.0)]
                Q2_df = df[(df["IF_ALIGN_MHz"]==self.ROiF2) & (df[self.XYLkey_name[0]]==0.0)]
                return {"total_DF":[Q1_df, Q2_df]}
            except:
                raise KeyError("Key name for XYL is wrong! it should be 'Q1XYL' and 'Q2XYL'.")  

    def base_df_arranger(self,df_dict):
        """A mix dataframe dict given, return the dataframe list in dict for prepare groung and prepare excite\n
           1Q : {"GEdf":[Gdf, Edf]} \n
           2Q : {"Q1_GEdf":[Q1g, Q1e],"Q2_GEdf":[Q2g, Q2e]}
        """
        if self.q_num == 1:
            if ("Q1XYL" and "Q2XYL") in list(df_dict["total_DF"].columns): # this pyqum record 2Q info.
                try:
                    if self.XYLkey_name == "Q1XYL":
                        df_dict["total_DF"] = df_dict["total_DF"][(df_dict["total_DF"]["Q2XYL"] == 0)]
                    else:
                        df_dict["total_DF"] = df_dict["total_DF"][(df_dict["total_DF"]["Q1XYL"] == 0)]
                except:
                    raise KeyError("Check the XYL key name you input. It should be Q1XYL or Q2XYL.")
                
            if "IF_ALIGN_MHz" in list(df_dict["total_DF"].columns):  # this pyqum record 2Q info.
                print(f"Two ROiF in the base df: {df_dict['total_DF']['IF_ALIGN_MHz'].unique()}")
                ROif = input("Input a ROiF you need to initialize GMM:")
                df_dict["total_DF"] = df_dict["total_DF"][(df_dict['total_DF']['IF_ALIGN_MHz'] == float(ROif))]

            try:
                Gdf = df_dict["total_DF"][df_dict["total_DF"][self.XYLkey_name]==df_dict["total_DF"][self.XYLkey_name].unique()[0]]
                Edf = df_dict["total_DF"][df_dict["total_DF"][self.XYLkey_name]==df_dict["total_DF"][self.XYLkey_name].unique()[1]]
                return {"GEdf":[Gdf, Edf]}
            except:
                raise KeyError("Key name for XYL is wrong! it should be 'Q1XYl' or 'Q2XYL'.") 
        else:
            Q1g = df_dict["total_DF"][0][(df_dict["total_DF"][0][self.XYLkey_name[0]]==df_dict["total_DF"][0][self.XYLkey_name[0]].unique()[0])]
            Q1e = df_dict["total_DF"][0][(df_dict["total_DF"][0][self.XYLkey_name[0]]==df_dict["total_DF"][0][self.XYLkey_name[0]].unique()[1])]
            Q2g = df_dict["total_DF"][1][(df_dict["total_DF"][1][self.XYLkey_name[1]]==df_dict["total_DF"][1][self.XYLkey_name[1]].unique()[0])]
            Q2e = df_dict["total_DF"][1][(df_dict["total_DF"][1][self.XYLkey_name[1]]==df_dict["total_DF"][1][self.XYLkey_name[1]].unique()[1])]
            return {"Q1_GEdf":[Q1g, Q1e],"Q2_GEdf":[Q2g, Q2e]}
    
    def RB_df_arranger(self,df):
        """a raw RB dataframe given, return the dataframe dict depends on ROiF."""
        if self.q_num == 1:
            return {"RB_df":df}
        else:
            if self.mode.lower() == 'mr':
                Q1_df = df[(df["IF_ALIGN_MHz"]==self.ROiF1)]
                Q1_df["Sequ"] *= 2
                Q2_df = df[(df["IF_ALIGN_MHz"]==self.ROiF2)]
                Q2_df["Sequ"] *= 2
            else:
                Q1_df = df[(df["IF_ALIGN_MHz"]==self.ROiF1)]
                Q2_df = df[(df["IF_ALIGN_MHz"]==self.ROiF2)]
            return {"RB_df":[Q1_df, Q2_df]}

    def preparation_statics(self,GEdf_dict):
        P00whenGG = give_probaInfo(self.Q1MD,self.Q2MD,GEdf_dict["Q1_GEdf"][0],GEdf_dict["Q2_GEdf"][0],'00')
        P01whenGE = give_probaInfo(self.Q1MD,self.Q2MD,GEdf_dict["Q1_GEdf"][0],GEdf_dict["Q2_GEdf"][1],'01')
        P10whenEG = give_probaInfo(self.Q1MD,self.Q2MD,GEdf_dict["Q1_GEdf"][1],GEdf_dict["Q2_GEdf"][0],'10')
        P11whenEE = give_probaInfo(self.Q1MD,self.Q2MD,GEdf_dict["Q1_GEdf"][1],GEdf_dict["Q2_GEdf"][1],'11')
        self.statePrepAbility = {"|00>_prepared":P00whenGG,"|01>_prepared":P01whenGE,"|10>_prepared":P10whenEG,"|11>_prepared":P11whenEE}
        return self.statePrepAbility
        

        
    def model_initializer(self,mixDF_dict,GEdf_dict,T1_list,T_ro,**kwargs):
        """Train the gmm model, 1Q : self.MDs / 2Q : self.Q1MD, self.Q2MD. """
        if self.q_num ==1 :
            self.MDs = GMM_MDs(T1=T1_list,XYF=self.fq,XYL=mixDF_dict["total_DF"][self.XYLkey_name].unique(),T_ro=T_ro)    
            self.MDs.train_model(df=mixDF_dict["total_DF"],Gdf=GEdf_dict["GEdf"][0],Edf=GEdf_dict["GEdf"][1],group_num=self.k_num)
        else:
            self.Q1MD = GMM_MDs(T1=T1_list[0],XYF=self.fq1,XYL=mixDF_dict["total_DF"][0][self.XYLkey_name[0]].unique(),T_ro=T_ro)
            self.Q2MD = GMM_MDs(T1=T1_list[1],XYF=self.fq2,XYL=mixDF_dict["total_DF"][1][self.XYLkey_name[1]].unique(),T_ro=T_ro)
            self.Q1MD.train_model(df=mixDF_dict["total_DF"][0],Gdf=GEdf_dict["Q1_GEdf"][0],Edf=GEdf_dict["Q1_GEdf"][1],group_num=self.k_num)
            self.Q2MD.train_model(df=mixDF_dict["total_DF"][1],Gdf=GEdf_dict["Q2_GEdf"][0],Edf=GEdf_dict["Q2_GEdf"][1],group_num=self.k_num)
            print(self.preparation_statics(GEdf_dict))
            if kwargs != {}:
                if "saveORnot" in list(kwargs.keys()):
                    save = kwargs["saveORnot"]
                else:
                    save = False

                if "prepare_state" in list(kwargs.keys()):
                    if kwargs["prepare_state"] in ["00","GG", "gg"]:
                        plotProb3DHist(Proba=give_probaInfo(self.Q1MD,self.Q2MD,GEdf_dict["Q1_GEdf"][0],GEdf_dict["Q2_GEdf"][0],'all'),saveORnot=save,title="Prepare |00>")
                    elif kwargs["prepare_state"] in ["11","EE", "ee"]:
                        plotProb3DHist(Proba=give_probaInfo(self.Q1MD,self.Q2MD,GEdf_dict["Q1_GEdf"][1],GEdf_dict["Q2_GEdf"][1],'all'),saveORnot=save,title="Prepare |11>")
                    elif kwargs["prepare_state"] in ["01","GE", "ge"]:
                        plotProb3DHist(Proba=give_probaInfo(self.Q1MD,self.Q2MD,GEdf_dict["Q1_GEdf"][0],GEdf_dict["Q2_GEdf"][1],'all'),saveORnot=save,title="Prepare |01>")
                    elif kwargs["prepare_state"] in ["10","EG", "eg"]:
                        plotProb3DHist(Proba=give_probaInfo(self.Q1MD,self.Q2MD,GEdf_dict["Q1_GEdf"][1],GEdf_dict["Q2_GEdf"][0],'all'),saveORnot=save,title="Prepare |10>")
                    else:
                        raise ValueError("Input prepare_state could not be recognized!")



    def RBdata_analyzer(self,RB_df_dict):
        """a RB dataframe given, return the grounded probability info.\n
           1Q : {"avgP":{"0":0.98,"5":0.9...}},"P_rec":[[0,0,0,5,5,5,...], [0.98,0.98,0.97,0.91,0.89,0.9,...]]} \n
           2Q : {"avgP":{"0":0.92,"5":0.85...},"P_rec":[[0,0,0,5,5,5,...], [0.92,0.91,0.9,0.84,0.85,0.84,...]]}
        """
        if self.q_num == 1:
            avgP0_per_gate = {}
            scatter_xaxis, scatter_yaxis = [], [] # plot the scattered probability dot on RB figure

            for gate_num in RB_df_dict["RB_df"]["Sequ"].unique():
                P0_per_time = []
                for repeat_num in RB_df_dict["RB_df"]["Repe"].unique():
                    this_time_df = RB_df_dict["RB_df"][(RB_df_dict["RB_df"]["Sequ"] == gate_num) & (RB_df_dict["RB_df"]["Repe"] == repeat_num)]
                    probas = self.MDs.model_predict(df=this_time_df,mode="proba")
                    # test 
                    labels = self.MDs.model_predict(df=this_time_df,mode="label")
                    state, count = unique(labels['label'],return_counts=True)

                    P0_per_time.append(probas["Pg"]) # to average
                    
                    scatter_xaxis.append(gate_num) # |00> probability record
                    scatter_yaxis.append(probas["Pg"])
                    
                avgP0_per_gate[str(gate_num)] = average(array(P0_per_time))
            return {"avgP":avgP0_per_gate,"P_rec":[scatter_xaxis, scatter_yaxis]}
        else:
            avgGG_per_gate = {}
            scatter_xaxis, scatter_yaxis = [], [] # plot the scattered probability dot on RB figure

            for gate_num in RB_df_dict["RB_df"][0]["Sequ"].unique():
                GG_per_time = []
                for repeat_num in RB_df_dict["RB_df"][0]["Repe"].unique():
                    Q1_oneshot_df = RB_df_dict["RB_df"][0][(RB_df_dict["RB_df"][0]["Sequ"] == gate_num) & (RB_df_dict["RB_df"][0]["Repe"] == repeat_num)]
                    Q2_oneshot_df = RB_df_dict["RB_df"][1][(RB_df_dict["RB_df"][1]["Sequ"] == gate_num) & (RB_df_dict["RB_df"][1]["Repe"] == repeat_num)]
                    P00 = give_probaInfo(self.Q1MD,self.Q2MD,Q1_oneshot_df,Q2_oneshot_df,"00")
                    
                    GG_per_time.append(P00) # to average
                    
                    scatter_xaxis.append(gate_num) # |00> probability record
                    scatter_yaxis.append(P00)
                    
                avgGG_per_gate[str(gate_num)] = average(array(GG_per_time))
            return {"avgP":avgGG_per_gate,"P_rec":[scatter_xaxis, scatter_yaxis]}
    
    def error_curveFit(self,probas_dict,**kwargs):
        def error_f(N,A,p,B):
            return A*p**N+B
        if self.q_num == 1:
            B_bot, B_top = 0.5, 1
        else:
            B_bot, B_top = 0.25, 0.5
        popt, pcov = curve_fit(error_f,array(list(probas_dict["avgP"].keys())).astype(float),array(list(probas_dict["avgP"].values())),maxfev = 100000,bounds=((0,0,B_bot),(1,1,B_top)))
        self.fitLine = error_f(array(list(probas_dict["avgP"].keys())).astype(float), *popt)
        self.error_calc(popt[1])
        if self.q_num > 1:
            try:
                SQ_epc = list(kwargs.values())[0]
                self.calc_CZ_epc(SQ_epc)
            except:
                raise ValueError("Calculate the CZ EPC needs the SQ EPC, check it !")
        

    def TQRB_plot(self,probas_dict):
        if self.q_num == 1:
            RBname = "SQRB"
            yaxis_label = "|0> probability" 
            self.CZ_error = 'nan'
            title = "%s 1Q_EPC=%.5f, CZ_error=%s"%(RBname, self.EPC,self.CZ_error)
        else:
            RBname = "TQRB"
            yaxis_label = "|00> probability"
            title = "%s 2Q_EPC=%.5f, CZ_error=%.5f"%(RBname, self.EPC,self.CZ_error)

        AVG_data = go.Scatter(
        x = array(list(probas_dict["avgP"].keys())).astype(float),
        y = list(probas_dict["avgP"].values()),
        marker = {'color': 'red','symbol':"square", 'size': 7},
        mode = 'markers',
        name = 'Average'
        )
        REC_data = go.Scatter(
        x = array(probas_dict["P_rec"][0]),
        y = array(probas_dict["P_rec"][1]),
        marker = {'color': '#1E90FF', 'size': 5},
        mode = 'markers',
        name = 'Data'
        )
        fit_Line = go.Scatter(
        x = list(probas_dict["avgP"].keys()),
        y = self.fitLine,
        marker = {'color': '#228B22', 'size': 4},
        mode = 'lines',
        name = 'Fitting'
        )
        layout = go.Layout(
        title = title,
        xaxis = {'title': 'Gate number'},
        yaxis = {'title': yaxis_label},
        font = {
        'size': 26,
        },
        plot_bgcolor='#FFF0F5',
        autosize=False,
        width=1120,
        height=630
        )
        init_notebook_mode(connected=True)
        fig = go.Figure(data = [REC_data,AVG_data,fit_Line], layout = layout)
        iplot(fig)
        
    def plot_G_num(self,RB_df_dict,gate_num_list,**kwargs):
        """plot the figure about the gate length abd the repeat time given in the list gate_num_list, kwargs["r"].
           If it didn't assign the repeat time r, there will plot all the repeat record. 
        """
        if not isinstance(gate_num_list,list):
            gate_num_list = [gate_num_list]

        if kwargs == {} :
            print("No specific repeat time, will show all records about that gate length.")
            if self.q_num == 1:
                repe_list = list(RB_df_dict["RB_df"]["Repe"].unique())
            else:
                repe_list = list(RB_df_dict["RB_df"][0]["Repe"].unique())
            saveORnot = False
        else:
            try:
                repe_list = kwargs["r"]# it should be list
            except:
                try:
                    repe_list = kwargs["R"]
                except:
                    try:
                        repe_list = kwargs["repe"]
                    except:
                        try:
                            repe_list = kwargs["Repe"]
                        except:
                            if self.q_num ==1:
                                repe_list = list(RB_df_dict["RB_df"]["Repe"].unique())
                            else:
                                repe_list = list(RB_df_dict["RB_df"][0]["Repe"].unique())
                            print("No specific repeat time, will show all records about that gate length.")
            if not isinstance(repe_list,list):
                repe_list = [repe_list]
            try:
                saveORnot = kwargs["saveORnot"]
            except:
                print("It didn't assign save figure or not so the result figure will not be saved.")
                saveORnot = False

        if self.q_num == 1:
            for gate_num in gate_num_list:
                for repeat_num in repe_list:
                    this_time_df = RB_df_dict["RB_df"][(RB_df_dict["RB_df"]["Sequ"] == gate_num) & (RB_df_dict["RB_df"]["Repe"] == repeat_num)]
                    result_dict = self.MDs.model_predict(df=this_time_df,mode="label")
                    self.MDs.plot_iq_scatter(prepare_state=result_dict,mode='single',title=f"RB @ Sequ={gate_num} & Repe={repeat_num}",saveORnot=saveORnot)
                    print("\n===============================\n")
        
        else:
            for gate_num in gate_num_list:
                for repeat_num in repe_list:
                    Q1_this_time_df = RB_df_dict["RB_df"][0][(RB_df_dict["RB_df"][0]["Sequ"] == gate_num) & (RB_df_dict["RB_df"][0]["Repe"] == repeat_num)]
                    Q2_this_time_df = RB_df_dict["RB_df"][1][(RB_df_dict["RB_df"][1]["Sequ"] == gate_num) & (RB_df_dict["RB_df"][1]["Repe"] == repeat_num)]
                    Q1_result_dict = self.Q1MD.model_predict(df=Q1_this_time_df,mode="label")
                    Q2_result_dict = self.Q2MD.model_predict(df=Q2_this_time_df,mode="label")
                    self.Q1MD.plot_iq_scatter(prepare_state=Q1_result_dict,mode='single',title=f"Q1RB @ Sequ={gate_num} & Repe={repeat_num}",saveORnot=saveORnot)
                    self.Q2MD.plot_iq_scatter(prepare_state=Q2_result_dict,mode='single',title=f"Q2RB @ Sequ={gate_num} & Repe={repeat_num}",saveORnot=saveORnot)
                    print("\n===============================\n")



# 1Q allXY related
class SQ_OXY_analyzer():
    def __init__(self,**kwargs):
        """kwargs ROF1 = 666, ROF2 = 777 for 2Q \n
           Q_label='1' for 1Q""" 
        self.k_num = 2
         
        if kwargs != {}:
            self.q_label = "Q" + str(kwargs['Q_label'])
            self.XYLkey_name = self.q_label+"XYL"
            self.XYFkey_name = self.q_label+"XYF"
        else:
            raise TypeError("plz tell me which qubit.")

    
    def base_df_arranger(self,df):
        """A mix dataframe dict given, return the dataframe list in dict for prepare groung and prepare excite\n
           2Q : {"Q1_GEdf":[Q1g, Q1e],"Q2_GEdf":[Q2g, Q2e]}
        """
        if ("Q1XYL" and "Q2XYL") in list(df.columns): # this pyqum record 2Q info.
            try:
                if self.XYLkey_name == "Q1XYL":
                    df = df[(df["Q2XYL"] == 0)]
                else:
                    df = df[(df["Q1XYL"] == 0)]
            except:
                raise KeyError("Check the XYL key name you input. It should be Q1XYL or Q2XYL.")
                
        if "IF_ALIGN_MHz" in list(df.columns):  # this pyqum record 2Q info.
            print(f"Two ROiF in the base df: {df['IF_ALIGN_MHz'].unique()}")
            ROif = input("Input a ROiF you need to initialize GMM:")
            df = df[(df['IF_ALIGN_MHz'] == float(ROif))]

        try:
            Gdf = df[df[self.XYLkey_name]==df[self.XYLkey_name].unique()[0]]
            Edf = df[df[self.XYLkey_name]==df[self.XYLkey_name].unique()[1]]
            return {"GEdf":[Gdf, Edf],"MIXdf":df}
        except:
            raise KeyError("Key name for XYL is wrong! it should be 'Q1XYl' or 'Q2XYL'.") 
        
    
    def OXY_df_arranger(self,df):
        """a raw allXY dataframe given, return the dataframe dict depends on ROiF."""
        y_deg = max(df["phase_1"].unique())
        x_deg = min(df["phase_1"].unique())
        ROdict = {}
        for xyl_1 in df["XYL_1"].unique():
            for xyl_2 in df["XYL_2"].unique():
                for phase_1 in df["phase_1"].unique():
                    for phase_2 in df["phase_2"].unique():
                        # first pulse determine X,Y,X/2,Y/2,I
                        if xyl_1 == sort(df["XYL_1"].unique())[0]:
                            label_1 = "I"
                        elif xyl_1 == sort(df["XYL_1"].unique())[-1]: 
                            if phase_1 == y_deg:
                                label_1 = "Y"
                            else:
                                label_1 = "X"
                        else:
                            if phase_1 == y_deg:
                                label_1 = "Y/2"
                            else:
                                label_1 = "X/2"
                        #second pulse determine X,Y,X/2,Y/2,I
                        if xyl_2 == sort(df["XYL_2"].unique())[0]:
                            label_2 = "I"
                        elif xyl_2 == sort(df["XYL_2"].unique())[-1]: 
                            if phase_2 == y_deg:
                                label_2 = "Y"
                            else:
                                label_2 = "X"
                        else:
                            if phase_2 == y_deg:
                                label_2 = "Y/2"
                            else:
                                label_2 = "X/2"
                        # append result df 
                        ROdict[label_1+","+label_2] = df[(df["XYL_1"]==xyl_1)&(df["XYL_2"]==xyl_2)&(df["phase_1"]==phase_1)&(df["phase_2"]==phase_2)]

        # sort key in dict
        orders = ['I,I', 'X,X', 'Y,Y', 'X,Y', 'Y,X', 'X/2,I', 'Y/2,I', 'X/2,Y/2', 'Y/2,X/2', 'X/2,Y', 'Y/2,X', 'X,Y/2', 'Y,X/2', 'X/2,X', 'X,X/2', 'Y/2,Y', 'Y,Y/2', 'X,I', 'Y,I', 'X/2,X/2', 'Y/2,Y/2']
        theoretical = [1, 1, 1, 1, 1, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0, 0, 0, 0]
        result_df_dict = {}
        self.theoretical_dict = {}
        for operation_idx in range(len(orders)) :
            result_df_dict[orders[operation_idx]] = ROdict[orders[operation_idx]]
            self.theoretical_dict[orders[operation_idx]] = theoretical[operation_idx]

        return result_df_dict

    def preparation_statics(self,GEdf_dict):
        P00whenGG = give_probaInfo(self.Q1MD,self.Q2MD,GEdf_dict["Q1_GEdf"][0],GEdf_dict["Q2_GEdf"][0],'00')
        P01whenGE = give_probaInfo(self.Q1MD,self.Q2MD,GEdf_dict["Q1_GEdf"][0],GEdf_dict["Q2_GEdf"][1],'01')
        P10whenEG = give_probaInfo(self.Q1MD,self.Q2MD,GEdf_dict["Q1_GEdf"][1],GEdf_dict["Q2_GEdf"][0],'10')
        P11whenEE = give_probaInfo(self.Q1MD,self.Q2MD,GEdf_dict["Q1_GEdf"][1],GEdf_dict["Q2_GEdf"][1],'11')
        self.statePrepAbility = {"|00>_prepared":P00whenGG,"|01>_prepared":P01whenGE,"|10>_prepared":P10whenEG,"|11>_prepared":P11whenEE}
        return self.statePrepAbility
        

        
    def model_initializer(self,mixDF_dict,GEdf_dict,T1_list,T_ro):
        """Train the gmm model, 1Q : self.MDs """
        self.MDs = GMM_MDs(T1=T1_list,XYF=self.fq,XYL=mixDF_dict[self.XYLkey_name].unique(),T_ro=T_ro)    
        self.MDs.train_model(df=mixDF_dict,Gdf=GEdf_dict["GEdf"][0],Edf=GEdf_dict["GEdf"][1],group_num=self.k_num)


    def OXYdata_analyzer(self,OXY_df_dict):
        """a allXY dataframe dict given, return the grounded probability info.\n
        """
        ground_proba = {}

        for operations in list(OXY_df_dict.keys()):
            oneshot_df = OXY_df_dict[operations]
            probas = self.MDs.model_predict(df=oneshot_df,mode="proba")
            ground_proba[operations] = probas["Pg"]
        
        return ground_proba
    

    def OXY_plot(self,probas_dict):
       
        exp_data = go.Scatter(
        x = array(list(probas_dict.keys())).astype(str),
        y = array(list(probas_dict.values())).astype(float),
        marker = {'color': '#1E90FF','symbol':"square", 'size': 7},
        mode = 'markers+lines',
        name = 'Experimental'
        )
        the_data = go.Scatter(
        x = array(list(self.theoretical_dict.keys())).astype(str),
        y = array(list(self.theoretical_dict.values())).astype(float),
        marker = {'color': 'red', 'size': 5},
        mode = 'markers+lines',
        name = 'Theoretical'
        )
        layout = go.Layout(
        title = self.q_label+"_all XY measurement results",
        xaxis = {'title': 'operations'},
        yaxis = {'title': "|0> probabilities"},
        font = {
        'size': 26,
        },
        plot_bgcolor='#FFF0F5',
        autosize=False,
        width=1120,
        height=630
        )
        init_notebook_mode(connected=True)
        fig = go.Figure(data = [exp_data,the_data], layout = layout)
        iplot(fig)
    
    def compa_plot(self,y_dict,**kwargs):
        x_axis = array(list(self.theoretical_dict.keys())).astype(str)
        y_dict["Theoretical"] = array(list(self.theoretical_dict.values())).astype(float)
        plt.figure(figsize=(18, 9))
        
        for meas in list(y_dict.keys()):
            if meas != "Theoretical":
                plt.plot(x_axis,y_dict[meas],label=meas,marker="o")
            else:
                plt.plot(x_axis,y_dict[meas],label=meas,marker="X")
        
        plt.legend()
        plt.xlabel("Operations")
        plt.ylabel("|0> probabilities")
        plt.title(self.q_label+"_all XY comparison")
        if kwargs != {}:
            if "saveORnot" in list(kwargs.keys()) and kwargs["saveORnot"]==True:
                plt.savefig()
        plt.show()

        
    def plot_operation(self,OXY_df_dict,operation_list,**kwargs):
        """plot the figure about the gate length abd the repeat time given in the list gate_num_list, kwargs["r"].
           If it didn't assign the repeat time r, there will plot all the repeat record. 
        """
        if not isinstance(operation_list,list):
            operation_list = [operation_list]

        if kwargs == {} :
            print("The result fig won't be saved.")
            saveORnot = False
        else:
            saveORnot = kwargs["saveORnot"]

        for operation in operation_list:
            this_time_df = OXY_df_dict[operation]
            result_dict = self.MDs.model_predict(df=this_time_df,mode="label")
            self.MDs.plot_iq_scatter(prepare_state=result_dict,mode='single',title=f"operation = {operation}",saveORnot=saveORnot)
            print("\n===============================\n")
           





class Data_transformer():
    def __init__(self,file_path,mode,datatype):
        self.path = file_path
        self.mode = mode
        self.datatype = datatype
    
    # load different types of raw data into dataframe
    def from_pyqum(self):
        """turns the pyqum file into a raw dataframe"""
        df = Load_pyqum(self.path).dataframe
        self.rjson = Load_pyqum(self.path).rjson()
        return df
    
    def from_else(self):
        pass    
    

    # raw dataframe processing
    def want_RB(self,df,Sequ_key_name,Repe_key_name):
        """edit dataframe column names into a RB recognizable form.\n
           SQRB return df with column name: Sequ, Repe, I, Q\n
           multiQRB return df with column name: Sequ, Repe, IF_ALIGN_MHz, I, Q.  
        """
        df["I"]*=1000
        df["Q"]*=1000

        if Sequ_key_name != "":
            df = df.rename({Sequ_key_name: 'Sequ'}, axis='columns')
        if Repe_key_name != "":
            df = df.rename({Repe_key_name: 'Repe'}, axis='columns')

        return df
    
    def want_GEOS(self,df):
        """return a dataframe which may contain several qubits OS info."""
        df["I"]*=1000
        df["Q"]*=1000
        return df
    
    def want_allXY(self,df):
        df["I"]*=1000
        df["Q"]*=1000

        return df


    
    def transform(self,**kwargs):
        """transform the dataframe into a specific form depends on the mode."""
        if self.mode.lower() == "rb":  # for RB
            try :
                repe_keyname = kwargs['r']
            except:
                repe_keyname = ""
            try :
                sequ_keyname = kwargs['s']
            except:
                sequ_keyname = ""
            if self.datatype.lower() == "pyqum":
                raw_df = self.from_pyqum()
            else:
                raise TypeError("Only surpport pyqum type file now!")
            recog_df = self.want_RB(raw_df,sequ_keyname,repe_keyname)
        elif self.mode.lower() == "os":  #generate an OneShot dataframe for a pretrained gmm model to predict.
            pass

        elif self.mode.lower() == "geos":  # generate the OneShot dataframe for model initializing
            if self.datatype.lower() == "pyqum":
                df = self.from_pyqum()
            else:
                raise TypeError("Only surpport pyqum type file now!")
            
            recog_df = self.want_GEOS(df)

        elif self.mode.lower() in ["allxy","oxy"]:
            if self.datatype.lower() == "pyqum":
                df = self.from_pyqum()
            else:
                raise TypeError("Only surpport pyqum type file now!")

            recog_df = self.want_allXY(df)

        else:
            pass

        return recog_df

        
             

        
        






























