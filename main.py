import requests
import websocket
from datetime import datetime
prevprice = 0
def roundfun(number):
    number = round(float(number), 2)
    return number
symbol = input("What is the symbol you want to lookup? ").upper()
action = input("What operation would you like to perfom? ")
if action == 'help':
    print('''
    Type \"info\" for current price and high + low
    Type \"live\" for live updates
    Type \"help\" for help (duh)
    ''')
if action == 'info':
    try:    
        print('The price of '+(eval(requests.get("https://finnhub.io/api/v1/stock/profile2?symbol="+symbol+"&token=c5resoqad3ifnpn51ou0").text))['name']+' is $'+str(roundfun((eval(requests.get("https://finnhub.io/api/v1/quote?symbol="+symbol+"&token=c5resoqad3ifnpn51ou0").text))['c']))+' USD')
        print('The daily high of '+(eval(requests.get("https://finnhub.io/api/v1/stock/profile2?symbol="+symbol+"&token=c5resoqad3ifnpn51ou0").text))['name']+' is $'+str(roundfun((eval(requests.get("https://finnhub.io/api/v1/quote?symbol="+symbol+"&token=c5resoqad3ifnpn51ou0").text))['h']))+ ' USD')
        print('The daily low of '+(eval(requests.get("https://finnhub.io/api/v1/stock/profile2?symbol="+symbol+"&token=c5resoqad3ifnpn51ou0").text))['name']+' is $'+str(roundfun((eval(requests.get("https://finnhub.io/api/v1/quote?symbol="+symbol+"&token=c5resoqad3ifnpn51ou0").text))['l']))+ ' USD')
    except:    
        print("That Symbol does not exist, please try again")  
    print('\r')

if action == 'live':
    def on_message(ws, message):
        message = eval(message)
        global prevprice
        for i in range(int(len(message['data']))):
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")    
            currentprice = roundfun(message['data'][i]['p'])
            print("Trade recieved at "+str(current_time))
            print("Price is now "+str(roundfun(message['data'][i]['p'])))
            print("Price changed "+str(roundfun(currentprice-prevprice)))
            prevprice = currentprice
            print('\r')

    def on_error(ws, error):
        print(error)

    def on_close(ws):
        print("### closed ###")

    def on_open(ws):
        ws.send('{"type":"subscribe","symbol":"'+symbol+'"}')

    if __name__ == "__main__":
        websocket.enableTrace(False)
        ws = websocket.WebSocketApp("wss://ws.finnhub.io?token=c5resoqad3ifnpn51ou0",
            on_message = on_message,
            # on_error = on_error,
            on_close = on_close)
        ws.on_open = on_open
        ws.run_forever()
