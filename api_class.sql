-- phpMyAdmin SQL Dump
-- version 5.1.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jul 15, 2022 at 03:41 AM
-- Server version: 5.7.24
-- PHP Version: 8.0.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `api_class`
--
CREATE DATABASE IF NOT EXISTS `api_class` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `api_class`;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE IF NOT EXISTS `user` (
  `id` int(100) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `account` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

--
-- Table structure for table `product`
--

CREATE TABLE IF NOT EXISTS `product` (
  `name` varchar(100) NOT NULL,
  `price` int(100) NOT NULL,
  `amount` int(100) NOT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;


--
-- Table structure for table `cart`
--

CREATE TABLE IF NOT EXISTS `cart` (
  `order_id` int(100) NOT NULL AUTO_INCREMENT,
  `product_name` varchar(100) NOT NULL,
  `user_id` int(100) NOT NULL,
  `amount` int(100) NOT NULL,
  PRIMARY KEY (`order_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

--
-- ADD FOREIGN KEY for table `cart`
--

ALTER TABLE cart ADD FOREIGN KEY (product_name) REFERENCES product (name);
ALTER TABLE cart ADD FOREIGN KEY (user_id) REFERENCES user(id);

--
-- Dumping data for table `product`
--

INSERT INTO `product`  (`name`, `price`, `amount`) VALUES
('apple', 30, 999),
('banana', 20, 999),
('cherry', 200, 999),
('pear', 50, 999),
('orange', 10, 999),
('mango', 100, 999);


/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
