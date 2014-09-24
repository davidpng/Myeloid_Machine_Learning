#!/usr/bin/env python
"""
Class definition for Find_and_Copy_FCS
"""
import os
import shutil

__author__ = "David Ng, MD"
__copyright__ = "Copyright 2014, David Ng"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "David Ng"
__email__ = "ngdavid@uw.edu"
__status__ = "Production"

class Find_and_Copy_FCS(object):
    """
    This class will recursively search a given source directory for *.fcs files
    with file names containing a case number string XX_XXXXX given by file_list_name
    Class object will contain variables:
        file_list = a list of cases loaded from file_list_name
        cases_not_found = a list of cases in file_list that were not matched
        statistics = a dictionary containing:
                'number_of_cases_queried'
                'number_of_cases_found'
                'number_of_files_transfered' - work in progress
    """
    def __init__(self,source,target,file_list_name,verbose=False):
        self.target_dir = target
        self.source_dir = source
        self.case_list_path = file_list_name
        self.verbose = verbose
        
        self._make_target_dir()
        self.file_list = self._load_file_list()
        if self.verbose:
            print self.file_list
        self.cases_not_found = self._search_for_cases()
        if self.verbose:
            print self.cases_not_found
    def _make_target_dir(self):
        #Make Target Director
        if not os.path.exists(self.target_dir):
            os.makedirs(self.target_dir)
        return None
    
    def _load_file_list(self):
        #Load list of files to find
        file_list=[]
        file = open(self.case_list_path,'rU')
        for name in file:
            if name:    # if line is empty or blank, skip it
                file_list.append(name.strip().strip('HP'))
        file.close()
        return file_list

    def _search_for_cases(self):
        #OS walk and search for files
        self.num_cases_found = 0
        file_list_tracking = self.file_list 
        for root,dirs,files in os.walk(self.source_dir):
            for _f in files:
                matches = [l for l in file_list_tracking if l in _f]
                if any(matches):
                    if self.verbose:
                        print "Source: "+root
                        print "Target: "+target_dir+"/"+matches[0]
                    shutil.copytree(root,target_dir+"/"+matches[0],
                                    ignore = self._ignore_except ) #this will copy all files over
                    file_list_tracking.remove(matches[0])
                    self.num_cases_found += 1
                    break
        return file_list_tracking
        
    def _ignore_except(self,adir,filenames):
        return [filename for filename in filenames if not filename.endswith('fcs')]

    def generate_statistics(self):
        return {'number_of_cases_queried' : len(self.file_list),
                'number_of_cases_found' : self.num_cases_found,
                'number_of_files_transfered' : 'work in progress'}

if __name__ == '__main__':
    source_dir = "/Volumes/archive/2010 archived flow files"
    target_dir = "/Users/davidng/Desktop/Examples/Toy"
    file_list_name = "/Users/davidng/Documents/PYTHON/Input_Output/Toy_HP_Cases.txt"
    t=Find_and_Copy_FCS(source_dir,target_dir,file_list_name,verbose=True)
