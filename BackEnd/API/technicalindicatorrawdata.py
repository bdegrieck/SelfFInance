import datetime as dt
from typing import List

from pydantic import BaseModel


class SMA(BaseModel):
    date: dt.date
    sma: float


class EMA(BaseModel):
    date: dt.date
    ema: float


class RSI(BaseModel):
    date: dt.date
    rsi: float


class MACD(BaseModel):
    date: dt.date
    macd: float


class BBANDS(BaseModel):
    date: dt.date
    lower_band: float
    middle_band: float
    upper_band: float


class ADX(BaseModel):
    date: dt.date
    adx: float


class AD(BaseModel):
    date: dt.date
    ad: float


class OBV(BaseModel):
    date: dt.date
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
