import requests
from bs4 import BeautifulSoup
import requests_cache
import re

#This files contains the functions for scraping the data

def scrape_data(stock):
    #scrapes the HTML content from yahoo finance for a given stock
    header = {'User-Agent':'Mozilla/5.0'}
    requests_cache.install_cache('yahoo_cache', expire_after=5)
    url = "https://finance.yahoo.com/quote/" + stock + "/"
    r = requests.get(url, headers=header)
    return r.text

def get_stock_data(content, stock):
    #extracts the specific data values for a stock from the HTML and store them in a dict
    soup = BeautifulSoup(content, 'html.parser')
    
    name = soup.find('h1', class_='yf-xxbei9')
    name = re.sub(r'\s*\([^)]*\)$', '', name.text).strip() #regex substitution to get rid of the garbage after the name
    price = soup.find("span", attrs={'data-testid': 'qsp-price'})
    price_change = soup.find("span", attrs={'data-testid': 'qsp-price-change'})
    percent_change = soup.find("span", attrs={'data-testid': 'qsp-price-change-percent'})
    market_cap = soup.find("fin-streamer", attrs={'data-field': 'marketCap'})
    trailingPE = soup.find_all('fin-streamer', {'data-field': 'trailingPE'})

    if not (name and price and price_change and percent_change and market_cap and len(trailingPE) >= 2):
        return {}

    price_to_earnings_ratio = trailingPE[0]['data-value']
    earnings_per_share = trailingPE[1]['data-value']

    stock_data = {}
    if name and price and price_change and percent_change and market_cap and trailingPE:
        stock_data['symbol'] = stock
        stock_data['name'] = name
        stock_data['price'] = price.text.strip()
        stock_data['price_change'] = price_change.text.strip()
        stock_data['percent_change'] = percent_change.text.strip()
        stock_data['market_cap'] = market_cap.text.strip()
        stock_data['P/E'] = price_to_earnings_ratio
        stock_data['EPS'] = earnings_per_share

    return stock_data