#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 21:58:30 2022

@author: ray
"""

import pandas as pd
from arch.unitroot import ADF
from arch.unitroot import PhillipsPerron
import argparse
import glob
import os
from colorama import init, Fore
import logging
from datetime import datetime
from pathlib import Path
from statsmodels.tsa.stattools import kpss
import warnings





class unitroot:
    
    def __init__(self, directory):
        
        init(autoreset = True)
        logging.getLogger().setLevel(logging.INFO)
        warnings.simplefilter('ignore')
        
        self.directory = directory
        

        csv_files = glob.glob(os.path.join(self.directory, '*.csv'))
        new_frame = pd.DataFrame()
        
        for f in csv_files:
            
            
            data = pd.read_csv(f).iloc[:, -1]
            data = pd.DataFrame(data)
            data.columns = [str(Path(f).stem)]
            new_frame = new_frame.append(data.T)
        
        self.new_frame = new_frame.T
        
    

    def uniroot_adf(self):
        
        columns = self.new_frame.columns
        
        adf_output = pd.DataFrame()
        
        for name in columns:
            
            data = self.new_frame[name]
        
            result = ADF(data)
            result = result.summary().as_html()
            result = pd.read_html(result, index_col=0)


            output = {'name': [name],
                      'ADF Statistic':['%f' % result[0][1]['Test Statistic']],
                      'p-value': ['%f' % result[0][1]['P-value']],
                      }
            
            output = pd.DataFrame(output)
            adf_output = adf_output.append(output)
        
            
        print(adf_output.T)
        
        return adf_output.T

    
    def uniroot_pp(self):
        
        columns = self.new_frame.columns
        
        pp_output = pd.DataFrame()
        
        for name in columns:
            
            data = self.new_frame[name]
        
            result = PhillipsPerron(data)
            result = result.summary().as_html()
            result = pd.read_html(result, index_col=0)


            output = {'name': [name],
                      'PhillipsPerron Statistic':['%f' % result[0][1]['Test Statistic']],
                      'p-value': ['%f' % result[0][1]['P-value']],
                      }
            
            output = pd.DataFrame(output)
            pp_output = pp_output.append(output)
        
            
        print(pp_output.T)
    
        return pp_output.T
  
    
    def uniroot_kpss(self):
        
        columns = self.new_frame.columns
        
        kpss_output = pd.DataFrame()
        
        for name in columns:
            
            data = self.new_frame[name]
        
            result = kpss(data)
    
            output = {'name': [name],
                      'KPSS Statistic':['%f' % result[0]],
                      'p-value': ['%f' % result[1]],
                      }
            
            output = pd.DataFrame(output)
            kpss_output = kpss_output.append(output)
        
            
        print(kpss_output.T)
        #print(type(kpss_output.T))
        return kpss_output.T

    def mkoutput(self, test_type):
    
        if test_type == 'adf' :
            
            layout = self.uniroot_adf()
        
        elif test_type == 'pp' :
            
            layout = self.uniroot_pp()
        
        elif test_type == 'kpss' :
            
            layout = self.uniroot_kpss()
            
        root_path = os.getcwd()[:os.getcwd().find('/bitcoin-volatility-forecast-improvement-through-random-forest-algorithm')+len('bitcoin-volatility-forecast-improvement-through-random-forest-algorithm/')]
        
        try:
    
            if os.path.isdir(root_path+'/report/unit_root_test') == True:
            
               if os.path.isdir(root_path+'/report/unit_root_test/' + str(Path(self.directory).stem)) == True:
                   
                   pass
               
            
               else:
                   
                   os.mkdir(root_path+'/report/unit_root_test/' + str(Path(self.directory).stem))
                   
                                      
            else:   
                
                os.mkdir(root_path+'/report/unit_root_test')
                os.mkdir(root_path+'/report/unit_root_test/' + str(Path(self.directory).stem))
    
            layout.to_csv(root_path+'/report/unit_root_test/'+ str(Path(self.directory).stem) + '/' +str(Path(self.directory).stem)+ '_'+ str(test_type)+'.csv')
            logging.info(f"{(datetime.now().strftime('%Y-%m-%d %H:%M:%S')):<10}{' ' + str(Path(self.directory).stem): ^10}{'Unit Root test Storage of': ^10}{test_type: ^10}{'·'*20: ^10}{Fore.GREEN}{'Pass'}")    

        except:
    
            logging.info(f"{(datetime.now().strftime('%Y-%m-%d %H:%M:%S')):<10}{' ' + str(Path(subdir).stem): ^10}{'Unit Root test Storage': ^10}{'·'*20: ^10}{Fore.RED}{'Error'}")    






if __name__ == '__main__' :
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-subdir", "--subdirectory", help="enter subdirectory name")
    params = parser.parse_args()
    subdir = params.subdirectory
    subdir = str(subdir)

    input_data = unitroot(subdir)
    input_data.mkoutput('adf')
    input_data.mkoutput('pp')
    input_data.mkoutput('kpss')















