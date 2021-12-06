import robin_stocks as robin
import pyotp
import json
from robin_stocks.robinhood.urls import currency_url

#Robinhood Authentication Prep
auth_keys = {}
with open('[insert directory to credentials file]') as authFile:
    for line in authFile:
        key, value = line.split()
        auth_keys[key] = value

#Robinhood Authentication
twofa = pyotp.TOTP(auth_keys['code']).now()
auth = robin.robinhood.authentication.login(auth_keys['username'], auth_keys['password'], store_session=False, mfa_code = twofa)

#Get full account history
def get_all():
    result = robin.robinhood.export.export_completed_option_orders('T:\Backups', file_name=None)
    
#Get current holdings
def get_holdings():

    print('SUMMARY OF STOCK POSITIONS:')
    stock_holdings = robin.robinhood.build_holdings()
    options_holdings = robin.robinhood.get_open_option_positions()

    #Parse responses
    stock_parse = json.dumps(stock_holdings)
    stocks = json.loads(stock_parse)
    option_parse = json.dumps(options_holdings)
    options = json.loads(option_parse)
    #print(option_parse)

    #Build lists for later use
    owned_shares = []
    unrealized_gains = []
    total_cost_basis = []
    
    #Loop through stock positions to massage data and do some calculation
    for k in stocks:
        
        cost_basis = float(stocks[k]['quantity']) * float(stocks[k]['average_buy_price'])
        unreal_gains = (float(stocks[k]['quantity']) * float(stocks[k]['price'])) - cost_basis
        print(k + ' |' , 'Shares: ', stocks[k]['quantity'], '| Cost Basis: $', cost_basis, '| Unrealized Gains: $', unreal_gains)
        
        owned_shares.append(k)
        total_cost_basis.append(cost_basis)
        unrealized_gains.append(unreal_gains)
    
    print('\r')
   
    #Loop through options chain information to massage data and do some calculation
    print('SUMMARY OF OPTIONS POSITIONS:')
    for i in range(len(options)):

        print(options[i]['chain_symbol'], '| Quantity:', options[i]['quantity'], '| Average Price', '$', options[i]['average_price'] )

    print('\r')
    print('SUMMARY OF ACCOUNT:')
    print('Total Cost Basis: ', '$', sum(total_cost_basis))
    print('Total Unrealized Gains:', '$', sum(unrealized_gains))

get_holdings()
