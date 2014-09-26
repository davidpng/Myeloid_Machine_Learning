# -*- coding: utf-8 -*-
"""
Created on Wed Sep 10 12:15:34 2014

@author: ngdavid
"""
from HEADER_Import_FCS import import_FCS_file
from HEADER_ND_Binning import ND_Binning
from HEADER_Generate_HDF5 import Bin_2_HDF5_File
import HEADER_Program_Variables as Prog_Var

import sys
import json

case_num = sys.argv[1]
tubes = json.loads(sys.argv[2])

HDF5_Cases = Bin_2_HDF5_File(Prog_Var.output_file,overwrite=False)

tube,binning = {},{}

for k in tubes.keys():
    tube[k] = import_FCS_file(tubes[k],Prog_Var.comp_file,gate_coords=Prog_Var.coords,limits=True,strict=False)
    binning[k] = ND_Binning(tube[k],Prog_Var.parameters,bins=10)
HDF5_Cases.push_case(case_num,tube,binning,ordering = Prog_Var.Pattern,saveFCS=False)
print('{} has been pushed to {}'.format(case_num,Prog_Var.output_file))