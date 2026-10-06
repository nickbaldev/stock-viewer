def init_ticker_set():
    #function that creates a set of all the stock tickers
    symbols = set()
    with open('tickers.txt', 'r') as f:
        for line in f:
            symbols.add(line.strip())
    return symbols

def init_sorting_keys():
    #initilizes a list containing the keys for sorting the data lst by certain key of the dictionaries
    lst = [
        lambda x: x['symbol'], 
        lambda x: x['name'],
        lambda x: float(x['price'].replace(',', '')),
        lambda x: float(x['price_change'].replace(',','')),
        lambda x: float(x['percent_change'].strip('+()%').replace(',','')),
        lambda x: float(x['market_cap'].replace(',','').replace('T','e12').replace('B','e9').replace('M','e6')),
        lambda x: float(x['P/E']), 
        lambda x: float(x['EPS'])
    ]
    return lst