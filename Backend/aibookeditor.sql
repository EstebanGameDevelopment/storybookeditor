-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 25, 2024 at 05:47 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `aibookeditor`
--

-- --------------------------------------------------------

--
-- Table structure for table `analytics`
--

CREATE TABLE `analytics` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `date` int(11) NOT NULL,
  `data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`data`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `bookdata`
--

CREATE TABLE `bookdata` (
  `id` int(11) NOT NULL,
  `data` longblob NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `bookimages`
--

CREATE TABLE `bookimages` (
  `id` int(11) NOT NULL,
  `story` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `category` varchar(100) NOT NULL,
  `size` int(11) NOT NULL,
  `data` longblob NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `bookindex`
--

CREATE TABLE `bookindex` (
  `id` int(11) NOT NULL,
  `user` int(11) NOT NULL,
  `data` int(11) NOT NULL,
  `title` varchar(200) NOT NULL,
  `description` varchar(4000) NOT NULL,
  `category1` int(11) NOT NULL,
  `category2` int(11) NOT NULL,
  `category3` int(11) NOT NULL,
  `time` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `bookpublish`
--

CREATE TABLE `bookpublish` (
  `id` int(11) NOT NULL,
  `data` mediumblob NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `booksounds`
--

CREATE TABLE `booksounds` (
  `id` int(11) NOT NULL,
  `story` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `category` varchar(100) NOT NULL,
  `extension` varchar(10) NOT NULL,
  `size` int(11) NOT NULL,
  `data` mediumblob NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `bookspeech`
--

CREATE TABLE `bookspeech` (
  `id` bigint(11) NOT NULL,
  `story` int(11) NOT NULL,
  `chapter` int(11) NOT NULL,
  `page` int(11) NOT NULL,
  `data` mediumblob NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `bookvideos`
--

CREATE TABLE `bookvideos` (
  `id` int(11) NOT NULL,
  `story` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `category` varchar(100) NOT NULL,
  `size` int(11) NOT NULL,
  `data` longblob NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `facebook`
--

CREATE TABLE `facebook` (
  `id` bigint(20) NOT NULL,
  `facebook` varchar(100) NOT NULL,
  `user` bigint(20) NOT NULL,
  `friends` varchar(5000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `forms`
--

CREATE TABLE `forms` (
  `id` int(11) NOT NULL,
  `email` varchar(100) NOT NULL,
  `registered` int(11) NOT NULL,
  `size` int(11) NOT NULL,
  `data` blob NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `profile`
--

CREATE TABLE `profile` (
  `id` bigint(20) NOT NULL,
  `user` bigint(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `address` varchar(500) NOT NULL,
  `description` varchar(5000) NOT NULL,
  `data` text NOT NULL,
  `autorun` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `sessionprompts`
--

CREATE TABLE `sessionprompts` (
  `id` int(11) NOT NULL,
  `session` varchar(200) NOT NULL,
  `mode` int(11) NOT NULL,
  `llm` varchar(200) NOT NULL,
  `command` varchar(200) NOT NULL,
  `data` mediumblob NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` bigint(20) NOT NULL,
  `email` varchar(100) NOT NULL,
  `nickname` varchar(100) NOT NULL,
  `password` varchar(500) NOT NULL,
  `platform` varchar(1000) NOT NULL,
  `registerdate` int(11) NOT NULL,
  `lastlogin` int(11) NOT NULL,
  `admin` int(11) NOT NULL,
  `code` varchar(100) NOT NULL,
  `validated` int(11) NOT NULL,
  `ip` varchar(300) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `analytics`
--
ALTER TABLE `analytics`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `bookdata`
--
ALTER TABLE `bookdata`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `bookimages`
--
ALTER TABLE `bookimages`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `bookindex`
--
ALTER TABLE `bookindex`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `bookpublish`
--
ALTER TABLE `bookpublish`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `booksounds`
--
ALTER TABLE `booksounds`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `bookspeech`
--
ALTER TABLE `bookspeech`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `bookvideos`
--
ALTER TABLE `bookvideos`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `facebook`
--
ALTER TABLE `facebook`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `forms`
--
ALTER TABLE `forms`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `profile`
--
ALTER TABLE `profile`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `sessionprompts`
--
ALTER TABLE `sessionprompts`
  ADD UNIQUE KEY `id` (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
