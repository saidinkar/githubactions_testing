import pandas as pd
from tests.settings import testdataPath


def test_data(Column):
    df = pd.read_excel(testdataPath)
    val1 = df[Column].tolist()
    return str(val1[0])
