from ..utilities.CustomLogging import getLogger
import pandas as pd

log = getLogger()


def df_compare_with_equal_vals(df1=pd.DataFrame, df2=pd.DataFrame):
    """
           Method to fetch matching values from the two dataframe ,when connect the database through API
    """
    try:
        dfFinal = df1.compare(df2, keep_equal=True)
        if dfFinal[dfFinal.columns[0]].count() == df1[df1.columns[0]].count():
            log.info("The dataframe matches with the other")
            print("Dataframe matches with the other")
        else:
            log.info("The dataframe doesnt match with the other")
            print("The dataframe doesnt match with the other")
    except Exception as E:
        print(E)
        log.info("There was a error")


def df_compare_with_equal_valscheck(df1, df2):
    """
           Method to fetch matching values from the two dataframe ,when connect the database through API
    """
    print("Function entered")
    print(df1)
    print(df2)

    dfFinal = df1.compare(df2, keep_equal=True)
    print(dfFinal)
    val1 = dfFinal[dfFinal.columns[0]].count()
    val2 = df1[df1.columns[0]].count()
    if val1.equals(val2):
        log.info("The dataframe matches with the other")
        print("Dataframe matches with the other")
    else:
        log.info("The dataframe doesnt match with the other")
        print("The dataframe doesnt match with the other")
    return dfFinal

def df_compare_with_not_equal_vals(df1=pd.DataFrame, df2=pd.DataFrame):
    """
           Method to fetch matching values from the two dataframe ,when connect the database through API
    """
    try:
        dfFinal = df1.compare(df2, keep_equal=False)
        if dfFinal[dfFinal.columns[0]].count() == 0:
            log.info("The dataframe matches with the other")
            print("Dataframe matches with the other")
        else:
            log.info("The dataframe doesnt match with the other")
            print("The dataframe doesnt match with the other")
    except Exception as E:
        print(E)
        log.info("There was a error")
