# -*- coding: utf-8 -*-
"""
Created on Tue Sep 16 13:14:35 2014
HEADER Read_HDF5_Binned_Data
@author: ngdavid
"""
import h5py
import pandas as pd
import numpy as np
import scipy.sparse as sp
class Manipulated_Binned_HDF5(object):
    """
    This class will import an HDF5 file object created by "HEADER_Generate_HDF5"
    Provides:
    Slicing
    Bin Coordinates
    
    """
    def __init__(self,filename):
        """
        Initializeation for this class
        """
        self.hd5f_object = h5py.File(filename,mode='r')
        
    def List_Cases(self):
        return [str(x) for x in self.hd5f_object['/tube'].keys()]
    
    
    def Return_Coordinates(self,case,coord):
        """
        Returns the bin parameters and the tube
        """
        tube = self.hd5f_object['/tube'][case]
        for k in tube.keys():
            print tube[k]['tube_coords'].value
            print k            
            if tube[k]['tube_coords'][0] <= coord and coord <= tube[k]['tube_coords'][1]:
                tube_name = tube[k]['tube_name']
                pointer = tube[k]['tube_coords'][0]
                bins = tube[k]['bins']
                antigens = tube[k]['antigens']
                break
        if tube[k]['tube_coords'][1] < coord:
                raise IOError('coords exceed matrix dimensions')
        shifted_coords = coord-pointer
        print shifted_coords
        x = np.array(np.unravel_index(shifted_coords,list(bins)),dtype=np.float32)
        y= x/np.array(bins)
        return tube_name.value, pd.DataFrame(data=y[np.newaxis],columns= antigens.value)
    
    def Find_Union_Indices(self):
        union = np.array([],dtype=np.int64) #initalize union as the empty set
        for case in self.List_Cases():
            union = np.union1d(union,self.hd5f_object['/data'][case]['indices'])
        return union
    
    def Filter_Matrix(self,matrix,fraction=2e-6):
        """returns CSR matrix"""
        return matrix.multiply(matrix > fraction)
        
    def Return_CSR_Matrix(self,cases):
        """returns CSR matrix for a case or list of cases"""
        if isinstance(cases,str):
            cases = [cases]
        if isinstance(cases,list):
            matrix_list=[]
            for case in cases:
                data = self.hd5f_object['/data'][case]['data']
                indices = self.hd5f_object['/data'][case]['indices']
                indptr = self.hd5f_object['/data'][case]['indptr']
                shape = self.hd5f_object['/data'][case]['shape']
                matrix_list.append(sp.csr_matrix((data,indices,indptr),shape = shape))
            return sp.vstack(matrix_list)
        else:
            raise IOError('Cases is not of a proper type')
    
    def Return_Dense_Matrix(self,matrix,columns):
        pass
    def Close_Case(self):
        self.hd5f_object.close()
        
if __name__ == "__main__":
    filename = '/home/ngdavid/Documents/test_file.hdf5'
    Cases = Manipulated_Binned_HDF5(filename)
    union = Cases.Find_Union_Indices()
    k=Cases.hd5f_object['data'].keys()
    for k in Cases.hd5f_object['data'].keys():
        print Cases.hd5f_object['data'][k]['data']
