import curses
from curseXcel import Table
import time
from scrape import scrape_data, get_stock_data
import tickers

#This file contains the main program function and curses display

TICKERS = tickers.init_ticker_set() #valid inputs
STOCKS = set(input("Enter stock ticker symbol(s) separated by commas (e.g., NVDA,MSFT,AAPL): ").strip().upper().split(','))
HEADERS = ['Symbol', 'Name', 'Price', 'Change', 'Change %', 'Market Cap', 'P/E', 'EPS']
SORTING_KEYS = tickers.init_sorting_keys()

def get_data():
    #Returns a list of dictionaries where each dictionary is the data for a stock
    stocks_data = [] 
    for stock in STOCKS:
        if stock in TICKERS:
            content = scrape_data(stock)
            stock_data = get_stock_data(content, stock)
            stocks_data.append(stock_data)
    return stocks_data

def refresh_with_colors(stdscr, table, data, rows, color_pairs):
    #refreshes the table and adds color to cells that contain a "change" variable
    table.refresh() 
    for r in range(rows):
        color_cell(stdscr, table, r, 3, data[r]['price_change'], color_pairs)
        color_cell(stdscr, table, r, 4, data[r]['percent_change'], color_pairs)

def color_cell(stdscr, table, row, col, value, color_pairs):
    #helper function for refresh that colors the cells
    if '+' not in value and '-' not in value:
        return
    
    y = row + 1
    x = col * (table.cell + table.spacing)
    if '+' in value:
        c = 0
    else:
        c = 1
    color = curses.color_pair(color_pairs[c])
    stdscr.chgat(y, x, table.cell, color)

def init_curses():
    #initilizes curses and color pairs -> did this to reduce the code volume in main
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)   #default color
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)   #green for positive
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)     #red for negative

def is_market_open():
    #returns true if the market is open (9:30am-4:00pm), false otherwise
    t = time.localtime()
    hour = t.tm_hour
    minute = t.tm_min
    if hour == 9 and minute >= 30:
        return True
    elif hour > 9 and hour < 16:
        return True
    return False

def fill_table(rows, cols, data, keys, table):
    #fills the table with the data values
    for r in range(rows):
        for c in range(cols):
            table.set_cell(r, c, data[r][keys[c]])

def main(stdscr):
    init_curses()

    data = get_data()

    rows = len(data)
    cols = 8    #len(data[0]) -> Hard coded to 8
    keys = ['symbol', 'name', 'price', 'price_change', 'percent_change', 'market_cap', 'P/E', 'EPS']

    table = Table(stdscr, rows, cols, 12, 100, 30, spacing=1, col_names=True) #create the Table object
    table.win.bkgd(' ', curses.color_pair(1)) #sets the windows background
    table.cursor = [100, 100] #sets the table cursor off the screen so its not visible
    curses.curs_set(0) #makes the cursor invisible
    
    #Fill table with headers and data
    for c in range(cols):
        table.set_column_header(HEADERS[c], c)
    fill_table(rows, cols, data, keys, table)

    last_update = time.time()
    sort_mode = False
    sort_index = None

    stdscr.nodelay(True) #makes getch() be non blocking
    while True:
        refresh_with_colors(stdscr, table, data, rows, [2,3])
        try:
            key = stdscr.getkey().lower()
            if key == 'q':
                break
            elif key == 'a':
                sort_mode = False #ascending
            elif key == 'd':
                sort_mode = True #descending
            elif key in ['1','2','3','4','5','6','7','8']:
                sort_index = int(key) - 1
                data.sort(key=SORTING_KEYS[sort_index], reverse=sort_mode)
                fill_table(rows, cols, data, keys, table)
        except:
            pass  
        if is_market_open(): #only updates the data if the market is open since the data doesn't change when its closed
            current_time = time.time()
            if current_time - last_update >= 10: #checks if 10 seconds have passed since the last data update
                new_data = get_data()   #get updated data
                if sort_index is not None:
                    new_data.sort(key=SORTING_KEYS[sort_index], reverse=sort_mode) #makes sure that data stays sorted when it is refreshed

                data = new_data
                last_update = current_time
                fill_table(rows, cols, data, keys, table)
        time.sleep(0.1)
    stdscr.nodelay(False) 

if __name__ == "__main__":
    curses.wrapper(main)
