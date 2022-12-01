import mariadb
import sys
from datetime import datetime
from ParkingLot import ParkingLot
from UserTicket import UserTicket
def main():    
    try:
        conn = mariadb.connect(
            user="root",
            password="password",
            host="localhost",
            port=3306,
            database="lotmanager"

        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    # Get Cursor
    cur = conn.cursor()

    location = input("What Lot Are You At?\n")
    
    cur.execute(
    "SELECT id, name, numfloors, numspaces FROM parkinglot WHERE name=?", 
    (location,))

    for (id, name, numfloors, numspaces) in cur:
        lot = ParkingLot(id, name, numfloors, numspaces)
    print(lot.id, lot.name, lot. numfloors, lot.numspaces)


    fullSpots = lot.getFullSpaces()
    print("The following spots are taken:" ,"\n", lot.getFullSpaces())

    floor = input("What floor do you want to park on?")
    spot = input("What spot do you want to park in?")

    while(not lot.validateParkingSpot(fullSpots, floor, spot)):
        print("Spot not available")
        floor = input("What floor do you want to park on?")
        spot = input("What spot do you want to park in?")


    amountTime = int(input("How many hours do you want to buy?"))
    ticket = None

    currentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    newTime = datetime.now().replace(hour=datetime.now().time().hour + amountTime).strftime('%Y-%m-%d %H:%M:%S')
    # print("Current Time is ", currentTime)
    # print("Adding Time: ", amountTime)
    validTime = datetime.now().time().replace(hour=amountTime,minute=0,second=0).strftime('%H:%M:%S')
    # print(validTime)
    ticket = UserTicket(1,lot.id, 1, 1, currentTime, validTime, newTime)
    ticket.getFullSpaces()
    # ticket.createTicket()
    # ticket.updatePaidTime(2)
    lot.chargeCustomer()
    

   

    

main()