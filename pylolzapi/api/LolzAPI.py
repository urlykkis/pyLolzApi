from __future__ import annotations

import urllib.parse
import requests
import json

from datetime import datetime

from .base import BaseLolzAPI
from pylolzapi.misc.exceptions import LolzAPIError


class LZTApi(BaseLolzAPI):
    def __init__(self,
                 token: str = None,
                 client_id: str = None,
                 client_secret: str = None,
                 scope: list[str] = None
                 ) -> LZTApi:
        super(LZTApi, self).__init__(token, client_id, client_secret, scope)
        self._session = requests.session()
        self._session.headers = {"Authorization": f"Bearer {self.token}"}

        me = self.me()
        self._user_id = me["user"]["user_id"]
        self._username = me["user"]["username"]
        self._permalink = me["user"]["links"]["permalink"]
        self._avatar = me["user"]["links"]["avatar"]

    def __request(self, method, *args, **kwargs) -> requests.Response:
        response = method(*args, **kwargs)
        try:
            resp_json = response.json()
        except json.decoder.JSONDecodeError:
            raise LolzAPIError(response.text.split('<h1>')[1].split('</h1>')[0])

        if resp_json.get("errors") or resp_json.get("error"):
            if resp_json.get("error_description", False) is not False:
                raise LolzAPIError(resp_json["error_description"])
            else:
                raise LolzAPIError(",".join(resp_json["errors"]))

        return response

    def _get(self, url: str, params=None) -> dict:
        if params is None:
            params = {}

        return self.__request(self._session.get,
                              self._base_url + url,
                              params=params).json()

    def _post(self, url: str, data=None) -> dict:
        if data is None:
            data = {}

        return self.__request(self._session.post,
                              self._base_url + url,
                              data=data).json()

    def _delete(self, url: str, data=None) -> dict:
        if data is None:
            data = {}

        return self.__request(self._session.delete,
                              self._base_url + url,
                              data=data).json()

    def me(self):
        return self._get("users/me")

    def market_payments(self,
                        payment_type: str = None,
                        pmin: int = None,
                        pmax: int = None,
                        receiver: str = None,
                        sender: str = None,
                        start_date: datetime = None,
                        end_date: datetime = None,
                        wallet: str = None,
                        comment: str = None,
                        is_hold: str = None):
        data = dict()

        if payment_type: data['type'] = payment_type
        if pmin: data['pmin'] = pmin
        if pmax: data['pmax'] = pmax
        if receiver: data['receiver'] = receiver
        if sender: data['sender'] = sender
        if start_date: data['startDate'] = start_date
        if end_date: data['endDate'] = end_date
        if wallet: data['wallet'] = wallet
        if comment: data['comment'] = comment
        if is_hold: data['is_hold'] = is_hold

        return self._post(f'market/user/{self._user_id}/payments', data)

    def transfer(self, amount: int = None, comment: str = None, hold: bool = None):
        url = f"https://zelenka.guru/market/balance/transfer?username={self._username}"

        if amount:
            url += f"&amount={amount}"
        if comment:
            comment = urllib.parse.quote(comment)
            url += f"&comment={comment}"
        if hold is not None:
            url += f"&hold={0 if hold is False else 1}"

        return url
