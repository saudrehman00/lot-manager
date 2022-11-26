#!/usr/bin/python3

import sys
from inquirer import list_input,prompt,Text
def newLotFloorValidation(answers,current):
    return (current.isdigit() and int(current) >0 and int(current) <= 26)
    # return isinstance(current,int)

def newLotSpaceValidation(answers,current):
    return (current.isdigit() and int(current) >0 and int(current) <= 150)


choice = list_input("What would you like to do:",choices = ["Create New Lot","View Lot Usages","View Lot Billing","Update Rates","Quit"])
while choice != "Quit":
    match choice:
        case "Create New Lot":
            newLotQuestions = [
                Text(name="lotname", message="What would you like to call this parking lot:"),
                Text(name="parkingFloors",message="How many floors does your parking lot have:",validate=newLotFloorValidation),
                Text(name="parkingSpaces",message="How many spaces are there on each floor of your parking lot:",validate=newLotSpaceValidation)
            ]
            print(prompt(newLotQuestions))
        case "View Lot Usages":
            print(2)
        case "View Lot Billing":
            print(3)
        case "Update Rates":
            print(4)
        case _:
            print("Something Went wrong in the application")
            sys.exit(1)

    choice = list_input("What would you like to do:",choices = ["Create New Lot","View Lot Usages","View Lot Billing","Quit"])


print("Have a nice day!")