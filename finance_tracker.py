import os
import csv
import json
from datetime import datetime, date

def path_exists(path, is_json = False, content = ""):
    file_content = ""
    if not os.path.exists(path):
        with open(path, "w", encoding='utf-8') as f:
            f.write(content)
    
            file_content = f.read()
            return json.loads(file_content) if is_json else file_content

saved_dir = "Saved_Finances"
os.makedirs(saved_dir, exist_ok=True)

# todo: Figure out a way to track multiple bills/finance objects under the same business
saved_json = path_exists(f"{saved_dir}/saved.json", True)
print(f"saved json: {saved_json}")
saved_aliases = path_exists(f"{saved_dir}/aliases.json", True)
print(f"saved aliases: {saved_aliases}")


now = datetime.today()
currentYear = now.year
currentMonth = now.month

# Create yearly csv
def create_yearly_csv(year = currentYear):
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
def create_monthly_csv(month = currentMonth, year = currentYear):
    monthly_csv = f"./{year}/{month}-{year}.csv"
    if not os.path.exists(monthly_csv):
        with open(monthly_csv, "w") as f:
            writer = csv.writer(f, quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([year] + [month] + ["Finances"])
            writer.writerow(["Business"] + ["Description"] + ["Amount"] + ["Date"])
            print(f)
    
    return monthly_csv

create_yearly_csv()
create_monthly_csv()


# Update csvs
def update_csvs(finance, month = currentMonth, year = currentYear):
    current_month_csv = create_monthly_csv(month, year)
    current_year_csv = create_yearly_csv(year)

    with open(current_month_csv, "a") as f_monthly, open(current_year_csv, "a") as f_yearly:
        monthly_writer = csv.writer(f_monthly, quotechar='|', quoting=csv.QUOTE_MINIMAL)
        yearly_writer = csv.writer(f_yearly, quotechar='|', quoting=csv.QUOTE_MINIMAL)

        finance_data = [finance.get_business()] + [finance.get_description()] + [finance.get_amount()] + [finance.get_date()]

        monthly_writer.writerow(finance_data)
        yearly_writer.writerow(finance_data)


# Update sheets

class Finance:
    def __init__(self):
        self.business = ""
        self.description = ""
        self.amount = float(0)
        self.date = datetime.now()

    def get_business(self):
        return self.business

    def get_description(self):
        return self.description

    def get_amount(self):
        return '{0:.2f}'.format(self.amount)
    
    def get_date(self):
        return self.date

    def get_splitdate(self):
        # formatted by DAY - MONTH - YEAR
        # splitDate = self.date.split('/')
        return self.date.split('/')
    
    def set_business(self, business):
        assert isinstance(business, str), f"Business variable must be a string, got {type(business).__name__}"
        self.business = business
    
    def set_description(self, description):
        assert isinstance(description, str), f"Description variable must be a string, got {type(description).__name__}"
        self.description = description
    
    def set_amount(self, amount):
        assert isinstance(amount, float), f"Amount variable must be a number (float), got {type(amount).__name__}"
        self.amount = amount
    
    def set_date(self, set_date):
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
        # implement flags and saving of recurring payments
        for step in range(4):
            variable = input(f"ENTER {variable_name[step]}")

            match step:
                case Steps.BUSINESS:
                    finance.set_business(variable if variable else "NOT PROVIDED")
                case Steps.DESCRIPTION:
                    finance.set_description(variable if variable else "NO DESCRIPTION PROVIDED")
                case Steps.AMOUNT:
                    finance.set_amount(round(float(variable), 2) if variable else float(0))
                case Steps.DATE:
                    date = variable
                    splitInput = variable.split("/")
                    if len(variable) <= 0:
                        date = datetime.now()

                    elif len(splitInput) == 2 or len(splitInput[2]) <= 0:
                        date = datetime.strptime(f'{splitInput[0]}/{splitInput[1]}/{currentYear}', "%d/%m/%Y")

                    finance.set_date(date.strftime("%d/%m/%Y"))

        financeDate = finance.get_splitdate()
        finance.print()
        
        update_csvs(finance, financeDate[1], financeDate[2])

        saveAsRecurring = input("Do you wish to save this as a recurring finance? y/N (No by default) ")
        saveAsRecurring = True if saveAsRecurring == "y" else False

        if saveAsRecurring:
            finance_name = finance.get_business()

            print(
                json.dumps({
                    f"{finance_name}": {
                        0: {
                            "Description": finance.get_description(),
                            "Amount": finance.get_amount(),
                        }
                    }
                })
            )
            if finance_name not in dict.keys(saved_json):
                saved_json.append({
                    finance_name: [
                        {
                            "Description": finance.get_description(),
                            "Amount": finance.get_amount()
                        }
                    ]
                })

            with open("Saved_Finances/saved.json", "a+", encoding='utf-8') as f:
                print()

            aliasesToSave = input("Enter aliases (separated by spaces) that this recurring payment can be saved under: ").split(" ")


    except EOFError:
        print("Exiting...")
        break
    

