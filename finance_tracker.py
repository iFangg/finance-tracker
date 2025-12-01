import requests
import csv
from datetime import datetime, date
import os
import typing

now = datetime.today()
currentYear = now.year
currentMonth = now.month

# Create yearly csv
def createYearlyCsv(year = currentYear):
    yearly_csv = f'./{year}/overview-{year}.csv'
    if not os.path.exists(f"./{year}"):
        os.mkdir(f"{year}")
        with open(yearly_csv, "w") as f:
            writer = csv.writer(f, quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([year] + [''] + ["Finances"])
            writer.writerow(["Description"] + ["Amount"] + ["Date"] + ["Reference"] + ["Transaction ID"])
            print(f)
    
    return yearly_csv


# Create monthly csv
def createMonthlyCsv(month = currentMonth, year = currentYear):
    monthly_csv = f"./{year}/{month}-{year}.csv"
    if not os.path.exists(monthly_csv):
        with open(monthly_csv, "w") as f:
            writer = csv.writer(f, quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([year] + [month] + ["Finances"])
            writer.writerow(["Business"] + ["Description"] + ["Amount"] + ["Date"])
            print(f)
    
    return monthly_csv

createYearlyCsv()
createMonthlyCsv()


# Update csvs
def updateCsvs(finance, month = currentMonth, year = currentYear):
    currentMonthCsv = createMonthlyCsv(month, year)
    currentYearCsv = createYearlyCsv(year)

    with open(currentMonthCsv, "a") as f_monthly, open(currentYearCsv, "a") as f_yearly:
        monthly_writer = csv.writer(f_monthly, quotechar='|', quoting=csv.QUOTE_MINIMAL)
        yearly_writer = csv.writer(f_yearly, quotechar='|', quoting=csv.QUOTE_MINIMAL)

        monthly_writer.writerow([finance.getBusiness()] + [finance.getDescription()] + [finance.getAmount()] + [finance.getDate()])
        yearly_writer.writerow([finance.getBusiness()] + [finance.getDescription()] + [finance.getAmount()] + [finance.getDate()])


# Update sheets

class Finance:
    def __init__(self):
        self.business = ""
        self.description = ""
        self.amount = float(0)
        self.date = datetime.now()

    def getBusiness(self):
        return self.business

    def getDescription(self):
        return self.description

    def getAmount(self):
        return '{0:.2f}'.format(self.amount)
    
    def getDate(self):
        return self.date

    def getSplitDate(self):
        # formatted by DAY - MONTH - YEAR
        # splitDate = self.date.split('/')
        return self.date.split('/')
    
    def setBusiness(self, business):
        assert isinstance(business, str), f"Business variable must be a string, got {type(business).__name__}"
        self.business = business
    
    def setDescription(self, description):
        assert isinstance(description, str), f"Description variable must be a string, got {type(description).__name__}"
        self.description = description
    
    def setAmount(self, amount):
        assert isinstance(amount, float), f"Amount variable must be a number (float), got {type(amount).__name__}"
        self.amount = amount
    
    def setDate(self, set_date):
        assert isinstance(set_date, str), f"Date variable must be a string, got {type(set_date).__name__}"
        self.date = set_date
    
    def print(self):
        print(
            f"----- Finance Object -----\n"
            f"{'Business:':<12} {self.business}\n"
            f"{'Description:':<12} {self.description}\n"
            f"{'Amount:':<12} {'-' if self.amount < 0 else ''}${abs(self.amount):.2f}\n"
            f"{'Date:':<12} {self.date}"
        )

variable_name = {
    0: "BUSINESS: ",
    1: "DESCRIPTION: ",
    2: "AMOUNT (e.g 100 | 10.00 | 29.35 | -99.21): ",
    3: "DATE (01/01/2001 | 1/1/2001 | Leave blank for today's date): ",
}

class Steps:
    BUSINESS = 0
    DESCRIPTION = 1
    AMOUNT = 2
    DATE = 3

while True:
    try:
        finance = Finance()
        for step in range(4):
            variable = input(f"ENTER {variable_name[step]}")

            match step:
                case Steps.BUSINESS:
                    finance.setBusiness(variable if variable else "NOT PROVIDED")
                case Steps.DESCRIPTION:
                    finance.setDescription(variable if variable else "NO DESCRIPTION PROVIDED")
                case Steps.AMOUNT:
                    finance.setAmount(round(float(variable), 2) if variable else float(0))
                case Steps.DATE:
                    date = variable
                    splitInput = variable.split("/")
                    if variable is None or len(variable) <= 0:
                        date = datetime.now()

                    elif len(splitInput) == 2 or len(splitInput[2]) <= 0:
                        date = datetime.strptime(f'{splitInput[0]}/{splitInput[1]}/{currentYear}', "%d/%m/%Y")

                    finance.setDate(date.strftime("%d/%m/%Y"))

        financeDate = finance.getSplitDate()
        finance.print()
        
        updateCsvs(finance, financeDate[1], financeDate[2])


    except EOFError:
        print("Exiting...")
        break
    

