from contextlib import contextmanager

import mysql.connector
import pandas as pd
from mysql.connector import Error
from sqlalchemy import create_engine
from BackEnd.constants import SQL_USERNAME, SQL_PASSWORD
from BackEnd.Data.techindicators import TechnicalIndicatorsDfs
import pymysql

from BackEnd.Data.companydata import CompanyData
from Tests.test_helper import TestCompanyDFS, TestTechnicalIndicators


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
                database=data_base,
                user=SQL_USERNAME,
                password=SQL_PASSWORD
            )
            if connection.is_connected():
                db_info = connection.get_server_info()
                print("Connected to MySQL Server version ", db_info)

            return connection

        except Error as e:
            print("Error while connecting to MySQL", e)

    def post_whole_company_data(self, company_raw_data: CompanyData, db_conn, db_name):
        try:
            with self.get_cursor(db_conn) as cursor:
                # Ensure there are no unread results left
                try:
                    while cursor.nextset():
                        pass
                except Error as e:
                    print("Error clearing unread results:", e)
                    return

                # Verify the database
                try:
                    cursor.execute("SELECT DATABASE()")
                    result = cursor.fetchone()
                    if result:
                        print("You're connected to database: ", result[0])
                    else:
                        print("No database selected")
                except Error as e:
                    print("Error executing SELECT DATABASE():", e)
                    return

                # engine that allows dfs to be inserted to sql
                engine = create_engine(f"mysql+pymysql://{SQL_USERNAME}:{SQL_PASSWORD}@localhost/{db_name}")

                # inserting stock prices into sql
                company_raw_data.company_dfs.stock_data_df.to_sql(
                    name="timeseries",
                    con=engine,
                    if_exists="replace",
                    index=True,
                    chunksize=1000
                )

                # inserting company overview into sql
                overview_columns_query = "INSERT INTO overview (ticker_symbol, company_description, market_cap, year_price_high, year_price_low) VALUES (%s, %s, %s, %s, %s)"
                overview_views_query = (
                    company_raw_data.company_overview.ticker_symbol,
                    company_raw_data.company_overview.company_description,
                    company_raw_data.company_overview.market_cap,
                    company_raw_data.company_overview.year_price_high,
                    company_raw_data.company_overview.year_price_low
                )
                cursor.execute(overview_columns_query, overview_views_query)

                # Ensure the insert is committed if using transactions
                db_conn.commit()

                # insert eps into sql
                company_raw_data.company_dfs.eps_df.to_sql(
                    name="eps",
                    con=engine,
                    if_exists="replace",
                    index=True
                )

                # insert balance sheet into sql
                company_raw_data.company_dfs.balance_sheet_df.to_sql(
                    name="balancesheet",
                    con=engine,
                    if_exists="replace",
                    index=True
                )

        except Error as e:
            print("Error in post_whole_company_data:", e)
        finally:
            if db_conn.is_connected():
                db_conn.close()

    def post_all_technical_indicator_data(self, technical_indicators: TechnicalIndicatorsDfs, db_conn, db_name: str):
        try:
            with self.get_cursor(db_conn) as cursor:
                # Ensure there are no unread results left
                try:
                    while cursor.nextset():
                        pass
                except Error as e:
                    print("Error clearing unread results:", e)
                    return

                # Verify the database
                try:
                    cursor.execute("SELECT DATABASE()")
                    result = cursor.fetchone()
                    if result:
                        print("You're connected to database: ", result[0])
                    else:
                        print("No database selected")
                except Error as e:
                    print("Error executing SELECT DATABASE():", e)
                    return

                # engine that allows dfs to be inserted to sql
                engine = create_engine(f"mysql+pymysql://{SQL_USERNAME}:{SQL_PASSWORD}@localhost/{db_name}")

                technical_indicators.ad.to_sql(
                    name="ad",
                    con=engine,
                    if_exists="replace",
                    index=True,
                    chunksize=1000
                )

                technical_indicators.adx.to_sql(
                    name="adx",
                    con=engine,
                    if_exists="replace",
                    index=True,
                    chunksize=1000
                )

                technical_indicators.bbands.to_sql(
                    name="bbands",
                    con=engine,
                    if_exists="replace",
                    index=True,
                    chunksize=1000
                )

                technical_indicators.ema.to_sql(
                    name="ema",
                    con=engine,
                    if_exists="replace",
                    index=True,
                    chunksize=1000
                )

                technical_indicators.macd.to_sql(
                    name="macd",
                    con=engine,
                    if_exists="replace",
                    index=True,
                    chunksize=1000
                )

                technical_indicators.obv.to_sql(
                    name="obv",
                    con=engine,
                    if_exists="replace",
                    index=True,
                    chunksize=1000
                )

                technical_indicators.rsi.to_sql(
                    name="rsi",
                    con=engine,
                    if_exists="replace",
                    index=True,
                    chunksize=1000
                )

                technical_indicators.sma.to_sql(
                    name="sma",
                    con=engine,
                    if_exists="replace",
                    index=True,
                    chunksize=1000
                )

        except Error as e:
            print("Error in post_whole_company_data:", e)
        finally:
            if db_conn.is_connected():
                db_conn.close()

    def get_all_company_df_data(self, db_conn):
        cursor = db_conn.cursor()
        try:
            # Fetching stock_data
            cursor.execute("SELECT * FROM timeseries")
            stock_data_df = pd.DataFrame(cursor.fetchall(), columns=[col[0] for col in cursor.description]).set_index("date", drop=True)

            # Fetching overview data
            cursor.execute("SELECT * FROM overview")
            overview_df = pd.DataFrame(cursor.fetchall(), columns=[col[0] for col in cursor.description])

            # Fetching EPS data
            cursor.execute("SELECT * FROM eps")
            eps_df = pd.DataFrame(cursor.fetchall(), columns=[col[0] for col in cursor.description]).set_index("quarterDate", drop=True)

            # Fetching balance sheet data
            cursor.execute("SELECT * FROM balancesheet")
            balance_sheet_df = pd.DataFrame(cursor.fetchall(), columns=[col[0] for col in cursor.description]).set_index("quarterDate", drop=True)

            return TestCompanyDFS(
                stock_data_df=stock_data_df,
                overview_df=overview_df,
                eps_df=eps_df,
                balance_sheet_df=balance_sheet_df
            )

        except Error as e:
            print(f"An error occurred: {e}")
            return None

    def get_all_technical_df_data(self, db_conn):
        cursor = db_conn.cursor()
        try:
            cursor.execute("SELECT * FROM ad")
            ad_df = pd.DataFrame(cursor.fetchall(), columns=[col[0] for col in cursor.description]).set_index("date", drop=True)

            cursor.execute("SELECT * FROM adx")
            adx_df = pd.DataFrame(cursor.fetchall(), columns=[col[0] for col in cursor.description]).set_index("date", drop=True)

            cursor.execute("SELECT * FROM bbands")
            bbands_df = pd.DataFrame(cursor.fetchall(), columns=[col[0] for col in cursor.description]).set_index("date", drop=True)

            cursor.execute("SELECT * FROM ema")
            ema_df = pd.DataFrame(cursor.fetchall(), columns=[col[0] for col in cursor.description]).set_index("date", drop=True)

            cursor.execute("SELECT * FROM macd")
            macd_df = pd.DataFrame(cursor.fetchall(), columns=[col[0] for col in cursor.description]).set_index("date", drop=True)

            cursor.execute("SELECT * FROM obv")
            obv_df = pd.DataFrame(cursor.fetchall(), columns=[col[0] for col in cursor.description]).set_index("date", drop=True)

            cursor.execute("SELECT * FROM rsi")
            rsi_df = pd.DataFrame(cursor.fetchall(), columns=[col[0] for col in cursor.description]).set_index("date", drop=True)

            cursor.execute("SELECT * FROM sma")
            sma_df = pd.DataFrame(cursor.fetchall(), columns=[col[0] for col in cursor.description]).set_index("date", drop=True)

            return TestTechnicalIndicators(
                ad=ad_df,
                adx=adx_df,
                bbands=bbands_df,
                ema=ema_df,
                macd=macd_df,
                obv=obv_df,
                rsi=rsi_df,
                sma=sma_df
            )

        except Error as e:
            print(f"An error occurred: {e}")
            return None




