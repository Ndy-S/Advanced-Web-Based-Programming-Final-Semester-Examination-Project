-- phpMyAdmin SQL Dump
-- version 4.9.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Nov 20, 2022 at 06:08 AM
-- Server version: 8.0.17
-- PHP Version: 7.3.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `universitas`
--

-- --------------------------------------------------------

--
-- Table structure for table `dosen`
--

CREATE TABLE `dosen` (
  `dosen_id` int(11) NOT NULL,
  `jurusan_id` int(11) NOT NULL,
  `nama` varchar(50) DEFAULT NULL,
  `univ` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `dosen`
--

INSERT INTO `dosen` (`dosen_id`, `jurusan_id`, `nama`, `univ`) VALUES
(8, 2, 'Zaiful Bahri', 'Universitas Riau'),
(13, 2, 'Susi', 'Universitas Riau'),
(14, 1, 'Salsa', 'Universitas Riau');

-- --------------------------------------------------------

--
-- Table structure for table `jurusan`
--

CREATE TABLE `jurusan` (
  `jurusan_id` int(11) NOT NULL,
  `nama` varchar(50) NOT NULL,
  `max` int(11) NOT NULL,
  `count_dosen` int(11) NOT NULL,
  `count_mhs` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `jurusan`
--

INSERT INTO `jurusan` (`jurusan_id`, `nama`, `max`, `count_dosen`, `count_mhs`) VALUES
(1, 'Biologi', 10, 1, 3),
(2, 'Ilmu Komputer', 10, 2, 3),
(4, 'Fisika', 15, 0, 0),
(5, 'Matematika', 10, 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `mhs`
--

CREATE TABLE `mhs` (
  `mhs_id` int(11) NOT NULL,
  `dosen_id` int(11) NOT NULL,
  `jurusan_id` int(11) NOT NULL,
  `nama` varchar(50) NOT NULL,
  `universitas` varchar(50) NOT NULL,
  `angkatan` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `mhs`
--

INSERT INTO `mhs` (`mhs_id`, `dosen_id`, `jurusan_id`, `nama`, `universitas`, `angkatan`) VALUES
(5, 8, 2, 'Hendy Saputra', 'Universitas Riau', '2020'),
(7, 14, 1, 'Doni', 'Universitas Riau', '2019'),
(8, 14, 1, 'Gartanto', 'Universitas Riau', '2020'),
(9, 8, 2, 'Stella', 'Universitas Riau', '2020'),
(10, 8, 2, 'Siska', 'Universitas Riau', '2019'),
(11, 14, 1, 'Ratanto', 'Universitas Riau', '2019');

-- --------------------------------------------------------

--
-- Table structure for table `nilai`
--

CREATE TABLE `nilai` (
  `nilai_id` int(11) NOT NULL,
  `mhs_id` int(11) NOT NULL,
  `jurusan_id` int(11) NOT NULL,
  `dosen_id` int(11) NOT NULL,
  `angkatan` varchar(50) NOT NULL,
  `kehadiran` int(11) NOT NULL,
  `tugas` int(11) NOT NULL,
  `uts` int(11) NOT NULL,
  `uas` int(11) NOT NULL,
  `hasil` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `nilai`
--

INSERT INTO `nilai` (`nilai_id`, `mhs_id`, `jurusan_id`, `dosen_id`, `angkatan`, `kehadiran`, `tugas`, `uts`, `uas`, `hasil`) VALUES
(1, 5, 2, 8, '2020', 16, 90, 85, 83, 0),
(3, 8, 1, 14, '2020', 15, 90, 90, 95, 0),
(4, 9, 2, 8, '2020', 12, 50, 75, 40, 1),
(5, 10, 2, 8, '2019', 16, 100, 90, 97, 0),
(7, 7, 1, 14, '2019', 14, 88, 90, 87, 0),
(8, 11, 1, 14, '2019', 13, 30, 40, 25, 1);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `user_id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`user_id`, `username`, `email`, `password`) VALUES
(1, 'Hendy Saputra 2003113132', 'hendy.saputra3132@student.unri.ac.id', '1234567');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `dosen`
--
ALTER TABLE `dosen`
  ADD PRIMARY KEY (`dosen_id`);

--
-- Indexes for table `jurusan`
--
ALTER TABLE `jurusan`
  ADD PRIMARY KEY (`jurusan_id`);

--
-- Indexes for table `mhs`
--
ALTER TABLE `mhs`
  ADD PRIMARY KEY (`mhs_id`);

--
-- Indexes for table `nilai`
--
ALTER TABLE `nilai`
  ADD PRIMARY KEY (`nilai_id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `dosen`
--
ALTER TABLE `dosen`
  MODIFY `dosen_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `jurusan`
--
ALTER TABLE `jurusan`
  MODIFY `jurusan_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `mhs`
--
ALTER TABLE `mhs`
  MODIFY `mhs_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `nilai`
--
ALTER TABLE `nilai`
  MODIFY `nilai_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
