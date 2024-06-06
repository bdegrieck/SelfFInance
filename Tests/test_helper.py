from pydantic import BaseModel
import pandas as pd


# class for initializing an object that be used for testing grabbing dfs from database
class TestCompanyDFS(BaseModel):
    stock_data_df: pd.DataFrame
    overview_df: pd.DataFrame
    eps_df: pd.DataFrame
    balance_sheet_df: pd.DataFrame

    class Config:
        arbitrary_types_allowed = True


class TestTechnicalIndicators(BaseModel):
    ad: pd.DataFrame
    adx: pd.DataFrame
    bbands: pd.DataFrame
    ema: pd.DataFrame
    macd: pd.DataFrame
    obv: pd.DataFrame
    rsi: pd.DataFrame
    sma: pd.DataFrame

    class Config:
        arbitrary_types_allowed = True
