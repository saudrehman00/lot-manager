# lot-manager

## Connect to VM
ssh azureuser@172.174.77.42 -i \<pathtopem>
pem file is in the outer directory

## Manager Terminal
To run the manager application run managerclient.py.

This requires the above packages along with ManagerPortal and ManagerParkingLot

\* default username is "root" and password is "password" *

## Client Terminal
To run the user facing application run main.py.

This requires ParkingLot and UserTicket.


\* Cloud db will be shut down on December 25. Please complete evaluation before then. database.sql contains a script to create a local instance of the db for further testing *