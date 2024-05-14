from pydantic import BaseModel
from typing import List


class SMA(BaseModel):
    date: str
    sma: float


class EMA(BaseModel):
    date: str
    ema: float


class RSI(BaseModel):
    date: str
    rsi: float


class MACD(BaseModel):
    date: str
    macd: float


class BBANDS(BaseModel):
    date: str
    lower_band: float
    middle_band: float
    upper_band: float


class ADX(BaseModel):
    date: str
    adx: float


class AD(BaseModel):
    date: str
    ad: float


class OBV(BaseModel):
    date: str
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
