# -*- coding: utf-8 -*-
"""
Created on Wed Sep 10 12:15:34 2014

@author: ngdavid
"""
from HEADER_Find_FCS_files import Find_FCS_Files
from HEADER_Import_FCS import import_FCS_file
from HEADER_ND_Binning import ND_Binning
from HEADER_Generate_HDF5 import Bin_2_HDF5_File
import HEADER_Program_Variables as Prog_Var

import tempfile
import json
import subprocess

FCS_Folder = Find_FCS_Files(Prog_Var.Dir,Prog_Var.File_list,Prog_Var.Pattern)
Cases = FCS_Folder.search_by_case()

for case_num,tubes in Cases.items():
    tube,binning = {},{}
    HDF5_Cases = Bin_2_HDF5_File(Prog_Var.output_file,overwrite=False)
    for k in tubes.keys():
        tube[k] = import_FCS_file(tubes[k],Prog_Var.comp_file,gate_coords=Prog_Var.coords,limits=True,strict=False)
        binning[k] = ND_Binning(tube[k],Prog_Var.parameters,bins=10)
    print case_num
    HDF5_Cases.push_case(case_num,tube,binning,ordering = Prog_Var.Pattern,saveFCS=False)
