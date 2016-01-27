from googlefinance import getQuotes
import json
import urllib2
import pprint


from yahoo_finance import Share

class Stock_Info:
    def __init__(self, symbol):
        self._symbol = symbol
        self._quote = 0
        self._name = ""
        self._offline = 0
        self._PE = 0
        self._PS = 0
        self._PB = 0
        self._open = 0
        self._change = 0

        if not self._offline:
            self._yahoo = Share(symbol)
            
    def update_quote(self):
            try:
                self._quote = self._yahoo.get_price()
                self._change = self._yahoo.get_change()
                self._name = "ONLINE NAME N/A-  " + self._symbol
                self._PE = self._yahoo.get_price_earnings_ratio()
                self._PS = self._yahoo.get_price_sales()
                self._PB = self._yahoo.get_price_book()
                self._open = self._yahoo.get_open()
            except:
                print "Couldn't Refresh Data"
                self._quote = -1.00
                self._open = -1.00
                self._name = "OFFLINE - " + self._symbol
                return

            if (self._PE != None): self._PE = float(self._PE)
            if (self._PS != None): self._PS = float(self._PS)
            if (self._PB != None): self._PB = float(self._PB)
            

    def get_historical1(self, start, end):
        try:
            rtndata = self._yahoo.get_historical(start, end)
        except:
            print "Couldn't Fetch Data"
            rtndata = []
        return rtndata
    def get_change(self):
        return self._change
    def get_PE(self):
        return self._PE
    def get_PS(self):
        return self._PS
    def get_PB(self):
        return self._PB
    
    def get_open(self):
        return self._open
    
    def get_name(self):
        return self._name
    
    def get_symbol(self):
        return self._symbol
       
    def read_quote(self):
        print
        print '{:>20}  {:>20}'.format("Symbol:", self._symbol)
        print '{:>20}  {:>20}'.format("Quote:", self._quote)

    def get_quote(self):
        return self._quote

def overview(stock):
    stock.update_quote()
    print
    print '{:>20}  {:>20}'.format("Symbol: ", str(stock.get_symbol()))
    print '{:>20}  {:>20}'.format("Price: ", str(stock.get_quote()))
    print '{:>20}  {:>20}'.format("Change: ", str(stock.get_change() + "%"))
    print '{:>20}  {:>20}'.format("Price Earnings: ", str(stock.get_PE()))
    print '{:>20}  {:>20}'.format("Price Sales: ", str(stock.get_PS()))
    print '{:>20}  {:>20}'.format("Price Book: ", str(stock.get_PB()))
    breakdown(stock)

def breakdown(stock):
    print
    print "Breakdown..."
    PB = stock.get_PB()
    PE = stock.get_PE()
    printed = False
    if(PB != None):
        print "------------------------------------------------------------------------------"
        printed = True
        if (PB < 1 ):
            print
            print "The PB is less than 1..."
            print
            print "A lower P/B ratio could mean that the stock is undervalued."
            print "However, it could also mean that something is fundamentally wrong with the company. This varies by industry."
        if (PB > 1):
            print "The PB is more than 1..."
            print
            print "MEANING UNKNOWN!"
    if(PE != None):
        print "------------------------------------------------------------------------------"

        printed = True
        if (0 < PE <= 22.5):
            print "The PE is lower than average (22.5)..."
            print
            print "A low P/E can indicate either that a company may currently be undervalued, or that the company is doing exceptionally well relative to its past trends."

        elif ( PE > 22.5 ):
            print "The PE is higher than average (22.5) ..."
            print
            print "In general, a high P/E suggests that investors are expecting higher earnings growth in the future compared to companies with a lower P/E."

    if printed: print "------------------------------------------------------------------------------"

def testing(): 
    print "Starting Tests..."
    print
    #print "Offline Test..."
    #test1 = Stock_Info("CBA.AX")
    #overview(test1)
    #print
    #print "Online Test..."
    #test2 = Stock_Info("CBA.AX")
    #overview(test2)
    #print
    #print "Online Test 2..."
    #test3 = Stock_Info("NAB.AX")
    #overview(test3)

    while(True):
        company = Stock_Info(str(input("Enter a symbol [ASX] : ")) + ".AX")
        overview(company)
        print
        print "Here is this weeks breakdown: "
        test1 = company.get_historical1('2016-01-20', '2016-01-27')
        unpack_historic(test1)

def unpack_historic(list_data):
    for day in list_data:
        date = day["Date"]
        close = day["Close"]
        print str(date) + ": " + str(close)
        
def main():
    testing()

if __name__ == '__main__':
    main()



    
