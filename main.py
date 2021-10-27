import requests
import websocket
from datetime import datetime
from termcolor import colored
import matplotlib.pyplot as plt
import time
import numpy as np
from scipy import interpolate
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
    x = []
    y = []
    t_end = time.time() + 10
    while time.time() < t_end:
        # do whatever you do
        def on_message(ws, message):
            message = eval(message)
            global prevprice
            for i in range(int(len(message['data']))):
                y.append(message['data'][i]['p'])
                x.append(time.time())
                print('appened '+str(i+1))
                

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
    print('plotting now')
    canvas = plt.figure()
    rect = canvas.patch
    rect.set_facecolor('white')    
    x_sm = np.asarray(x)
    y_sm = np.asarray(y)

    x_smooth = np.linspace(x_sm.min(), x_sm.max(), 200)
    y_smooth = interpolate.make_interp_spline(x, y, x_smooth, bc_type=None, axis=0, check_finite=True)

    # Define the matrix of 1x1 to place subplots
    # Placing the plot1 on 1x1 matrix, at pos 1
    sp1 = canvas.add_subplot(1,1,1, axisbg='w')
    #sp1.plot(x, y, 'red', linewidth=2)
    sp1.plot(x_smooth, y_smooth, 'red', linewidth=1)

    # Colorcode the tick tabs 
    sp1.tick_params(axis='x', colors='red')
    sp1.tick_params(axis='y', colors='red')

    # Colorcode the spine of the graph
    sp1.spines['bottom'].set_color('r')
    sp1.spines['top'].set_color('r')
    sp1.spines['left'].set_color('r')
    sp1.spines['right'].set_color('r')

    # Put the title and labels
    sp1.set_title('matplotlib example 1', color='red')
    sp1.set_xlabel('matplot x label', color='red')
    sp1.set_ylabel('matplot y label', color='red')

    # Show the plot/image
    plt.tight_layout()
    plt.grid(alpha=0.8)
    plt.savefig("example6.eps")
    plt.show()
    print('done!')   