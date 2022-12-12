from __future__ import annotations


class BaseLolzAPI:
    def __init__(self,
                 token: str = None,
                 client_id: str = None,
                 client_secret: str = None,
                 scope: list[str] = None,
                 ) -> BaseLolzAPI:
        """

        :param token: Token
        :param client_id: Client APP Id
        :param client_secret: Client APP Secret Key
        :param scope: Scopes
        :param verify_token: True
        """
        self._token = token
        self._client_id = client_id
        self._client_secret = client_secret
        self._scope = "+".join(scope) if scope is not None else ""
        self._base_url = "https://api.zelenka.guru/"

    @property
    def token(self):
        return self._token

    @property
    def scopes(self):
        return self._scope

    @property
    def client_id(self):
        return self._client_id

    @token.setter
    def token(self, token):
        self._token = token
