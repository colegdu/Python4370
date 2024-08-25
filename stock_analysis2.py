"""
Cole Gibson
July 27, 2024
Stock analysis module refactored for week 6 assignment
"""

from datetime import datetime

def calculate_earnings(stock_list):
    for stock in stock_list:
        earnings_or_loss = (stock.current_price - stock.purchase_price) * stock.shares
        stock.earnings_or_loss = earnings_or_loss

def calculate_earnings_percent(stock_list):
    for stock in stock_list:
        earning_percentage = ((stock.current_price - stock.purchase_price) / stock.purchase_price) * 100
        stock.earning_percentage = earning_percentage

def calculate_earnings_rate(stock_list):
    current_date = datetime.now()
    for stock in stock_list:
        years_held = (current_date - stock.purchase_date).days / 365.25
        yearly_earnings_rate = (((stock.current_price - stock.purchase_price) / stock.purchase_price) / years_held) * 100
        stock.yearly_earnings_rate = yearly_earnings_rate

def calculate_bond_earnings(bond_list):
    for bond in bond_list:
        earnings_or_loss = (bond.current_price - bond.purchase_price) * bond.shares
        bond.earnings_or_loss = earnings_or_loss

def calculate_bond_earnings_percent(bond_list):
    for bond in bond_list:
        earning_percentage = ((bond.current_price - bond.purchase_price) / bond.purchase_price) * 100
        bond.earning_percentage = earning_percentage

def calculate_bond_earnings_rate(bond_list):
    current_date = datetime.now()
    for bond in bond_list:
        years_held = (current_date - bond.purchase_date).days / 365.25
        yearly_earnings_rate = (((bond.current_price - bond.purchase_price) / bond.purchase_price) / years_held) * 100
        bond.yearly_earnings_rate = yearly_earnings_rate

