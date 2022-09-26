
VENV = ./venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip


help: 
	@echo '-----------------------------------------------------------------------------------'
	@echo '|Use the following command line to reproduce the experiments and statistical tests|'
	@echo '-----------------------------------------------------------------------------------'


install: # make venv and install the packages needed.
install: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt


unitroots: # Do the unit-root test for processed data and store.
unitroots: 
	@python ./src/unitroot_test.py -subdir ./data/processed/btc_info
	@python ./src/unitroot_test.py -subdir ./data/processed/currency
	@python ./src/unitroot_test.py -subdir ./data/processed/precious_metals
	@python ./src/unitroot_test.py -subdir ./data/processed/stocks


descriptive_statistics: # Do the descriptive statistic for processed data and store.
descriptive_statistics: 
	@python ./src/descriptive_stat.py -subdir ./data/processed/btc_info
	@python ./src/descriptive_stat.py -subdir ./data/processed/currency
	@python ./src/descriptive_stat.py -subdir ./data/processed/precious_metals
	@python ./src/descriptive_stat.py -subdir ./data/processed/stocks



random_forest_feature_importance: # Make the random forest feature importance output and store.
random_forest_feature_importance: 
	@python ./src/rf_importance.py -subdir ./data/processed/btc_info
	@python ./src/rf_importance.py -subdir ./data/processed/currency
	@python ./src/rf_importance.py -subdir ./data/processed/precious_metals
	@python ./src/rf_importance.py -subdir ./data/processed/stocks


realized_volatility: # Calculate the realized volatility and store.
realized_volatility: 
	@python ./src/realized_volatility.py


	
garch_model_forecast: # Make the GARCH(1,1) model forecast and store the result.
garch_model_forecast: 
	@python ./models/model.py -type garch


rf_model_forecast: # Make the random forest  model forecast with whole features and store the result.
rf_model_forecast: 
	@python ./models/model.py -type whole



rf_model_feature_picked_forecast: # Make the random forest  model forecast with picked features and store the result.
rf_model_feature_picked_forecast: 
	@python ./models/model.py -type picked


forecast_result_verification: #Verify the forecast result by loss function and diebold-mariano test
forecast_result_verification: 
	@python ./models/verify.py -subdir ./report/forecast_result


clean: #clean the venv and __pycache__
clean: 
	rm -rf __pycache__
	rm -rf $(VENV)



	