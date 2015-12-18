from googlefinance import getQuotes
import json

class Share:
    def __init__(self, market, symbol, pprice, units, commission):
        self._market = market
        self._symbol = symbol
        self._purchase_price = pprice
        self._units = units
        self._commission = commission
        self._purchasecost = self._purchase_price*self._units + self._commission
        self._quote = ""
        

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
        self._gainloss = self._currentworth/self._purchasecost * 100 - 100
        self._gainloss = round(self._gainloss, 2)

    def read_quote(self):
        print
        print '{:>20}  {:>20}'.format("Market:", self._market)
        print '{:>20}  {:>20}'.format("Symbol:", self._symbol)
        print '{:>20}  {:>20}'.format("Last Trade & :", self._LastTradeWithCurrency)
        print '{:>20}  {:>20}'.format("Last Trade DateTime:", self._LastTradeDateTime)
        print '{:>20}  {:>20}'.format("Last Trade Price:", self._LastTradePrice)
        print '{:>20}  {:>20}'.format("Last Trade Time:", self._LastTradeTime)
        print '{:>20}  {:>20}'.format("Last Trade:", self._LastTradeDateTimeLong)
        print '{:>20}  {:>20}'.format("ID:", self._ID)
        
    def read_quote_simple(self):
        print
        print '{:>20}  {:>20}'.format("Symbol:", self._symbol)
        print '{:>20}  {:>20}'.format("Last Trade Price:", self._LastTradePrice)
        print '{:>20}  {:>20}'.format("Last Trade:", self._LastTradeDateTimeLong)

    def get_quote(self):
        return self._quote
    def get_basic(self):
        self.updatequote()
        return '{:>20}:  {:>20}'.format(self._symbol, self._LastTradePrice)
    def print_summary(self):
        self.updatequote()
        print'{:>0}  {:>10}  {:>10}   {:>10}   {:>10}'.format(self._symbol, self._LastTradePrice, self._purchasecost, self._currentworth, self._gainloss)

    def get_profit(self):
        self._profit = self._currentworth - self._purchasecost
        return self._profit
    def get_purchasecost(self):
        return self._purchasecost
        
        
shares = {}   
def ownsummary():
    print "Set Market: ASX"
    print ("Setting Shares")
    market = "ASX"
    shares["AGL"] = Share("ASX","AGL", 15.186, 56.0, 0.0)
    
    shares["CBA"] = Share("ASX","CBA", 92.500, 10.0, 0.0)
    shares["NAB"] = Share("ASX","NAB", 39.050, 22.0, 0.0)
    shares["RIO"] = Share("ASX","RIO", 56.233, 15.0, 0.0)
    shares["SUN"] = Share("ASX","SUN", 14.158, 60.0, 0.0)
    shares["TLS"] = Share("ASX","TLS", 6.282, 135.0, 0.0)
    shares["WOR"] = Share("ASX","WOR", 11.387, 163.0, 0.0)

    owned_shares = [shares["CBA"], shares["NAB"], shares["RIO"], shares["SUN"], shares["CBA"], shares["TLS"], shares["WOR"]]

    print ("Getting Quotes...")
    print
    print ("Current Quotes:")
    print
    print "Overview:"
    print

    print '{:>0}  {:>10}  {:>10}   {:>10}   {:>10}'.format("Symbol", "Current","P. Cost", "C. Value", "Gain/Lost" )
    totalprofit = 0
    totalcost = 0
    for share in owned_shares:
        share.print_summary()
        totalprofit += share.get_profit()
        totalcost += share.get_purchasecost()

    print
    print '{:>0}  {:>10}AUD  {:>10}%'.format("Total Profit:", round(totalprofit,2), round(totalprofit / totalcost * 100, 2)) 

ownsummary()
