# Import required libraries
import os
from random import randint

import plotly.plotly as py
from plotly.graph_objs import *

import flask
import dash
from dash.dependencies import Input, Output, State, Event
import dash_core_components as dcc
import dash_html_components as html


# Setup the app
# Make sure not to change this file name or the variable names below,
# the template is configured to execute 'server' on 'app.py'
server = flask.Flask(__name__)
server.secret_key = os.environ.get('secret_key', str(randint(0, 1000000)))
app = dash.Dash(__name__, server=server)


# Put your Dash code here
# income statement
sf.set_data_dir('~/simfin_data/')
api_key = "ZxGEGRnaTpxMF0pbGQ3JLThgqY2HBL17"
df_income = sf.load(dataset='income', variant='annual', market='us', refresh_days=3, index=[TICKER])
df_publish = df_income.copy()
df_pe = pd.DataFrame()
df_pe['Date'] = df_publish['Fiscal Year']
df_pe['EPS'] = df_publish[NET_INCOME].div(df_publish[SHARES_DILUTED], axis=0)
df_shares = df_income[SHARES_DILUTED]
df_income = df_income.drop(['Currency', 'SimFinId', 'Fiscal Period', 'Publish Date', 'Shares (Basic)',
                            'Abnormal Gains (Losses)', 'Net Extraordinary Gains (Losses)',
                            'Income (Loss) from Continuing Operations',
                            'Net Income (Common)', 'Pretax Income (Loss), Adj.', 'Report Date', 'Restated Date'],
                           axis=1)
# df_income=df_income.fillna(0)
df_income = df_income.apply(lambda x: x / 1000000)
decimals = 0
df_income['Fiscal Year'] = df_income['Fiscal Year'].apply(lambda x: x * 1000000)
df_income['Fiscal Year'] = df_income['Fiscal Year'].apply(lambda x: round(x, decimals))
ticker = "AAPL"
df_income.rename(
    columns={FISCAL_YEAR: 'Year', SHARES_DILUTED: 'Shares', SGA: 'SGA', RD: 'R&D', DEPR_AMOR: 'D&A',
             OP_INCOME: 'Operating Income', NON_OP_INCOME: 'Non Operating Income',
             INTEREST_EXP_NET: 'Interest Expense', PRETAX_INCOME_LOSS: 'Pretax Income',
             INCOME_TAX: 'Income Tax'}, inplace=True)
# restated date
df_names = df_income.index.copy()
df_names = df_names.drop_duplicates()

# income signals
df_negative = df_income.copy()
df_negative[['Cost of Revenue', 'R&D', 'Operating Expenses', 'SGA', 'Income Tax', 'D&A', 'Interest Expense']] = \
    df_negative[
        ['Cost of Revenue', 'R&D', 'Operating Expenses', 'SGA', 'Income Tax', 'D&A', 'Interest Expense']].apply(
        lambda x: x * -1)
df_negative['Expenses'] = df_negative['Operating Expenses'] + df_negative['SGA'] + df_negative['R&D'] + df_negative[
    'D&A']
df_signals = pd.DataFrame(index=df_negative.index)
df_signals['Year'] = df_negative['Year'].copy()
df_signals['Gross Profit Margin %'] = round((df_negative['Gross Profit'] / df_negative['Revenue']) * 100,
                                            2).copy()
df_signals['SGA Of Gross Profit'] = round((df_negative['SGA'] / df_negative['Gross Profit']) * 100, 2).copy()
df_signals['R&D Of Gross Profit'] = round((df_negative['R&D'] / df_negative['Gross Profit']) * 100, 2).copy()
df_signals['D&A Of Gross Profit'] = round((df_negative['D&A'] / df_negative['Gross Profit']) * 100, 2).copy()
df_signals['Operating margin ratio'] = round((df_negative['Operating Income'] / df_negative['Revenue']) * 100,
                                             2).copy()
df_signals['Interest to Operating Income %'] = round((df_negative['Interest Expense'] / df_negative['Operating Income'])
                                                     * 100, 2).copy()
df_signals['Taxes paid'] = round((df_negative['Income Tax'] / df_negative['Pretax Income']) * 100, 2).copy()
df_signals['Net income margin'] = round((df_negative['Net Income'] / df_negative['Revenue']) * 100, 2).copy()
df_signals['Interest to Operating Income %'] = df_signals['Interest to Operating Income %'].replace(-np.inf, 0)
df2_original = df_signals.loc[ticker]

# income growth per year
df1_growth = pd.DataFrame(index=df_income.index)
df1_growth['Year'] = df_income['Year'].copy()
df1_growth['Revenue Growth'] = df_income['Revenue'].pct_change().mul(100).round(2).copy()
df1_growth['Profit Growth'] = df_income['Gross Profit'].pct_change().mul(100).round(2).copy()
df1_growth['Operating Income Growth'] = df_income['Operating Income'].pct_change().mul(100).round(2).copy()
df1_growth['Pretax Income Growth'] = df_income['Pretax Income'].pct_change().mul(100).round(2).copy()
df1_growth['Net Income Growth'] = df_income['Net Income'].pct_change().mul(100).round(2).copy()
df1_growth = df1_growth.fillna(0)

# compounded income growth
df_income_compound_original = pd.DataFrame()
df_income_compound_original['Revenue %'] = []
df_income_compound_original['Inventory %'] = []
df_income_compound_original['Gross Profit %'] = []
df_income_compound_original['Operating Income %'] = []
df_income_compound_original['Pre tax %'] = []
df_income_compound_original['Net Income %'] = []

# balance sheet
df_balance = sf.load_balance(variant='annual', market='us', refresh_days=3, index=[TICKER])
df_balance = df_balance.drop(
    ['Currency', 'SimFinId', 'Fiscal Period', 'Publish Date', 'Shares (Basic)', 'Shares (Diluted)', 'Report Date',
     'Total Liabilities & Equity', 'Restated Date'], axis=1)
df_balance = df_balance.fillna(0)
df_balance = df_balance.apply(lambda x: x / 1000000)
df_balance['Fiscal Year'] = df_balance['Fiscal Year'].apply(lambda x: x * 1000000)
df_balance['Fiscal Year'] = df_balance['Fiscal Year'].apply(lambda x: round(x, 0))
df_balance.rename(columns={FISCAL_YEAR: 'Year', CASH_EQUIV_ST_INVEST: 'Cash & Equivalent',
                           ACC_NOTES_RECV: 'Accounts Receivable', TOTAL_CUR_ASSETS: 'Current Assets',
                           PPE_NET: 'Prop Plant & Equipment', LT_INVEST_RECV: 'Long Term Investments',
                           OTHER_LT_ASSETS: 'Other Long Term Assets', TOTAL_NONCUR_ASSETS: 'Noncurrent assets',
                           PAYABLES_ACCRUALS: 'Accounts Payable', TOTAL_CUR_LIAB: 'Current Liabilities',
                           TOTAL_NONCUR_LIAB: 'Noncurrent Liabilities', SHARE_CAPITAL_ADD: 'C&APIC Stock',
                           ST_DEBT: 'ShortTerm debts', LT_DEBT: 'LongTerm Debts',
                           INVENTORIES: 'Inventory & Stock'}, inplace=True)
df_balance['Book Value'] = round((df_balance['Total Equity'] / df_income['Shares']), 2)
df_balance['EPS'] = round((df_income['Net Income'] / df_income['Shares']), 2)
df3_original = df_balance.loc[ticker]

# balance signals
df_balance_signals = pd.DataFrame(index=df_balance.index)
df_balance_signals['Year'] = df_balance['Year'].copy()
df_balance_signals['Return on EquityT'] = round(
    (df_income['Net Income'] / (df_balance['Total Equity'] + (-1 * df_balance['Treasury Stock']))), 2).copy()
df_balance_signals['Liabilities to EquityT'] = round(
    (df_balance['Total Liabilities'] / (df_balance['Total Equity'] + (-1 * df_balance['Treasury Stock']))),
    2).copy()
df_balance_signals['Debt (LS) to EquityT'] = round(
    ((df_balance['LongTerm Debts'] + df_balance['ShortTerm debts']) / (df_balance['Total Equity'] +
                                                                       (-1 * df_balance['Treasury Stock']))), 2).copy()
df_balance_signals['Long Term Debt Coverage'] = round((df_income['Net Income'] / df_balance['LongTerm Debts']),
                                                      2).copy()
df_balance_signals['Long Term Debt Coverage'] = df_balance_signals['Long Term Debt Coverage'].replace([np.inf, -np.inf],
                                                                                                      0)
df_balance_signals['Current Ratio'] = round((df_balance['Current Assets'] / df_balance['Current Liabilities']),
                                            2).copy()
df_balance_signals['Return on Assets%'] = round((df_income['Net Income'] / df_balance['Total Assets']) * 100, 2).copy()
df_balance_signals['Retained Earning to Equity%'] = round(
    (df_balance['Retained Earnings'] / df_balance['Total Equity']) * 100, 2).copy()
df_balance_signals['Receivables of Revenue%'] = round((df_balance['Accounts Receivable'] / df_income['Revenue']) * 100,
                                                      2).copy()
df_balance_signals['PP&E of Assets%'] = round((df_balance['Prop Plant & Equipment'] / df_balance['Total Assets']) * 100,
                                              2).copy()
df_balance_signals['Inventory of Assets%'] = round((df_balance['Inventory & Stock'] / df_balance['Total Assets']) * 100,
                                                   2).copy()
df4_original = df_balance_signals.loc[ticker]

# balance growth per year
balance_growth = pd.DataFrame(index=df_balance.index)
balance_growth['Year'] = df_balance['Year'].copy()
balance_growth['Cash Growth'] = df_balance['Cash & Equivalent'].pct_change().mul(100).round(2).copy()
balance_growth['Inventory Growth'] = df_balance['Inventory & Stock'].pct_change().mul(100).round(2).copy()
balance_growth['Current Assets Growth'] = df_balance['Current Assets'].pct_change().mul(100).round(2).copy()
balance_growth['PP&E Growth'] = df_balance['Prop Plant & Equipment'].pct_change().mul(100).round(2).copy()
balance_growth['Investment Growth'] = df_balance['Long Term Investments'].pct_change().mul(100).round(2).copy()
balance_growth['Asset Growth'] = df_balance['Total Assets'].pct_change().mul(100).round(2).copy()
balance_growth['Liability Growth'] = df_balance['Total Liabilities'].pct_change().mul(100).round(2).copy()
balance_growth['Retained Earnings Growth'] = df_balance['Retained Earnings'].pct_change().mul(100).round(2).copy()
balance_growth['Equity Growth'] = df_balance['Total Equity'].pct_change().mul(100).round(2).copy()
balance_growth = balance_growth.fillna(0)

# balance compound growth
df_balance_compound_original = pd.DataFrame()
df_balance_compound_original['Cash %'] = []
df_balance_compound_original['Inventory %'] = []
df_balance_compound_original['Current Assets %'] = []
df_balance_compound_original['PP&E %'] = []
df_balance_compound_original['Long Term Investment%'] = []
df_balance_compound_original['Assets %'] = []
df_balance_compound_original['Liability %'] = []
df_balance_compound_original['Retained Earnings %'] = []
df_balance_compound_original['Equity %'] = []

# cashflow statement
df_cashflow = sf.load_cashflow(variant='annual', market='us', refresh_days=3, index=[TICKER, FISCAL_YEAR])
df_cashflow = df_cashflow.drop(
    ['Currency', 'SimFinId', 'Fiscal Period', 'Publish Date', 'Shares (Basic)', 'Report Date',
     'Shares (Diluted)', 'Restated Date'], axis=1)
df_cashflow = df_cashflow.apply(lambda x: x / 1000000)
df_cashflow.rename(
    columns={'Net Income/Starting Line': 'Net Income', 'Depreciation & Amortization': 'D&A',
             'Change in Working Capital': 'ΔWorking Capital', 'Change in Accounts Receivable': 'ΔReceivables',
             'Change in Inventories': 'ΔInventory', 'Change in Accounts Payable': 'ΔPayables',
             'Change in Other': 'ΔOther',
             'Net Cash from Operating Activities': 'Cash from Operating',
             'Change in Fixed Assets & Intangibles': 'Capital Expenditure',
             'Net Change in Long Term Investment': 'ΔLT Investment',
             'Net Cash from Acquisitions & Divestitures': 'Acquisitions& Divestitures',
             'Net Cash from Investing Activities': 'Cash from Investing',
             'Cash from (Repayment of) Debt': 'Debt Repayment', 'Cash from (Repurchase of) Equity': 'Equity Repurchase',
             'Net Cash from Financing Activities': 'Cash from Financing'}, inplace=True)

# complicated transposing issue where fiscal year is originally needed as an index, for graph use fiscal year
df_cashflow = df_cashflow.fillna(0)
df_freecashflow = pd.DataFrame()
df_freecashflow['Cash from Operating'] = df_cashflow['Cash from Operating']
df_freecashflow['Capital Expenditure'] = df_cashflow['Capital Expenditure']
df_freecashflow['Free Cash Flow'] = (df_cashflow['Cash from Operating'] + df_cashflow['Capital Expenditure']).round(2)

df_cashflow = df_cashflow.reset_index()
df_cashflow = df_cashflow.set_index('Ticker')

df_dividend = pd.DataFrame()
df_dividend['Dividend per share'] = (df_cashflow['Dividends Paid'] * -1000000) / df_shares
df_dividend['Year'] = df_cashflow['Fiscal Year']

df_positive_cashflow = df_cashflow.copy()
df_positive_cashflow[['Cash from Investing', 'Cash from Financing', 'Equity Repurchase', 'ΔLT Investment']] = \
    df_positive_cashflow[['Cash from Investing', 'Cash from Financing', 'Equity Repurchase', 'ΔLT Investment']].apply(
        lambda x: x * -1)
df_positive_cashflow['Free Cash Flow'] = (
        df_positive_cashflow['Cash from Operating'] + df_positive_cashflow['Capital Expenditure']).round(2)
df_positive_cashflow['Capex FCF'] = (
        ((df_cashflow['Capital Expenditure'] * -1) / df_cashflow['Cash from Operating']) * 100).round(2)
df_positive_cashflow['Capex Income'] = (
        ((df_cashflow['Capital Expenditure'] * -1) / df_cashflow['Net Income']) * 100).round(2)

df2_growth = pd.DataFrame(index=df_cashflow.index)
df2_growth['Year'] = df_cashflow['Fiscal Year'].copy()
df2_growth['Net Income'] = df_cashflow['Net Income'].pct_change().mul(100).round(2).copy()
df2_growth['Free Cash Flow'] = df_positive_cashflow['Free Cash Flow'].pct_change().mul(100).round(2).copy()
df2_growth['Cash from Operating'] = df_cashflow['Cash from Operating'].pct_change().mul(100).round(2).copy()
df2_growth['Cash from Investing'] = df_positive_cashflow['Cash from Investing'].pct_change().mul(100).round(2).copy()
df2_growth['Cash from Financing'] = df_positive_cashflow['Cash from Financing'].pct_change().mul(100).round(2).copy()
df2_growth['Equity Repurchase'] = df_positive_cashflow['Equity Repurchase'].pct_change().mul(100).round(2).copy()
df2_growth['Capex of Operating'] = df_positive_cashflow['Capex FCF']
df2_growth['Capex of Income'] = df_positive_cashflow['Capex Income']
df2_growth = df2_growth.fillna(0)

df_cashflow_compound_original = pd.DataFrame()
df_cashflow_compound_original['Net Income %'] = []
df_cashflow_compound_original['Free Cash Flow %'] = []
df_cashflow_compound_original['Owners Earnings'] = []
df_cashflow_compound_original['Cash from Operating %'] = []
df_cashflow_compound_original['Cash from Investing %'] = []
df_cashflow_compound_original['Cash from Financing %'] = []
df_cashflow_compound_original['Total Capex Of Total Income'] = []
df_cashflow_compound_original['Capex Avergae of Operating'] = []

# Buffett Indicator
end = datetime.datetime.now()
start = end - relativedelta(years=20)
gdp = pdr.get_data_fred('GDP', start, end)
wilshire = pdr.get_data_fred('WILL5000PR', start, end)

combined = pd.concat([gdp, wilshire], axis=1)
gdp_dates = gdp.index.values
prev_date = 'NaN'

for date in gdp_dates:
    if prev_date == 'NaN':
        combined.loc[:date, 'GDP'] = gdp.loc[date, 'GDP']
    else:
        combined.loc[date, 'GDP'] = gdp.loc['GDP']
    # combined.loc['GDP'] = gdp.loc[date, 'GDP']

combined['Buffet_Indicator'] = combined.WILL5000PR / combined.GDP * 100

fig30 = make_subplots()
fig30.add_trace(go.Scatter(x=list(combined.index), y=list(combined['Buffet_Indicator']), name='Buffet'))
fig30.update_layout(legend=dict(x=0, y=1,
                                traceorder="normal",
                                font=dict(family="sans-serif", size=12, color="black"),
                                bgcolor="rgba(50, 50, 50, 0)", bordercolor="rgba(50, 50, 50, 0)", borderwidth=0))
fig30.update_layout(title={'text': "Buffett Indicator", 'y': 0.96, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'})
fig30.update_layout(margin={'t': 25, 'b': 0, 'l': 0, 'r': 0})

# PCA Kmeans preprocessing
clustersignals = pd.DataFrame()

clustersignals['Gross profit margin'] = (df_income['Gross Profit'] / df_income['Revenue'])
clustersignals['Net Income Margin'] = (df_income['Net Income'] / df_income['Revenue'])
clustersignals['Return on Equity'] = (df_income['Net Income'] / df_balance['Total Equity'])
clustersignals['Return on Assets'] = (df_income['Net Income'] / df_balance['Total Assets'])
clustersignals['Liabilities to Equity'] = (df_balance['Total Liabilities'] / df_balance['Total Equity'])
clustersignals['Retained earnings to Equity'] = (df_balance['Retained Earnings'] / df_balance['Total Equity'])
clustersignals['Year'] = df_income['Year']

# be careful this must be here or half of data gets destroyed
clustersignals.dropna(inplace=True)

# selecting only the 2018 value for each ticker
clustersignals['Ticker'] = clustersignals.index
clustersignals = clustersignals.set_index(clustersignals['Year'])
clustersignals = clustersignals.drop(['Year'], axis=1)
clustersignals = clustersignals.loc[2018]
clustersignals = clustersignals.set_index(clustersignals['Ticker'])
clustersignals = clustersignals.drop(['Ticker'], axis=1)


# Run the Dash app
if __name__ == '__main__':
    app.server.run(debug=True, threaded=True)
