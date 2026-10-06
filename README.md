# Stock Viewer

A Python command-line stock viewer that retrieves market data, displays it in a terminal interface, and lets you sort and refresh the results.

## Features

- Retrieves stock data from Yahoo Finance
- Displays data in a curses-based terminal table
- Sorts by multiple stock fields
- Supports ascending and descending sorting
- Automatically refreshes every 10 seconds while the market is open
- Caches requests to reduce repeated network requests
- Highlights positive and negative price changes

## Files

- `stock.py` — main terminal interface and sorting/refresh logic
- `scrape.py` — retrieves and parses stock data
- `tickers.py` — ticker configuration
- `tickers.txt` — stock symbols used by the application
- `requirements.txt` — Python dependencies

## Running

Install the dependencies:

```bash
pip install -r requirements.txt
```

Then run:

```bash
python stock.py
```

The application is designed to run in a terminal that supports curses.

## What It Demonstrates

Python application development, web scraping, data parsing, request caching, terminal UI development, sorting, periodic refresh, and handling of market-hours behavior.
