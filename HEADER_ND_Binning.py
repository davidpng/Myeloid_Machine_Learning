# -*- coding: utf-8 -*-
"""
Created on Wed Sep 10 13:26:27 2014
High-D-Binning Function
@author: ngdavid
"""
import pandas as pd
import numpy as np
import scipy as sp
from HEADER_Import_FCS import import_FCS_file


class ND_Binning(import_FCS_file):
    """
    Creates an N-Dimenstional Bin into a sparse array
    """
    def __init__(self,tube_class,parameters,bins=10):
        """
        input_data - pandas DF
        columns - dictionary of parameters to use
        bins - 3 options
            int  - equal size bins
            list - lists of bin sizes
            dict - columns names with list of bin divisions
        """
        self.columns = parameters[tube_class.tube_name]
        self.bins = self._Generate_Bin_Dict(self.columns,bins)
        self.vector_length,self.coordinates = self._Uniform_Bin_Data(tube_class.data)
        self.histogram = self._coord2sparse_histogram().tocsr()
                
    def _coord2sparse_histogram(self):
        output=sp.sparse.lil_matrix((1,self.vector_length), dtype=np.float32)
        for i in self.coordinates:
            output[0,i]+=1
        return output/ len(self.coordinates)
         
    def _Uniform_Bin_Data(self,input_data):
        basis = [1]
        for i in self.bins.values:
            basis.append(i*basis[-1])
        vector_length = basis.pop() # this is the highest coordinate value
        basis = pd.Series(data=basis,index = self.bins.index.values)
        rounded = input_data.copy()
        for key in self.bins.index.values:
            rounded[key] = np.floor(rounded[key]*self.bins[key])
        output = rounded[self.bins.index.values].dot(basis)
        return vector_length, output.apply(np.int64)
        
    def _Generate_Bin_Dict(self,columns,bins):
        """
        Performs error checking and type converion for bins
        """
        if isinstance(bins,int):
            bin_dict = pd.Series([bins] * len(columns),index=columns)
        elif isinstance(bins,list):
            if len(bins) != len(columns):
                raise RuntimeWarning("number of bins in the list does not match the number of parameters")
            else:
                bin_dict = pd.Series(bins,columns)
        elif isinstance(bins,dict):
            if bins.keys() not in columns or columns not in bins.keys():
                raise RuntimeWarning("The bin keys do not match the provided columns")
            else:
                raise RuntimeWarning("bin dict not implemented")
        else:
            raise TypeError("provided bins parameter is not supported")
        return bin_dict
    
    def Return_Coordinates(self,index):
        """
        Returns the bin parameters 
        """
        coords = self.histogram.indices[index]
        self.x = np.array(np.unravel_index(coords,list(self.bins)),dtype=np.float32).T
        return pd.DataFrame(self.x / np.array(self.bins)[np.newaxis],
                            index = coords,
                            columns=self.bins.index.values)

if __name__ == "__main__":
    from HEADER_Import_FCS import import_FCS_file

    filename='/home/ngdavid/Desktop/Ubuntu_Dropbox/Myeloid_Data/Myeloid/12-00005/12-00005_Myeloid 2.fcs'
    comp_file='/home/ngdavid/Desktop/Ubuntu_Dropbox/Comp_Libs/M2_Comp_Lib_LSRA.txt'
    M4_tube=import_FCS_file(filename,comp_file,limits=True)
    parameters = [x for x in M4_tube.data.columns if x not in ['FSC-H','SSC-A','Time']]
    binned_data = ND_Binning(M4_tube,parameters,bins=10)
    print binned_data.Return_Coordinates([5,6,7,8,9])
