from urllib.parse import urlencode
from typing import Literal
import hashlib
import httpx
import hmac




class CoinPaymentsAsyncIO():
    def __init__(self, public_key: str, private_key: str, version: int = 1):
        self.__PUBLIC_KEY = public_key
        self.__PRIVATE_KEY = private_key
        self.__VERSION = version
        self.__BASE_ENDPOINT = 'https://www.coinpayments.net/api.php'


    async def __gen_hmac(self, data: dict) -> str:
        return hmac.new(
            bytes(self.__PRIVATE_KEY, 'utf-8'),
            urlencode(data).encode('utf-8'),
            hashlib.sha512
        ).hexdigest()


    async def __request_api(self, data: dict, method: Literal['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS']):

        data.update({
            'cmd': data.get('cmd'),
            'key': self.__PUBLIC_KEY,
            'version': self.__VERSION,
            'format': 'json'
        })

        hmac_signature = await self.__gen_hmac(data)

        async with httpx.AsyncClient() as client:
            response = await getattr(client, method.lower())(
                url=self.__BASE_ENDPOINT,
                data=data,
                headers={'hmac': hmac_signature}
            )

            return response.json()


    async def coinpayments(self, data: dict, method: Literal['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS'] = 'POST'):
        return await self.__request_api(data, method)




