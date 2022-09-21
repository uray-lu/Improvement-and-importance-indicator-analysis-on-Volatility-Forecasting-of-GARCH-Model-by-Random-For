#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 11 18:00:09 2022

@author: ray
"""

from arch.univariate import arch_model
import pandas as pd
import numpy as np
from sklearn import ensemble
import time   
import matplotlib.pyplot as plt
import glob
import os
from colorama import init, Fore
import logging
from datetime import datetime
from pathlib import Path
import warnings


class Model:
    
    
    
    def __init__(self):
        plt.figure(figsize=(10,4))
        init(autoreset = True)
        logging.getLogger().setLevel(logging.INFO)
        warnings.simplefilter('ignore')
        
        self.root_path = os.getcwd()[:os.getcwd().find('/bitcoin-volatility-forecast-improvement-through-random-forest-algorithm')+len('bitcoin-volatility-forecast-improvement-through-random-forest-algorithm/')]
        self.target = pd.read_csv(self.root_path +'/Data/processed/btc_info/Daily_returns.csv')
        
        self.date  = self.target.Date
        self.target = self.target.iloc[:, -1]
        
        
        garch_mod =  arch_model(self.target,  mean = 'ARX')
        res = garch_mod.fit(disp="off")

        self.vols = pd.DataFrame(res.conditional_volatility)
        self.labels = self.vols.drop(self.vols.index[0])
        self.labels = self.labels.reset_index(drop = True)
        self.labels = pd.DataFrame(self.labels)
        
        try:
            
            self.create_dir('whole_vols')
            
        
            if os.path.isfile(self.root_path +'/report/whole_vols/volatility.png') == True:
            
                pass
                logging.info(f"{(datetime.now().strftime('%Y-%m-%d %H:%M:%S')):<10}{Fore.BLUE}{' Whole data Volatility plot is already exist'}")
        
            else:
                
                plt.figure(figsize=(15,8))
                plt.plot(self.date,self.target)
                plt.plot(self.date, self.vols)
                plt.xticks(range(0,1462, 200))
                plt.tick_params(axis='both', which = 'major', labelsize = 8)
                plt.title('Volatility Plot of Bitcoin Returns', fontsize=20)
                plt.legend(['Returns', 'Volatility'], fontsize=16)
                plt.savefig(self.root_path +'/report/whole_vols/volatility.png', dpi =300)
                logging.info(f"{(datetime.now().strftime('%Y-%m-%d %H:%M:%S')):<10}{' Whole data Volatility plot stored': ^10}{'·'*20: ^10}{Fore.GREEN}{'Pass'}")    

        except:
            
            logging.info(f"{(datetime.now().strftime('%Y-%m-%d %H:%M:%S')):<10}{'Whole data Volitility plot stored': ^10}{'·'*20: ^10}{Fore.RED}{'Path Error'}")    
    
        
        
    def garch_forecast(self):
        
        test_size =  int(len(self.target)*0.3)
        date = self.date[-test_size:]
        
        rolling_predictions = []
        
        for i in range(test_size):
            
            train = self.target[:-(test_size-i)]
            model = arch_model(train,mean = 'ARX' )
            model_fit = model.fit(disp='off')
            pred = model_fit.forecast(horizon=1)
            out = np.sqrt(pred.variance.values[-1,:][0])
            rolling_predictions.append(out)
        
        rolling_predictions = pd.DataFrame(rolling_predictions)
        
        try:
            
            self.create_dir('forecast_result')
            
            plt.plot(date, self.vols[-test_size:].reset_index(drop = True))
            plt.plot(date, rolling_predictions.iloc[:,-1])
            plt.xticks(range(0,437, 60))
            plt.tick_params(axis='both', which = 'major', labelsize = 8)
            plt.title('Volatility Prediction - Rolling Forecast Garch(1,1)', fontsize=20)
            plt.legend(['True Volatility', 'Predicted Volatility'], fontsize=16)
            plt.savefig(self.root_path +'/report/forecast_result/Garch(1,1)_forecast.png')
            logging.info(f"{(datetime.now().strftime('%Y-%m-%d %H:%M:%S')):<10}{' Garch(1,1) forecast_result plot stored': ^10}{'·'*20: ^10}{Fore.GREEN}{'Pass'}")    

        except:
            
            logging.info(f"{(datetime.now().strftime('%Y-%m-%d %H:%M:%S')):<10}{' Garch(1,1) forecast_result plot stored': ^10}{'·'*20: ^10}{Fore.RED}{'Error'}")    
    
        try:
          
       
           rolling_predictions.to_csv(self.root_path+'/report/forecast_result/garch(1,1)_model_forecast.csv')
           logging.info(f"{(datetime.now().strftime('%Y-%m-%d %H:%M:%S')):<10}{' Garch(1,1) forecast csv file stored': ^10}{'·'*20: ^10}{Fore.GREEN}{'Pass'}")    
           
        except:
           
           logging.info(f"{(datetime.now().strftime('%Y-%m-%d %H:%M:%S')):<10}{' Garch(1,1) forecast csv file stored': ^10}{'·'*20: ^10}{Fore.RED}{'Error'}")    

           
        

    def rf_forecast(self, model_types):
        
       
       
        
       btc_infos = self.get_element(self.root_path + '/Data/processed/btc_info')
       currencies = self.get_element(self.root_path + '/Data/processed/currency')
       metals = self.get_element(self.root_path + '/Data/processed/precious_metals') 
       stocks = self.get_element(self.root_path + '/Data/processed/stocks')
       
       
       
       if model_types == 'whole':
           
           exog_list = pd.concat([btc_infos, currencies, metals, stocks], axis = 1)
           
       elif model_types == 'picked':
           
           btc_infos = btc_infos[['BTC_VIX_growth', 'BTC_address_growth']]
           currencies = currencies['JPYUSD_growth']
           metals = metals['pladium_growth']
           stocks = stocks[['DJI_growth', 'HSI_growth']]
           
           exog_list =  pd.concat([btc_infos, currencies, metals, stocks], axis = 1)
       
       
       exog_list = pd.concat([self.vols.drop(self.vols.index[-1]), exog_list], axis =1)
       test_data_size = int(len(self.labels)*0.3)
       
       print('-'*10 +'Training labe' +'-'*10)
       print(self.labels)
       print('-'*10 +'Training Feature' +'-'*10)
       print(exog_list)
       
       
       start = time.process_time()
       
       forecast_model = self.OneStepForecast(self.labels, exog_list, test_data_size)
       
       end = time.process_time()

       print('-'*10,'Total prediction time:', int((end - start)/60), 'min', '-'*10)
       
       date = self.date[-test_data_size:]
       
       print(forecast_model)
       #forecast_output = pd.DataFrame(date).reset_index(drop = True)
       #forecast_output.columns = ['Date']
       #orecast_output  =pd.concat([forecast_output, forecast_model], axis = 1)
       
       
       
       try:
           
           self.create_dir('forecast_result')
           
           plt.figure(figsize=(10,4))
           plt.plot(date, self.labels[-(test_data_size+1):(len(self.labels)-1)].reset_index(drop = True))
           plt.plot(date, forecast_model)
           plt.xticks(range(0,437, 60))
           plt.tick_params(axis='both', which = 'major', labelsize = 8)
           plt.title('Volatility Prediction - Rolling Forecast ' + model_types + ' exog', fontsize=20)
           plt.legend(['True Volatility', 'Predicted Volatility'], fontsize=16)
           plt.savefig(self.root_path +'/report/forecast_result/' + model_types +'_exog_model_forecast.png')
           
           
           logging.info(f"{(datetime.now().strftime('%Y-%m-%d %H:%M:%S')):<10}{' Random forest model forecast plot stored': ^10}{'·'*20: ^10}{Fore.GREEN}{'Pass'}")    

       except:
           
           logging.info(f"{(datetime.now().strftime('%Y-%m-%d %H:%M:%S')):<10}{' Random forest model forecast plot stored': ^10}{'·'*20: ^10}{Fore.RED}{'Error'}")    
   
       
   
       try:
       
           #forecast_output.to_csv(self.root_path+'/report/forecast_result/' + model_types +'_model_forecast.csv')
           logging.info(f"{(datetime.now().strftime('%Y-%m-%d %H:%M:%S')):<10}{' Random forest model forecast csv file stored': ^10}{'·'*20: ^10}{Fore.GREEN}{'Pass'}")    
           
       except:
           
           logging.info(f"{(datetime.now().strftime('%Y-%m-%d %H:%M:%S')):<10}{' Random forest model forecast csv file stored': ^10}{'·'*20: ^10}{Fore.RED}{'Error'}")    

           
             
   
    
    def OneStepForecast(self, label, feature, test_size):
       
       print('-'*25, 'Start Training', '-'*25,)
       pred_list = []
       total = 0
       for i in range(test_size):
        
            start = time.process_time()
        
            trainX = feature[:-(test_size - i)]
            trainy = label[:-(test_size - i)]
            testX = feature[len(trainX):]
            
            print('Now Step:', i)
            
            
            model = ensemble.RandomForestRegressor(n_estimators = 1000)
            model_fit = model.fit(trainX, trainy)
            
            
            predict = model_fit.predict(testX[0:1])
            #predict = pd.DataFrame(predict)
            pred_list.append(predict)
            
            
            
            print('===> Completion:', '%.3f'%((i/test_size)*100), '%')
            
            end = time.process_time()+total
            total = (end - start)
            print('-'*10,'Been through :', '%.3f'%((total)/60), 'min', '-'*10)
        
       print('-'*25, 'Prediction Completed', '-'*25,)
       
       #pred_list = pred_list.reset_index(drop = True)
       #pred_list.columns = ['forecast result']
       
       return pred_list 
    
    
    
    
    def get_element(self, directory):
        
        
        csv_files = glob.glob(os.path.join(directory, '*.csv'))
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
                data = data.T
                
                element_frame = element_frame.append(data)
                
        
        element_frame = element_frame.T
        element_frame = element_frame.drop(element_frame.index[-1])
        
        return element_frame
    
    
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
        



if __name__ == '__main__' :
    
    Model().rf_forecast('picked')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    