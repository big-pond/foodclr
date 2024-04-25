CREATE TABLE `products` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `name` varchar(191) DEFAULT NULL,
  `isgroup` tinyint UNSIGNED DEFAULT NULL,
  `calory` double DEFAULT NULL,
  `protein` double DEFAULT NULL,
  `fat` double DEFAULT NULL,
  `carbohydrate` double DEFAULT NULL,
  `products_id` int UNSIGNED DEFAULT NULL,
  FOREIGN KEY (`products_id`) REFERENCES `products`(`id`)
);

CREATE TABLE `users` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `login` varchar(191) DEFAULT NULL,
  `name` varchar(191) DEFAULT NULL,
  `password` varchar(191) DEFAULT NULL,
  `birthdate` date DEFAULT NULL,
  `gender` tinyint UNSIGNED DEFAULT NULL,
  `registered` datetime DEFAULT NULL
);

CREATE TABLE `periods` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `startdate` date DEFAULT NULL,
  `height` int UNSIGNED DEFAULT NULL,
  `weight` double DEFAULT NULL,
  `activity` tinyint UNSIGNED DEFAULT NULL,
  `prot` tinyint UNSIGNED DEFAULT NULL,
  `fat` tinyint UNSIGNED DEFAULT NULL,
  `carb` tinyint UNSIGNED DEFAULT NULL,
  `variate` double DEFAULT NULL,
  `note` varchar(191) DEFAULT NULL,
  `users_id` int UNSIGNED DEFAULT NULL,
  FOREIGN KEY (`users_id`) REFERENCES `users`(`id`)
);

CREATE TABLE `days` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `mdate` date DEFAULT NULL,
  `weight` double DEFAULT NULL,
  `waist` int UNSIGNED DEFAULT NULL,
  `hips` int UNSIGNED DEFAULT NULL,
  `periods_id` int UNSIGNED DEFAULT NULL,
  FOREIGN KEY (`periods_id`) REFERENCES `periods`(`id`)
);

CREATE TABLE `meals` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `mtime` varchar(191) DEFAULT NULL,
  `weight` int UNSIGNED DEFAULT NULL,
  `days_id` int UNSIGNED DEFAULT NULL,
  `products_id` int UNSIGNED DEFAULT NULL,
  FOREIGN KEY (`days_id`) REFERENCES `days`(`id`),
  FOREIGN KEY (`products_id`) REFERENCES `products`(`id`)
);
