# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 20:07:14 2019
@author: Carlos Bonilla | email: carlos.abel.bonilla@gmail.com 
@linkedIn: https://www.linkedin.com/in/carlosbonilla1/
"""
#Basic function to calculate a single period present value
def pv(cash_flow, period, day_count, cost_of_capital):
    #day_count is meant to proxy the length of the "period" the cash flow is received in 
    v = cash_flow/((1+cost_of_capital)**(period*day_count))
    return v

#Present value table; can either provide a matching size list discount curve or a single discount rate
def cash_pv_table(cash_flows, discount_curve, day_count = 1, interpolate_discount_curve = False):
    #day_count is meant to proxy the length of the "period" the cash flow is received in 
    # If interpolate_discount_curve is true then will use provided discount rates to interpolate a log curve
    
    #Package dependencies
    import pandas as pd

    #Create a dataframe to hold and calclate the relevant data/factors
    df = pd.DataFrame(list(range(len(cash_flows))), columns = ["Period"]) 
    #df = pd.DataFrame(periods, columns = ["Period"]) 
    df['Cash_Flow'] = cash_flows
    
    if interpolate_discount_curve == True:
        import numpy as np
        df['Discount_Rate'] = np.geomspace(discount_curve[0], discount_curve[1], num=len(cash_flows))
    else: df['Discount_Rate'] = discount_curve

    #Calculate discount factors
    df['Discount_Factor'] = pd.DataFrame(1/((1+df['Discount_Rate'][x])**(df['Period'][x]*day_count)) for x in df['Period'])

    #Can loop through the periods and calculate each PV or multiple the cash flow by the discount factor
    #df['PV'] = pd.DataFrame(cash_flows[x]/((1+cost_of_capital[x])**(periods[x]*day_count)) for x in df['Period'])
    df['PV']= df['Cash_Flow'] * df['Discount_Factor']

    #Return a pandas dataframe 
    return df

#%% PV Table exmple with interpolation
cash_flows = [-100.0,3.0,3,3,3,3,3,3,3,3,3,3,103.0]
discount_curve = [.03,.05]
day_count = 1

df = cash_pv_table(cash_flows=cash_flows, discount_curve=discount_curve,interpolate_discount_curve = True)
df

#%%
df['Cash_Flow'][2-1]
#%%Gordon Growth Model equations
def sustainable_dividend_growth(Net_Income,Dividends,Sales,Total_Assets,Shareholders_Equity):
    g= (Net_Income-Dividends)/Net_Income*(Net_Income/Sales)*(Sales/Total_Assets)*(Total_Assets/Shareholders_Equity)
    return g

def gordon_growth_valuation(dividend_growth_rate,discount_rate,dividend):
    D1 = (dividend*(1+dividend_growth_rate))
    val = D1/(discount_rate-dividend_growth_rate)
    return val

def leading_price_earnings(dividend_growth,dividend,earnings_estimate,discount_rate,dividend_growth_rate):
    D1 = (dividend*(1+dividend_growth_rate))
    val = D1/earnings_estimate/(discount_rate-dividend_growth_rate)
    return val

#%% The H-Model equation
# The basic two-stage model assumes a constant, extraordinary rate for the supernormal growth period that is followed by a constant, normal growth rate thereafter. 
def H_dividend_valuation(short_term_growth,long_term_growth,high_growth_periods,discount_rate,dividend):
    val = (((dividend*(1+long_term_growth))/(discount_rate-long_term_growth))+
    ((dividend*(high_growth_periods/2)*(short_term_growth-long_term_growth))/(discount_rate-long_term_growth)))
    return val

#%% The H-Model example
H_dividend_valuation(short_term_growth= .12,long_term_growth=.02,high_growth_periods=8,
                           discount_rate=.08,dividend=.37)

#%%The Present Value of Growth Opportunities
#Present value table; can either provide a matching size list discount curve or a single discount rate
def dividend_pv_table(initial_dividend, dividend_growth_curve, discount_curve,
                      terminal_period, day_count = 1, interpolate_dividend_growth_curve = False,
                      interpolate_discount_curve = False):
    #day_count is meant to proxy the length of the "period" the cash flow is received in 
    # If interpolate_discount_curve is true then will use provided discount rates to interpolate a log curve
    
    #Package dependencies
    import pandas as pd

    #Create a dataframe to hold and calclate the relevant data/factors
    df = pd.DataFrame(list(range(terminal_period+1)), columns = ["Period"]) 
    #df = pd.DataFrame(periods, columns = ["Period"]) 
    
    if interpolate_discount_curve == True:
        import numpy as np
        df['Discount_Rate'] = np.geomspace(discount_curve[0], discount_curve[1], num=len(cash_flows))
    else: df['Discount_Rate'] = discount_curve

#Calculate discount factors
    df['Discount_Factor'] = pd.DataFrame(1/((1+df['Discount_Rate'][x])**(df['Period'][x]*day_count)) for x in df['Period'])
    
    if interpolate_dividend_growth_curve == True:
        import numpy as np
        df['Div_Growth_Rate'] = np.geomspace(dividend_growth_curve[0], dividend_growth_curve[1], num=terminal_period)
    else: df['Div_Growth_Rate'] = dividend_growth_curve

    #Calculate dividend estimates
    df['Dividend'] = initial_dividend
    for x in range(1,terminal_period+1):
        df.loc[x, 'Dividend'] = ((df.loc[x-1, 'Dividend'])*(1+df.loc[x, 'Div_Growth_Rate']))

    #Can loop through the periods and calculate each PV or multiple the cash flow by the discount factor
    df['PV_Div'] = df['Dividend'] * df['Discount_Factor']
    df.loc[terminal_period, 'PV_Div'] = ((df.loc[terminal_period, 'Dividend']/
          (df.loc[terminal_period, 'Discount_Rate']-df.loc[terminal_period, 'Div_Growth_Rate']))
    *df.loc[terminal_period, 'Discount_Factor'])

    #Return a pandas dataframe 
    return df

#%%Spreadsheet Model Example
dividend_pv_table(initial_dividend = 1, dividend_growth_curve = .02, discount_curve = .05,
                      terminal_period = 8)


#%%Dependencies and/or references
#https://www.cfainstitute.org/membership/professional-development/refresher-readings/2019/discounted-dividend-valuation
#https://docs.scipy.org/doc/numpy/reference/generated/numpy.geomspace.html#numpy.geomspace   