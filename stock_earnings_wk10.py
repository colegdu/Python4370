"""
Cole Gibson
August 25, 2024
A stock program complete with data analystics, error handeling, classes, 
functions, modules, databse integration, reading and writing to files, data
presentation, and interaction with Yahoo Finance for quotes.
"""

import pandas as pd
from datetime import datetime
import sqlite3
import stock_analysis2 as sa
from data_analytics_mod import load_stock_data, calculate_statistics, display_statistics, convert_to_datetime, plot_stock_data
from quote_mod import fetch_quotes, display_quotes

# Create a connection to the SQLite database
try:
    # Attempt to create a connection to the SQLite database
    conn = sqlite3.connect('portfolio.db')
    # Create a cursor
    c = conn.cursor()
    print("Connection to database was successful.")
except sqlite3.Error as e:
    # Print an error message if the connection fails
    print(f"Failed to connect to the database. Error: {e}")
    exit(1)  # Exit the program since the connection failed

# Define a function to read data from the database
def read_data_from_db():
    c.execute("SELECT * FROM stocks")
    stock_data = c.fetchall()
    c.execute("SELECT * FROM bonds")
    bond_data = c.fetchall()
    return stock_data, bond_data

# Define a function to read investor data from the database
def read_investor_from_db(investor_id):
    c.execute("SELECT * FROM investors WHERE INVESTOR_ID = ?", (investor_id,))
    return c.fetchone()

# Read data from the database
stock_data, bond_data = read_data_from_db()

# Read investor data
investor_id = 1  # Assuming we are fetching the investor with ID 1
investor_data = read_investor_from_db(investor_id)

# Create Investor class
class Investor:
    def __init__(self, investorID, name, address, phone):
        """Initialize investor ID, address, and phone number"""
        self.investorID = investorID
        self.name = name
        self.address = address
        self.phone = phone
        self.stocks = []
        self.bonds = []

    def add_stock(self, investorID, purchaseID, symbol, shares, purchase_price, current_price, purchase_date):
        stock = Stock(investorID, purchaseID, symbol, shares, purchase_price, current_price, purchase_date)
        self.stocks.append(stock)

    def add_bond(self, investorID, purchaseID, symbol, shares, purchase_price, current_price, purchase_date, coupon, bond_yield):
        bond = Bond(investorID, purchaseID, symbol, shares, purchase_price, current_price, purchase_date, coupon, bond_yield)
        self.bonds.append(bond)

# Create Stock class
class Stock:
    def __init__(self, investorID, purchaseID, symbol, shares, purchase_price, current_price, purchase_date):
        self.investorID = investorID
        self.purchaseID = purchaseID
        self.symbol = symbol
        self.shares = shares
        self.purchase_price = purchase_price
        self.current_price = current_price
        self.purchase_date = purchase_date
        self.earnings_or_loss = 0
        self.earning_percentage = 0
        self.yearly_earnings_rate = 0

# Create Bond class
class Bond(Stock):
    def __init__(self, investorID, purchaseID, symbol, shares, purchase_price, current_price, purchase_date, coupon, bond_yield):
        super().__init__(investorID, purchaseID, symbol, shares, purchase_price, current_price, purchase_date)
        self.coupon = coupon
        self.bond_yield = bond_yield

# Initialize the investor using the data fetched from the database
if investor_data:
    investor = Investor(investorID=investor_data[0], name=investor_data[1], address=investor_data[2], phone=investor_data[3])
else:
    raise ValueError("Investor data not found in the database.")

# Populate the stock data
for row in stock_data:
    investor.add_stock(row[0], row[1], row[2], row[3], row[4], row[5], datetime.strptime(row[6], '%m/%d/%Y'))

# Populate the bond data
for row in bond_data:
    investor.add_bond(row[0], row[1], row[2], row[3], row[4], row[5], datetime.strptime(row[6], '%m/%d/%Y'), row[7], row[8])

# stock analysis calculations
sa.calculate_earnings(investor.stocks)
sa.calculate_earnings_percent(investor.stocks)
sa.calculate_earnings_rate(investor.stocks)

sa.calculate_bond_earnings(investor.bonds)
sa.calculate_bond_earnings_percent(investor.bonds)
sa.calculate_bond_earnings_rate(investor.bonds)

# Create a DataFrame for stocks
stocks_data = [{
    'Symbol': stock.symbol,
    'Shares': stock.shares,
    'Earnings/Loss': stock.earnings_or_loss,
    'Yearly Earnings/Loss': stock.yearly_earnings_rate
} for stock in investor.stocks]

stocks_df = pd.DataFrame(stocks_data)

# Create a DataFrame for bonds
bonds_data = [{
    'Symbol': bond.symbol,
    'Shares': bond.shares,
    'Earnings/Loss': bond.earnings_or_loss,
    'Yearly Earnings/Loss': bond.yearly_earnings_rate
} for bond in investor.bonds]

bonds_df = pd.DataFrame(bonds_data)

# Display the data in table format
print("Stocks Data:")
print(stocks_df.to_string(index=False))

print("\nBonds Data:")
print(bonds_df.to_string(index=False))

# data analytics
# List of file names
files = ["AIG", "F", "FB", "GOOG", "IBM", "M", "MSFT", "RDS-A", "SPY"]

# Load stock data
stock_data = load_stock_data(files)

# Calculate statistics
average_prices, std_devs, correlation_coefficients = calculate_statistics(stock_data)

# Display statistics
display_statistics(average_prices, std_devs, correlation_coefficients)
print('\n')

# Convert 'Date' to datetime
convert_to_datetime(stock_data)

# Get quotes for all stocks
# Fetch the tickers (adjust the column name to match your database)
query = "SELECT DISTINCT Symbol FROM stocks2"  # Replace 'symbol' with the actual column name
tickers_df = pd.read_sql(query, conn)

# Convert the DataFrame column to a list
tickers = tickers_df['Symbol'].tolist()  # Replace 'symbol' with the actual column name

# Fetch the latest quotes for the tickers
quotes = fetch_quotes(tickers)
print('\n')

# Display the quotes
print('Most recent price quote')
display_quotes(quotes)

# Plot stock data
plot_stock_data(stock_data)

# Write the data to CSV files
stocks_df.to_csv('Stocks_Data.csv', index=False)
bonds_df.to_csv('Bonds_Data.csv', index=False)
print("\nData has been written to Stocks_Data.csv and Bonds_Data.csv \n")

# Close the connection
conn.close()





