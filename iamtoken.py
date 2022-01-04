import json
import requests
from datetime import datetime, timedelta, timezone

from loguru import logger

import config


class IamToken:

    API_URL = "https://iam.api.cloud.yandex.net/iam/v1/tokens"
    FILE = ".iamtoken"
    DT_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"

    def __init__(self, oauth_token=None):
        self.oauth_token = config.OAUTH_TOKEN
        try:
            self.load_from_file()
            self.check_freshness()
        except FileNotFoundError:
            self.token_request()
        except Exception as e:
            logger.exception("Load from file error:")
            raise

    def token_request(self):
        params = {"yandexPassportOauthToken": self.oauth_token}
        response = requests.post(IamToken.API_URL, json=params)
        response_data = response.json()
        self._token = response_data["iamToken"]
        self.expires_at = self.parse_yandex_dt(response_data["expiresAt"])
        self.received_at = self.now()
        self.save_to_file()

    def check_freshness(self):
        if self.received_at - self.now() > timedelta(hours=1):
            self.token_request()

    @property
    def token(self):
        self.check_freshness()
        return self._token

    def save_to_file(self, file=None):
        file = file or self.FILE

        fields = {
            "token": self._token,
            "expires_at": self.dt_to_str(self.expires_at),
            "received_at": self.dt_to_str(self.received_at),
        }
        json.dump(fields, open(file, "w"))

    def load_from_file(self, file=None):
        file = file or self.FILE
        data = json.load(open(file, "r"))
        self._token = data["token"]
        self.expires_at = self.dt_parse(data["expires_at"])
        self.received_at = self.dt_parse(data["received_at"])

    @staticmethod
    def now():
        tz = datetime.now(timezone.utc).astimezone().tzinfo
        return datetime.now(tz=tz)

    @staticmethod
    def parse_yandex_dt(yandex_dt_str):
        return IamToken.dt_parse(IamToken.prepare_yandex_dt(yandex_dt_str))

    @staticmethod
    def prepare_yandex_dt(yandex_dt_str):
        "Yandex datetime include nanoseconds, but python not parse nanoseconds"
        "Remove 3 symbols"
        return yandex_dt_str[:-4] + yandex_dt_str[-1:]

    @staticmethod
    def dt_parse(dt_str: str):
        return datetime.strptime(dt_str, IamToken.DT_FORMAT)

    @staticmethod
    def dt_to_str(dt: datetime):
        return dt.strftime(IamToken.DT_FORMAT)
