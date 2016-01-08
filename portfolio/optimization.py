import numpy as np
import pandas as pd
import scipy
import os
import pandas.io.data as web
import matplotlib.pyplot as plt
import scipy.optimize as sco

from util import get_data, plot_data
from analysis import get_portfolio_value, get_portfolio_stats




def find_optimal_allocations(prices):

    noa = len(prices.columns)
    rets = np.log(prices / prices.shift(1))
    #print rets

    prets = [0, 0, 0, 0]
    pvols = [0, 0, 0, 0]
    for p in range (2500):
        allocs = np.random.random(noa)
        allocs /= np.sum(allocs)
        prets.append(np.sum(rets.mean() * allocs) * 252)
        pvols.append(np.sqrt(np.dot(allocs.T, np.dot(rets.cov() * 252, allocs))))

    prets = np.array(prets)
    pvols = np.array(pvols)

    def statistics(allocs):
        ''' Returns portfolio statistics.
        Parameters
        ==========
        weights : array-like
        weights for different securities in portfolio
        Returns
        =======
        pret : float
        expected portfolio return
        pvol : float
        expected portfolio volatility
        pret / pvol : float
        Sharpe ratio for rf=0
        '''
        allocs = np.array(allocs)
        pret = np.sum(rets.mean() * allocs) * 252
        pvol = np.sqrt(np.dot(allocs.T, np.dot(rets.cov() * 252, allocs)))
        return np.array([pret, pvol, pret / pvol])


    def min_func_sharpe(allocs):
        return -statistics(allocs)[2]

    
    cons = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bnds = tuple((0, 1) for x in range(noa))

    opts = sco.minimize(min_func_sharpe, noa * [1. / noa,], method='SLSQP', bounds=bnds, constraints=cons)

    allocs = opts['x']
    return allocs




def optimize_portfolio(start_date, end_date, symbols):
    """Simulate and optimize portfolio allocations."""

    noa = len(symbols)


    allocs = np.random.random(noa)
    allocs /= np.sum(allocs)



    dates = pd.date_range(start_date, end_date)
    prices_all = get_data(symbols, dates)  # automatically adds SPY
    prices = prices_all[symbols]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later

    allocs = find_optimal_allocations(prices) #optimize allocations
    
    allocs = allocs / np.sum(allocs)  # normalize allocations, if they don't sum to 1.0

    # Get daily portfolio value (already normalized since we use default start_val=1.0)
    port_val = get_portfolio_value(prices, allocs)

    #Get portfolio statistics (note: std_daily_ret = volatility)
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = get_portfolio_stats(port_val)
    

    
    # Print statistics
    print "Start Date:", start_date
    print "End Date:", end_date
    print "Symbols:", symbols
    print "Optimal allocations:", allocs 
    print "Sharpe Ratio:", sharpe_ratio
    print "Volatility (stdev of daily returns):", std_daily_ret
    print "Average Daily Return:", avg_daily_ret
    print "Cumulative Return:", cum_ret

    # Compare daily portfolio value with normalized SPY
    normed_SPY = prices_SPY / prices_SPY.ix[0, :]
    df_temp = pd.concat([port_val, normed_SPY], keys=['Portfolio', 'SPY'], axis=1)
    plot_data(df_temp, title="Daily Portfolio Value and SPY")

    # to use the Sci.optimize to find maxi sharpe_ratio where return to the allocs


def test_run():
    """Driver function."""
    # Define input parameters
    start_date = '2010-01-01'
    end_date = '2010-12-31'
    symbols = ['GOOG', 'AAPL', 'GLD', 'HNZ']  # list of symbols
    
    # Optimize portfolio
    optimize_portfolio(start_date, end_date, symbols)

if __name__ == "__main__":
    test_run()

