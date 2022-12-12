from pylolzapi import LZTApi
from time import sleep

api = LZTApi("c2621f0d632cb31e2222e3f91608a270d2d218c3")
sleep(5)
s = api.market_item(44333914)
print(s)
