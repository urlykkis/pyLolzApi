from __future__ import annotations

import urllib.parse
from typing import Tuple, List

import requests
import json

from datetime import datetime

from .base import BaseLolzAPI
from pylolzapi.types.user import User
from pylolzapi.types.payment import Operation
from pylolzapi.types.items import Item
from pylolzapi.utils.exceptions import LolzAPIError


class LZTApi(BaseLolzAPI):
    def __init__(self,
                 token: str = None,
                 client_id: str = None,
                 client_secret: str = None,
                 scope: list[str] = None
                 ) -> LZTApi:
        super(LZTApi, self).__init__(token, client_id, client_secret, scope)
        self._session = requests.session()
        self._session.headers = {"Authorization": f"Bearer {self._token}"}

        self.user_info: User = self.me()

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
            params = dict()

        return self.__request(self._session.get,
                              self._base_url + url,
                              params=params).json()

    def _post(self, url: str, data=None) -> dict:
        if data is None:
            data = dict()

        return self.__request(self._session.post,
                              self._base_url + url,
                              data=data).json()

    def _delete(self, url: str, data=None) -> dict:
        if data is None:
            data = dict()

        return self.__request(self._session.delete,
                              self._base_url + url,
                              data=data).json()

    def me(self) -> User:
        """Отображает информацию о вашем профиле."""
        return User.parse_obj(self._get("users/me")["user"])

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
                        is_hold: str = None
                        ) -> tuple[list[Operation], dict]:
        """
        Выводит список транзакций на аккаунте.
        :param payment_type: Тип операции. Разрешенные типы операций: income, cost, refilled_balance,
        withdrawal_balance, paid_item, sold_item, money_transfer, receiving_money, internal_purchase, claim_hold
        :param pmin: Минимальная стоимость операции
        :param pmax: Максимальная стоимость операции
        :param receiver: Имя пользователя, который получает от вас деньги
        :param sender: Имя пользователя, который отправил вам деньги
        :param start_date: Дата начала операции (формат даты RFC 3339)
        :param end_date: Дата окончания операции (формат даты RFC 3339)
        :param wallet: Кошелек, который используется для денежных выплат
        :param comment: Комментарий для денежных переводов
        :param is_hold: Отображение операций удержания
        :return: dict
        """
        data = dict()

        if payment_type:
            data['type'] = payment_type
        if pmin:
            data['pmin'] = pmin
        if pmax:
            data['pmax'] = pmax
        if receiver:
            data['receiver'] = receiver
        if sender:
            data['sender'] = sender
        if start_date:
            data['startDate'] = start_date
        if end_date:
            data['endDate'] = end_date
        if wallet:
            data['wallet'] = wallet
        if comment:
            data['comment'] = comment
        if is_hold:
            data['is_hold'] = is_hold

        resp = self._get(f'market/user/{self.user_info.user_id}/payments', params=data)

        return [Operation.parse_obj(resp["payments"][operation]) for operation in resp["payments"]], resp

    def market_list(self, category: str = None,
                    pmin: int = None,
                    pmax: int = None,
                    title: str = None,
                    parse_sticky_items: str = None,
                    optional: dict = None
                    ) -> tuple[list[Item], dict]:
        """
        Получить все последние аккаунты маркета.
        :param category: Категория на маркете
        :param pmin: Минимальная цена для аккаунта
        :param pmax: Максимальная цена для аккаунта
        :param title: Название аккаунта
        :param parse_sticky_items: Условие для разбора параметров
        :param optional: Получить параметры URL-адреса из market
        :return:
        """
        if category:
            data = dict()

            if title:
                data['title'] = title
            if pmin:
                data['pmin'] = pmin
            if pmax:
                data['pmax'] = pmax
            if parse_sticky_items:
                data['parse_sticky_items'] = parse_sticky_items
            if optional:
                data = {**data, **optional}

            resp = self._get(f'market/{category}', params=data)
        else:
            resp = self._get('market')

        return [Item.parse_obj(i) for i in resp["items"]], resp

    def market_fave(self) -> dict:
        """
        Получить свои избранные товары
        :return: dict
        """
        return self._get(f'market/fave')

    def market_viewed(self) -> [Item, dict]:
        """
        Получить свои просмотренные товары.
        :return:
        """
        resp = self._get(f'market/viewed')
        return [Item.parse_obj(i) for i in resp["items"]], resp

    def market_item(self, item: int) -> Item:
        """
        Показывает информацию об аккаунте на маркете.
        :param item: Item ID
        :return:
        """
        return Item.parse_obj(self._get(f'market/{item}'))

    def market_reserve(self, item: int, price: int = None) -> dict:
        """
        Резервирует аккаунт.
        :param item: ID аккаунта
        :param price: Ваша Цена за аккаунт, по умолчанию указанная цена
        :return:
        """
        price = price if price is not None else (self.market_item(item)).price
        return self._post(f'market/{item}/reserve', data={'price': price})

    def market_cancel_reserve(self, item: int) -> dict:
        """
        Отменяет резерв аккаунта.
        :param item: ID аккаунта
        :return:
        """
        return self._post(f'market/{item}/cancel-reserve')

    def market_check_account(self, item: int) -> dict:
        """
        Проверяет аккаунт.
        :param item: ID аккаунта
        :return:
        """
        return self._post(f'market/{item}/check-account')

    def market_confirm_buy(self, item: int) -> dict:
        """
        Подтверждение покупки.
        :param item: ID аккаунта
        :return:
        """
        return self._post(f'market/{item}/confirm-buy')

    def market_fast_buy(self, item: int) -> dict:
        """
        Автоматическая проверка и покупка аккаунта.
        :param item: ID аккаунта
        :return:
        """
        return self._post(f'market/{item}/fast-buy')

    def market_get_email(self, item: int, email: str):
        """
        Получить код подтверждения с почты маркета.
        :param item: ID аккаунта
        :param email: Почта аккаунта
        :return:
        """
        return self._get(f'market/{item}/email-code', {'email': email})

    def market_refuse_guarantee(self, item: int) -> dict:
        """
        Отказаться от гарантии.
        :param item: ID Аккаунта
        :return: dict
        """
        return self._post(f'market/{item}/refuse-guarantee')

    def market_change_password(self, item: int) -> dict:
        """
        Изменить пароль аккаунта.
        :param item: ID аккаунта
        :return:
        """
        return self._post(f'market/{item}/change-password')

    def market_delete(self, item: int, reason: str):
        """
        Удалить свой аккаунт с маркета.
        :param item: ID аккаунта
        :param reason: Причина удаления
        :return:
        """
        return self._delete(f'market/{item}/delete', {'reason': reason})

    def market_bump(self, item: int):
        """
        Поднять аккаунт.
        :param item: ID аккаунта
        :return:
        """
        return self._post(f'market/{item}/bump')
