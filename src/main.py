import mariadb
import MySQLdb
import os
import sys
from dotenv import load_dotenv
from tabulate import tabulate 
from datetime import datetime
from ParkingLot import ParkingLot
from UserTicket import UserTicket
from inquirer import list_input,prompt,Text,Checkbox,List,Password


def main(): 

    parkingLot = None
    global parkingLotName
    global parkingFloor
    global parkingSpot
    carNumber = ''
    ticket = None


    load_dotenv()

    # SQL Connection - 
    try:
        conn = MySQLdb.connect(
            user=os.environ['dbuser'],
            password=os.environ['dbpswd'],
            host=os.environ['dbhost'],
            port=3306,
            database='lotmanager'
        )
    except MySQLdb.Error as e:
        print(f"Error connecting to  Platform: {e}")
        sys.exit(1)

    connection = conn.cursor(MySQLdb.cursors.DictCursor)
    connection.execute("SELECT * FROM parkinglot;")
    cur = conn.cursor()
    print('\n')


    # User menu choices -
    choice = list_input("What would you like to do:", 
            choices = ["View Parking Lot Info",
                       "Choose A Parking Spot",
                       "Extend Parking Time", 
                       "Exit", 
                       "Quit"])
    
    while choice != "Quit":
        match choice:

            #Option 1: View parking lot information.
            case "View Parking Lot Info":
                parkingSpaces = []
                viewParkingLotInfoStatement = "SELECT * FROM parkinglot;"
                cur.execute(viewParkingLotInfoStatement)
                for (id, name, numfloors, numspaces) in cur:
                    parkingSpaces.append([name, numfloors, numspaces])
                print("\n")
                print(tabulate(parkingSpaces, headers=["Parking Lot", "Floors", "Spaces Availble"]))
                print("\n")


            # #Option 2: Choose a parking spot

            # case "Choose A Parking Spot":

                # Choice variables
                # parkingLots = []
                # chosenLot = []
                # lot = None
                # spotsAvailable = False

                # # See all parking lots to select from
                # getParkingLots = "SELECT name FROM parkinglot;"
                # cur.execute(getParkingLots)

                # for (name) in cur: 
                #     parkingLots.append(name[0])
                # chooseLotQuestions = [
                #     Checkbox(name="lotnames",message="What lot are you at", choices = parkingLots)
                # ]

                # for cLot in prompt(chooseLotQuestions)['lotnames']:
                #     parkingLotName = cLot

                # # Get chosen parking lot information
                # cur.execute(f"SELECT id, name, numfloors, numspaces FROM parkinglot WHERE name={parkingLotName};")
                
                # for (id, name, numfloors, numspaces) in cur :
                #     chosenLot.append([name, numfloors, numspaces])
                #     lot = ParkingLot(id, name, numfloors, numspaces)
                #     break

                # print('Lot chosen: ', parkingLotName, '\n')
                # print(tabulate(chosenLot, headers=["Parking Lot", "Floors", "Total Spaces"]))
                # print('\n')



                # # Select Floor from parkingLot
                # def getParkingFloor ():
                #     global parkingFloor
                #     while True:
                #         try:
                #             floor = int(input(f"What floor do you want to park on? - please choose from 1 - {chosenLot[0][1]}"))
                #         except ValueError:
                #             print(f"Please enter a valid integer 1-{chosenLot[0][1]}")
                #             continue
                #         if floor >= 1 and floor <= chosenLot[0][1]:
                #             parkingFloor = floor
                #             print(f'You entered: {floor}')
                #             break
                #         else:
                #             print(f'The integer must be in the range 1-{chosenLot[0][1]}')

                
                # getParkingFloor()
                # fullSpots = lot.getFullSpaces(parkingFloor)


                # if (len(fullSpots)) == 0:
                #     print ("All spots are empty.\n")
                # else:
                #     print("The following spots are taken:" ,"\n", fullSpots)
     
                # spot = int(input("Please choose a spot to park in?"))
                # while(type(spot)!= int or spot > lot.numspaces or spot < 0):
                #     print("Please enter a valid spot")                
                # parkingSpot = spot

                # # Validate Parking Spots
                # while(not lot.validateParkingSpot(fullSpots, parkingFloor, parkingSpot)):
                #     print("Spot not available")
                #     getParkingFloor()
                #     # floor = input("What floor do you want to park on?")
                    
                #     # while(type(floor)!= str or floor > lot.numfloors):
                #     #     print("Please enter a valid floor")
                #     #     floor = int(input("What floor do you want to park on?"))
                #     spot = input("What spot do you want to park in?")
                #     while(type(spot)!= int or spot > numspaces or spot < 0):
                #         print("Please enter a valid spot")
                               
                # # Time    
                # amountTime = int(input("How many hours do you want to buy?"))
                # while(type(amountTime)!=int):
                #     print("Please enter a valid amount of time")
                #     amountTime = int(input("How many hours do you want to buy?"))


                # currentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                # newTime = datetime.now().replace(hour=datetime.now().time().hour + amountTime).strftime('%Y-%m-%d %H:%M:%S') 
                # validTime = datetime.now().time().replace(hour=amountTime,minute=0,second=0).strftime('%H:%M:%S')
                # ticket = UserTicket(lot.id, parkingFloor, parkingSpot, currentTime, validTime, newTime)
                # print(ticket)
                # lot.chargeCustomer(ticket.id)
                print('done')
            
            case "Choose A Parking Spot":
                # Choice variables
                parkingLots = []
                chosenLot = []
                lot = None
                spotsAvailable = False

                # See all parking lots to select from
                getParkingLots = "SELECT name FROM parkinglot;"
                cur.execute(getParkingLots)

                for (name) in cur: 
                    parkingLots.append(name[0])
                chooseLotQuestions = [
                    Checkbox(name="lotnames",message="What lot are you at", choices = parkingLots)
                ]

                for cLot in prompt(chooseLotQuestions)['lotnames']:
                    parkingLotName = cLot

                # Get chosen parking lot information
                cur.execute(f"SELECT id, name, numfloors, numspaces FROM parkinglot WHERE name={parkingLotName};")
                    
                for (id, name, numfloors, numspaces) in cur :
                    chosenLot.append([name, numfloors, numspaces])
                    lot = ParkingLot(id, name, numfloors, numspaces)
                    break

                print('Lot chosen: ', parkingLotName, '\n')
                print(tabulate(chosenLot, headers=["Parking Lot", "Floors", "Total Spaces"]))
                print('\n')        

                # Select Floor from parkingLot
                def getParkingFloor ():
                    global parkingFloor
                    while True:
                        try:
                            floor = int(input(f"What floor do you want to park on? - please choose from 1 - {chosenLot[0][1]}"))
                        except ValueError:
                            print(f"Please enter a valid integer 1-{chosenLot[0][1]}")
                            continue
                        if floor >= 1 and floor <= chosenLot[0][1]:
                            parkingFloor = floor
                            print(f'You entered: {floor}')
                            break
                        else:
                            print(f'The integer must be in the range 1-{chosenLot[0][1]}')

                # Select Parking Spot
                def getParkingSpot():
                    global parkingFloor
                    global parkingSpot
                    fullSpots = lot.getFullSpaces(parkingFloor)
                    if (len(fullSpots)) == 0:
                        print ("All spots are empty.\n")
                    else:
                        print("The following spots are taken:" ,"\n", fullSpots)
                            
                    while True:
                        try:
                            spot = int(input(f"Please choose a parking spot from 1 - {chosenLot[0][2]}"))
                        except ValueError:
                            print(f"Please enter a valid integer 1-{chosenLot[0][2]}")
                            continue
                            
                        if spot < 1 or spot > chosenLot[0][2]:
                            print(f'The integer must be in the range 1-{chosenLot[0][2]}')
                        else:
                            parkingSpot = spot
                            print(f'You chose spot: {spot}')

                            break
                                
                getParkingFloor()
                getParkingSpot()
                fullSpots = lot.getFullSpaces(parkingFloor)

                print(parkingSpot)
                print(parkingFloor)
                # Validate Parking Spots
                while(not lot.validateParkingSpot(fullSpots, parkingFloor, parkingSpot)):
                    print("Spot not available")
                    getParkingFloor()
                    getParkingSpot()
                               
                # Time     
                amountTime = int(input("How many hours do you want to buy?"))
                while(type(amountTime)!=int):
                    print("Please enter a valid amount of time")
                    amountTime = int(input("How many hours do you want to buy?"))

                currentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                newTime = datetime.now().replace(hour=datetime.now().time().hour + amountTime).strftime('%Y-%m-%d %H:%M:%S') 
                validTime = datetime.now().time().replace(hour=amountTime,minute=0,second=0).strftime('%H:%M:%S')

                cur.execute(f"SELECT MAX(id) FROM userticket;")
                ticketId = 0
                for (id) in cur:
                    print(id[0])
                    ticketId = id[0]
                print(type(ticketId))
                print("ticketID: ", ticketId)
                ticket = UserTicket(ticketId + 1, lot.id, parkingFloor, parkingSpot, currentTime, validTime, newTime)
                print(ticket)
                print('done')

            #Option 3: Extend Ticket Time
            case "Extend Parking Time":
                addTime = int(input("How much time do you want to add?"))

                while(not type(addTime) == int):
                    print("Please enter a valid number")
                    addTime = input("How much time do you want to add?") 
                
                ticket.updatePaidTime(addTime)
                print("Your time has been added")

            #Option 4: Exit
            case "Exit":
                if ticket == None:
                    print("You don't have a ticket")
                    continue
                else:
                    # ticket.deleteTicket()
                    lot.chargeCustomer(lot.id)
                    print("Have a great day")

        choice = list_input("What would you like to do:", choices = ["View Parking Lot Info","Choose A Parking Spot","Extend Parking Time", "Exit", "Quit"])
                   
main()