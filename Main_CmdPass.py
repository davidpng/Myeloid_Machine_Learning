# -*- coding: utf-8 -*-
"""
Created on Wed Sep 10 12:15:34 2014

@author: ngdavid
"""
from HEADER_Find_FCS_files import Find_FCS_Files
import HEADER_Program_Variables as Prog_Var

import tempfile
import json
import subprocess

FCS_Folder = Find_FCS_Files(Prog_Var.Dir,Prog_Var.File_list,Prog_Var.Pattern)
Cases = FCS_Folder.search_by_case()

for case_num,tubes in Cases.items():
    with tempfile.TemporaryFile() as f:
        f = json.dumps(tubes)
        # CMD_LINE_Process.py takes 2 parameters
        subprocess.call(['python','CMD_LINE_Process.py',case_num,f])
        print 'file complete'