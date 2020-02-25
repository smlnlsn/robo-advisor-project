#robo_advisor.py
# author: Samuel Nelson, feb 24 2020
# this program will automate the process of providing clients with stock trading options


# import packages
from dotenv import load_dotenv
import os
import json
import requests
import pandas
#from alpha_vantage.timeseries import TimeSeries


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
        if len(user_input) >= 6:
            length_check = input("Your IPO code is pretty long. Are you sure it's correct? (Y/N): ")
        
        if length_check.upper() == "Y":
            print("You entered:", user_input)
            #os.environ["ALPHAVANTAGE_API_KEY"] = input("Please provide your API key: ")
            load_dotenv()
            key = os.environ["ALPHAVANTAGE_API_KEY"]
            print("Your key is:", key)
            print("---------------\n")

            request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=" + user_input + "&interval=5min&outputsize=full&apikey=" + key
            response = requests.get(request_url)
            stock_data = json.loads(response.text)
            print(stock_data['Meta Data'])
    elif user_input == "000":
        print("Thank you for using the STOCK INFO APP. Goodbye!")
    else:
        print("You entered an invalid input. Please try again.")
    user_input = input("Please enter an IPO or \"000\" to quit: ")
