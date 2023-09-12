:: Install virtualenv
::pip install virtualenv

:: Create virtual env with python3 installed
::virtualenv -p python3 test_env

:: ONLY RUN THIS COMMAND if you get an error from the above command(windows users issue perhaps)
:: virtualenv -p python test_env

:: Activate virtual environment and allow us to work with contained dependencies
:: .\test_env/Scripts/activate

:: Install python packages:
:: pip install pip --upgrade
pip install --no-cache-dir -r requirements.txt

:: Run tests:
python .\tests\run.py

::need to install allure to generate reports
allure serve .\tests_results\reports\allure_report
