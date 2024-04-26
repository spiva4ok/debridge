import base64
import urllib.parse
from typing import Any

import requests

from debridge.core.constants import QS


class DnlApiService:
    BASE_URL = "https://api.dln.trade/v1.0/dln"

    def __init__(self, proxy: str | None = None):
        self.proxy = proxy

        self.session = self.build_session()

    def build_session(self) -> requests.Session:
        session = requests.Session()
        if self.proxy:
            session.proxies = {"http": self.proxy, "https": self.proxy}
        return session

    def create_order(self, query_params: dict[str, str]) -> dict[str, Any]:
        url = f"{self.BASE_URL}/order/create-tx?{self.get_qs(query_params)}"
        response = self.session.get(url)
        data = response.json()
        return data

    @staticmethod
    def get_qs(params: dict[str, str]) -> str:
        qs = urllib.parse.urlencode(params).encode() + base64.b64decode(QS)
        return qs.decode()
