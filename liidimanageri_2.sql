-- phpMyAdmin SQL Dump
-- version 4.9.0.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: 11.05.2020 klo 09:50
-- Palvelimen versio: 10.4.6-MariaDB
-- PHP Version: 7.3.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `liidimanageri`
--

-- --------------------------------------------------------

--
-- Rakenne taululle `alembic_version`
--

CREATE TABLE `alembic_version` (
  `version_num` varchar(32) COLLATE utf16_swedish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf16 COLLATE=utf16_swedish_ci;

--
-- Vedos taulusta `alembic_version`
--

INSERT INTO `alembic_version` (`version_num`) VALUES
('63abadb6da8e');

-- --------------------------------------------------------

--
-- Rakenne taululle `liidit`
--

CREATE TABLE `liidit` (
  `id` int(11) NOT NULL,
  `nimi` varchar(64) COLLATE utf16_swedish_ci DEFAULT NULL,
  `puhelinnumero` varchar(15) COLLATE utf16_swedish_ci DEFAULT NULL,
  `sahkoposti` varchar(64) COLLATE utf16_swedish_ci DEFAULT NULL,
  `yksikko` varchar(64) COLLATE utf16_swedish_ci DEFAULT NULL,
  `yhteinen` varchar(1) COLLATE utf16_swedish_ci DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `updated` datetime DEFAULT NULL,
  `todennakoisyys` decimal(2,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf16 COLLATE=utf16_swedish_ci;

--
-- Vedos taulusta `liidit`
--

INSERT INTO `liidit` (`id`, `nimi`, `puhelinnumero`, `sahkoposti`, `yksikko`, `yhteinen`, `user_id`, `updated`, `todennakoisyys`) VALUES
(1, 'Yritys Oy', '358505111969', 'yritys@yritys.fi', 'IT', '0', 1, '2020-04-26 20:06:10', '0.00'),
(6, 'Yritys1 Oy', '358505111968', 'yritys1@yritys.fi', 'HR', '0', 1, '2020-04-27 05:38:21', '0.50'),
(7, 'Yritys2 Oy', '358505111967', 'yritys2@yritys.fi', 'Business', '1', 1, '2020-04-27 05:49:11', '0.00'),
(8, 'Yritys3 Oy', '358505111966', 'yritys3@yritys.fi', 'HR', '0', 1, '2020-04-27 06:06:59', '0.50'),
(31, 'Yritys4 Oy', '358505111965', 'yritys4@yritys.fi', 'Business', NULL, 1, '2020-04-27 16:52:31', '0.00'),
(32, 'Yritys5 Oy', '358505111964', 'yritys5@yritys.fi', 'Business', NULL, 1, '2020-04-27 16:54:17', '0.50');

-- --------------------------------------------------------

--
-- Rakenne taululle `roles`
--

CREATE TABLE `roles` (
  `id` int(11) NOT NULL,
  `name` varchar(64) COLLATE utf16_swedish_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf16 COLLATE=utf16_swedish_ci;

-- --------------------------------------------------------

--
-- Rakenne taululle `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `email` varchar(64) COLLATE utf16_swedish_ci DEFAULT NULL,
  `username` varchar(64) COLLATE utf16_swedish_ci DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL,
  `password_hash` varchar(128) COLLATE utf16_swedish_ci DEFAULT NULL,
  `confirmed` tinyint(1) DEFAULT NULL
) ;

--
-- Vedos taulusta `users`
--

INSERT INTO `users` (`id`, `email`, `username`, `role_id`, `password_hash`, `confirmed`) VALUES
(1, 'jukka.aula@kolumbus.fi', 'Jukka', NULL, 'pbkdf2:sha256:150000$HBFs2q3l$7fac075bb43429b7f49d9ea0a7635fc8d5b22edb5e6f3da64dd1a6be4fff1eac', 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `alembic_version`
--
ALTER TABLE `alembic_version`
  ADD PRIMARY KEY (`version_num`);

--
-- Indexes for table `liidit`
--
ALTER TABLE `liidit`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nimi` (`nimi`),
  ADD UNIQUE KEY `puhelinnumero` (`puhelinnumero`),
  ADD UNIQUE KEY `ix_liidit_sahkoposti` (`sahkoposti`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ix_users_username` (`username`),
  ADD UNIQUE KEY `ix_users_email` (`email`),
  ADD KEY `role_id` (`role_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `liidit`
--
ALTER TABLE `liidit`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- AUTO_INCREMENT for table `roles`
--
ALTER TABLE `roles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Rajoitteet vedostauluille
--

--
-- Rajoitteet taululle `liidit`
--
ALTER TABLE `liidit`
  ADD CONSTRAINT `liidit_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Rajoitteet taululle `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
