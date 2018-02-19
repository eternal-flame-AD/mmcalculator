import csv
class Equation:
    def __init__(self,symbol,symbols):
        self.items=[(symbol,1)]    #should be like [('Mn',1),('Fe',2)]
        self.symbols=symbols
    def merge(self):
        count=[]
        for item in self.items:
            try:
                count[item[0]]+=item[1]
            except:
                count.append((item[0],item[1]))
        self.items=count
    def dump(self):
        for item in self.items:
            print(item)

def readcsv(fn):
    readfile=open(fn)
    return csv.DictReader(readfile)

def parse(equ,symbols):
    target=Equation(equ,symbols)
    target.merge()
    target.dump()

def init():
    data=readcsv('data.csv')
    symbols=[]
    for row in data:
        symbols.append(row['symbol'])
    return symbols

def symbol_ident(s1,s2):
    return s1.upper==s2.upper
def reader(symbols):
    while True:
        equ=input('Pls provide a chemical formula, enter exit to stop:')
        try:
            equ.index('exit')
            break
        except:
            parse(equ,symbols)

symbols=init()
reader(symbols)