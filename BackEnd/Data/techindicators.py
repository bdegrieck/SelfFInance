from typing import List

import pandas as pd

from BackEnd.API.api import get_raw_api_data, get_technical_indicator_endpoints, get_technical_indicator_raw_data
from BackEnd.API.technicalindicatorrawdata import SMA, EMA, BBANDS, RSI, AD, ADX, MACD, OBV


class TechnicalIndicators:

    def __init__(self, ticker: str):
        endpoints = get_technical_indicator_endpoints(ticker=ticker)
        raw_data = get_raw_api_data(endpoints=endpoints)
        raw_technical_indicator_data = get_technical_indicator_raw_data(indicator_raw_data=raw_data)
        self.dfs = TechnicalIndicatorsDfs(raw_technical_indicator_data=raw_technical_indicator_data)


class TechnicalIndicatorsDfs:
    def __init__(self, raw_technical_indicator_data):
        self.sma = get_sma_df(raw_sma_data=raw_technical_indicator_data.sma)
        self.ema = get_ema_df(raw_ema_data=raw_technical_indicator_data.ema)
        self.rsi = get_rsi_df(raw_rsi_data=raw_technical_indicator_data.rsi)
        self.ad = get_ad_df(raw_ad_data=raw_technical_indicator_data.ad)
        self.adx = get_adx_df(raw_adx_data=raw_technical_indicator_data.adx)
        self.macd = get_macd_df(raw_macd_data=raw_technical_indicator_data.macd)
        self.obv = get_obv_df(raw_obv_data=raw_technical_indicator_data.obv)
        self.bbands = get_bbands_df(raw_bbands_data=raw_technical_indicator_data.bbands)


def get_sma_df(raw_sma_data: List[SMA]) -> pd.DataFrame:
    dates = []
    sma_values = []
    for sma in raw_sma_data:
        dates.append(sma.date)
        sma_values.append(sma.sma)

    sma_df = pd.DataFrame({
        "date": dates,
        "sma": sma_values
    }).set_index("date", drop=True)

    return sma_df


def get_ema_df(raw_ema_data: List[EMA]) -> pd.DataFrame:
    dates = []
    ema_values = []
    for ema in raw_ema_data:
        dates.append(ema.date)
        ema_values.append(ema.ema)

    ema_df = pd.DataFrame({
        "date": dates,
        "ema": ema_values
    }).set_index("date", drop=True)

    return ema_df


def get_rsi_df(raw_rsi_data: List[RSI]) -> pd.DataFrame:
    dates = []
    rsi_values = []
    for rsi in raw_rsi_data:
        dates.append(rsi.date)
        rsi_values.append(rsi.rsi)

    rsi_df = pd.DataFrame({
        "date": dates,
        "rsi": rsi_values
    }).set_index("date", drop=True)

    return rsi_df


def get_ad_df(raw_ad_data: List[AD]) -> pd.DataFrame:
    dates = []
    ad_values = []
    for ad in raw_ad_data:
        dates.append(ad.date)
        ad_values.append(ad.ad)

    ad_df = pd.DataFrame({
        "date": dates,
        "ad": ad_values
    }).set_index("date", drop=True)

    return ad_df


def get_adx_df(raw_adx_data: List[ADX]) -> pd.DataFrame:
    dates = []
    adx_values = []
    for adx in raw_adx_data:
        dates.append(adx.date)
        adx_values.append(adx.adx)

    adx_df = pd.DataFrame({
        "date": dates,
        "adx": adx_values
    }).set_index("date", drop=True)

    return adx_df


def get_macd_df(raw_macd_data: List[MACD]) -> pd.DataFrame:
    dates = []
    macd_values = []
    for macd in raw_macd_data:
        dates.append(macd.date)
        macd_values.append(macd.macd)

    macd_df = pd.DataFrame({
        "date": dates,
        "macd": macd_values
    }).set_index("date", drop=True)

    return macd_df


def get_obv_df(raw_obv_data: List[OBV]) -> pd.DataFrame:
    dates = []
    obv_values = []
    for obv in raw_obv_data:
        dates.append(obv.date)
        obv_values.append(obv.obv)

    obv_df = pd.DataFrame({
        "date": dates,
        "obv": obv_values
    }).set_index("date", drop=True)

    return obv_df


def get_bbands_df(raw_bbands_data: List[BBANDS]) -> pd.DataFrame:
    dates = []
    lower_bands = []
    middle_bands = []
    upper_bands = []

    for bbands in raw_bbands_data:
        dates.append(bbands.date)
        lower_bands.append(bbands.lower_band)
        middle_bands.append(bbands.middle_band)
        upper_bands.append(bbands.upper_band)

    bbands_df = pd.DataFrame({
        "date": dates,
        "lowerBand": lower_bands,
        "middleBand": middle_bands,
        "upperBand": upper_bands
    }).set_index("date", drop=True)

    return bbands_df
