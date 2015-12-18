from googlefinance import getQuotes
import json

class Share:
    def __init__(self, market, name, symbol, catergory, pprice, units, commission):
        self._market = market
        self._name = name
        self._symbol = symbol
        self._catergory = catergory
        self._purchase_price = pprice
        self._units = units
        self._commission = commission
        self._purchasecost = self._purchase_price*self._units + self._commission
        self._quote = ""
        self._LastTradePrice = 0       

    def updatequote(self):
        #get quotes and format
        quotes = json.dumps(getQuotes(self._market + ":" + self._symbol))
        quotes = quotes[2:-2]
        quoteitems = quotes.split("\",")

        #def containers
        item = {}
        splits = []

        
        for quote in quoteitems:
            quote = quote.replace('\"', "").strip()
            splits.append(quote.split(":", 1))      
        
        split = []
        for split in splits:
            for i, item in enumerate(split):
                split[i] = item.replace("\'", "").strip()
        self._quote = splits
        self._LastTradeWithCurrency = splits[1][1]
        self._LastTradeDateTime = splits[2][1]
        self._LastTradePrice = float(splits[3][1])
        self._LastTradeTime = splits[4][1]
        self._LastTradeDateTimeLong = splits[5][1]
        self._ID = splits[7][1]
        self._currentworth = self._LastTradePrice*self._units
        if self._purchasecost != 0:
            self._gainloss = self._currentworth/self._purchasecost * 100 - 100
            self._gainloss = round(self._gainloss, 2)
        else:
            self._gainloss = 0

    def get_symbol(self):
        return self._symbol
    
    def read_quote(self):
        print
        print '{:>20}  {:>50}'.format("Market:", self._market)
        print '{:>20}  {:>50}'.format("Name:", self._name)
        print '{:>20}  {:>50}'.format("Symbol:", self._symbol)
        print '{:>20}  {:>50}'.format("Last Trade & :", self._LastTradeWithCurrency)
        print '{:>20}  {:>50}'.format("Last Trade DateTime:", self._LastTradeDateTime)
        print '{:>20}  {:>50}'.format("Last Trade Price:", self._LastTradePrice)
        print '{:>20}  {:>50}'.format("Last Trade Time:", self._LastTradeTime)
        print '{:>20}  {:>50}'.format("Last Trade:", self._LastTradeDateTimeLong)
        print '{:>20}  {:>50}'.format("ID:", self._ID)
        
    def read_quote_simple(self):
        print
        print '{:>20}  {:>20}'.format("Symbol:", self._symbol)
        print '{:>20}  {:>20}'.format("Last Trade Price:", self._LastTradePrice)
        print '{:>20}  {:>20}'.format("Last Trade:", self._LastTradeDateTimeLong)

    def get_quote(self):
        return self._quote
    def get_basic(self):
        return '{:>20}:  {:>20}'.format(self._symbol, self._LastTradePrice)
    def print_summary(self):
        print'{:>0}  {:>10}  {:>10}   {:>10}   {:>10}'.format(self._symbol, self._LastTradePrice, self._purchasecost, self._currentworth, self._gainloss)

    def get_profit(self):
        self._profit = self._currentworth - self._purchasecost
        return self._profit
    def get_purchasecost(self):
        return self._purchasecost
    def get_price(self):
        return self._LastTradePrice

    
f = open('ASXCompanies.txt', 'r')
companies = f.read()
f.close()
print companies
companysplit = companies.split("\n")
companydict = {}
companylist = []

for company in companysplit:
    details = company.split(",")
    companylist.append(details[1])
    newcompany = Share("ASX",details[0], details[1], details[2], 0, 0, 0)
    companydict[details[1]] = newcompany
#Company name,ASX code,GICS industry group
def listallcompaniesASX():
    for company in companylist:
        try: 
            companydict[company].updatequote()
            print companydict[company].get_basic()
        except:
            print (company + " didn't work.")
            
def quote(company):
    companydict[company].updatequote()
    companydict[company].read_quote()

quote("WOR")
