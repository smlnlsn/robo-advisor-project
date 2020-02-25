#robo_advisor.py
# author: Samuel Nelson, feb 24 2020
# this program will automate the process of providing clients with stock trading options


# import packages
from dotenv import load_dotenv
import os
import json
import requests
import pandas as pd
import datetime
import ast
#from alpha_vantage.timeseries import TimeSeries

def find_high(data):
    return 0
        
def find_low(data):
    return 0

def recommendation(data):
    return 0

#variables
user_input = ""
key = ""
request_url = ""
length_check = "Y"

#APP BEGINS
os.system('clear')


print("-------------------")
print("  STOCK INFO APP   ")
print("-------------------")

user_input = input("Please enter an IPO: ")

while user_input != "000": 
    if user_input.isalpha():
        length_check = "Y"
        stock_data = ""
        if len(user_input) >= 6:
            length_check = input("Your IPO code is pretty long. Are you sure it's correct? (Y/N): ")
        if length_check.upper() == "Y":
            print("You entered:", user_input)
            user_input = user_input.upper()
            #os.environ["ALPHAVANTAGE_API_KEY"] = input("Please provide your API key: ")
            load_dotenv()
            key = os.environ["ALPHAVANTAGE_API_KEY"]
            print("Your key is:", key)
            print("---------------\n")
            output_size = "compact"
            request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + user_input + "&outputsize=" + output_size + "&apikey=" + key
            response = requests.get(request_url)
            time_of_request = datetime.datetime.now()
            stock_data = json.loads(response.text)

            if "Error Message" in stock_data.keys():
                print("Something went wrong.")
                print(stock_data["Error Message"])
            else:
                df = pd.DataFrame(stock_data)
                file_path = "./data/prices_" + user_input.lower() + ".csv"
                df.to_csv(r"%s" % file_path)
                
                last_refreshed = stock_data['Meta Data']['3. Last Refreshed']
                latest_day = '2020-02-24' #TO-DO: make dynamic
                latest_close = stock_data['Time Series (Daily)'][latest_day]['4. close']

                recent_high = find_high(stock_data)
                recent_low = find_low(stock_data)

                #recommendation
                rec = recommendation(stock_data)

                #output
                print("-------------------------")
                print("SELECTED SYMBOL:", stock_data['Meta Data']['2. Symbol'])
                print("-------------------------")
                print("REQUESTING STOCK MARKET DATA...")
                print("REQUEST AT:", time_of_request.ctime() )
                print("-------------------------")
                print("LATEST DAY:", latest_day)
                print("LATEST CLOSE:", latest_close)
                print("RECENT HIGH:", recent_high)
                print("RECENT LOW:", recent_low)
                print("-------------------------")
                print("RECOMMENDATION:")
                print("RECOMMENDATION REASON:")
                print("-------------------------")
                print("HAPPY INVESTING!")
                print("-------------------------")
                
    elif user_input == "000":
        print("Thank you for using the STOCK INFO APP. Goodbye!")
    else:
        print("You entered an invalid input. Please try again.")
    user_input = input("Please enter an IPO or \"000\" to quit: ")
