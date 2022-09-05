
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 20:39:11 2022

@author: ray
"""



import pandas as pd
import argparse
import glob
import os
from colorama import init, Fore
import logging
from datetime import datetime
from pathlib import Path
import numpy as np






class descriptive_stat:
    
    def __init__(self, directory):
        
        self.directory = directory
    
    def check_data(self):
        
        raw = pd.read_csv(self.directory)
        
        if len(raw.columns) == 2:
            
            data = raw.iloc[:, -1]
            
            df = pd.DataFrame(data)
            df.columns = [str(Path(self.directory).stem)]
          
        else:
            
            if 'Close' in raw.columns:
                
                data = raw['Close']
            
            elif 'close' in raw.columns:
                
                data = raw['close']
            
            elif 'Price' in raw.columns:
                
                data = raw['Price']
                
            elif ' Close' in raw.columns:
                
                data = raw[' Close']
            
            
            df = pd.DataFrame(data, )
            df.columns = [str(Path(self.directory).stem)]

        
        return df
            

    def stat(self, x) : 
        
        return pd.Series(['%.0f'%x.count(), '%.2f'%x.min(), '%.2f'%x.mean(), '%.2f'%x.max(), '%.2f'%x.var(),
                     '%.2f'%x.std(), '%.2f'%x.skew(), '%.2f'%x.kurt()],
                     index=['Observation','Min','Mean','Max','Var','Std','Skwness','Kurtosis'])

    def output(self):
        
            
        
        try:
            stats_data = self.check_data().apply(self.stat)
            
            logging.info(f"{(datetime.now().strftime('%Y-%m-%d %H:%M:%S')):<10}{' ' + str(Path(self.directory).stem): ^10}{' Descripitive Statistic': ^10}{'·'*20: ^10}{Fore.GREEN}{'Pass'}")
    
        except:
        
            logging.info(f"{(datetime.now().strftime('%Y-%m-%d %H:%M:%S')):<10}{' ' +str(Path(self.directory).stem): ^10}{' Descripitive Statistic': ^10}{'·'*20: ^10}{Fore.RED}{'Error'}")    
    
        
        
        return stats_data
        
        
        
        
    
init(autoreset = True)
logging.getLogger().setLevel(logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument("-subdir", "--subdirectory", help="enter subdirectory name")
params = parser.parse_args()
subdir = params.subdirectory
subdir = str(subdir)

csv_files = glob.glob(os.path.join(subdir, '*.csv'))


layout = pd.DataFrame()
for f in csv_files:
    
    
    data = descriptive_stat(f)
    data = data.output().T
    
    layout = layout.append(data)


layout = layout.sort_values('Observation', ascending = False)
layout = layout.T
print(layout)





root_path = os.getcwd()[:os.getcwd().find('/bitcoin-volatility-forecast-improvement-through-random-forest-algorithm')+len('bitcoin-volatility-forecast-improvement-through-random-forest-algorithm/')]


try:
    
    if os.path.isdir(root_path+'/report/descriptive_stattistic') == True:
            
        pass
    
    else:   
        os.mkdir(root_path+'/report')
        os.mkdir(root_path+'/report/descriptive_statistic')
    
    layout.to_csv(root_path+'/report/descriptive_statistic/'+ str(Path(subdir).stem) + '.csv')
    logging.info(f"{(datetime.now().strftime('%Y-%m-%d %H:%M:%S')):<10}{' ' + str(Path(subdir).stem): ^10}{'descriptive statistic stored': ^10}{'·'*20: ^10}{Fore.GREEN}{'Pass'}")    

except:
    
    logging.info(f"{(datetime.now().strftime('%Y-%m-%d %H:%M:%S')):<10}{' ' + str(Path(subdir).stem): ^10}{'descriptive statistic store': ^10}{'·'*20: ^10}{Fore.RED}{'Error'}")    



    
    
    
    
    
    

