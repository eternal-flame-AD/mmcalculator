import csv
import calc
class Equation:
    def __init__(self,symbol,symbols,mass,name):
        self.items=[(symbol,1)]    #should be like [('Mn',1),('Fe',2)]
        self.symbols=symbols
        self.mass=mass
        self.name=name
    
    def parse_whole_chemical(self,string):
        mult=""
        pos=0
        while isdigit(string[pos]):
            mult+=string[pos]
            pos+=1
        if mult=="":
            mult="1"
        return (string[pos:],int(mult))
    
    def split_dots(self):
        target=self.items[0]
        self.items=[]
        string=target[0].replace("·",'.')
        while True:
            try:
                pos=string.index('.')
                self.items.append(self.parse_whole_chemical(string[0:pos]))
                string=string[pos+1:]
            except ValueError:
                break
        self.items.append(self.parse_whole_chemical(string))
    
    def split_paren(self):
        items_new=[]
        items_old=self.items
        for item in items_old:
            string=item[0]
            mult=item[1]
            chemical_now=""
            in_paren=False
            pos=0
            while pos<len(string):
                char=string[pos]
                if char=='(':
                    assert in_paren==False,"'(' met, ')' expected"
                    items_new.append((chemical_now,mult))
                    chemical_now=""
                    in_paren=True
                elif char==")":
                    assert in_paren==True,"')' met, '(' expected"
                    digit=""
                    while ((pos+1<len(string)) and (isdigit(string[pos+1]))):
                        digit+=string[pos+1]
                        pos+=1
                    if digit=="":
                        digit="1"
                    items_new.append((chemical_now,mult*int(digit)))
                    chemical_now=""
                else:
                    chemical_now+=char
                pos+=1
            if chemical_now!="":
                items_new.append((chemical_now,mult))
        self.items=items_new
    
    def split_symbols(self):
        items_new=[]
        items_old=self.items
        for item in items_old:
            string=item[0]
            mult=item[1]
            pos=0
            while pos<len(string):
                if (pos+1<len(string)) and issymbol(string[pos:pos+2],self.symbols):
                    this_symbol=string[pos:pos+2]
                    pos+=2
                    digit=""
                    while (pos<len(string)) and isdigit(string[pos]):
                        digit+=string[pos]
                        pos+=1
                    if digit=="":
                        digit="1"
                    items_new.append((this_symbol,mult*int(digit)))
                elif issymbol(string[pos],self.symbols):
                    this_symbol=string[pos]
                    pos+=1
                    digit=""
                    while (pos<len(string)) and isdigit(string[pos]):
                        digit+=string[pos]
                        pos+=1
                    if digit=="":
                        digit="1"
                    items_new.append((this_symbol,mult*int(digit)))
                elif string[pos]==" ":
                    pos+=1
                else:
                    raise ValueError("ERR:Unsplittable expression:",string)
        self.items=items_new
    
    def dump(self):
        for item in self.items:
            print(item)
    
    def calculate_mass(self):
        sum=0
        for item in self.items:
            this=getmass(item[0],self.mass)*item[1]
            sum+=this
            print('{0:<3}'.format(better_looking_symbol(item[0])),'{0:<10}'.format(getname(item[0],self.name)),'\t',getmass(item[0],self.mass),'g/mol\t * ',item[1],'\t = ',this,'\taccumulate:',sum)
        print("==================================================================")
        print("Total mass=",sum,"g/mol")
    
    def digest(self):
        self.split_dots()
        self.split_paren()
        self.split_symbols()
        self.calculate_mass()

def better_looking_symbol(s):
    if len(s)==1:
        return s[0].upper()
    else:
        return s[0].upper()+s[1:].lower()

def issymbol(string,symbols):
    for item in symbols:
        if symbol_ident(string,item):
            return True
    return False

def isdigit(s):
    return ((s>='0') and (s<='9'))

def getmass(s,mass):
    for item in mass:
        if symbol_ident(item[0],s):
            return item[1]
    raise ValueError("ERR:Unknown symbol:",s)

def getname(s,name):
    for item in name:
        if symbol_ident(item[0],s):
            return item[1]
    raise ValueError("ERR:Unknown symbol:",s)

def readcsv(fn):
    readfile=open(fn)
    return csv.DictReader(readfile)

def parse(equ,symbols,mass,name):
    target=Equation(equ,symbols,mass,name)
    target.digest()

def init():
    data=readcsv('data.csv')
    symbols=[]
    mass=[]
    name=[]
    for row in data:
        symbols.append(row['symbol'])
        mass.append((row['symbol'],float(row['mass'])))
        name.append((row['symbol'],row['name']))
    return symbols,mass,name

def symbol_ident(s1,s2):
    return s1.upper()==s2.upper()

def reader(symbols,mass,name):
    while True:
        equ=input('Pls provide a chemical formula, enter exit to stop:')
        try:
            equ.index('exit')
            break
        except:
            if equ[0:5]=="calc ":
                calc.main(equ[5:])
            else:
                parse(equ,symbols,mass,name)

symbols,mass,name=init()
reader(symbols,mass,name)