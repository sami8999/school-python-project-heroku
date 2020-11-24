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
app.title = 'Financial Statements'
app.config['suppress_callback_exceptions'] = True

app.layout = html.Div([
    html.Div([
        html.H2('Fundamental Analysis'),
        html.A(html.Button(id="logout-button", n_clicks=0, children="Log Out", className="logout2"),
               href='https://financial8999.herokuapp.com/logout/'),
        html.Img(src="/assets/stock-icon.png"),
        # html.Img(src= dashapp1.get_asset_url('stock-icon.png'))
    ], className="banner"),
    html.Div([
        dcc.Dropdown(id='drop-down', options=[
            {'label': i, 'value': i} for i in df_names
        ], value=ticker, multi=False, placeholder='Enter a ticker'),
    ], className='drops'),
    dcc.Tabs(id="tabs", value='Tab4', className='custom-tabs-container', children=[
        dcc.Tab(label='Financial Statements', id='tab2', value='Tab2', selected_className='custom-tab--selected',
                children=[]),
        dcc.Tab(label='Intrinsic value estimations', id='tab3', value='Tab3', selected_className='custom-tab--selected',
                children=[]),
        dcc.Tab(label='Machine learning', id='tab4', value='Tab4', selected_className='custom-tab--selected', children=[
        ]),
    ]),
    html.Div(id='dynamic-content'),
    html.Div([
        html.Div([  # modal div
            html.Div([  # content div
                html.Img(
                    id='modal-close-button',
                    src="/assets/times-circle-solid.svg",
                    # html.Img(src= dashapp1.get_asset_url('stock-icon.png'))
                    n_clicks=0,
                    className='info-icon2',
                    style={'margin': 0},
                ),
                html.Div(
                    children=[
                        dcc.Markdown(dedent('''
                        The Income Statement has been simplified by dividing by 1,000,000.

                        _**SGA**_ - Companies that do not have competitive advantage suffer from intense competition 
                        showing wild variation in SGA (selling, general and administrative) costs as a percentage of 
                        gross profit. 

                        _**R&D**_ - Companies that spend heavily on R&D have an inherent flaw in their competitive 
                        advantage that will always put their long term economics at risk since what seems like long 
                        term competitive advantage is bestowed by a patent or technological advancement that will 
                        expire or be replaced by newer technologies. Furthermore, since they constantly have to 
                        invest in new products they must also redesign and update sales programs increasing 
                        administrative costs. 

                        _**A&D**_ – Machinery and equipment eventually wear out over time with the amount they 
                        depreciate each year deducted from gross profit. Depreciation is a real cost of doing 
                        business because at some point in the future the printing press will need to be replaced. 

                        _**Interest Expense**_ – Interest paid out during the year is reflective of the total debt that 
                        a company is carrying on its books. It can be very informative as to the level of economic 
                        danger a company is in. Generally speaking, in any given industry, the company with the 
                        lowest ratio of interest payments to operating income has some kind of competitive advantage. 

                         _**Pre Tax Income**_ – This is the number Warren Buffet uses when calculating the return 
                         he’ll be getting from a business as all investments are marketed on a pre tax basis. Since 
                         all investments compete with each other, it is easier to think about them on equal terms. 

                         _**Net Income**_ – Must have a historical uptrend with consistent earnings. Share 
                         repurchasing increase per share earnings by decreasing the shares outstanding – while a lot 
                         of analysts look at per share earnings, Warren Buffet looks at the business as a whole and 
                         its net earnings to see what is actually happening. 


                    '''))]
                ),

            ],
                style={'textAlign': 'center', },
                className='modal-content',
            ),
        ], id='modal', className='modal', style={"display": "none"}),
        html.Div([  # modal div
            html.Div([  # content div
                html.Img(
                    id='modal-close-button2',
                    src="/assets/times-circle-solid.svg",
                    # html.Img(src= dashapp1.get_asset_url('stock-icon.png'))
                    n_clicks=0,
                    className='info-icon2',
                    style={'margin': 0},
                ),
                html.Div(
                    children=[
                        dcc.Markdown(dedent('''

                    _**Gross Profit Margin**_ - Companies with excellent economics and high profit margins tend to 
                    have a durable competitive advantage as they have the freedom to price their products well in 
                    excess of costs of goods sold. Without competitive advantage companies have too compete by 
                    lowering their prices of products or service they are selling. As a general rule 40% or better 
                    tend to have durable competitive advantage 

                    _**SGA of Gross Profit**_ – Anything under 30% of gross profit is considered fantastic. However, 
                    there are lots of companies with durable competitive advantage that have SGA expenses in 30-80%. 

                    _**D&A of Gross Profit**_ – Companies with durable competitive advantage have low depreciation 
                    costs e.g. Coca Cola at 6% compared to GM at 22-57%. 

                    _**Interest of Operating Income**_ – Warren Buffet’s favourite durable competitive advantage 
                    holders in the consumer products category have interest pay-outs of less than 15% of operating 
                    income. This changes from industry to industry e.g Wells Fargo has 30% of operating income on 
                    interest because it’s a bank. 

                    _**Tax**_ – Check how much a company pays in taxes. Businesses that are busy misleading the IRS 
                    are usually hard at work misleading their shareholders as well. Companies with long term 
                    competitive advantage make so much money it doesn’t have to mislead anyone to look good. 

                    _**Net Income to Revenue**_ – A company showing net earnings history of more than 20% of revenue 
                    is likely to be benefitting from durable competitive advantage long term. If under 10% it may not 
                    have competitive advantage but 10-20% are lots of good businesses ripe for the mining long term 
                    investment gold. E.g Coca Cola with 21%, Moody’s with 31% compared with Southwest Airlines with a 
                    meagre 7% which reflects the highly competitive nature of the airline business. 

                    Although an exception to this is banks and financial institutions where abnormally high ratios is 
                    seen as a slacking off for the risk management department and acceptance of greater risk for 
                    easier money. 

                    '''))]
                ),

            ],
                style={'textAlign': 'center', },
                className='modal-content',
            ),
        ], id='modal2', className='modal', style={"display": "none"}),
        html.Div([  # modal div
            html.Div([  # content div
                html.Img(
                    id='modal-close-button3',
                    src="/assets/times-circle-solid.svg",
                    # html.Img(src= dashapp1.get_asset_url('stock-icon.png'))
                    n_clicks=0,
                    className='info-icon2',
                    style={'margin': 0},
                ),
                html.Div(
                    children=[
                        dcc.Markdown(dedent('''

                    _**Cash & Short-term Investments**_ – A low amount or lack of cash stockpile usually means that the 
                    company has poor or mediocre economics. Companies that have a surplus of cash resulting from 
                    ongoing business activities, little or no debt, no new sales of shares or assets and a history of 
                    consistent earnings probably have excellent economics and competitive advantage working in their 
                    favour. If we see a lot of cash and marketable securities with little to no debt, chances are the 
                    business will sail through troubled times. 

                    _**Property plant and equipment**_ (net accumulated depreciation) – Companies that are in constant 
                    competition constantly have to update their manufacturing facilities to try to stay competitive 
                    often before equipment is already worn out. This creates an ongoing expense that is often quite 
                    substantial and keeps adding to the amount of plant and equipment the company lists on its 
                    balance sheet. A company with durable competitive advantage doesn’t need to constantly upgrade 
                    its plant and equipment to stay competitive. Instead it replaces equipment as they wear out. PP&E 
                    depreciates in value over time. 

                    _**Short term debts**_ – Money owed and due within a year is historically cheaper than long term 
                    money. Institutions make money by borrowing short term and lending long term but the problem with 
                    this is money borrowed in the short term needs to be payed off. This works fine until short term 
                    rates jump above what we leant long term. This makes aggressive borrowers of short-term money at 
                    the mercy of sudden shifts in the credit market. Smartest and safest way to make money is borrow 
                    money long term and lend it long term.  Warren does not invest in companies with lots of 
                    short-term debt. E.g Wells Fargo has $0.57 of short-term debt to every dollar of long-term debt 
                    compared to Bank of America who has $2.09. 

                    _**Long term debt**_ – Some companies lump it with short term debt which creates the illusion 
                    that the company has more short-term debt then it actually does. As a rule, companies with 
                    durable competitive advantage have little to no long-term debt. 

                    Sometimes an excellent business with a consumer monopoly will add large amounts of debt to 
                    finance the acquisition of another business, if so check the acquisition is also a consumer 
                    monopoly – when two combine lots of excess profits quickly reduce these debt mountains but when a 
                    consumer monopoly acquires a commodity business it will only suck out profits to support its poor 
                    economics. 

                    _**Treasury shares**_ – Shares set aside that can be brought back for additional funding and reduces 
                    the number of shares owned by private investors lowering the amount that must be paid out in 
                    dividends. If a company feels the market has undervalued its business, it might buy back some 
                    shares possibly reissuing once the price has been corrected. Reducing the number of shares boosts 
                    certain ratios as a form of financial engineering such as earnings per share which causes short 
                    term investors to flock back to stock seeing improved ratios increasing share price. 

                    _**Retained Earnings**_ – Net Income can either be paid out as a dividend, used to buy back 
                    company shares or it can be retained to keep the business growing. When income is retained it is 
                    put on the balance sheet under shareholders equity and when they are profitability used, 
                    they can greatly improve the long-term economic picture of the business. 

                    It is an accumulated number which means each year new retained earnings are added to the total 
                    accumulated retained earnings years prior. This is one of the most important metrics when 
                    determining if a business has durable competitive advantage – if a company is not adding to its 
                    retained earnings pool it is not growing its long term net worth and is unlikely to make you 
                    super rich long term. 

                    Not all growth in retained earnings is due to incremental increases in sales of existing 
                    products, some off it is due to the acquisition of other businesses. When two companies merge, 
                    their retained earnings pools are joined which creates an even larger pool. 

                    _**Leverage**_ – using debt to increase earnings of a company can give of the illusion of 
                    competitive advantage. The problem is while there seems to be some consistency in the income 
                    stream the source paying the interest payments may not be able to maintain these payments – just 
                    look at the sub prime lending crisis where banks borrowed billions at 6% and loaned at 8% to 
                    homebuyers but when the economy started to slip these buyers started to default on mortgages. 

                    These subprime borrowers did not have a durable source of income which ultimately meant 
                    investment banks didn’t have either. 

                    In assessing the quality and durability of a company’s competitive advantage, Warren Buffet 
                    avoids businesses that use a lot of leverage to generate earnings – in the short run they appear 
                    to be the goose that lays the golden egg but at the end of the day they are not. _**“Only when 
                    the tide goes out do you discover who's been swimming naked.”**_ 

                    '''))]
                ),

            ],
                style={'textAlign': 'center', },
                className='modal-content',
            ),
        ], id='modal3', className='modal', style={"display": "none"}),
        html.Div([  # modal div
            html.Div([  # content div
                html.Img(
                    id='modal-close-button4',
                    src="/assets/times-circle-solid.svg",
                    # html.Img(src= dashapp1.get_asset_url('stock-icon.png'))
                    n_clicks=0,
                    className='info-icon2',
                    style={'margin': 0},
                ),
                html.Div(
                    children=[
                        dcc.Markdown(dedent('''

                    The reason cash flow statements were implemented is it provides more clarity to where earnings 
                    are being used such as towards buying assets and paying off debts. Furthermore, 
                    selling shares/bonds can also contribute to cash flow but isn’t listed on the income statement. 
                    Shares bought in other companies and the dividend produced are on the cash flow statement. There 
                    are also unaccounted expenditures which are not on the income statement but are on the cash flow 
                    statement such as paying off bond holder coupons or buying back shares in the company. 

                    If cash from operations exceeds net income, the company is said to have high quality 
                    earnings-implying it is operating efficiently. 

                    The bottom line is that if a company is consistently generating more money that it is using it 
                    will potentially be able to do a number of useful things with the surplus such as: increase 
                    dividend payments, paying off existing debts, reducing its expenditure on interest payments and 
                    repurchasing shares. 

                    _**Capital Expenditure**_ – Buying a new track for your company is a capital expenditure, 
                    the value of the truck will be expensed through depreciation over its life time but the gasoline 
                    is a current expense with the full price deducted from the income during the current year. 

                    If CAPEX remains high over a number of years, they start to have a deep impact on earnings. 
                    Warren has said that this is the reason that he never invested in telephone companies, 
                    the tremendous capital outlays in building out communication networks greatly hamper their 
                    long-term economics. 

                    When looking at capital expenditures we simply add a company’s total CAPEX over a ten-year period 
                    and compare the figure with the companies net earnings for the same ten-year period. If a company 
                    is historically using less than 50% of its annual net earnings for CAPEX, it is a good place to 
                    start to look for durable competitive advantage. If it consistently using less than 25% then it 
                    more then likely has durable competitive advantage. As a rule, a company with durable competitive 
                    advantage uses a smaller portion of its earnings for capital expenditures for continuing 
                    operations. 

                    Coca Cola over the last 10 years earned a total of $20.21 per share while only using $4.01 per 
                    share or 19% of its total net earnings. If CAPEX is greater then earnings this means the company 
                    is being financed by debt. 

                    _**D&A**_ – Depreciation and Amortisation + non cash items have already been accounted for 
                    through deductions on the income statement. To get a true representation of the cash flow in the 
                    business we must we add back the cash reserved for this. 

                    _**Δ Working Capital**_ – Working capital is defined as current assets minus current liabilities.
                     It is positive if the company has more current assets or decreased current liabilities. 
                     It is negative if the company has less current assets and more current liabilities which affect
                      the cash flow in the business. 

                    _**Δ Receivables**_ – If net receivables on the balance sheet decreases this means some receivables
                     have been turned into cash therefore being a positive number on the cash flow statement.
                      If net receivables increased then more of the net income is on credit therefore to reflect cash 
                      outstanding it must be deducted. If there are large net receivable deductions this could be a sign
                       of a commodity business as most of the company’s income is on credit which is unfavourable. 

                    _**Δ Inventory**_ – If Inventory levels have increased like seen on balance sheet this figure will 
                    be negative as cash has flowed out of the business to pay for the inventory. If inventory decreased
                     annually then then it will be positive as cash flowed into the business via selling the inventory.

                    _**Δ Accounts payable**_ helps boost the cash on hand the company has by having preferable payment
                     terms suggesting competitive advantage and trust between partners. 

                    _**Cash from investing**_ – The money used to buy more supplies, upgrade facilities, build buildings
                    , purchase stock, bonds and other companies. This figure should be negative as these are
                     expenditures showing investments have been bought. If positive it means the company sold some of
                      its investments contributing to positive cash flow. 

                    _**Cash from financing**_ – Raise money or repurchase equity (shares) or bonds or give out 
                    dividends. If you see a positive number it means the company has sold bonds but incurred debt which
                     is not a good thing. This should be a negative number as it shows bonds and shares have been 
                     bought back which increases the value of your stake and reduces debt in the company. 

                    _**Net change in cash**_ – If largely positive it could suggest the company is going to conduct an 
                    acquisition. 
                    '''))]
                ),

            ],
                style={'textAlign': 'center', },
                className='modal-content',
            ),
        ], id='modal4', className='modal', style={"display": "none"}),
    ])  # hidden divs
])
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
