#robo_advisor.py
# author: Samuel Nelson, feb 24 2020
# this program will automate the process of providing clients with stock trading options


# import packages
from dotenv import load_dotenv
import os
import json
import requests
#import pandas

#variables
user_input = ""
api_key = ""

#APP BEGINS
os.system('clear')


print("-------------------")
print("  STOCK INFO APP   ")
print("-------------------")

user_input = input("Please enter an IPO: ")

if user_input.isalpha():
    print("You entered:", user_input)
    os.environ["ALPHAVANTAGE_API_KEY"] = input("Please provide your API key: ")
    print("Your key is:", os.environ["ALPHAVANTAGE_API_KEY"])
else:
    print("You entered an invalid input. Please try again.")

