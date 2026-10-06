# Stock Viewer Command Line Tool

A Python command-line tool for viewing and sorting stock market data.

The program retrieves stock information from Yahoo Finance, displays it in a terminal table, and supports sorting and automatic updates while the market is open.

## Features

- Enter multiple stock ticker symbols at startup
- Retrieve price, daily change, percentage change, market cap, P/E, and EPS
- Display data in a terminal UI using curses
- Sort by any displayed metric using keys 1–8
- Toggle ascending/descending sorting with `a` and `d`
- Refresh market data automatically every 10 seconds while the market is open
- Cache Yahoo Finance requests to reduce repeated network requests
- Color-code positive and negative price changes

## Project Structure

```text
.
├── stock.py       # Main program and curses display
├── scrape.py      # Yahoo Finance scraping and data extraction
├── tickers.py     # Ticker validation and sorting functions
├── tickers.txt    # Supported ticker symbols
└── requirements.txt
```

## Installation

Create a virtual environment and install the dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running

```bash
python3 stock.py
```

Enter ticker symbols separated by commas when prompted, for example:

```text
NVDA,MSFT,AAPL
```

The terminal should be expanded to give the table enough room to display all columns.

### Controls

| Key | Action |
| --- | --- |
| `1`–`8` | Sort by the corresponding column |
| `a` | Ascending order |
| `d` | Descending order |
| `q` | Quit |

## Background

Originally developed as a command-line programming project. The current repository is a cleaned version of the original work, preserving the original program structure and implementation while removing generated files and adding clearer documentation.
