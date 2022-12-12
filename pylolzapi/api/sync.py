from __future__ import annotations

import requests
import json
import types

from datetime import datetime

from .base import BaseLolzAPI
from pylolzapi.utils.exceptions import LolzAPIError


class LZTApi(BaseLolzAPI):
    def __init__(self, token: str = None, client_id: str = None,
                 client_secret: str = None, scope: list[str] = None):
        super(LZTApi, self).__init__(token, client_id, client_secret, scope)
        self._session = requests.session()
        self._session.headers = {"Authorization": f"Bearer {self._token}"}

        self.user_info: types.User = self.me()

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

        return self.__request(self._session.get, self._base_url + url, params=params).json()

    def _post(self, url: str, data=None) -> dict:
        if data is None:
            data = dict()

        return self.__request(self._session.post, self._base_url + url, data=data).json()

    def _delete(self, url: str, data=None) -> dict:
        if data is None:
            data = dict()

        return self.__request(self._session.delete, self._base_url + url, data=data).json()

    def me(self) -> types.User:
        """Отображает информацию о вашем профиле."""
        return types.User.parse_obj(self._get("users/me")["user"])


    def market_fave(self) -> dict:
        """Получить свои избранные товары."""
        return self._get(f'market/fave')

    def market_viewed(self) -> [types.Item, dict]:
        """Получить свои просмотренные товары."""
        resp = self._get(f'market/viewed')
        return [types.Item.parse_obj(i) for i in resp["items"]], resp

    def market_item(self, item: int) -> types.Item:
        """
        Показывает информацию об аккаунте на маркете.
        :param item: Item ID
        """
        return types.Item.parse_obj(self._get(f'market/{item}'))

    def market_reserve(self, item: int, price: int = None) -> dict:
        """
        Резервирует аккаунт.
        :param item: ID аккаунта
        :param price: Ваша Цена за аккаунт, по умолчанию указанная цена
        """
        price = price if price is not None else (self.market_item(item)).price
        return self._post(f'market/{item}/reserve', data={'price': price})

    def market_cancel_reserve(self, item: int) -> dict:
        """
        Отменяет резерв аккаунта.
        :param item: ID аккаунта
        """
        return self._post(f'market/{item}/cancel-reserve')

    def market_check_account(self, item: int) -> dict:
        """
        Проверяет аккаунт.
        :param item: ID аккаунта
        """
        return self._post(f'market/{item}/check-account')

    def market_confirm_buy(self, item: int) -> dict:
        """
        Подтверждение покупки.
        :param item: ID аккаунта
        """
        return self._post(f'market/{item}/confirm-buy')

    def market_fast_buy(self, item: int) -> dict:
        """
        Автоматическая проверка и покупка аккаунта.
        :param item: ID аккаунта
        """
        return self._post(f'market/{item}/fast-buy')

    def market_get_email(self, item: int, email: str):
        """
        Получить код подтверждения с почты маркета.
        :param item: ID аккаунта
        :param email: Почта аккаунта
        """
        return self._get(f'market/{item}/email-code', params={'email': email})

    def market_refuse_guarantee(self, item: int) -> dict:
        """
        Отказаться от гарантии.
        :param item: ID Аккаунта
        """
        return self._post(f'market/{item}/refuse-guarantee')

    def market_change_password(self, item: int) -> dict:
        """
        Изменить пароль аккаунта.
        :param item: ID аккаунта
        """
        return self._post(f'market/{item}/change-password')

    def market_delete(self, item: int, reason: str):
        """
        Удалить свой аккаунт с маркета.
        :param item: ID аккаунта
        :param reason: Причина удаления
        """
        return self._delete(f'market/{item}/delete', data={'reason': reason})

    def market_bump(self, item: int):
        """
        Поднять аккаунт.
        :param item: ID аккаунта
        """
        return self._post(f'market/{item}/bump')

    def market_payments(self, payment_type: str = None, pmin: int = None, pmax: int = None, receiver: str = None,
                        sender: str = None, start_date: datetime = None, end_date: datetime = None, wallet: str = None,
                        comment: str = None, is_hold: str = None) -> tuple[list[types.Operation], dict]:
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
        """
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

        resp = self._get(f'market/user/{self.user_info.user_id}/payments', params=data)

        return [types.Operation.parse_obj(resp["payments"][operation]) for operation in resp["payments"]], resp

    def market_list(self, category: str = None, pmin: int = None, pmax: int = None, title: str = None,
                    parse_sticky_items: str = None, optional: dict = None) -> tuple[list[types.Item], dict]:
        """
        Получить все последние аккаунты маркета.
        :param category: Категория на маркете
        :param pmin: Минимальная цена для аккаунта
        :param pmax: Максимальная цена для аккаунта
        :param title: Название аккаунта
        :param parse_sticky_items: Условие для разбора параметров
        :param optional: Получить параметры URL-адреса из market
        """
        if category:
            data = dict()

            if title: data['title'] = title
            if pmin: data['pmin'] = pmin
            if pmax: data['pmax'] = pmax
            if parse_sticky_items: data['parse_sticky_items'] = parse_sticky_items
            if optional: data = {**data, **optional}

            resp = self._get(f'market/{category}', params=data)
        else:
            resp = self._get('market')

        return [types.Item.parse_obj(i) for i in resp["items"]], resp

    def market_transfer(self, receiver: int, receiver_username: str, amount: int, secret_answer: str,
                        currency: str = 'rub', comment: str = None, transfer_hold: str = None,
                        hold_length_value: str = None, hold_length_option: int = None):
        data = {
            'user_id': receiver,
            'username': receiver_username,
            'amount': amount,
            'secret_answer': secret_answer,
            'currency': currency
        }
        if comment: data['comment'] = comment
        if transfer_hold: data['transfer_hold'] = transfer_hold
        if hold_length_value: data['hold_length_value'] = hold_length_value
        if hold_length_option: data['hold_length_option'] = hold_length_option

        return self._post('market/balance/transfer', data=data)

    def market_category_params(self, category_name: str):
        """
        Отображает параметры поиска для категории
        :param category_name: Название категории
        """
        return self._get(f'market/{category_name}/params')

    def market_category_games(self, category_name: str):
        """
        Отображает список игр в категории
        :param category_name: Название категории
        """
        return self._get(f'market/{category_name}/games')

    def market_add_item(self, title: str, price: int, category_id: int, item_origin: str, extended_guarantee: int,
                        currency: str = 'rub', title_en: str = None, description: str = None, information: str = None,
                        has_email_login_data: bool = None, email_login_data: str = None, email_type: str = None,
                        allow_ask_discount: bool = None, proxy_id: int = None) -> dict:
        """
        Добавляет аккаунт на маркет.
        :param title: Название
        :param price: Цена
        :param category_id: Идентификатор категории (MarketCategories)
        :param item_origin: Происхождение аккаунта (brute, fishing, stealer, autoreg, personal, resale)
        :param extended_guarantee: Срок гарантии (-1 (12 hours), 0 (24 hours), 1 (3 days))
        :param currency: Валюта (cny, usd, rub, eur, uah, kzt, byn, gbp)
        :param title_en: Название на английском.
        :param description: Информация об аккаунта
        :param information: Приватная информация для покупателя.
        :param has_email_login_data:
        :param email_login_data: логин:пароль
        :param email_type: собственный или авторег
        :param allow_ask_discount: разрешить запрашивать скидку для пользователей.
        :param proxy_id: идентификатор прокси-сервера
        """

        data = {
            'title': title,
            'price': price,
            'category_id': category_id,
            'currency': currency,
            'item_origin': item_origin,
            'extended_guarantee': extended_guarantee
        }

        if title_en: data['title_en'] = title_en
        if description: data['description'] = description
        if information: data['information'] = information
        if has_email_login_data: data['has_email_login_data'] = has_email_login_data
        if email_login_data: data['email_login_data'] = email_login_data
        if email_type: data['email_type'] = email_type
        if allow_ask_discount: data['allow_ask_discount'] = allow_ask_discount
        if proxy_id: data['proxy_id'] = proxy_id

        return self._post('market/item/add', data=data)

    def market_add_item_check(self, item: int, login: str = None, password: str = None,
                              log_pass: str = None, close_item: bool = None) -> dict:
        """
        Проверьте аккаунт на действительность. Если он действителен, аккаунт будет опубликован на маркете.
        :param item: ID Item
        :param login: Логин
        :param password: Пароль
        :param log_pass: Логин:Пароль
        :param close_item: Закрыть аккаунт.
        """
        data = dict()

        if login: data['login'] = login
        if password: data['password'] = password
        if log_pass: data['loginpassword'] = log_pass
        if close_item: data['close_item'] = close_item

        return self._post(f'market/{item}/goods/check', data=data)
