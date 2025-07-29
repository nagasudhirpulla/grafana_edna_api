import random
import requests
from src.config.appConfig import getAppConfig
import datetime as dt
import pandas as pd
import json


def fetchScadaPntHistData(pntId: str, startTime: dt.datetime, endTime: dt.datetime, samplingType: str = 'snap', samplingSecs: int = 60,  avoidFuture: bool = False, timeOffsetSecs: int = 0) -> list[list[float]]:
    # https://nagasudhir.blogspot.com/2024/05/json-grafana-plugin-to-fetch-api-data.html
    appConf = getAppConfig()
    if appConf.isRandom:
        return fetchScadaPntRandHistData(pntId, startTime, endTime)
    pntId = pntId.strip()
    if pntId == "":
        return []
    timeOffsetDelta = dt.timedelta(seconds=timeOffsetSecs)
    urlStr = appConf.histDataUrlBase
    paramsObj = {"pnt": pntId,
                 "strtime": (startTime+timeOffsetDelta).strftime("%d/%m/%Y/%H:%M:%S"),
                 "endtime": (endTime+timeOffsetDelta).strftime("%d/%m/%Y/%H:%M:%S"),
                 "secs": samplingSecs,
                 "type": samplingType}
    try:
        r = requests.get(url=urlStr, params=paramsObj)
        data = json.loads(r.text)
        r.close()
    except Exception as e:
        print("Error loading data from scada api")
        print(e)
        data = []
    dataRes: list[list[float]] = []
    nowDt = dt.datetime.now()
    for sampl in data:
        samplDt = dt.datetime.strptime(
            sampl["timestamp"], "%Y-%m-%dT%H:%M:%S")-dt.timedelta(seconds=timeOffsetSecs)
        if (avoidFuture and samplDt > nowDt):
            continue
        dataRes.append([
            sampl["dval"],
            int(samplDt.timestamp()*1000)
        ])
    return dataRes


def fetchScadaPntRandHistData(pntId, startTime: dt.datetime, endTime: dt.datetime) -> pd.Series:
    # TODO add timeOffsetSecs and avoidFuture features
    pntId = pntId.strip()
    if pntId == "":
        return pd.Series()
    if startTime > endTime:
        return pd.Series()
    timestamps = pd.date_range(
        startTime, endTime, freq=dt.timedelta(minutes=1)).tolist()
    dataSeries = [[random.randint(-1000, 1000), x.timestamp()*1000]
                  for x in timestamps]
    return dataSeries
