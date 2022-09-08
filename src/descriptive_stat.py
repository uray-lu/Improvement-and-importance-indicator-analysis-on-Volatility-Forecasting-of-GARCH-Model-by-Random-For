
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
import warnings

##review



class descriptive_stat:
    
    def __init__(self, directory):
        
        
        init(autoreset = True)
        logging.getLogger().setLevel(logging.INFO)
        warnings.simplefilter('ignore')
        
        self.directory = directory
        
        csv_files = glob.glob(os.path.join(self.directory, '*.csv'))
        layout = []
        
        for f in csv_files:
            
            raw = pd.read_csv(f)
            
            if len(raw.columns) == 2:
                
                input_data = raw.iloc[:, -1]
                
                df = pd.DataFrame(input_data)
                df.columns = [str(Path(f).stem)]
              
            else:
                
                if 'Close' in raw.columns:
                    
                    input_data = raw['Close']
                
                elif 'close' in raw.columns:
                    
                    input_data = raw['close']
                
                elif 'Price' in raw.columns:
                    
                    input_data = raw['Price']
                    
                elif ' Close' in raw.columns:
                    
                    input_data = raw[' Close']
                
                df = pd.DataFrame(input_data, )
                df.columns = [str(Path(f).stem)]
                
            
            
            try:
               
                df = self.to_int(df[str(Path(f).stem)])  
            
            except:
                
                pass
            
            #df = pd.DataFrame(df.T)
            
            layout.append(df)
            
        self.layout = layout
        
        
            

    def stat(self, x) : 
        
        return pd.Series(['%.0f'%x.count(), '%.2f'%x.min(), '%.2f'%x.mean(), '%.2f'%x.max(), '%.2f'%x.var(),
                     '%.2f'%x.std(), '%.2f'%x.skew(), '%.2f'%x.kurt()],
                     index=['Observation','Min','Mean','Max','Var','Std','Skwness','Kurtosis'])

    def mkoutput(self):
        
        
        try :
            des_output = pd.DataFrame()    
        
            for i in range(len(self.layout)):
            
                stats_data = self.layout[i].apply(self.stat)    
                stats_data = pd.DataFrame(stats_data)
    
                des_output = des_output.append(stats_data.T)
            
        
            des_output = des_output.sort_values(['Observation'], ascending= False)
            des_output = des_output.T
        
        
            print(des_output)
            
            logging.info(f"{(datetime.now().strftime('%Y-%m-%d %H:%M:%S')):<10}{' ' + str(Path(self.directory).stem): ^10}{'Descripitive Statistic': ^10}{'·'*20: ^10}{Fore.GREEN}{'Pass'}")
            
       
        except:
        
            logging.info(f"{(datetime.now().strftime('%Y-%m-%d %H:%M:%S')):<10}{' ' +str(Path(self.directory).stem): ^10}{'Descripitive Statistic': ^10}{'·'*20: ^10}{Fore.RED}{'Error'}")    
    
        
        root_path = os.getcwd()[:os.getcwd().find('/bitcoin-volatility-forecast-improvement-through-random-forest-algorithm')+len('bitcoin-volatility-forecast-improvement-through-random-forest-algorithm/')]


        try:
            
            if os.path.isdir(root_path+'/report/descriptive_statistic') == True:
                    
                pass
            
            else:   
                os.mkdir(root_path+'/report')
                os.mkdir(root_path+'/report/descriptive_statistic')
            
            des_output.to_csv(root_path+'/report/descriptive_statistic/'+ str(Path(self.directory).stem) + '.csv')
            logging.info(f"{(datetime.now().strftime('%Y-%m-%d %H:%M:%S')):<10}{' ' + str(Path(subdir).stem): ^10}{'Descriptive statistic stored': ^10}{'·'*20: ^10}{Fore.GREEN}{'Pass'}")    

        except:
            
            logging.info(f"{(datetime.now().strftime('%Y-%m-%d %H:%M:%S')):<10}{' ' + str(Path(subdir).stem): ^10}{'Descriptive statistic store': ^10}{'·'*20: ^10}{Fore.RED}{'Error'}")    
             
    
    
            
        
    
    def to_int(self, x):
        
        x = x.str.replace(',' ,'' )
        x = x.astype(float)
        x = pd.DataFrame(x)
        
        return x
        
        
        
    


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-subdir", "--subdirectory", help="enter subdirectory name")
    params = parser.parse_args()
    subdir = params.subdirectory
    subdir = str(subdir)
    
    data = descriptive_stat(subdir)
    data.mkoutput()



    
    
    
    
    
    

