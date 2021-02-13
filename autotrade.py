import bybit
import settings
import sys, time

MARGIN = 0.0
SYMBOL = 'BTCUSD'
UNIT = 100
INTERVAL = 5

client = bybit.bybit(test=False, api_key=settings.API_KEY, api_secret=settings.SECRET_KEY)

while True:
    try:
        # get orderbook
        res = client.Market.Market_orderbook(symbol=SYMBOL).result()[0]['result']

        bidPrice = sys.maxsize
        askPrice = 0

        for val in res:
            if val['side'] == 'Buy':
                if askPrice < float(val['price']):
                    askPrice = float(val['price'])
            elif val['side'] == 'Sell':
                if bidPrice > float(val['price']):
                    bidPrice = float(val['price'])
        
        longPrice = askPrice - MARGIN
        shortPrice = bidPrice + MARGIN

        print(longPrice, shortPrice)

        # place order
        # long
        res = client.Order.Order_new(
            side='Buy', symbol=SYMBOL, order_type='Limit',
            qty=UNIT, price=longPrice, time_in_force='GoodTillCancel'
            ).result()
        
        print('--- long ---')
        print(res)

        #short
        res = client.Order.Order_new(
            side='Sell', symbol=SYMBOL, order_type='Limit',
            qty=UNIT, price=bidPrice, time_in_force='GoodTillCancel'       
        ).result()

        print('--- short ---')
        print(res)

        time.sleep(INTERVAL)
    except Exception as e:
        print(e)


