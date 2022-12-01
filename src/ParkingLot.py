# Module Imports
import mariadb
import sys


# Sample class with init method
class ParkingLot:
 
    # init method or constructor
    def __init__(self, id, name, numfloors, numspaces):
        self.id = id
        self.name = name
        self.numfloors = numfloors
        self.numspaces = numspaces

        try:
            self.conn = mariadb.connect(
                user="root",
                password="password",
                host="localhost",
                port=3306,
                database="lotmanager"
        )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
        self.cur = self.conn.cursor()

    def chargeCustomer(self):
        self.cur.execute(
            "SELECT rate FROM rates WHERE lotid=?", (self.id,))
        rates = self.cur.fetchone()
        for (rate) in rates:
            parkingRate = rate
        
        print("Please make a payment of $" , parkingRate)

    def getFullSpaces(self):
        self.cur.execute(
            "SELECT floor, spacenumber FROM userticket")
        spaces = self.cur.fetchall()

        spaceList = []
        for(space) in spaces:
            spaceList.append((space[0],space[1]))
        
        return spaceList

    def validateParkingSpot(self, takenSpaces, floor, spot):
        parkingSpot = (floor, int(spot))
        
        if parkingSpot not in takenSpaces:
            return True
        else:
            return False
        
    



