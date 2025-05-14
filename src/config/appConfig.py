from dataclasses import dataclass, field
import json


@dataclass
class AppConfig:
    isRandom: bool = field(default=True)
    histDataUrlBase: str = field(default="")
    flaskSecret: str = field(default="")
    testPnt: str = field(default="")
    flaskHost: str = field(default="localhost")
    flaskPort: int = field(default=8080)


def loadAppConfig(fName="config/config.json") -> AppConfig:
    global jsonConfig
    with open(fName) as f:
        data = json.load(f)
        jsonConfig = AppConfig(**data)
        return jsonConfig


def getAppConfig() -> AppConfig:
    global jsonConfig
    return jsonConfig
