-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : mar. 10 déc. 2024 à 10:05
-- Version du serveur : 8.2.0
-- Version de PHP : 8.2.13

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `jojo_legion`
--

-- --------------------------------------------------------

--
-- Structure de la table `archived_likes`
--

DROP TABLE IF EXISTS `archived_likes`;
CREATE TABLE IF NOT EXISTS `archived_likes` (
  `archived_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `item_type` enum('character','theory') NOT NULL,
  `character_id` int DEFAULT NULL,
  `theory_id` int DEFAULT NULL,
  `archived_date` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`archived_id`),
  KEY `user_id` (`user_id`),
  KEY `character_id` (`character_id`),
  KEY `theory_id` (`theory_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `character_votes`
--

DROP TABLE IF EXISTS `character_votes`;
CREATE TABLE IF NOT EXISTS `character_votes` (
  `character_votes_id` int NOT NULL AUTO_INCREMENT,
  `character_id` int NOT NULL,
  `part_id` int NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`character_votes_id`),
  KEY `user_id` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `theories`
--

DROP TABLE IF EXISTS `theories`;
CREATE TABLE IF NOT EXISTS `theories` (
  `theory_id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `content` text NOT NULL,
  `content_date` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`theory_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `create_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `archived_id` int DEFAULT NULL,
  `character_votes_id` int DEFAULT NULL,
  `role` enum('user','admin') DEFAULT 'user',
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`),
  KEY `archived_id` (`archived_id`),
  KEY `character_votes_id` (`character_votes_id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `users`
--

INSERT INTO `users` (`user_id`, `username`, `email`, `password`, `create_date`, `archived_id`, `character_votes_id`, `role`) VALUES
(1, 'admin', 'admin@brando.com', 'admin123', '2024-12-10 10:50:03', NULL, NULL, 'admin'),
(2, 'Trinita95', 'trinita95@example.com', 'Thelastottoman', '2024-12-10 10:53:08', NULL, NULL, 'user'),
(3, 'Elijah95', 'elijah95@yahoo.com', 'Thenigerianightmare', '2024-12-10 10:53:08', NULL, NULL, 'user'),
(4, 'Adam78', 'adam78@taksim.com', 'Lemeilleurdresseur', '2024-12-10 10:53:08', NULL, NULL, 'user'),
(5, 'Songoku95', 'songoku95@saiyan.com', '7dragonball', '2024-12-10 10:53:08', NULL, NULL, 'user');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
