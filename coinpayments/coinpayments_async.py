from .helpers.encoders import http_data_encoder_for_php
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
            http_data_encoder_for_php(data).encode('utf-8'),
            hashlib.sha512
        ).hexdigest()


    async def __request_api(self, data: dict, method: Literal['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS']):

        if not 'cmd' in data:
            raise ValueError('The field `cmd` is mandatory when requesting the API')


        data.update({
            'key': self.__PUBLIC_KEY,
            'version': self.__VERSION,
            'format': 'json'
        })

        hmac_signature = await self.__gen_hmac(data)

        content = http_data_encoder_for_php(data).encode('utf-8')

        content_length = str(len(content))
        content_type = "application/x-www-form-urlencoded"

        headers = {
            'Content-Length': content_length,
            'Content-Type': content_type,
            'hmac': hmac_signature
            }

        async with httpx.AsyncClient() as client:
            response = await getattr(client, method.lower())(
                url=self.__BASE_ENDPOINT,
                content=content,
                headers=headers
            )

            return response.json()


    async def coinpayments(self, data: dict, method: Literal['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS'] = 'POST'):
        return await self.__request_api(data, method)




