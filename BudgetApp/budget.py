from sre_parse import CATEGORIES


class Category:
    def __init__(self, name, ledger = None):
        self.name = name
        if ledger is None :
            self.ledger = []

    def __str__(self) : 
        i=0
        asteriskNumber = 30 -len(self.name) #get rid of this for a single string literal that centers in 30 on *
        if asteriskNumber % 2 != 0 : 
            leaderAsterisk = asteriskNumber - 1
            trailingAsterisk = asteriskNumber + 1
        else : 
            leaderAsterisk = asteriskNumber /2
            trailingAsterisk = asteriskNumber / 2

        title = "*" * int(leaderAsterisk) + self.name + "*" * int(trailingAsterisk)
        total = self.get_balance()
        return str(title + "\n" + "\n".join(f"{x.description :<23.23} {x.amount:>7}" for x in self.ledger ) + "\n" + "Total: " + str(total)   )
            
        
    
    def deposit(self,amount, description = None) : # this is the deposit method
        if description is None : 
                description = ""
        class LedgerItem:   
            def __init__(self, amount, description):
                self.amount = amount
                self.description = description

        ledgerItem = LedgerItem(amount, description)
        self.ledger.append(ledgerItem)
        return

    def withdraw(self, amount, description = None): #this is the withdraw method
        if description is None : 
            description = ""
        
        if  self.check_funds(amount) : 
            self.deposit(amount * -1,description)
            return True
        else : 
            return False
            
        
    def get_balance(self): #this method gets the balance of the self object
        balance = 0
        for x in self.ledger : 
            balance = balance + x.amount
       
        return balance

    def transfer(self, amount, otherCategory) : #this is the transfer method. 
        if self.check_funds(amount) == False : 
            return False
        self.withdraw(amount, "transfer to " + otherCategory.name)
        otherCategory.deposit(amount, "transfer from " + self.name)
        return True
    def check_funds(self, amount): #this is the check fund method
        balance = 0
        for x in self.ledger : 
            balance = balance + x.amount
        if amount > balance :
            return False
        else :
            return True

        
def create_spend_chart(categories): #this is the chrat creating method
    
    chartTitle = "Percentage Spend by Category\n"
    chartBody = ["100|"," 90|",' 80|',' 70|',' 60|',' 50|',' 40|',' 30|',' 20|',' 10|','  0|']
    
    percentSpentList = []
    totalSpent = 0
    for x in categories:
        totalSpent = 0
        initialDeposit = x.ledger[0].amount
        for y in x.ledger : 
            if y.amount < 0: 
                totalSpent += y.amount
        percentSpentList.append(round(totalSpent*-1/initialDeposit,1) *100)
    
    for x in percentSpentList : 
        i = 100
        j = 0
        while i >=0:
            if i > x : 
                chartBody[j] = chartBody[j] + "  "
            elif i <= x : 
                chartBody[j] = chartBody[j]+ "o "
            i -= 10
            j += 1
    def transposeCategories(categories) : #this mehod takes the categories them to strings that are vertical for display purposes
        catNameList = []
        transposedCategories = []
        for x in categories :
            catNameList.append(x.name)
        i = max(catNameList, key = len)
        i = len(i)
        j = 0
        
        while i > 0: 
            catString = ""
            for x in catNameList : 
                try : 
                    catString = catString +  x[j] + " "
                except : 
                    catString += "  "
            j += 1
            i-= 1
            transposedCategories.append(catString)
                

        return transposedCategories
    def buildXAxis(chartBody) : #this method builds the Xaxis based on the length of the chartbody string. 
        xAxis = "   "
        i = len(chartBody[1]) - 3
        while i >= 0 :
            xAxis += "-"
            i-= 1
        return xAxis
    xAxis = buildXAxis(chartBody)
    transposedCategories = transposeCategories(categories)
    chart = chartTitle + "\n" + "\n".join(chartBody)+ "\n" + xAxis + "\n    " + "\n    ".join(transposedCategories)    
    return chart