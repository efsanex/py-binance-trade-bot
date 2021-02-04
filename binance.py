from binance.client import Client
import time
import requests

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

def hesapla(anlıkFiyat, alımFiyat):
    degisim = ((anlıkFiyat - alımFiyat) / anlıkFiyat) * 100
    return degisim

def do():
    coinler = []
    coinGetir = binance.get_account()
    for i in range(0, len(coinGetir['balances'])): 
        if(float(coinGetir['balances'][i]['locked']) > 0):
            if(float(coinGetir['balances'][i]['locked']) > 1.0):
                coinler.append(coinGetir['balances'][i]['asset']+'USDT')
                if(coinGetir['balances'][i]['asset'] == 'USDT'):
                    coinler.remove('USDTUSDT')
                else:
                    stopLossVar(coinGetir['balances'][i]['asset']+'USDT')
            
        if(float(coinGetir['balances'][i]['free']) > 0):
            if(float(coinGetir['balances'][i]['free']) > 1.0):
                coinler.append(coinGetir['balances'][i]['asset']+'USDT')
                if(coinGetir['balances'][i]['asset'] == 'USDT'):
                    coinler.remove('USDTUSDT')
                else:
                    tekLimit(coinGetir['balances'][i]['asset']+'USDT')
                

def stopLossVar(sembol):
    orderS = binance.get_all_orders(symbol=sembol, limit=2)
    if(orderS[0]['type'] == 'MARKET'):
        alınanAdet = float(orderS[0]['executedQty'])
        toplamFiyat = float(orderS[0]['cummulativeQuoteQty'])
        almaFiyatı = toplamFiyat / alınanAdet
        anlıkFiyat = float(tumFiyatlar[fiyatBul(orderS[0]['symbol'])].get('price'))
        anlıkToplamFiyat = alınanAdet * anlıkFiyat
        
        fiyatDegisim_ = hesapla(float(anlıkFiyat),almaFiyatı)
        fiyatDegisim = '% ' +str(float("{:.3f}".format(fiyatDegisim_)))
        
        sonuc_ = toplamFiyat-anlıkToplamFiyat
        sonuc = str(float("{:.3f}".format(sonuc_)))
        
        if(almaFiyatı > anlıkFiyat):
            sonuc = ' | '+fiyatDegisim+' | '+ sonuc +' zarar'
            if(fiyatDegisim_ < -5):
                sonuc = ''
                sonuc = ' | '+fiyatDegisim + ' ZARAR | '+ str(float("{:.3f}".format(sonuc_))) +' dikkatli ol :)'
        if(anlıkFiyat > almaFiyatı):
            sonuc = ' | '+fiyatDegisim+' | '+ sonuc + ' KAR'

        send_text = 'https://api.telegram.org/bot+botToken+/sendMessage?chat_id='+chatId+'&text='+ orderS[0]['symbol'] + sonuc
        response = requests.get(send_text)
        print(sonuc)
        
    #if(orderS[1]['type'] == 'STOP_LOSS_LIMIT'):
    #    stoptakiAdet = float(orderS[1]['origQty'])
    #    almaFiyatı_ = toplamFiyat / stoptakiAdet
    #    anlıkFiyat_ = tumFiyatlar[fiyatBul(orderS[0]['symbol'])].get('price')
    #    print(stoptakiAdet)
    #    print(almaFiyatı_)
    #    print(anlıkFiyat_)

def tekLimit(sembol):
    orderS = binance.get_all_orders(symbol=sembol, limit=1)
    if(orderS[0]['type'] == 'MARKET'):
        alınanAdet = float(orderS[0]['executedQty'])
        toplamFiyat = float(orderS[0]['cummulativeQuoteQty'])
        almaFiyatı = toplamFiyat / alınanAdet
        anlıkFiyat = float(tumFiyatlar[fiyatBul(orderS[0]['symbol'])].get('price'))
        anlıkToplamFiyat = alınanAdet * anlıkFiyat
        
        fiyatDegisim_ = hesapla(float(anlıkFiyat),almaFiyatı)
        fiyatDegisim = '% ' +str(float("{:.3f}".format(fiyatDegisim_)))
        
        sonuc_ = anlıkToplamFiyat-toplamFiyat
        sonuc = str(float("{:.3f}".format(sonuc_)))
        
        if(almaFiyatı > anlıkFiyat):
            sonuc = ' | '+fiyatDegisim+' | '+ sonuc +' zarar'
            if(fiyatDegisim_ < -5):
                sonuc = ''
                sonuc = ' | '+fiyatDegisim + ' ZARAR | '+ str(float("{:.3f}".format(sonuc_))) +' dikkatli ol :)'
           
        if(anlıkFiyat > almaFiyatı):
            sonuc = ' | '+fiyatDegisim+' | '+ sonuc + ' KAR'
            if(fiyatDegisim_ > 9):
                orderZ = binance.order_market_sell(symbol=orderS[0]['symbol'],quantity=alınanAdet)
                print(orderZ)

        send_text = 'https://api.telegram.org/bot'+botToken+'/sendMessage?chat_id='+chatId+'&text='+ orderS[0]['symbol'] + sonuc
        response = requests.get(send_text)
        print(sonuc)
        

if __name__ == "__main__":
    while True:
        tumFiyatlar = binance.get_all_tickers()
        do()
        time.sleep(15)
