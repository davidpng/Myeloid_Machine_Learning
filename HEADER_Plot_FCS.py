# -*- coding: utf-8 -*-
"""
Created on Thu Sep 11 15:13:48 2014
Plot creation functions
@author: ngdavid
"""
import numpy as np
import matplotlib.pyplot as plt

def Channel_Histograms(input_DF,exclude = ['FSC-A','FSC-H','Time']):
    plt.figure(figsize=(10,16))
    param = [x for x in input_DF.columns.values if x not in exclude]
    i=1
    for x in param:
        plt.subplot(len(param),1,i)
        plt.title(x)
        plt.hist(input_DF[x],bins=500,range=(-0.5,1),edgecolor='b')
        i+=1
    plt.tight_layout()
        
Channel_Histograms(test.data)