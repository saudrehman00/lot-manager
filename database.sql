SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

--
-- Database: `lotmanager`
--
CREATE DATABASE IF NOT EXISTS `lotmanager`;
USE `lotmanager`;

-- --------------------------------------------------------

--
-- Table structure for table `manager`
--

CREATE TABLE `manager` (
  `id` int(11) NOT NULL,
  `fullname` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `manager`
--

INSERT INTO `manager` (`id`, `fullname`, `username`, `password`) VALUES
(1, 'default', 'root', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8');

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
  `lotid` int(11) NOT NULL,
  `rate` decimal(10,2) NOT NULL,
  `overtimerate` decimal(10,2) NOT NULL,
  `effective` timestamp NOT NULL DEFAULT current_timestamp(),
  `expirydate` timestamp NULL DEFAULT NULL
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
  `validitystart` timestamp NOT NULL DEFAULT current_timestamp(),
  `paidtime` time NOT NULL,
  `validityEnd` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `manager`
--
ALTER TABLE `manager`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `parkinglot`
--
ALTER TABLE `parkinglot`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `rates`
--
ALTER TABLE `rates`
  ADD PRIMARY KEY (`id`),
  ADD KEY `lotid` (`lotid`);

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
-- AUTO_INCREMENT for table `manager`
--
ALTER TABLE `manager`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `parkinglot`
--
ALTER TABLE `parkinglot`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `rates`
--
ALTER TABLE `rates`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `userticket`
--
ALTER TABLE `userticket`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `rates`
--
ALTER TABLE `rates`
  ADD CONSTRAINT `rates_ibfk_1` FOREIGN KEY (`lotid`) REFERENCES `parkinglot` (`id`);

--
-- Constraints for table `userticket`
--
ALTER TABLE `userticket`
  ADD CONSTRAINT `userticket_ibfk_1` FOREIGN KEY (`lotid`) REFERENCES `parkinglot` (`id`);
COMMIT;
