# optimize-portfolio-
 find how much of a portfolio's funds should be allocated to each stock so as to optimize it's performance
 define "optimal" as maximum Sharpe ratio.
 find allocations to the symbols that maximizes Sharpe Ratio.
 Assume 252 trading days in a year and a risk free rate of 0

 Implement a Python function named optimize_portfolio() in the file
 optimization.py that can find the optimal allocations for a given set of stocks
 The function accept as input a list of symbols as well as start and end dates
 and return a list of floats (as a one-dimensional numpy array) that represents the allocations to each of the equities.
 returned output is:

allocs: A 1-d Numpy array of allocations to the stocks, must sum to 1.0
cr: Cumulative return
adr: Average daily return
sddr: Standard deviation of daily return
The input parameters are:

sd: A datetime object that represents the start date
ed: A datetime object that represents the end date
syms: A list of symbols that make up the portfolio (note that your code should support any symbol in the data directory)
gen_plot: If True, create a plot named plot.png


