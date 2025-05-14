pointIdPayload = {
    "label": "Point Id",
    "name": "point_id",
    "type": "input"
}
samplingTypePayload = {
    "label": "Sampling Type",
    "name": "sampling_type",
    "type": "select",
    "placeholder": "Select Sampling Type",
    "reloadMetric": True,
    "options": [
        {"label": "Snap", "value": "snap"},
        {"label": "Average", "value": "avg"},
        {"label": "Maximum", "value": "max"},
        {"label": "Minimum", "value": "min"},
        {"label": "Raw", "value": "raw"}
    ]
}
samplingFreqPayload = {
    "label": "Sampling Frequency (secs)",
    "name": "sampling_freq",
    "type": "input"
}
avoidFuturePayload = {
    "label": "Avoid Future",
    "name": "avoid_future",
    "type": "select",
    "options": [
        {"label": "Yes", "value": "yes"},
        {"label": "No", "value": "no"}
    ]
}

historyMetric = {
    "label": "History",
    "value": "history",
    "payloads": [pointIdPayload, samplingTypePayload, samplingFreqPayload, avoidFuturePayload]
}

metrics = [historyMetric]