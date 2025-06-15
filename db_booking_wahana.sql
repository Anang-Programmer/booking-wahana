-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 14, 2025 at 02:42 PM
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
-- Database: `db_booking_wahana`
--

-- --------------------------------------------------------

--
-- Table structure for table `jadwal_wahana`
--

CREATE TABLE `jadwal_wahana` (
  `id` int(11) NOT NULL,
  `wahana_id` int(11) NOT NULL,
  `waktu_mulai` datetime NOT NULL,
  `waktu_selesai` datetime NOT NULL,
  `sisa_tiket` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `jadwal_wahana`
--

INSERT INTO `jadwal_wahana` (`id`, `wahana_id`, `waktu_mulai`, `waktu_selesai`, `sisa_tiket`) VALUES
(7, 1, '2025-06-12 10:00:00', '2025-06-12 10:30:00', 15),
(8, 1, '2025-06-12 10:30:00', '2025-06-12 11:00:00', 100),
(10, 2, '2025-06-12 11:20:00', '2025-06-12 11:40:00', 30),
(11, 3, '2025-06-12 13:00:00', '2025-06-12 13:15:00', 7),
(12, 3, '2025-06-12 13:15:00', '2025-06-12 13:30:00', 0),
(13, 1, '2025-06-12 22:09:00', '2025-06-26 22:09:00', 7);

-- --------------------------------------------------------

--
-- Table structure for table `pemesanan`
--

CREATE TABLE `pemesanan` (
  `id` int(11) NOT NULL,
  `pengguna_id` int(11) NOT NULL,
  `tanggal_pemesanan` timestamp NOT NULL DEFAULT current_timestamp(),
  `total_harga` decimal(10,2) NOT NULL,
  `status_pembayaran` enum('Menunggu','Lunas','Gagal') DEFAULT 'Menunggu'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `pemesanan`
--

INSERT INTO `pemesanan` (`id`, `pengguna_id`, `tanggal_pemesanan`, `total_harga`, `status_pembayaran`) VALUES
(1, 1, '2025-06-12 07:13:15', 0.00, 'Lunas'),
(2, 1, '2025-06-12 07:16:04', 0.00, 'Lunas'),
(4, 1, '2025-06-12 09:02:17', 0.00, 'Lunas'),
(5, 1, '2025-06-12 09:41:50', 0.00, 'Lunas'),
(6, 1, '2025-06-12 09:44:43', 0.00, 'Lunas'),
(7, 1, '2025-06-12 09:51:00', 0.00, 'Lunas'),
(24, 7, '2025-06-13 23:52:21', 0.00, 'Lunas'),
(25, 1, '2025-06-14 00:48:20', 0.00, 'Lunas'),
(26, 1, '2025-06-14 00:48:20', 0.00, 'Lunas'),
(27, 1, '2025-06-14 00:49:44', 0.00, 'Lunas'),
(28, 1, '2025-06-14 00:50:00', 0.00, 'Lunas'),
(29, 8, '2025-06-14 04:05:52', 0.00, 'Lunas'),
(30, 8, '2025-06-14 04:12:47', 0.00, 'Lunas'),
(31, 1, '2025-06-14 05:07:32', 0.00, 'Lunas');

-- --------------------------------------------------------

--
-- Table structure for table `pengguna`
--

CREATE TABLE `pengguna` (
  `id` int(11) NOT NULL,
  `nama_lengkap` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `tanggal_daftar` timestamp NOT NULL DEFAULT current_timestamp(),
  `role` varchar(20) NOT NULL DEFAULT 'user'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `pengguna`
--

INSERT INTO `pengguna` (`id`, `nama_lengkap`, `email`, `password_hash`, `tanggal_daftar`, `role`) VALUES
(1, 'Jaka Perdana', 'jaka@gmail.com', '$5$rounds=535000$apQpjo4ycB3oZM/G$9z4w2GC3so5dxw04V6kHzcjWjF4y323OdrVmgAPuE85', '2025-06-12 07:11:51', 'user'),
(5, 'Admin', 'admin@wahana.com', '$5$rounds=535000$lZm4JIe.iYymmsGt$X5r5pEvf7FUuaeK.jldPX0JDJNZlyG.BImwUDnzkUs0', '2025-06-12 15:08:06', 'admin'),
(7, 'anang', 'anang@gmail.com', '$5$rounds=535000$o6N.N0hl6Ksh1Dv9$Pmd6joICtven17ATqkd4XesqB4rUOouJ3C7uuYH2Sx7', '2025-06-12 11:10:43', 'user'),
(8, 'Firda Nabilah', 'firda@gmail.com', '$5$rounds=535000$5FPvUhtknS17lAOP$.RJBCRpURKkyuLjIlXuVd/2ZZUIxV7MAnNwiY/GVlm1', '2025-06-14 00:11:28', 'user'),
(9, 'Hasanah Nur Aini', 'hasanah@gmail.com', '$5$rounds=535000$AqB/bivWNWFAKVSK$KEwpM7TjZoze.fs/01cbk7tzeme4dcKIO91NT24u.98', '2025-06-14 00:11:43', 'user'),
(10, 'Azri Anggia Putri', 'azri@gmail.com', '$5$rounds=535000$veNVo/azgi9QTA9e$sh4U4duvOUSEeC3olaU9eTmCXaMHIiiFUViWudfdyG6', '2025-06-14 00:12:08', 'user'),
(11, 'Anggina Pertiwi Nasution', 'anggina@gmail.com', '$5$rounds=535000$3cI/Yvbk7JUADrNM$KByqJXJtU6FNrGqhJjqUhYDJsJyam0WD6OV16WUdueB', '2025-06-14 00:12:34', 'user'),
(12, 'jaka ', 'jaka1@gmail.com', '$5$rounds=535000$Z7h52YEVA7bmXCG3$5SGC3GosMAY4/2pBBTYSMXHdn4vpSIVXPeS1k6TFcc3', '2025-06-14 04:57:12', 'user'),
(13, 'Jaka2', 'jaka2@gmail.com', '$5$rounds=535000$uqy.8cskc2d3o5.I$RlK7MK3jTzmXIaTZvYt1bPnMa/kBev.Pn347LWBFyu1', '2025-06-14 04:57:58', 'user'),
(14, 'Reza', 'reza@gmail.com', '$5$rounds=535000$a2lIZuiKGJINK/Ki$oFnoLOV9QO.BONPqudHSI6AamcduI6cpNLb9k1LJNc2', '2025-06-14 04:59:00', 'user');

-- --------------------------------------------------------

--
-- Table structure for table `tiket`
--

CREATE TABLE `tiket` (
  `id` int(11) NOT NULL,
  `pemesanan_id` int(11) NOT NULL,
  `jadwal_id` int(11) NOT NULL,
  `kode_booking` varchar(20) NOT NULL,
  `status` enum('Aktif','Digunakan','Batal') DEFAULT 'Aktif'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `tiket`
--

INSERT INTO `tiket` (`id`, `pemesanan_id`, `jadwal_id`, `kode_booking`, `status`) VALUES
(1, 2, 8, 'T6FQJ2QX', 'Aktif'),
(2, 2, 8, 'EEDSI3RD', 'Aktif'),
(3, 2, 8, 'J50P7OIY', 'Aktif'),
(4, 2, 8, '8JTE74KV', 'Aktif'),
(5, 2, 8, 'SPL09WOF', 'Aktif'),
(58, 24, 13, 'EF6WKOGV', 'Aktif'),
(59, 24, 13, '9P1Y3236', 'Aktif'),
(60, 25, 7, 'E4Q6T623', 'Aktif'),
(61, 26, 7, 'MMFLGPTW', 'Aktif'),
(62, 27, 7, '3NL2GIHH', 'Aktif'),
(63, 28, 7, 'NLLZXJUW', 'Aktif'),
(64, 29, 11, 'O351JJD3', 'Aktif'),
(65, 30, 7, 'NILEJ62W', 'Aktif'),
(66, 30, 7, '67NAIQZD', 'Aktif'),
(67, 30, 7, 'RTT6FL2X', 'Aktif'),
(68, 31, 7, 'JJY9R7N3', 'Aktif'),
(69, 31, 7, 'E4XCFYNK', 'Aktif');

-- --------------------------------------------------------

--
-- Table structure for table `wahana`
--

CREATE TABLE `wahana` (
  `id` int(11) NOT NULL,
  `nama_wahana` varchar(100) NOT NULL,
  `deskripsi` text DEFAULT NULL,
  `lokasi` varchar(50) DEFAULT NULL,
  `kapasitas` int(11) DEFAULT NULL,
  `gambar_url` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `wahana`
--

INSERT INTO `wahana` (`id`, `nama_wahana`, `deskripsi`, `lokasi`, `kapasitas`, `gambar_url`) VALUES
(1, 'Roller Coaster Halilintar', 'Rasakan kecepatan kilat.', 'Pasar Pagi', 20, 'coaster.jpg'),
(2, 'Istana Boneka Nusantara', 'Perjalanan magis budaya Indonesia.', 'Zona Anak', 30, 'boneka.jpg'),
(3, 'Arung Jeram Niagara', 'Terjang ombak dan basah-basahan.', 'Zona Air', 8, 'rafting.jpg'),
(5, 'Bioskop 3D', 'Nikmati keindahan bioskop 3d', 'Kota Medan', 100, 'bioskop.jpg'),
(6, 'Perjalanan Antariksa', 'suasana penjelajahan antariksa', 'United State of America', 1000, 'antariksa.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `waiting_list`
--

CREATE TABLE `waiting_list` (
  `id` int(11) NOT NULL,
  `jadwal_id` int(11) NOT NULL,
  `pengguna_id` int(11) NOT NULL,
  `waktu_masuk` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `waiting_list`
--

INSERT INTO `waiting_list` (`id`, `jadwal_id`, `pengguna_id`, `waktu_masuk`) VALUES
(5, 12, 1, '2025-06-12 19:50:27'),
(6, 12, 1, '2025-06-12 19:51:57'),
(7, 12, 1, '2025-06-12 19:52:15');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `jadwal_wahana`
--
ALTER TABLE `jadwal_wahana`
  ADD PRIMARY KEY (`id`),
  ADD KEY `wahana_id` (`wahana_id`);

--
-- Indexes for table `pemesanan`
--
ALTER TABLE `pemesanan`
  ADD PRIMARY KEY (`id`),
  ADD KEY `pengguna_id` (`pengguna_id`);

--
-- Indexes for table `pengguna`
--
ALTER TABLE `pengguna`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `tiket`
--
ALTER TABLE `tiket`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `kode_booking` (`kode_booking`),
  ADD KEY `pemesanan_id` (`pemesanan_id`),
  ADD KEY `jadwal_id` (`jadwal_id`);

--
-- Indexes for table `wahana`
--
ALTER TABLE `wahana`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `waiting_list`
--
ALTER TABLE `waiting_list`
  ADD PRIMARY KEY (`id`),
  ADD KEY `jadwal_id` (`jadwal_id`),
  ADD KEY `pengguna_id` (`pengguna_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `jadwal_wahana`
--
ALTER TABLE `jadwal_wahana`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `pemesanan`
--
ALTER TABLE `pemesanan`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT for table `pengguna`
--
ALTER TABLE `pengguna`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `tiket`
--
ALTER TABLE `tiket`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=70;

--
-- AUTO_INCREMENT for table `wahana`
--
ALTER TABLE `wahana`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `waiting_list`
--
ALTER TABLE `waiting_list`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `jadwal_wahana`
--
ALTER TABLE `jadwal_wahana`
  ADD CONSTRAINT `jadwal_wahana_ibfk_1` FOREIGN KEY (`wahana_id`) REFERENCES `wahana` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `pemesanan`
--
ALTER TABLE `pemesanan`
  ADD CONSTRAINT `pemesanan_ibfk_1` FOREIGN KEY (`pengguna_id`) REFERENCES `pengguna` (`id`);

--
-- Constraints for table `tiket`
--
ALTER TABLE `tiket`
  ADD CONSTRAINT `tiket_ibfk_1` FOREIGN KEY (`pemesanan_id`) REFERENCES `pemesanan` (`id`),
  ADD CONSTRAINT `tiket_ibfk_2` FOREIGN KEY (`jadwal_id`) REFERENCES `jadwal_wahana` (`id`);

--
-- Constraints for table `waiting_list`
--
ALTER TABLE `waiting_list`
  ADD CONSTRAINT `waiting_list_ibfk_1` FOREIGN KEY (`jadwal_id`) REFERENCES `jadwal_wahana` (`id`),
  ADD CONSTRAINT `waiting_list_ibfk_2` FOREIGN KEY (`pengguna_id`) REFERENCES `pengguna` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
