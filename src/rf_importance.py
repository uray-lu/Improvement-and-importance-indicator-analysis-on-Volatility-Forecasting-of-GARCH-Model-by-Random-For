#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 21:26:21 2022

@author: ray
"""

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from matplotlib import pyplot as plt
import numpy as np
import argparse
import glob
import os
from colorama import init, Fore
import logging
from datetime import datetime
from pathlib import Path
import warnings


class rf_importance:
    
    def __init__(self, directory):
        
        init(autoreset = True)
        logging.getLogger().setLevel(logging.INFO)
        warnings.simplefilter('ignore')
        plt.rcParams.update({'figure.figsize': (23.0, 8.0)})
        plt.rcParams.update({'font.size': 14})
        
        self.root_path = os.getcwd()[:os.getcwd().find('/bitcoin-volatility-forecast-improvement-through-random-forest-algorithm')+len('bitcoin-volatility-forecast-improvement-through-random-forest-algorithm/')]

        self.directory = directory
        
        self.target = pd.read_csv(self.root_path +'/Data/processed/btc_info/Realized_volatility_unit(d).csv')
        
        csv_files = glob.glob(os.path.join(self.directory, '*.csv'))
        element_frame = pd.DataFrame()
        
        for f in csv_files:
            
            if 'Realized_volatility_unit(d)' in f:
                
                pass
            
            elif 'Daily_returns' in f:
                
                pass
            
            else:
                
                data = pd.read_csv(f).iloc[:, -1]
                data = pd.DataFrame(data)
                data.columns = [str(Path(f).stem)]
                data = self.standarRV(data)
                data = data.T
                
                element_frame = element_frame.append(data)
                
        
        self.element_frame = element_frame.T
        self.element_frame = self.element_frame.drop(self.element_frame.index[-1])
        
        self.target = self.standarRV(self.target)
        self.target = self.target.iloc[:, -1]
        self.target = self.target.drop(self.target.index[0])
        
        
    def standarRV(self, data):
        
        data.iloc[:, -1] =(data.iloc[:, -1]-data.iloc[:, -1].min())/(data.iloc[:, -1].max()-data.iloc[:, -1].min())
        
        
        
        
        logging.info(f"{(datetime.now().strftime('%Y-%m-%d %H:%M:%S')):<10}{'Standarization of ': ^10}{str(data.columns[-1]): ^10}{'·'*20: ^10}{Fore.GREEN}{'Pass':^10}")
        
        return data
        
    def mkoutput(self):
        
        np.random.seed(1234)
        rf = RandomForestRegressor(n_estimators=1000)
        
        try:
            
            rf.fit(self.element_frame, self.target)
            logging.info(f"{(datetime.now().strftime('%Y-%m-%d %H:%M:%S')):<10}{'Model fitting': ^10}{'·'*20: ^10}{Fore.GREEN}{'Pass': ^10}")
        
        except:
            
            logging.info(f"{(datetime.now().strftime('%Y-%m-%d %H:%M:%S')):<10}{'Model fitting': ^10}{'·'*20: ^10}{Fore.GREEN}{'Error': ^10}")
        
        plt.barh(self.element_frame.columns, rf.feature_importances_)
        plt.title("Random Forest Importance") # title
        plt.xlabel("Features") # y label
        plt.ylabel("Importance for predicting BTC Realized Volatility")
    

        #root_path = os.getcwd()[:os.getcwd().find('/bitcoin-volatility-forecast-improvement-through-random-forest-algorithm')+len('bitcoin-volatility-forecast-improvement-through-random-forest-algorithm/')]


        try:
            
            if os.path.isdir(self.root_path+'/report') == True:
                    
                if os.path.isdir(self.root_path+'/report/randomforest_importance') == True:
                    
                    pass
                
                else:
                
                    os.mkdir(self.root_path+'/report/randomforest_importance')
            
            else:   
                
                os.mkdir(self.root_path+'/report')
                os.mkdir(self.root_path+'/report/randomforest_importance')
            
            
            plt.savefig(self.root_path +'/report/randomforest_importance/' + str(Path(self.directory).stem) +'.png', dpi =300)
            logging.info(f"{(datetime.now().strftime('%Y-%m-%d %H:%M:%S')):<10}{' ' + str(Path(subdir).stem): ^10}{'Random forest importance plot stored': ^10}{'·'*20: ^10}{Fore.GREEN}{'Pass'}")    

        except:
            
            logging.info(f"{(datetime.now().strftime('%Y-%m-%d %H:%M:%S')):<10}{' ' + str(Path(subdir).stem): ^10}{'Random forest importance plot stored': ^10}{'·'*20: ^10}{Fore.RED}{'Error'}")    
    
        
        
        
if __name__ == '__main__':        
        
    parser = argparse.ArgumentParser()
    parser.add_argument("-subdir", "--subdirectory", help="enter subdirectory name")
    params = parser.parse_args()
    subdir = params.subdirectory
    subdir = str(subdir)

    input_data = rf_importance(subdir)          
    input_data.mkoutput()    
        
        
        
        
        
        