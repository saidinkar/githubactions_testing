import os
import sys
import pytest


__dir = os.path.dirname(os.path.realpath(__file__))
XML_DIR = os.path.join((os.path.dirname(__dir)), "tests_results")
xml_report_path = os.path.join(XML_DIR, "integration.xml")
report_dir = os.path.join(os.path.dirname(__dir), "tests_results", "reports")
allure_report = os.path.join(report_dir, "allure_report")
test_dirs = os.path.join(__dir, "test_openPowerBI.py")

parallel_test_args = [
    "--junitxml=" + xml_report_path,
    "--alluredir="+allure_report,
    test_dirs
    ]


res = pytest.main(parallel_test_args)

sys.exit(res)
