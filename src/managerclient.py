#!/usr/bin/python3

import sys
import os
from dotenv import load_dotenv
from inquirer import list_input,prompt,Text,Checkbox,List,Password
from ManagerPortal import *

def newLotFloorValidation(answers,current):
    return (current.isdigit() and int(current) >0 and int(current) <= 26)
    # return isinstance(current,int)

def newLotSpaceValidation(answers,current):
    return (current.isdigit() and int(current) >0 and int(current) <= 150)

def rateValidation(answers,current):
    return current.replace('.','',1).isdigit()

load_dotenv()

loginQuestions = [
    Text(name="username",message="Username"),
    Password(name="password",message="Password")
]
loginData = prompt(loginQuestions)
lotManager = ManagerPortal(os.environ['dbhost'],os.environ['dbuser'],os.environ['dbpswd'],loginData['username'],loginData['password'])
choice = list_input("What would you like to do",choices = ["Create New Manager","Create New Lot","View Lot Usages","View Lot Rates","View Lot Past Month Revenue","Update Rates","Quit"])
while choice != "Quit":
    match choice:
        case "Create New Manager":
            newManagerQuestions = [
                Text(name="fullname",message="What is the name of the new manager"),
                Text(name="username",message="What is the username of the new manager"),
                Password(name="password",message="What is the password for the new manager"),
            ]
            newManagerData = prompt(newManagerQuestions)
            lotManager.createNewManager(newManagerData['fullname'],newManagerData['username'],newManagerData['password'])
        case "Create New Lot":
            newLotQuestions = [
                Text(name="lotname", message="What would you like to call this parking lot"),
                Text(name="parkingfloors",message="How many floors does your parking lot have",validate=newLotFloorValidation),
                Text(name="parkingspaces",message="How many spaces are there on each floor of your parking lot",validate=newLotSpaceValidation),
                Text(name="rate",message="What is the standard rate",validate=rateValidation),
                Text(name="overtimerate",message="What is the overtime rate",validate=rateValidation)
            ]
            newlotdata = prompt(newLotQuestions)
            lotManager.createNewLot(newlotdata['lotname'],newlotdata['parkingfloors'],newlotdata['parkingspaces'],newlotdata['rate'],newlotdata['overtimerate'])
        case "View Lot Usages":
            lotUsageQuestions = [
                Checkbox(name="lotnames",message="Which lots would you like to view the usage for",choices=lotManager.getLots())
            ]
            for lot in prompt(lotUsageQuestions)['lotnames']:
                print(f"{lot}: {lotManager.getOccupancy(lot)}%")

        case "View Lot Rates":
            lotRateQuestions = [
                Checkbox(name="lotnames",message="Which lots would you like to view the rates for",choices=lotManager.getLots())
            ]
            for lot in prompt(lotRateQuestions)['lotnames']:
                print(f"{lot}: {lotManager.getRate(lot)} {lotManager.getOvertimeRate(lot)}")
        case "View Lot Past Month Revenue":
            lotRateQuestions = [
                Checkbox(name="lotnames",message="Which lots would you like to view the rates for",choices=lotManager.getLots())
            ]
            for lot in prompt(lotRateQuestions)['lotnames']:
                print(f"{lot}: {lotManager.getRevenueGenerated(lot)}")
        
        case "Update Rates":
            if len(lotManager.getLots()):
                updateRateQuestions = [
                    List(name="lotname",message="Which lot would you like to update rates for",choices=lotManager.getLots()),
                    Checkbox(name="ratetype",message="Which rate would you like to update",choices=["Overtime","Standard"]),
                    Text(name="rate",message="What is the standard rate",validate=rateValidation,ignore=lambda x: "Standard" not in x['ratetype']),
                    Text(name="overtimerate",message="What is the overtime rate",validate=rateValidation,ignore=lambda x: "Overtime" not in x['ratetype'])
                ]
                updateratedata = prompt(updateRateQuestions)
                if len(updateratedata['ratetype']) == 1:
                    if "Standard" in updateratedata['ratetype']:
                        lotManager.setRate(updateratedata['lotname'],updateratedata['rate'])
                    if "Overtime" in updateratedata['ratetype']:
                        lotManager.setOvertimeRate(updateratedata['lotname'],updateratedata['overtimerate'])
                elif len(updateratedata['ratetype']) == 2:
                    lotManager.setBothRate(updateratedata['lotname'],updateratedata['rate'],updateratedata['overtimerate'])
                else:
                    pass
            else:
                print("You need to first create a lot to update rates")
        case _:
            print("Something Went wrong in the application")
            sys.exit(1)

    choice = list_input("What would you like to do",choices = ["Create New Manager","Create New Lot","View Lot Usages","View Lot Rates","View Lot Past Month Revenue","Update Rates","Quit"])


print("Have a nice day!")