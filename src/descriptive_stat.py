#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 20:39:11 2022

@author: ray
"""



import argparse
import pandas as pd
import numpy as np
from pathlib import Path
from colorama import Back, init, Front
import os




init(autoreset=True)



class descriptive_stat:
    
    def __init__(self, directory):
        
        self.directory = directory
    
    def check_data(self):
        
        raw = pd.read_csv(self.directory)
        
        if len(raw.columns) < 4:
            
              
            data = raw.iloc[:, -1]
            
            df = pd.DataFrame(np.array(data).T,
                              columns = str(Path(self.directory).stem))
            
        else:
            
            data = raw['Close'] or raw['close'] or raw['Price']
            
            df = pd.DataFrame(np.array(data).T,
                              columns = str(Path(self.directory).stem))

        
        return df    

    def stat(x) : 
        
        return pd.Series(['%.0f'%x.count(), '%.2f'%x.min(), '%.2f'%x.mean(), '%.2f'%x.max(), '%.2f'%x.var(),
                     '%.2f'%x.std(), '%.2f'%x.skew(), '%.2f'%x.kurt()],
                     index=['Observation','Min','Mean','Max','Var','Std','Skwness','Kurtosis'])

    def output(self):
        
        output = self.check_data().apply(self.stat())
        print(output)
        
        
        
        #make root dir
        
        
        try:
            output.to_csv('report/descripitive_statistics/'+ str(Path(self.directory).stem)+'.csv')
            print(f"{'Descriptive statistic result has sstored in the report file ': <10}{'·'*20 : ^10}{Back.GREEN}{'Done': ^10}")
        except:
            print(f"{Front.RED}{'Warning: Something wrong with the Raw data please check again '}")





parser = argparse.ArgumentParser()
parser.add_argument("-subdir", "--subdirectory", help="enter subdirectory name")
params = parser.parse_args()
subdir = params.subdirectory


out = descriptive_stat(subdir)
out.output()

