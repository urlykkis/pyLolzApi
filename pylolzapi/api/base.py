import urllib.parse


class BaseAPI:
    def __init__(self, token: str = None, client_id: str = None,
                 client_secret: str = None, scope: list[str] = None):
        """
        https://zelenka.guru/account/api
        :param token: Токен
        :param client_id: Client ID (Временно не работает)
        :param client_secret: Client Secret (Временно не работает)
        :param scope: Разрешения (Временно не работает)
        """
        self.__token = token
        self._client_id = client_id
        self._client_secret = client_secret
        self._scope = "+".join(scope) if scope is not None else ""
        self._base_url = "https://api.zelenka.guru/"

    @property
    def _token(self):
        return self.__token

    @property
    def scopes(self):
        return self._scope

    @property
    def client_id(self):
        return self._client_id

    @_token.setter
    def _token(self, token):
        self.__token = token

    @staticmethod
    def transfer(username: str, amount: int = None, comment: str = None, hold: bool = None):
        """
        Создает ссылку для перевода денег.
        :param username: Ник пользователя
        :param amount:  Сумма
        :param comment: Комментарий
        :param hold: Задержать перевод
        :return:
        """
        url = f"https://zelenka.guru/market/balance/transfer?username={username}"

        if amount: url += f"&amount={amount}"
        if hold is not None:  url += f"&hold={0 if hold is False else 1}"
        if comment:
            comment = urllib.parse.quote(comment)
            url += f"&comment={comment}"

        return url
