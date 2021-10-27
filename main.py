import requests
import websocket
from datetime import datetime
from termcolor import colored
import matplotlib.pyplot as plt
import time
import numpy as np
from scipy.interpolate import splrep, splev
x = []
y = []
smoothness = 0
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
    Type \"graph\" to make a graph of prices for 1 minute
    Made by ItCameFr0mMars
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
            print("Trade recieved at "+str((datetime.now()).strftime("%H:%M:%S")))
            print("Price is now "+str(roundfun(message['data'][i]['p'])))
            if '-' in str(roundfun((roundfun(message['data'][i]['p']))-prevprice)):
                print(colored("Price changed "+str(roundfun((roundfun(message['data'][i]['p']))-prevprice)), 'red'))
            elif str(roundfun((roundfun(message['data'][i]['p']))-prevprice)) == '0.0':
                print(colored("Price changed "+str(roundfun((roundfun(message['data'][i]['p']))-prevprice)), 'white'))
            else:
                print(colored("Price changed "+str(roundfun((roundfun(message['data'][i]['p']))-prevprice)), 'green'))
            prevprice = roundfun(message['data'][i]['p'])
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
            on_error = on_error,
            on_close = on_close)
        ws.on_open = on_open
        ws.run_forever()
if action == 'graph':
    t_end = time.time() + 1
    while time.time() < t_end:
        # do whatever you do

        def on_message(ws, message):
            message = eval(message)
            global prevprice
            for i in range(int(len(message['data']))):
                y.append(message['data'][i]['p'])
                x.append(time.time())
            print('Time remaining until graph can be created '+str(round(t_end - time.time())))
            print('Number of price datapoints '+str(len(y)))     
            print('Smoothness factor '+str(round(len(y)/120)+3)) 
                 

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
                on_error = on_error,
                on_close = on_close
            )
                
            ws.on_open = on_open
            ws.run_forever()
    print('plotting now')
    plt.figure()
    bspl = splrep(x,y,s=(len(y)/120)+3)
    bspl_y = splev(x,bspl)
    #plt.plot(x,y)
    if y[0] < y[len(y)-1]:
        color = 'green'
    else:
        color = 'red'    
    plt.plot(x,bspl_y, color)
    plt.plot(x, y, 'orange', alpha=0.2)  

    # Colorcode the tick tabs and prevent scientific notation (bad)
    plt.ticklabel_format(useOffset=False)
    plt.tick_params(axis='x', colors='white')
    plt.tick_params(axis='y', colors=color)

    # Put the title and labels
    plt.title('Graph of '+symbol, color=color)
    plt.xlabel('time', color=color)
    plt.ylabel('price ($)', color=color)

    # Show the plot/image
    plt.tight_layout()
    plt.grid(alpha=0.8)
    plt.savefig("yeah it works.png")
    plt.show()
    print('done!')