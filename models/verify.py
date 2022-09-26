#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 24 19:25:23 2022

@author: ray
"""



import pandas as pd
from math import sqrt
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from diebold_mariano_test import *
import glob
import os
from colorama import init, Fore
import logging
from datetime import datetime
from pathlib import Path
import warnings
import argparse



class result_stats_test:
    
    def __init__(self, directory):
        
        init(autoreset = True)
        logging.getLogger().setLevel(logging.INFO)
        warnings.simplefilter('ignore')
        
        self.directory = directory
        self.root_path = os.getcwd()[:os.getcwd().find('/bitcoin-volatility-forecast-improvement-through-random-forest-algorithm')+len('bitcoin-volatility-forecast-improvement-through-random-forest-algorithm/')]
                
        csv_files = glob.glob(os.path.join(self.directory, '*.csv'))
        new_frame = pd.DataFrame()
        
        for f in csv_files:
            
            
            data = pd.read_csv(f).iloc[:, -1]
            data = pd.DataFrame(data)
            data.columns = [str(Path(f).stem)]
            new_frame = new_frame.append(data.T)
        
        self.frame = new_frame.T
        
    def loss_func(self):
        
        out_frame = pd.DataFrame()
        for i in range(len(self.frame.columns)):
            
            if i == 0:
            
                pass
            
            else:
            
                mse = mean_squared_error(self.frame.iloc[:,0], self.frame.iloc[:,i])
                mae = mean_absolute_error(self.frame.iloc[:,0], self.frame.iloc[:,i])
                rmse = sqrt(mse)
                
                out = pd.DataFrame([mse, mae, rmse]).T
                out.index = [str(self.frame.columns[i])]
                out.columns = ['mse', 'mae', 'rmse']
                
                out_frame = out_frame.append(out)                
        
        logging.info(f"{(datetime.now().strftime('%Y-%m-%d %H:%M:%S')):<10}{' Forecast error test': ^10}{'·'*20: ^10}{Fore.GREEN}{'Pass'}")
        print(out_frame)
        
        try:
            
            self.create_dir('verification')
            
            out_frame.to_csv(self.root_path + '/report/verification/forecast_error.csv')
            logging.info(f"{(datetime.now().strftime('%Y-%m-%d %H:%M:%S')):<10}{' Forecast error stored': ^10}{'·'*20: ^10}{Fore.GREEN}{'Pass'}")
        
        except:
            
            logging.info(f"{(datetime.now().strftime('%Y-%m-%d %H:%M:%S')):<10}{' Forecast error stored': ^10}{'·'*20: ^10}{Fore.RED}{'Error'}")
        
    
    def dm_test(self):
        
        
        
        dm_list_12 = cul_d_t(MSE, self.frame.iloc[:, 0], self.frame.iloc[:, 1], self.frame.iloc[:, 2])
        t_stat_12 = cul_DM(dm_list_12)
        p_val_12 = cul_P(dm_list_12)
        
        dm_list_13 = cul_d_t(MSE, self.frame.iloc[:, 0], self.frame.iloc[:, 1], self.frame.iloc[:, 3])
        t_stat_13 = cul_DM(dm_list_13)
        p_val_13 = cul_P(dm_list_13)
        
        dm_list_23 = cul_d_t(MSE, self.frame.iloc[:, 0], self.frame.iloc[:, 2], self.frame.iloc[:, 3])
        t_stat_23 = cul_DM(dm_list_23)
        p_val_23 = cul_P(dm_list_23)
        
        
        out_12 = pd.DataFrame([t_stat_12, p_val_12]).T
        out_12.index = ['garch vs. rf_picked']
        out_12.columns = ['Diebold-Mariano Test statistic', 'Diebold-Mariano P Value']
        
        out_13 = pd.DataFrame([t_stat_13, p_val_13]).T
        out_13.index = ['garch vs. rf_whole']
        out_13.columns = ['Diebold-Mariano Test statistic', 'Diebold-Mariano P Value']
        
        out_23 = pd.DataFrame([t_stat_23, p_val_23]).T
        out_23.index = ['rf_picked vs. rf_whole']
        out_23.columns = ['Diebold-Mariano Test statistic', 'Diebold-Mariano P Value']


        out_frame = pd.concat([out_12, out_13, out_23])
        
        logging.info(f"{(datetime.now().strftime('%Y-%m-%d %H:%M:%S')):<10}{' diebold-mariano_test': ^10}{'·'*20: ^10}{Fore.GREEN}{'Pass'}")
        print(out_frame)
        
        try:
            
            self.create_dir('verification')
            
            out_frame.to_csv(self.root_path + '/report/verification/diebold-mariano_test.csv')
            logging.info(f"{(datetime.now().strftime('%Y-%m-%d %H:%M:%S')):<10}{' diebold-mariano_test stord': ^10}{'·'*20: ^10}{Fore.GREEN}{'Pass'}")
        
        except:
            
            logging.info(f"{(datetime.now().strftime('%Y-%m-%d %H:%M:%S')):<10}{' diebold-mariano_test stored': ^10}{'·'*20: ^10}{Fore.RED}{'Error'}")
        
        
        
    def create_dir(self, file_name):
        
        try:
            
            if os.path.isdir(self.root_path+'/report') == True:
                    
                if os.path.isdir(self.root_path+'/report/' + file_name) == True:
                    
                    pass
                
                else:
                
                    os.mkdir(self.root_path+'/report/' + file_name)
            
            else:   
                
                os.mkdir(self.root_path+'/report')
                os.mkdir(self.root_path+'/report/' + file_name)
            
                logging.info(f"{(datetime.now().strftime('%Y-%m-%d %H:%M:%S')):<10}{' '+file_name}{' Directory creation': ^10}{'·'*20: ^10}{Fore.GREEN}{'Pass'}")
        
        except:
            
            logging.info(f"{(datetime.now().strftime('%Y-%m-%d %H:%M:%S')):<10}{' '+ file_name}{' Directory creation': ^10}{'·'*20: ^10}{Fore.RED}{'Error'}")
                 




if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-subdir", "--subdirectory", help="enter subdirectory name")
    params = parser.parse_args()
    subdir = params.subdirectory
    subdir = str(subdir)

    result = result_stats_test(subdir)
    
    result.loss_func()
    result.dm_test()
