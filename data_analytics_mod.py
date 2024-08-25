import pandas as pd
import matplotlib.pyplot as plt

def load_stock_data(files):
    """
    Loads stock data from CSV files into a dictionary of DataFrames.

    Args:
        files (list): A list of stock file names (without the .csv extension).

    Returns:
        dict: A dictionary containing stock symbols as keys and their respective DataFrames as values.
    """
    stock_data = {}
    for file in files:
        try:
            stock_data[file] = pd.read_csv(f"{file}.csv")
        except FileNotFoundError:
            print(f"Unable to find \"{file}.csv\"")
    return stock_data

def calculate_statistics(stock_data):
    """
    Calculates average prices, standard deviations, and correlation coefficients.

    Args:
        stock_data (dict): A dictionary containing stock symbols as keys and their respective DataFrames as values.

    Returns:
        dict: A dictionary containing average prices, standard deviations, and correlation coefficients.
    """
    average_prices = {}
    std_devs = {}
    correlation_coefficients = {}

    for stock, df in stock_data.items():
        average_prices[stock] = df['Close'].mean()
        std_devs[stock] = df['Close'].std()

        if stock != "SPY":  # Calculate correlation with SPY
            correlation_coefficients[stock] = df['Close'].corr(stock_data['SPY']['Close'])

    return average_prices, std_devs, correlation_coefficients

def display_statistics(average_prices, std_devs, correlation_coefficients):
    """
    Displays the calculated statistics for average prices, standard deviations, and correlations.

    Args:
        average_prices (dict): A dictionary containing average prices for each stock.
        std_devs (dict): A dictionary containing standard deviations for each stock.
        correlation_coefficients (dict): A dictionary containing correlation coefficients with SPY for each stock.
    """
    print("Average Closing Prices:")
    for stock, avg_price in average_prices.items():
        print(f"{stock}: \t {avg_price:.2f}")

    print("\nStandard Deviations of Closing Prices:")
    for stock, std_dev in std_devs.items():
        print(f"{stock}: \t {std_dev:.2f}")

    print("\nCorrelation Coefficients with SPY:")
    for stock, corr_coeff in correlation_coefficients.items():
        print(f"{stock}: \t {corr_coeff:.4f}")

def convert_to_datetime(stock_data):
    """
    Converts the 'Date' column to datetime format for each stock's DataFrame.

    Args:
        stock_data (dict): A dictionary containing stock symbols as keys and their respective DataFrames as values.
    """
    for stock, df in stock_data.items():
        df['Date'] = pd.to_datetime(df['Date'])

def plot_stock_data(stock_data):
    """
    Plots the closing prices of stocks over time.

    Args:
        stock_data (dict): A dictionary containing stock symbols as keys and their respective DataFrames as values.
    """
    plt.figure(figsize=(14, 8))

    for stock, df in stock_data.items():
        plt.plot(df['Date'], df['Close'], label=stock)

    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.title('Closing Prices of Stocks Over Time')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.show()
