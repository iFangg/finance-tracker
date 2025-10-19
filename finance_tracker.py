import requests
import csv
from datetime import datetime, date
import os
import typing

now = datetime.today()
year = now.year
month = now.month

# Create yearly csv
yearly_csv = f'./{year}/overview-{year}.csv'
if not os.path.exists(f"./{year}"):
    os.mkdir(f"{year}")
    with open(yearly_csv, "w") as f:
        writer = csv.writer(f, quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([year] + [''] + ["Finances"])
        writer.writerow(["Description"] + ["Amount"] + ["Date"] + ["Reference"] + ["Transaction ID"])
        print(f)


# Create monthly csv
monthly_csv = f"./{year}/{month}-{year}.csv"
if not os.path.exists(monthly_csv):
    with open(monthly_csv, "w") as f:
        writer = csv.writer(f, quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([year] + [month] + ["Finances"])
        writer.writerow(["Business"] + ["Description"] + ["Amount"] + ["Date"])
        print(f)

# Update sheets

class Finance:
    def __init__(self):
        self.business = ""
        self.description = ""
        self.amount = float(0)
        self.date = datetime.now()
    
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
            f"{'Amount:':<12} ${self.amount:.2f}\n"
            f"{'Date:':<12} {self.date}"
        )

variable_name = {
    0: "BUSINESS: ",
    1: "DESCRIPTION: ",
    2: "AMOUNT (e.g 100 | 10.00 | 29.35 | -99.21): ",
    3: "DATE (01/01/2001 | 1/1/2001 | Leave blank for today's date): ",
}

finance = Finance()
for step in range(4):
    variable = input(f"ENTER {variable_name[step]}")
    while variable is None or len(variable) <= 0:
        variable = input(f"ENTER {variable_name[step]}")

    match step:
        case 0:
            finance.setBusiness(variable)
        case 1:
            finance.setDescription(variable)
        case 2:
            finance.setAmount(round(float(variable), 2))
        case 3:
            finance.setDate((datetime.strptime(variable, "%d/%m/%Y") if variable else datetime.now()).strftime("%d/%m/%Y"))

finance.print()
    
# with open(monthly_csv, "a") as f_monthly, open(yearly_csv, "a") as f_yearly:
#     monthly_writer = csv.writer(f_monthly, quotechar='|', quoting=csv.QUOTE_MINIMAL)
#     yearly_writer = csv.writer(f_yearly, quotechar='|', quoting=csv.QUOTE_MINIMAL)

