import pandas as pd
import requests
import json

from pyti.smoothed_moving_average import smoothed_moving_average as sma # pyti is a library for technical indicators

from plotly.offline import plot
import plotly.graph_objs as go


class TradingModel:

    def __init__(self, symbol):
        self.symbol = symbol # holds all the properties and methods needed for the trading bot
        self.df = self.getData()

    def getData(self):
        # define url
        base = 'https://api.binance.com' # get data from binance api
        endpoint = '/api/v1/klines' # candlestick data
        params = '?&symbol='+self.symbol+'&interval=1h' # specify the sumbol that we're looking for ( BTC/USD ) and the length/interval of candlestick (i.e. 1hr)

        url = base + endpoint + params

        # dowload data
        data = requests.get(url)
        dictionary = json.loads(data.text)

        # put in dataframe and clean-up
        df = pd.DataFrame.from_dict(dictionary) # getting data
        df = df.drop(range(6, 12), axis=1) # drop colums 6-12

        # rename columns
        col_names = ['time', 'open', 'high', 'low', 'close', 'volume'] # rename remaining columns
        df.columns = col_names

        # transform values from strings to floats
        for col in col_names:
            df[col] = df[col].astype(float)

        # add the moving averages
        df['fast_sma'] = sma(df['close'].tolist(), 10) # using the smoothed_moving_average function provided by pyti
        df['slow_sma'] = sma(df['close'].tolist(), 30)



        # print(df) # testing

        return(df)

    def strategy(self):
        df = self.df

        buy_signals = []
        for i in range(1, len(df['close'])): # looking through all the candlesticks
            if df['slow_sma'][i] > df['low'][i] and (df['slow_sma'][i] - df['low'][i]) > 0.03 * df['low'][i]:
                # if slow_sma - low_price > 3% of low_price: buy
                buy_signals.append([df['time'][i], df['low'][i]]) # placing all the buy signals in a list (time and price) which we're then going to plot
        
        self.plotData(buy_signals = buy_signals)


    def plotData(self, buy_signals = False):
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

        # plot MAs as curves
        fsma = go.Scatter(
            x = df['time'],
            y = df['fast_sma'],
            name = 'Fast SMA',
            line = dict(color = ('rgba(102, 207, 255, 50)'))
        )


        ssma = go.Scatter(
            x = df['time'],
            y = df['slow_sma'],
            name = 'Slow SMA',
            line = dict(color = ('rgba(255, 207, 102, 50)'))
        )

        data = [candle, ssma, fsma]

        if buy_signals:
            buys = go.Scatter(
                x = [item[0] for item in buy_signals], # on the x axis we have the time
                y = [item[1] for item in buy_signals], # on the y axis we have the buying price
                name = 'Buy Signals',
                mode = 'markers'
            )

            sells = go.Scatter(
                x = [item[0] for item in buy_signals], # on the x axis we have the time
                # we'll sell at 2% over our buying price
                y = [item[1]*1.02 for item in buy_signals], # on the y axis we have the buying price
                name = 'Sell Signals',
                mode = 'markers'
            )
            data = [candle, ssma, fsma, buys, sells]

        # style and display
        layout = go.Layout(title = self.symbol)
        fig = go.Figure(data = data, layout = layout)

        plot(fig, filename=self.symbol)

    

def Main():
    symbol = 'BTCUSDT'
    model = TradingModel(symbol)
    model.strategy()

if __name__ == '__main__':
    Main()

