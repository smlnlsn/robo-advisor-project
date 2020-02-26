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
import matplotlib.pyplot as plt
import numpy as np

def get_latest_day(data):
    l_day = sorted(data['Time Series (Daily)'])[-1]
    return l_day

def find_high(data):
    day = get_latest_day(data)[-2:]
    highest = float(data['Time Series (Daily)']['2020-02-' + day]['2. high'])
    for day in data['Time Series (Daily)'].values():
        if float(day['2. high']) > highest:
            highest = float(day['2. high'])
    return highest
        
def find_low(data):
    day = get_latest_day(data)[-2:]
    lowest = float(data['Time Series (Daily)']['2020-02-' + day]['3. low'])
    for day in data['Time Series (Daily)'].values():
        if float(day['3. low']) < lowest:
            lowest = float(day['3. low'])
    return lowest

def recommendation(data):
    global reason
    high = find_high(data)
    low = find_low(data)
    difference = high - low
    today_closing = float(data['Time Series (Daily)'][get_latest_day(data)]['4. close'])
    if today_closing < ((difference*0.2)+low):
        reason = "Closing price is relatively low."
        return "BUY"
    elif today_closing > (high-(difference*0.2)):
        reason = "Closing price is relatively high."
        return "SELL"
    reason = "Closing price is neither low nor high enough to buy or sell."
    return "NEITHER BUY OR SELL"

def to_usd(num):
    return str('$' + format(num, ',.2f'))

#variables
user_input = ""
key = ""
request_url = ""
length_check = "Y"
closing_prices = []

#APP BEGINS
os.system('clear')  


print("-------------------")
print("  STOCK INFO APP   ")
print("-------------------")


os.environ["ALPHAVANTAGE_API_KEY"] = input("Please provide your API key: ")
load_dotenv()
key = os.environ["ALPHAVANTAGE_API_KEY"]
print("---------------\n")

user_input = input("Please enter an IPO: ")

while user_input != "000": 
    if user_input.isalpha():
        length_check = "Y"
        stock_data = ""
        closing_prices = []
        #dates = [] #no longer used, enable if showing dates as ticks
        if len(user_input) >= 6:
            length_check = input("Your IPO code is pretty long. Are you sure it's correct? (Y/N): ")
        if length_check.upper() == "Y":
            print("You entered:", user_input)
            user_input = user_input.upper()
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
                latest_day = get_latest_day(stock_data)
                latest_close = float(stock_data['Time Series (Daily)'][latest_day]['4. close'])
                recent_high = float(find_high(stock_data))
                recent_low = float(find_low(stock_data))

                #recommendation
                rec = recommendation(stock_data)

                #for day in stock_data['Time Series (Daily)'].keys():
                #   dates.append(day)
                for day in stock_data['Time Series (Daily)'].values():
                    closing_prices.append(float(day['4. close']))
                
                #format plot
                plt.plot(closing_prices)
                plt.title("Last 100 days for " + user_input.upper())
                plt.axis([0,100,0,recent_high*1.2])
                plt.xlabel("Days Ago")

                #output
                print("-------------------------")
                print("SELECTED SYMBOL:", stock_data['Meta Data']['2. Symbol'])
                print("-------------------------")
                print("REQUESTING STOCK MARKET DATA...")
                print("REQUEST AT:", time_of_request.ctime() )
                print("-------------------------")
                print("LATEST DAY:", latest_day)
                print("LATEST CLOSE:", to_usd(latest_close))
                print("RECENT HIGH:", to_usd(recent_high))
                print("RECENT LOW:", to_usd(recent_low))
                print("-------------------------")
                plt.show()
                print("RECOMMENDATION:", rec)
                print("RECOMMENDATION REASON:", reason)
                print("-------------------------")
                print("HAPPY INVESTING!")
                print("-------------------------")
                
    elif user_input == "000":
        print("Thank you for using the STOCK INFO APP. Goodbye!")
    else:
        print("You entered an invalid input. Please try again.")
    user_input = input("Please enter an IPO or \"000\" to quit: ")
