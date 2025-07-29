from flask import Flask, request, jsonify
from copy import deepcopy
import datetime as dt
from src.config.appConfig import loadAppConfig
from src.grafanaMetrics.dataSourceMetrics import metrics, pointIdPayload, samplingTypePayload, avoidFuturePayload, samplingFreqPayload, timeOffsetPayload
from src.services.scadaFetcher import fetchScadaPntHistData
from dateutil import tz


appConfig = loadAppConfig()

app = Flask(__name__)
app.secret_key = appConfig.flaskSecret


@app.route("/api")
def healthCheck():
    return ""


@app.route("/api/metrics", methods=["POST"])
def getMetrics():
    metricsFinal = deepcopy(metrics)
    queryData = request.get_json()
    metricName = queryData.get("metric", "")
    samplingType = queryData.get("payload", {}).get("sampling_type", "")
    if metricName == "history" and samplingType == "raw":
        metricsFinal[0]["payloads"] = [pointIdPayload,
                                       samplingTypePayload, avoidFuturePayload]
    return jsonify(metricsFinal)


@app.route("/api/query", methods=["POST"])
def queryData():
    queryData = request.get_json()
    # print(queryData)
    startTime = dt.datetime.strptime(
        queryData["range"]["from"], "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=tz.tzutc()).astimezone(tz.tzlocal())
    endTime = dt.datetime.strptime(
        queryData["range"]["to"], "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=tz.tzutc()).astimezone(tz.tzlocal())
    targets = queryData["targets"]
    response = []
    for t in targets:
        targetPayload = t.get("payload", {})
        targetData = {
            "target": t["refId"],
            "datapoints": []
        }
        samplFreq = int(targetPayload.get(samplingFreqPayload["name"], "60"))
        samplingType = targetPayload.get(samplingTypePayload["name"], "")
        pntId = targetPayload.get(pointIdPayload["name"], "")
        avoidFuture = targetPayload.get(avoidFuturePayload["name"], "no")
        timeOffsetSecs = targetPayload.get(timeOffsetPayload["name"], 0)
        data = fetchScadaPntHistData(
            pntId, startTime, endTime, samplingType, samplFreq, avoidFuture == "yes", int(timeOffsetSecs))
        targetData["datapoints"] = data
        response.append(targetData)
    # print(response)
    return jsonify(response)


app.run(host=appConfig.flaskHost, port=appConfig.flaskPort, debug=True)
