import os

url = "https://app.powerbi.com/groups/me/reports/5c7e7adf-b35a-4880-bae5-1831df416cce/ReportSection59b352136fd9452af512?experience=power-bi"
browser = "chrome"
emailID = "vaishnavi.gopala@tigeranalytics.com"
encryptedPasscode = "VGlnZXIjNjc4OQ=="
testdataPath = "././test_data/test_data_Smoke.xlsx"
htmlDir = "./testResults/PytestHTMLReport/TestAutomation.htm"
alluredir = "./testResults/allure-results"
DIR_ = os.path.dirname(os.path.realpath(__file__))
TARGET_DIR = os.path.join((os.path.dirname(DIR_)), "tests_results")
SCREENSHOTS_DIR = os.path.join(TARGET_DIR, "screenshots")
BROWSER_LOGS_DIR = os.path.join(TARGET_DIR, "browser_logs")
