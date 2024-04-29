from urllib.parse import urlencode
from typing import Literal
import hashlib
import httpx
import hmac




class CoinPayments():
    def __init__(self, public_key: str, private_key: str, version: int = 1):
        self.__PUBLIC_KEY = public_key
        self.__PRIVATE_KEY = private_key
        self.__VERSION = version
        self.__BASE_ENDPOINT = 'https://www.coinpayments.net/api.php'


    def __gen_hmac(self, data: dict) -> str:
        return hmac.new(
            bytes(self.__PRIVATE_KEY, 'utf-8'),
            urlencode(data).encode('utf-8'),
            hashlib.sha512
        ).hexdigest()


    def __request_api(self, data: dict, method: Literal['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS']):
        
        data.update({
            'cmd': data.get('cmd'),
            'key': self.__PUBLIC_KEY,
            'version': self.__VERSION,
            'format': 'json'
        })

        hmac_signature = self.__gen_hmac(data)

        with httpx.Client() as client:
            response = getattr(client, method.lower())(
                url=self.__BASE_ENDPOINT,
                data=data,
                headers={'hmac': hmac_signature}
            )

            return response.json()


    def coinpayments(self, data: dict, method: Literal['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS'] = 'POST'):
        return self.__request_api(data, method)



