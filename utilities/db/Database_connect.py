import mysql.connector
from utilities.CustomLogging import getLogger
import pandas as pd

log = getLogger()


class DatabaseConnect:

    @staticmethod
    def connect_to_database(db_user, db_password, host, port):
        """
        Method to connect the database through API
        """
        log.info("Mysql Connection is closed")
        try:
            db_connection = mysql.connector.connect(
                host=host,
                user=db_user,
                password=db_password,
                port=port
            )
            cursor = db_connection.cursor()
            return [cursor, db_connection]
        except Exception as e:
            print(e)
            log.error("Error while connecting to Mysql")

    @staticmethod
    def alter_data_into_table(cursor, db_connection, query):
        """
        Method to perform insert,delete & update operations
        """
        log.info("Altering data")
        cursor.execute(query)
        db_connection.commit()

    @staticmethod
    def fetch_single_data_from_table(cursor, query):
        """
        Method to fetch the single data from db
        """
        cursor.execute(query)
        result = cursor.fetchone()
        return result

    @staticmethod
    def fetch_multiple_data_from_table(cursor, query):
        """
        Method to fetch the single data from db
        """
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    @staticmethod
    def execute_query_db(cursor, query):
        """
        Method to perform Drop & create database operations
        """
        log.info("Execute mysql query")
        cursor.execute(query)

    @staticmethod
    def close_db_connect(cursor, db_connection):
        """
        Method to close the db connection
        """
        log.info("Closing DB connection")
        cursor.close()
        db_connection.close()
        log.info("Mysql connection is closed")

    @staticmethod
    def query_result_to_df(db_connection,query):
        log.info("Query result to a Dataframe")
        return pd.read_sql_query(query, db_connection)
