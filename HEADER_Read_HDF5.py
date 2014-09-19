# -*- coding: utf-8 -*-
"""
Created on Tue Sep 16 13:14:35 2014
HEADER Read_HDF5_Binned_Data
Class to read and manipulate data saved in a HDF5 file by prior program
@author: ngdavid
"""
__author__ = "David Ng, MD"
__copyright__ = "Copyright 2014, David Ng"
__license__ = "GPL v3"
__version__ = "0.5"
__maintainer__ = "David Ng"
__email__ = "ngdavid@uw.edu"
__status__ = "Development"

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
        
    def _Return_CSR_Matrix(self,cases):
        """returns CSR matrix for a case or list of cases"""
        if isinstance(cases,str):
            cases = [cases]
        if isinstance(cases,list):
            matrix_list=[]
        else:
            raise IOError('Cases is not of a proper type')
            
        for case in cases:
            data = self.hd5f_object['/data'][case]['data']
            indices = self.hd5f_object['/data'][case]['indices']
            indptr = self.hd5f_object['/data'][case]['indptr']
            shape = self.hd5f_object['/data'][case]['shape']
            matrix_list.append(sp.csr_matrix((data,indices,indptr),shape = shape))
        return sp.vstack(matrix_list)
        
    def _Return_LIL_Matrix(self,cases):
        """returns LIL matrix for a case or list of cases"""
        if isinstance(cases,str):
            cases = [cases]
        elif isinstance(cases,list):
            matrix_list=[]
        else:
            raise IOError('Cases is not of a proper type')
 
        for case in cases:
                data = self.hd5f_object['/data'][case]['data']
                indices = self.hd5f_object['/data'][case]['indices']
                indptr = self.hd5f_object['/data'][case]['indptr']
                shape = self.hd5f_object['/data'][case]['shape']
                matrix_list.append(sp.csr_matrix((data,indices,indptr),shape = shape))
        return sp.vstack(matrix_list).tolil()
            
    def Return_Dense_Matrix(self,cases,columns):
        """
        Returns a dense pandas dataframe given columns and cases
        """
        dense_array = Cases._Return_LIL_Matrix(cases)[:,columns].todense()
        return pd.DataFrame(data = dense_array,index = cases, columns = columns)
        #return Cases._Return_LIL_Matrix(cases)[:,columns].todense()

    def Filter_by_Variance(self,cases,columns,**kwargs):
        """
        Filters columns by Variance using a cutoff or fraction
        """
        if kwargs.has_key('cutoff'):
            t=self.Return_Dense_Matrix(cases,columns)
            mask = t.var(axis=0) > kwargs['cutoff']
            return t.icol(np.where(mask)[0])
        elif kwargs.has_key('fraction'):
            print "not implemented yet"
            return None
    def Close_Case(self):
        self.hd5f_object.close()
        
if __name__ == "__main__":
    filename = '/home/ngdavid/Documents/test_file.hdf5'
    Cases = Manipulated_Binned_HDF5(filename)
    union = Cases.Find_Union_Indices()
    k=Cases.hd5f_object['data'].keys()
    for k in Cases.hd5f_object['data'].keys():
        print Cases.hd5f_object['data'][k]['data']
    #t1=Cases.Return_Dense_Matrix(Cases.List_Cases(),union)
    #t2 = Cases.Return_CSR_Matrix(Cases.List_Cases())
    t1=Cases.Filter_by_Variance(Cases.List_Cases(),union,cutoff=10e-13)
    print t1