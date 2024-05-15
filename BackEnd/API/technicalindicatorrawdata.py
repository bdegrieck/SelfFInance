import datetime
from typing import List

from pydantic import BaseModel


class SMA(BaseModel):
    date: datetime.datetime
    sma: float


class EMA(BaseModel):
    date: datetime.datetime
    ema: float


class RSI(BaseModel):
    date: datetime.datetime
    rsi: float


class MACD(BaseModel):
    date: datetime.datetime
    macd: float


class BBANDS(BaseModel):
    date: datetime.datetime
    lower_band: float
    middle_band: float
    upper_band: float


class ADX(BaseModel):
    date: datetime.datetime
    adx: float


class AD(BaseModel):
    date: datetime.datetime
    ad: float


class OBV(BaseModel):
    date: datetime.datetime
    obv: float


class TechnicalIndicatorsRawData(BaseModel):
    sma: List[SMA]
    ema: List[EMA]
    rsi: List[RSI]
    macd: List[MACD]
    bbands: List[BBANDS]
    adx: List[ADX]
    ad: List[AD]
    obv: List[OBV]
