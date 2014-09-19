# -*- coding: utf-8 -*-
"""
Created on Wed Sep 10 12:15:34 2014

@author: ngdavid
"""e
from HEADER_Find_FCS_files import Find_FCS_Files
from HEADER_Import_FCS import import_FCS_file
from HEADER_ND_Binning import ND_Binning
from HEADER_Generate_HDF5 import Bin_2_HDF5_File

Pattern = [['Myeloid 1'],['Myeloid 2'], ['Myeloid 4','T Cells']]

Dir = "/home/ngdavid/Desktop/Ubuntu_Dropbox/Myeloid_Data/Myeloid"

File_list = '/home/ngdavid/Desktop/Ubuntu_Dropbox/Myeloid_Data/Myeloid/file_list.txt'

comp_file={'Myeloid 1': '/home/ngdavid/Desktop/Ubuntu_Dropbox/Comp_Libs/M1_Comp_Lib_LSRA.txt',
           'Myeloid 2': '/home/ngdavid/Desktop/Ubuntu_Dropbox/Comp_Libs/M2_Comp_Lib_LSRA.txt',
           'Myeloid 4': '/home/ngdavid/Desktop/Ubuntu_Dropbox/Comp_Libs/M4_Comp_Lib_LSRA.txt',
           'T Cells': '/home/ngdavid/Desktop/Ubuntu_Dropbox/Comp_Libs/M1_Comp_Lib_LSRA.txt'}
#note, CD19-PE-TR was changed to CD19 PE-CF594 at some point}
parameters = {
    'Myeloid 1': ['FSC-A', 'SSC-H', 'CD15 FITC', 'CD33 PE', 'CD19 PE-TR',
                  'CD117 PE-Cy5','CD13 PE-Cy7', 'HLA-DR PB', 'CD38 A594', 
                  'CD34 APC', 'CD71 APC-A700', 'CD45 APC-H7'], 
    'Myeloid 2': ['FSC-A', 'SSC-H', 'CD64 FITC', 'CD123 PE', 'CD4 PE-TR', 
                  'CD14 PE-Cy55', 'CD13 PE-Cy7', 'HLA-DR PB', 'CD38 A594', 'CD34 APC', 
                  'CD16 APC-A700', 'CD45 APC-H7'], 
    'Myeloid 4': ['FSC-A', 'SSC-H', 'CD56 A488', 'CD7 PE', 'CD5 PE-Cy5', 
                  'CD34 APC', 'CD45 APC-H7'],
    'T Cells'   : ['FSC-A', 'SSC-H', 'CD56 PE-Cy5', 'CD7 APC', 'CD5 PE',
                  'CD34 PE-TR', 'CD45 APC-H7']}

coords={'singlet': [ (0.01,0.06), (0.60,0.75), (0.93,0.977), (0.988,0.86),
                     (0.456,0.379),(0.05,0.0),(0.0,0.0)],
        'viable': [ (0.358,0.174), (0.609,0.241), (0.822,0.132), (0.989,0.298),
                    (1.0,1.0),(0.5,1.0),(0.358,0.174)]}

output_file = '/home/ngdavid/Documents/test_file.hdf5'


FCS_Folder = Find_FCS_Files(Dir,File_list,Pattern)
Cases = FCS_Folder.search_by_case()

tube, binning = {},{}

HDF5_Cases = Bin_2_HDF5_File(output_file)

for case_num,tubes in Cases.items():
    for k in tubes.keys():
        tube[k] = import_FCS_file(Cases[case_num][k],comp_file,gate_coords=coords,limits=True)
        binning[k] = ND_Binning(tube[k],parameters,bins=10)
    HDF5_Cases.push_case(case_num,tube,binning,ordering = Pattern)

HDF5_Cases.close_case()
