import pandas as pd
import requests
import json

from pyti.smoothed_moving_average import smoothed_moving_average as sma # pyti is a library for technical indicators
from pyti.bollinger_bands import lower_bollinger_band as lbb

from plotly.offline import plot
import plotly.graph_objs as go

from Binance import Binance

class TradingModel:

    def __init__(self, symbol, timeframe:str='4h'):
        self.symbol = symbol # holds all the properties and methods needed for the trading bot
        self.timeframe = timeframe
        self.exchange = Binance()
        self.df = self.exchange.GetSymbolData(symbol, timeframe)
        self.last_price = self.df['close'][len(self.df['close'])-1]
        # self.buy_signals = []

        try:
            # add the moving averages
            self.df['fast_sma'] = sma(self.df['close'].tolist(), 10) # using the smoothed_moving_average function provided by pyti
            self.df['slow_sma'] = sma(self.df['close'].tolist(), 30)
            self.df['low_boll'] = lbb(self.df['close'].tolist(), 14)
        except Exception as e:
            print(" Exception raised when trying to compute indicators on "+self.symbol)
            print(e)
            return None

    # def getData(self):
    #     # define url
    #     base = 'https://api.binance.com' # get data from binance api
    #     endpoint = '/api/v1/klines' # candlestick data
    #     params = '?&symbol='+self.symbol+'&interval=1h' # specify the sumbol that we're looking for ( BTC/USD ) and the length/interval of candlestick (i.e. 1hr)

    #     url = base + endpoint + params

    #     # dowload data
    #     data = requests.get(url)
    #     dictionary = json.loads(data.text)

    #     # put in dataframe and clean-up
    #     df = pd.DataFrame.from_dict(dictionary) # getting data
    #     df = df.drop(range(6, 12), axis=1) # drop colums 6-12

    #     # rename columns
    #     col_names = ['time', 'open', 'high', 'low', 'close', 'volume'] # rename remaining columns
    #     df.columns = col_names

    #     # transform values from strings to floats
    #     for col in col_names:
    #         df[col] = df[col].astype(float)

    #     # add the moving averages
    #     df['fast_sma'] = sma(df['close'].tolist(), 10) # using the smoothed_moving_average function provided by pyti
    #     df['slow_sma'] = sma(df['close'].tolist(), 30)



    #     # print(df) # testing

    #     return(df)

    # def strategy(self):
    #     '''If Price is 3% below Slow Moving Average, then Buy
	# 	Put selling order for 2% above buying price'''

    #     df = self.df

    #     buy_signals = []

    #     for i in range(1, len(df['close'])): # looking through all the candlesticks
    #         if df['slow_sma'][i] > df['low'][i] and (df['slow_sma'][i] - df['low'][i]) > 0.03 * df['low'][i]:
    #             # if slow_sma - low_price > 3% of low_price: buy
    #             buy_signals.append([df['time'][i], df['low'][i]]) # placing all the buy signals in a list (time and price) which we're then going to plot
        
    #     self.plotData(buy_signals = buy_signals)


    def plotData(self, buy_signals = False, sell_signals = False, plot_title:str="", indicators=[]):
        df = self.df

        # plot candlestick chart
        candle = go.Candlestick(
            x = df['time'],
            open = df['open'],
            close = df['close'],
            high = df['high'],
            low = df['low'],
            name = 'Candlesticks'
        )
        
        data = [candle]

        if indicators.__contains__('fast_sma')
        # plot MAs

        # plot MAs as curves
            fsma = go.Scatter(
                x = df['time'],
                y = df['fast_sma'],
                name = 'Fast SMA',
                line = dict(color = ('rgba(102, 207, 255, 50)'))
            )
            data.append(fsma)

        if indicators.__contains__('slow_sma')
            ssma = go.Scatter(
                x = df['time'],
                y = df['slow_sma'],
                name = 'Slow SMA',
                line = dict(color = ('rgba(255, 207, 102, 50)'))
            )
            data.append(ssma)

        if indicators.__contains__('low_boll')
            lowbb = go.Scatter(
                x = df['time'],
                y = df['low_boll'],
                name = 'Lower Bollinger Band',
                line = dict(color = ('rgba(255, 102, 207, 50)'))
            )
            data.append(lowbb)

        data = [candle, ssma, fsma, lowbb]

        if buy_signals:
            buys = go.Scatter(
                x = [item[0] for item in buy_signals], # on the x axis we have the time
                y = [item[1] for item in buy_signals], # on the y axis we have the buying price
                name = 'Buy Signals',
                mode = 'markers',
                marker_size = 20
            )
            data.append(buys)

        if sell_signals:
            sells = go.Scatter(
                x = [item[0] for item in sell_signals], # on the x axis we have the time
                # we'll sell at 2% over our buying price
                y = [item[1] for item in sell_signals], # on the y axis we have the buying price
                name = 'Sell Signals',
                mode = 'markers'
            )
            data.append(sells)

        # style and display
        layout = go.Layout(title=plot_title)
        fig = go.Figure(data = data, layout = layout)

        plot(fig, filename='graphs/'+plot_title+'.html')

#     def maStrategy(self, i:int):
#         # if price is 10% below the Slow MA, put a Buy Signal Return True

#         df = self.df
#         buy_price = 0.8 * df['slow_sma'][i]
#         if buy_price >= df['close'][i]:
#             self.buy_signals.append([df['time'][i], df['close'][i], df['close'][i] * 1.045])
#             return True

#         return False

#     def bollStrategy(self, i:int):
#         # if price is 5% below the Lower Bollinger Band, return True

#         df = self.df
#         buy_price = 0.98 * df['low_boll'][i]
#         if buy_price >= df['close'][i]:
#             self.buy_signals.append([df['time'][i], df['close'][i], df['close'][i] * 1.045])
#             return True

#         return False

    

# def Main():
#     # symbol = 'BTCUSDT'
#     # model = TradingModel(symbol)
#     # model.strategy()
#     exchange = Binance()

#     symbols = exchange.getTradingSymbols()

#     for symbol in symbols:

#         print(symbol)

#         model = TradingModel(symbol)

#         plot = False

#         # if model.maStrategy(len(model.df['close'])-1):
#         #     print(" MA Strategy match on " +symbol)
#         #     plot = True

#         if model.bollStrategy(len(model.df['close'])-1):
#             print(" Boll Strategy match on " +symbol)
#             plot = True

#         if plot:
#             model.plotData()

# if __name__ == '__main__':
#     Main()

