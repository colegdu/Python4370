import yfinance as yf

def fetch_quotes(tickers):
    """
    Fetches the latest closing prices for the given tickers using yfinance.
    Args:
        tickers (list): Accepts a list of tickers
    Returns:
        dict: A dictionary with ticker symbols as keys and the latest closing prices as values.
    """
    quotes = {}
    
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="1d")
            
            # Check if we have data
            if not hist.empty:
                quotes[ticker] = hist['Close'].iloc[-1]  # Fetch the latest closing price
            else:
                quotes[ticker] = f"No data found for {ticker}; symbol may be delisted or changed"
        except Exception as e:
            quotes[ticker] = f"Error: {e}"
    
    return quotes

def display_quotes(quotes):
    """
    Displays the fetched quotes in a readable format.
    Args:
        quotes: A dictionary with ticker symbols as keys and the latest closing prices as values.
    """
    for ticker, quote in quotes.items():
        print(f"{ticker} \t {quote}")
 