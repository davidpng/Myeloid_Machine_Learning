# -*- coding: utf-8 -*-
"""
Created on Tue Sep 30 18:34:54 2014
Refactorized code from FCM package by Jacob Frelinger.
@author: ngdavid
"""

import re
from datetime import datetime
import numpy as np
import pandas as pd
from warnings import warn
from struct import calcsize, unpack

class loadFCS(object):
    """
    This class will import an FCS file to a pandas datatable
    """
    def __init__(self,filename,**kwargs):
        """
        Takes filename, 
        import_dataframe = True to import listmode as a dataframe
        import_dataframe = False to import listmode as a numpy array
        """
        self.fh = open(filename,'rb')
        self.header = self.parse_header()
        self.text = self._parse_text()
        self.parameters = self.parameter_header()
        self.channels = self.parameters.loc['Channel Name'].tolist()
        if 'import_dataframe' in kwargs:
            if kwargs['import_dataframe']:            
                self.data = pd.DataFrame(self._parse_data(),columns = self.channels)
            else:
                self.data = self._parse_data()
        
        self.fh.close() #not included in FCM package, leads to a memory leak
        
    def parse_header(self):
        """
        Parse the FCM data in fcs file at the offset (supporting multiple 
        data segments in a file
        """
        header = {}
        header['version'] = float(self._get_block(3, 5))
        header['text_start'] = int(self._get_block(10, 17))
        header['text_stop'] = int(self._get_block(18, 25))
        header['data_start'] = int(self._get_block(26, 33))
        header['data_end'] = int(self._get_block(34, 41))
        try:
            header['analysis_start'] = int(self._get_block(42, 49))
        except ValueError:
            header['analysis_start'] = -1
        try:
            header['analysis_end'] = int(self._get_block(50, 57))
        except ValueError:
            header['analysis_end'] = -1
        return header
         
    def _get_block(self, start, stop):
        """Read in bytes from start to stop inclusive."""
        self.fh.seek(start)
        return self.fh.read(stop - start + 1)
        
    def _parse_data(self):
        """parses the data structure, only listmode float support"""
        start = self.header['data_start']
        end = self.header['data_end']
        datatype = self.text['datatype'].lower()
        mode = self.text['mode'].lower()
        num_events = int(self.text['tot'])
        byteorder = self.text['byteord']
        byteorder_translation = {'4,3,2,1': '>',
                                 '1,2,3,4': '<'}
        if byteorder in byteorder_translation:
            byteorder = byteorder_translation[byteorder]

        if mode != 'l' or datatype != 'f':
            raise ValueError('unsupported mode or datatype')
        else:
            return self._float_parsing(start,end,datatype,byteorder,num_events)
            
    def _float_parsing(self,start,end,datatype,byteorder,num_events):
        """
        Parses floating point data given the byte coordinates
        """
        num_items = (end - start + 1) / calcsize(datatype)
        tmp = unpack('%s%d%s' % (byteorder, num_items, datatype), self._get_block(start, end))
        if len(tmp) % num_events != 0:
            raise IndexError('the byte stream mismatch with number of events')
        return np.array(tmp).reshape((num_events, len(tmp) / num_events))
    def py_export_time(self):
        export_time = self.text['date']+'-'+self.text['etim']
        return datetime.strptime(export_time,'%d-%b-%Y-%H:%M:%S')
    def parameter_header(self):
        par = int(self.text['par'])  # number of parameters
        framework = [['s','Channel Name'],
                     ['n','Short name'],
                     ['b','Bits'],
                     ['e','Amp type'],
                     ['g','Amp gain'],
                     ['r','Range'],
                     ['v','Voltage'],
                     ['f','Optical Filter Name'],
                     ['l','Excitation Wavelength'],
                     ['o','Excitation Power'],
                     ['t','Detector Type'],
                     ['d','suggested scale']]
        framework = np.array(framework)
        depth = len(framework)
        columns = []
        for i in range(1,par+1):
            columns.append(self.text['p{}n'.format(i)])
        header_df = pd.DataFrame(data=None, index=framework[:,1] ,columns=columns)        
        for i in range(1,par+1):
            for j in range(depth):
                x = columns[i-1]
                y = framework[j,1]
                if 'p{}{}'.format(i,framework[j,0]) in self.text:
                    if self.text['p{}{}'.format(i,framework[j,0])].isdigit():
                        header_df[x][y] = int(self.text['p{}{}'.format(i,framework[j,0])])
                    else:
                        temp = self.text['p{}{}'.format(i,framework[j,0])]
                        header_df[x][y] = temp.replace('CD ','CD')
        
        for i in range(1,par+1):
            x = columns[i-1]
            if pd.isnull(header_df[x]['Channel Name']):
                header_df[x]['Channel Name'] = header_df[x]['Short name']
        
        return header_df
        
    def _parse_text(self):
        """return parsed text segment of fcs file"""
        start = self.header['text_start']
        stop = self.header['text_stop']
        text = self._get_block(start, stop)
        delim = text[0]
        if delim == r'|':
            delim = '\|'
        if delim == r'\a'[0]: # test for delimiter being \
            delim = '\\\\' # regex will require it to be \\
        if delim != text[-1]:
            warn("text in segment does not start and end with delimiter")
        tmp = text[1:-1].replace('$', '')
        # match the delimited character unless it's doubled
        regex = re.compile('(?<=[^%s])%s(?!%s)' % (delim, delim, delim))
        tmp = regex.split(tmp)
        return dict(zip([ x.lower() for x in tmp[::2]], tmp[1::2]))

if __name__ == '__main__':
    filename = '/home/ngdavid/Desktop/MDS_Plates/Hodgkin_Cases_2008_2013/08-00656/08-00656_Hodgkins.fcs'
    temp = loadFCS(filename,import_dataframe = True)
    print temp.parameter_header()
