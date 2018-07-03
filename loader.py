import sys,os
from os import listdir
from os.path import isfile, join
import numpy as np
import matplotlib.pylab as plt
import pandas as pd

path = "./DataDivided/"
features = ['CO2', 'Hum', 'Temp']# 'HeatIdx',


def get_dat(path=path,feat=['CO2'],parse=''):
    """Function to retrieve CO2 Occupancy Dataset (K30 Sensor)
    Inputs :
        path := (str) Relative path to DataDivided dir.
        feat := (list of str) Sensors to be extracted from csv. 
                Possible vals: 'CO2', 'Hum', 'Temp', 'HeatIdx'
        parse:= (str) Search string for dirs within DataDivided.
                For example, '09-' considered only September.
        

    Outputs:
        x := (list) All sensor series from files. Series vary
             in length, but all are in steps of 1min.
        y := (list) Corresponding Occ Labels.
        z := (list) Occupancy Transition Events.
     t_ind:= (list) Test index. Groups files from same test but
             multiple sensors. Used for secure Train/Test split.
    """

    feature_list = []
    label_list = []
    event_list = []
    test_list = []
    noise=0

    ti=0

    for dirname in sorted(os.listdir(path)):
    #Ignore directories not matching search str.
        if parse!='' and parse not in dirname:
            continue

        for file in os.listdir(path+dirname):
            data = pd.read_csv(join(path+dirname, file))
            sample = data.iloc[:][feat].as_matrix().T.tolist()[0]
            
            label = np.where(data.iloc[:,4]<0, 0, data.iloc[:,4])

            #Find changes in occupancy label, prepend with 0.
            event = np.insert([(label[i]!=label[i-1])*1.0 for i in range(1,len(label))],0,0)

            feature_list.append(np.array(sample))
            label_list.append(np.array(label))
            event_list.append(np.array(event))
            test_list.append(ti)
        
        ti+=1 #Increment per DIR not per FILE.

    x = np.array(feature_list)
    y = np.array(label_list)
    z = np.array(event_list)
    t_ind = np.array(test_list)

    return x,y,z,t_ind

def show_dat(x,y,z,t_ind):
    """Plots all CO2 data series, grouped by test id.
    Inputs : [All Outs from get_dat]
    Outputs: None, but makes 16 figs if no parsing.
    """
    clrs = ['b','g','r']
    #For each unique test...
    unq,cnt = np.unique(t_ind,return_counts=True)
    for u,c in zip(unq,cnt):
        f,ax_arr = plt.subplots(c+1,1,sharex=True)
        tid=t_ind[np.where(t_ind==(u))[0][0]]#Ind in x,y,z lists.
        x_set=[x[i] for i in range(len(x)) if t_ind[i] in [tid]]
        y_set=[y[i] for i in range(len(x)) if t_ind[i] in [tid]]
        z_set=[z[i] for i in range(len(x)) if t_ind[i] in [tid]]

        y_max = 450
        for ci in range(c):
            ax_arr[ci].plot(x_set[ci],color=clrs[ci])
            ax_arr[ci].set_ylabel('CO2 (ppm)')
            
            while max(x_set[ci])>y_max:
                y_max+=100
            ax_arr[c].plot(y_set[ci],color=clrs[ci])#Label same for all series within test.

        for ci in range(c):
            ax_arr[ci].set_ylim([325,y_max])
        ax_arr[c].set_ylim([-0.25,5.25])
        ax_arr[c].set_yticks([0,1,2,3,4,5])
        ax_arr[c].set_ylabel('#Occupants')
        ax_arr[c].set_xlabel('Test Time')
        


if __name__ == '__main__':
    print('Retrieving Data')
    x,y,z,t_ind=get_dat()
    print('Rendering')
    show_dat(x,y,z,t_ind)
    plt.show()
