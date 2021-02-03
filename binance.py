from binance.client import Client
import time
import requests

binance = Client('api_', 'secret_')
gt = binance.get_server_time()

tumFiyatlar = binance.get_all_tickers()

def fiyatBul(sym):
    count = 0
    for i in tumFiyatlar:
        count += 1
        ticker = i.get('symbol')
        if ticker == sym:
            val = i.get('price')
            count = count-1
            return count

def hesapla(anlıkFiyat, alımFiyat):
    #degisim = (alımFiyat * 100) / anlıkFiyat
    degisim = ((anlıkFiyat - alımFiyat) / anlıkFiyat) * 100
    #sonuc = 100 - degisim
    return degisim

def do():
    
    coinler = []
    coinGetir = binance.get_account()
    
    for i in range(0, len(coinGetir['balances'])): 
        adet = float(coinGetir['balances'][i]['free'])
        if(adet > 1):
            coinler.append(coinGetir['balances'][i]['asset']+'USDT')

    coinler.remove('USDTUSDT')

    for i in range(0, len(coinler)): 

        alınanlar = binance.get_all_orders(symbol=coinler[i], limit=1)
        adet = float(alınanlar[0]['executedQty'])
        fiyat = float(alınanlar[0]['cummulativeQuoteQty']) / adet

        coinFiyat = tumFiyatlar[fiyatBul(coinler[i])].get('price')

        fiyatDegisim_ = hesapla(float(coinFiyat),fiyat)
        fiyatDegisim = '% ' +str(float("{:.3f}".format(fiyatDegisim_)))

        almaFiyatı = float(alınanlar[0]['cummulativeQuoteQty'])
        anlıkFiyat = float(adet * float(coinFiyat))

        sonuc_ = anlıkFiyat-almaFiyatı
        sonuc = str(float("{:.3f}".format(sonuc_)))

        if(almaFiyatı > anlıkFiyat):
            sonuc = sonuc + ' dolar zarar'
        if(anlıkFiyat > almaFiyatı):
            sonuc = sonuc + ' dolar kar'
        if(fiyatDegisim_ < -5):
            sonuc = 'dikkatli ol :)'

        send_text = 'https://api.telegram.org/bot'+bot_token+'/sendMessage?chat_id='+chat_id+'&text='+ coinler[i] +' -> '+ fiyatDegisim + ' -> '+sonuc
        response = requests.get(send_text)
        print(almaFiyatı)
        print(anlıkFiyat)

if __name__ == "__main__":
    while True:
        tumFiyatlar = binance.get_all_tickers()
        do()
        time.sleep(62)
