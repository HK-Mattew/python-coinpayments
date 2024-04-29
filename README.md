# Sync and AsyncIO CoinPayments Client

Before use, it is advisable to familiarize yourself with the official CoinPayments documentation (https://www.coinpayments.net/apidoc). The application implements the interaction protocol described in this document.

## Installation

```
pip install git+https://github.com/HK-Mattew/python-coinpayments.git
```

## Usage example without AsyncIO

```python
from coinpayments import CoinPayments


coinp = CoinPayments(
    public_key='<your-public-key>',
    private_key='<your-private-key>'
)


result = coinp.coinpayments(
    data={
        'cmd': 'balances'
    },
    method='POST'
    )


print(result)
```

## Example of use with AsyncIO

```python
from coinpayments import CoinPaymentsAsyncIO
import asyncio



async def main():

    coinp = CoinPaymentsAsyncIO(
        public_key='<your-public-key>',
        private_key='<your-private-key>'
    )


    result = await coinp.coinpayments(
        data={
            'cmd': 'balances'
        },
        method='POST'
        )


    print(result)



if __name__ == "__main__":
    asyncio.run(main())
```
