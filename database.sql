IF db_id('parkingLot') IS NULL 
    CREATE DATABASE parkingLot

GO

CREATE DATABASE IF NOT EXISTS parkinglot ;
USE parkingLot;

CREATE TABLE customer(
    vehicleId int
); 

GO

CREATE TABLE parkingMachine ( 
    machineID int PRIMARY KEY,
    avaiableSpot tinyint,
    rate int
); 

GO

CREATE TABLE pakringManager (
    managerID int PRIMARY KEY,
    managerPassword varchar(100)
); 