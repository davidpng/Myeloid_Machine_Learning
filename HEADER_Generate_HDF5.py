# -*- coding: utf-8 -*-
"""
Created on Fri Sep 12 13:06:55 2014

@author: ngdavid
"""

import h5py
import numpy as np
import scipy as sp

class Bin_2_HDF5_File(object):
    def __init__(self,filename,overwrite=True):
        self.__tube_nums=0        
        self.filename=filename
        if overwrite:
            hdf5_file = h5py.File(filename,mode='w')
            hdf5_file.close()
        
    def push_case(self,case_name,tubes,binnings,saveFCS=False,**kwargs):
        """
        Takes classes tubes and binnings
        """
        if kwargs.has_key('mode'):
            hdf5_file = h5py.File(self.filename,mode=kwargs['mode'])
        else:
            hdf5_file = h5py.File(self.filename,mode='a')

        if len(tubes) != len(binnings):
            raise IOError('number of tubes and binnings do not match')
        else:
            self.__tube_nums=len(tubes)
        
        if kwargs.has_key('ordering'):
            self.ordering = self._ordering_match_pattern(tubes.keys(),kwargs['ordering'])
        else:
            self.ordering = range(len(tubes))
        
        coords = self._tube_coords(binnings)        
        self.coords = coords
        
        for i in self.ordering:
            tube_info = hdf5_file.create_group('/tube/'+case_name+'/'+str(i))
            tube_info.create_dataset('tube_name',data = tubes[i].tube_name)
            tube_info.create_dataset('antigens',data=binnings[i].columns)
            tube_info.create_dataset('bins',data=binnings[i].bins.values)
            tube_info.create_dataset('export_time',data=tubes[i].export_time)
            tube_info.create_dataset('cytometer_name',data=tubes[i].cytometer_name)
            tube_info.create_dataset('cytometer_num',data=tubes[i].cytometer_num)
            tube_info.create_dataset('total_events',data=tubes[i].total_events)
            tube_info.create_dataset('gated_events',data=tubes[i].gated_events)
            tube_info.create_dataset('tube_coords', data = coords[i])
            tube_info.create_dataset('binning_length', data = binnings[i].vector_length)
            for k,v in tubes[i].coords.items():     # go through the dict of gates
                tube_info.create_dataset('gates/'+k,data = np.array(v))
            if saveFCS:
                tube_info.create_dataset('listmode_data',data=tubes[i].data.values)
        case = hdf5_file.create_group('/data/'+case_name)
        
        data_to_write = sp.sparse.hstack([binnings[i].histogram for i in self.ordering],format='csr')
        case.create_dataset('data', data = data_to_write.data)
        case.create_dataset('indices', data = data_to_write.indices)
        case.create_dataset('indptr', data = data_to_write.indptr)
        case.create_dataset('shape',data = data_to_write.shape)
        hdf5_file.flush()
        hdf5_file.close()
        return data_to_write
        

    def _ordering_match_pattern(self,keys,pattern):
        """
        internal function that generates an ordered list of keys based on a passed pattern
        """
        output = []
        for segment in pattern:
            for tube_type in segment:
                if tube_type in keys:
                    output.append(tube_type)
                    break
        return output
        
    def _tube_coords(self, binning):
        sizes = np.array([0]+[binning[k].histogram.shape[1] for k in self.ordering])
        sizes = [sum(sizes[:i]) for i in range(1,5)]
        coords = []
        for i in range(0,len(sizes)-1):
            coords.append((sizes[i],sizes[i+1]-1))
        return dict(zip(self.ordering,coords))
        
    def _concatentate_csr_array(self,*args):
        """
        Takes multiple csr sparse arrays and concatentates them column-wise
        """
        if len(args) == 1:              # args can be passed individually or as a list
            data = np.concatenate([d.data for d in args[0]],axis=1)
            temp = [s.shape[1] for s in args[0]]   # list comp for loading the sparse_array lengths
            indices = [i.indices for i in args[0]]
        else:
            data=np.concatenate([d.data for d in args],axis=1)  # concatenate data
            temp = [s.shape[1] for s in args]   # list comp for loading the sparse_array lengths
            indices = [i.indices for i in args]
        shift=[0]                           # initialize shift
        for i in temp:
            shift.append(shift[-1]+i)   #add sparse_array lenghts recursively
        shape = (1,shift.pop())         # last lenght is the lenght of the output array
        temp = zip(indices,shift) # create a list of tuple of indices and their shift
        temp = [i+s for i,s in temp]                # add shift to the indices
        indices=np.concatenate(temp,axis=1)         # concatenate this list of shifted indicies
        indptr = np.array([0,len(indices)])         # make the indptr for new rows(not used)
        return sp.sparse.csr_matrix((data,indices,indptr),shape=shape)

if __name__ == "__main__":
    filename='/home/ngdavid/Documents/test_file.hdf5'
    
    ordering=['Myeloid 1','Myeloid 2','Myeloid 4']

    #binning[k].histogram.shape
