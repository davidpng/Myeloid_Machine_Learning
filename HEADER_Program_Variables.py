# -*- coding: utf-8 -*-
"""
Created on Fri Sep 26 16:47:20 2014
Contains program variables
@author: ngdavid
"""

Pattern = [['Myeloid 1'],['Myeloid 2'], ['Myeloid 4','T Cells']]

Dir = "/home/ngdavid/Desktop/Ubuntu_Dropbox/Myeloid_Data/Myeloid"

File_list = '/home/ngdavid/Desktop/Ubuntu_Dropbox/Myeloid_Data/Myeloid/file_list.txt'

comp_file={'H0152':'/home/ngdavid/Desktop/PYTHON/Myeloid_Machine_Learning/Input_Outputs/Comp_Libs/Spectral_Overlap_Lib_LSRA.txt',
           '1':'/home/ngdavid/Desktop/PYTHON/Myeloid_Machine_Learning/Input_Outputs/Comp_Libs/Spectral_Overlap_Lib_LSRA.txt',
           '2':'/home/ngdavid/Desktop/PYTHON/Myeloid_Machine_Learning/Input_Outputs/Comp_Libs/Spectral_Overlap_Lib_LSRB.txt'}

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

output_file = '/home/ngdavid/Documents/16_cases_temp.hdf5'