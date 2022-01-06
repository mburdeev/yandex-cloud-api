from typing import Dict, List, Optional
from urllib.parse import urljoin


import requests
from loguru import logger

import config
from api.errors import YandexAPIError
from iamtoken import IamToken


class Translator:

    BASE_API_URL = "https://translate.api.cloud.yandex.net/translate/v2/"

    def __init__(self, folder_id=config.FOLDER_ID, iamtoken=IamToken()) -> None:
        self.folder_id = folder_id
        self.iamtoken = iamtoken

    def _request(self, path, params=dict(), headers=dict()):
        api_url = urljoin(Translator.BASE_API_URL, path)

        default_params = {
            "folderId": self.folder_id,
        }
        default_params.update(params)
        _params = default_params.copy()

        default_headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.iamtoken.token),
        }
        default_headers.update(headers)
        _headers = default_headers.copy()

        response = requests.post(
            api_url,
            json=_params,
            headers=_headers,
        )
        return self._check_response(response)

    def _check_response(self, response: requests.Response) -> dict:
        data = self._parse_response(response)
        if "code" in data.keys():
            raise YandexAPIError(**data)
        else:
            return data

    def _parse_response(self, response: requests.Response) -> dict:
        try:
            return response.json()
        except Exception as e:
            raise YandexAPIError(
                code=-1,
                message="The response is not implemented in JSON format",
                details={"raw_content": response.content},
            )

    def translate(self, texts: List[str], target_language_code: str):
        api_path = "translate"

        params = {
            "targetLanguageCode": target_language_code,
            "texts": texts,
        }

        response = self._request(api_path, params)
        return response["translations"]

    def __call__(self, text: str, to: str):
        tranlations = self.translate([text], to)
        return tranlations[0]["text"]

    def get_available_langs(self) -> Dict[str, str]:
        api_path = "languages"
        data = self._request(api_path)
        return data["languages"]


def test_translator_translate():
    translator = Translator()
    return translator.translate(["Hello, World!"], "ru")


def test_translator_error():
    translator = Translator()
    return translator("Hello, World!", "emj")


def test_translator_call():
    translator = Translator()
    return translator("Hello, World!", "ru")


def test_get_available_langs():
    translator = Translator()
    return translator.get_available_langs()
