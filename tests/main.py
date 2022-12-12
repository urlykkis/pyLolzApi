from pylolzapi import LZTApi
from time import sleep

api = LZTApi("123")
sleep(2)
print(api.market_payments())
