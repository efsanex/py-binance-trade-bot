from binance.client import Client
import time
import requests
import math

binance = Client('+api+', '+secret+')
tumFiyatlar = binance.get_all_tickers()
coinler = []

def fiyatBul(sym):
    count = 0
    for i in tumFiyatlar:
        count += 1
        ticker = i.get('symbol')
        if ticker == sym:
            val = i.get('price')
            count = count-1
            return count


def do():
    coinler = []
    coinGetir = binance.get_account()
    for i in range(0, len(coinGetir['balances'])): 
        if(float(coinGetir['balances'][i]['free']) > 0):
            if(float(coinGetir['balances'][i]['free']) > 0.2):
                coinler.append(coinGetir['balances'][i]['asset']+'USDT')
                if(coinGetir['balances'][i]['asset'] == 'USDT'):
                    coinler.remove('USDTUSDT')
                else:
                    tekLimit(coinGetir['balances'][i]['asset']+'USDT')
                
def tekLimit(sembol):
    orderS = binance.get_all_orders(symbol=sembol, limit=1)
    if(orderS[0]['type'] == 'MARKET'):
        coinName = orderS[0]['symbol'].replace("USDT", "")
        minSatmaOranı = binance.get_symbol_info(orderS[0]['symbol'])
        minSatmaOranı = float(minSatmaOranı['filters'][2]['minQty'])
        satınAlmaGecmisi = binance.get_my_trades(symbol=orderS[0]['symbol'], limit=1)
        if(satınAlmaGecmisi[0]['isBuyer'] == True):
            alınanMiktar = float(satınAlmaGecmisi[0]['qty'])
            alımFiyatı = float(satınAlmaGecmisi[0]['price'])
            toplamFiyat = float(satınAlmaGecmisi[0]['quoteQty'])

            anlıkFiyat = float(tumFiyatlar[fiyatBul(orderS[0]['symbol'])].get('price'))
            toplamFiyatAnlık = anlıkFiyat * alınanMiktar

            yuzdeDegisim = float("{:.3f}".format(((anlıkFiyat - alımFiyatı) / anlıkFiyat) * 100))
            fiyatDeğişimi = float("{:.3f}".format(toplamFiyatAnlık - toplamFiyat))

            if(minSatmaOranı == 1.00000000):
                satılacakMiktar=round(alınanMiktar)
            if(minSatmaOranı == 0.10000000):
                virguldenSonra = 1
                satılacakMiktar= float("{:.1f}".format(alınanMiktar))
            if(minSatmaOranı == 0.01000000):
                virguldenSonra = 2
                satılacakMiktar=float("{:.2f}".format(alınanMiktar))
            if(minSatmaOranı == 0.00100000):
                virguldenSonra = 3
                satılacakMiktar=float("{:.3f}".format(alınanMiktar))
            if(minSatmaOranı == 0.00010000):
                virguldenSonra = 3
                satılacakMiktar=float("{:.4f}".format(alınanMiktar))
            if(minSatmaOranı == 0.00001000):
                virguldenSonra = 3
                satılacakMiktar=float("{:.5f}".format(alınanMiktar))
            if(minSatmaOranı == 0.00000100):
                virguldenSonra = 3
                satılacakMiktar=float("{:.6f}".format(alınanMiktar))
            
            sonuc = coinName+' % '+str(yuzdeDegisim)+' ve '+str(fiyatDeğişimi)+' dolar'
            print(sonuc)
            if(yuzdeDegisim > 4.5):
                order = binance.order_market_sell(symbol=sembol,quantity=satılacakMiktar)
                send_text = 'https://api.telegram.org/bot'+botToken+'/sendMessage?chat_id='+chatId+'&text='+sonuc
                response = requests.get(send_text)
        
if __name__ == "__main__":
    while True:
        tumFiyatlar = binance.get_all_tickers()
        do()
        time.sleep(15)
