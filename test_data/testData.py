from utilities.FileReader.read_json import ReadFromJson as RJ
from utilities.FileReader.read_excel import ReadFromExcel as RE
import os


def testData(attribute):
    testDataPath = os.path.abspath("././test_data/test_data.json")
    try:
        testDataJsonFile = RJ.readJson(testDataPath)
    except:
        testDataPath = os.path.abspath("../../test_data/test_data.json")
        testDataJsonFile = RJ.readJson(testDataPath)
    return testDataJsonFile[attribute]


def testDataExcel(attribute):
    testDataPath = os.path.abspath("././test_data/test_data.xlsx")
    try:
        testDataJsonFile = RE.readFromExcel(testDataPath)
    except:
        testDataPath = os.path.abspath("../../test_data/test_data.json")
        testDataJsonFile = RE.readFromExcel(testDataPath)
    return testDataJsonFile[attribute]
