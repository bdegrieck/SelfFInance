from contextlib import contextmanager

import mysql.connector
from mysql.connector import Error
from sqlalchemy import create_engine

from BackEnd.Data.companydata import CompanyData


class DBConn:

    @contextmanager
    def get_cursor(self, connection):
        cursor = connection.cursor()
        try:
            yield cursor
        finally:
            cursor.close()

    def get_connection(self, data_base):
        """ Connect to MySQL database """
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database=f"{data_base}",
                user='root',
                password='Maggie01'
            )
            if connection.is_connected():
                db_info = connection.get_server_info()
                print("Connected to MySQL Server version ", db_info)

            return connection

        except Error as e:
            print("Error while connecting to MySQL", e)

    def post_whole_company_data(self, company_raw_data: CompanyData, db_connection):

        with self.get_cursor(db_connection) as cursor:
            database = cursor.fetchone()
            print("You're connected to database: ", database)
            engine = create_engine("mysql+pymysql://root:Maggie01@localhost/appledata")
            company_raw_data.company_dfs.stock_data_df.to_sql(
                name="timeseries",
                con=engine,
                if_exists="replace",
                index=True
            )

            company_raw_data.company_dfs.eps_df.to_sql(
                name="eps",
                con=engine,
                if_exists="replace",
                index=True
            )

            company_raw_data.company_dfs.balance_sheet_df.to_sql(
                name="balancesheet",
                con=engine,
                if_exists="replace",
                index=True
            )


