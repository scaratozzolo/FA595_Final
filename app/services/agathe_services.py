import numpy as np
import pandas as pd
import scipy.linalg as la
import yfinance as yf
from scipy.optimize import minimize
from cvxopt import matrix, solvers
import matplotlib.pyplot as plt

# Getting the returns of two assets
def ret(tick):
    d = yf.download(tick, start=pd.Timestamp.today() - pd.DateOffset(days=1), progress=False)
    d = d['Adj Close'].pct_change()
    return(d[1])

# Efficient frontier based on maximizing return of the portfolio with two assets given the return and variance of each and the covariance between them
def max_ret(tick1,tick2,s1,s2,cor):
    rho = matrix([ret(tick1), ret(tick2)])
    sig = matrix([[s1, cor], [cor, s2]])
    sig_inv = la.inv(sig)
    e = matrix([1.0, 1.0])
    A = e.T @ sig_inv @ rho
    B = rho.T @ sig_inv @ rho
    C = e.T @ sig_inv @ e
    rts = np.zeros(20)
    vols = np.linspace(0.09, 0.4, 20)
    w = matrix([0.0, 0.0])
    for i in range(0, 20):
        var = vols[i] ** 2
        D = np.sqrt((1 - C * var) / (A * A - B * C))
        w = D * (sig_inv @ rho) - ((A * D - 1) / C) * (sig_inv @ e)
        rts[i] = rho.T @ w
    result = dict(zip(rts , vols))
    print(result)
    #plt.xlabel("Portfolio Risk")
    #plt.ylabel("Portfolio Expected Returns")
    #plt.title("Efficient Frontier")
    #plt.plot(vols, rts, color='green')
    #plt.show()
    return {"return:risk" : result}

# Efficient frontier based on minimizing risk of the portfolio with two assets given the return and variance of each and the covariance between them
def min_risk(tick1,tick2,s1,s2,cor):
    matrix([ret(tick1), ret(tick2)])
    sig = matrix([[s1, cor], [cor, s2]])
    sig_inv = la.inv(sig)
    e = matrix([1.0, 1.0])
    A = e.T @ sig_inv @ rho
    B = rho.T @ sig_inv @ rho
    C = e.T @ sig_inv @ e
    E = B * C - A * A
    rts = np.linspace(0.07, 0.15, 20)
    vols = np.zeros(20)
    w = matrix([0.0, 0.0])
    for i in range(0, 20):
        rho_P = rts[i]
        w1 = (1 / E) * ((C * rho_P - A) * (sig_inv @ rho) + (B - A * rho_P) * (sig_inv @ e))
        vols[i] = np.sqrt(w1.T @ sig @ w1)
    #plt.xlabel("Portfolio Risk")
    #plt.ylabel("Portfolio Expected Returns")
    #plt.title("Efficient Frontier")
    #plt.plot(vols, rts, color='green')
    #plt.show()
    result = dict(zip(rts, vols))
    return {"return:risk", result}
