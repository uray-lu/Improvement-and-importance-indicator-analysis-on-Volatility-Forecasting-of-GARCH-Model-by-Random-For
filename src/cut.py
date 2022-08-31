#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 19:21:09 2022

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



init(autoreset = True)
logging.getLogger().setLevel(logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument("-subdir", "--subdirectory", help="enter subdirectory name")
params = parser.parse_args()
subdir = params.subdirectory
subdir = str(subdir)

csv_files = glob.glob(os.path.join(subdir, '*.csv'))




def fillter(data):
    
    try:
        mask = (data['date']> '2017-12-31')&(data['date'] <'2022-01-01') 
    
    except:
        mask = (data['Date']> '2017-12-31')&(data['Date'] <'2022-01-01') 

    
    return mask







for f in csv_files:
    
    
        data = pd.read_csv(f)
        mask = fillter(data)

        try:
            data['date'] = pd.DatetimeIndex(data['date'])
        except:
            data['Date'] = pd.DatetimeIndex(data['Date'])
        
        
        data = data.loc[fillter]    
        data = data.reset_index(drop = True)
        
        try:
        
            if data.columns[0] == 'Unnamed: 0':
                data = data.drop('Unnamed: 0', axis=1)
            else:
                data = data
        
            data.to_csv(f, index = None)
    
            logging.info(f"{(datetime.now().strftime('%Y-%m-%d %H:%M:%S')):<10}{' ' + str(Path(f).stem): ^10}{'cutting': ^10}{'·'*20: ^10}{Fore.GREEN}{'Pass'}")
    
        except:
        
            logging.info(f"{(datetime.now().strftime('%Y-%m-%d %H:%M:%S')):<10}{' ' +str(Path(f).stem): ^10}{'cutting': ^10}{'·'*20: ^10}{Fore.RED}{'Error'}")    



