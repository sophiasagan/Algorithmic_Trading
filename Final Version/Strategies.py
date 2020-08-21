class Strategies:

	@staticmethod
	def maStrategy(df, i:int):
		''' If price is 10% below the Slow MA, return True'''

		buy_price = 0.96 * df['slow_sma'][i]
		if buy_price >= df['close'][i]:
			return min(buy_price, df['high'][i])

		return False

	@staticmethod
	def bollStrategy(df, i:int):
		''' If price is 2.5% below the Lower Bollinger Band, return True'''

		buy_price = 0.975 * df['low_boll'][i]
		if buy_price >= df['close'][i]:
			return min(buy_price, df['high'][i])

		return False

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