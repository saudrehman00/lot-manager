-- phpMyAdmin SQL Dump
-- version 5.2.0-1.fc36
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Nov 26, 2022 at 06:48 PM
-- Server version: 10.5.16-MariaDB
-- PHP Version: 8.1.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `lotmanager`
--
DROP DATABASE IF EXISTS `lotmanager`;
CREATE DATABASE IF NOT EXISTS `lotmanager` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `lotmanager`;

-- --------------------------------------------------------

--
-- Table structure for table `parkinglot`
--

CREATE TABLE `parkinglot` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `numfloors` int(11) NOT NULL,
  `numspaces` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `rates`
--

CREATE TABLE `rates` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `rate` decimal(10,0) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `userticket`
--

CREATE TABLE `userticket` (
  `id` int(11) NOT NULL,
  `lotid` int(11) NOT NULL,
  `floor` varchar(2) NOT NULL,
  `spacenumber` int(11) NOT NULL,
  `validitystart` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `paidtime` time NOT NULL,
  `validityEnd` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `parkinglot`
--
ALTER TABLE `parkinglot`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `userticket`
--
ALTER TABLE `userticket`
  ADD PRIMARY KEY (`id`),
  ADD KEY `lotid` (`lotid`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `parkinglot`
--
ALTER TABLE `parkinglot`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `userticket`
--
ALTER TABLE `userticket`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `userticket`
--
ALTER TABLE `userticket`
  ADD CONSTRAINT `userticket_ibfk_1` FOREIGN KEY (`lotid`) REFERENCES `parkinglot` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
