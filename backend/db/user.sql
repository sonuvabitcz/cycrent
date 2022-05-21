CREATE DATABASE IF NOT EXISTS `cycrent_db` CHARACTER SET utf8;
USE `cycrent`;

CREATE TABLE IF NOT EXISTS `bicycles` (
  -- `id` int unsigned NOT NULL AUTO_INCREMENT,
  `brand` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `type` int unsigned NOT NULL,
  `wheel_size` int unsigned NOT NULL,
  `description` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `price` int unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


INSERT INTO `bicycles` (`brand`, `model`, `type`, `wheel_size`, `description`, `price`) VALUES
	('Cannondale', 'Scalpel HT', 'Cross Country', 29, 'Scalpel HT is an XC race hardtail that gives you more. More of that stuff you love about a hardtail the explosive acceleration and lighter-than-air climbing feel, plus a little something extra.', 15),

	('Cube', 'Stereo ONE77', 'Enduro', 29, 'Any trail, any mountain, all the time the Stereo ONE77 is a bike for all reasons. Coil shock or air, adjustable geometry and 29er wheels give you the tools you need for all mountain and bike park fun. Move mountains, have fun, rinse and repeat.', 20),

	('Scott', 'Speedster 10', 'Road', 28, 'The SCOTT Speedster 10 is a light, agile, and cost efficient alloy road bike. With fully integrated cables, not only will this bike ride well, but it will most definitely look the part!', 15);


  -- BankCard.objects.create(num='9275928376987264',ccv='532')
  -- BankCard.objects.create(num='6352938992848738',ccv='298')
  -- BankCard.objects.create(num='8297592882976529',ccv='105')

  -- User.objects.create(first_name='Paul', last_name='Traputs',login='goingtowow',telephone='375295552019',password='1111',bank_card=)


-- Bicycle.objects.create(brand='Scott', model='Speedster 10', type='Road', wheel_size=28, description='The SCOTT Speedster 10 is a light, agile, and cost efficient alloy road bike. With fully integrated cables, not only will this bike ride well, but it will most definitely look the part!', price=15)

-- Bicycle.objects.create(brand='Cannondale', model='Scalpel HT', type='Cross Country', wheel_size=29, description='Scalpel HT is an XC race hardtail that gives you more. More of that stuff you love about a hardtail the explosive acceleration and lighter-than-air climbing feel, plus a little something extra.', price=15)

-- Bicycle.objects.create(brand='Cube', model='Stereo ONE77', type='Enduro', wheel_size=29, description='Any trail, any mountain, all the time the Stereo ONE77 is a bike for all reasons. Coil shock or air, adjustable geometry and 29er wheels give you the tools you need for all mountain and bike park fun. Move mountains, have fun, rinse and repeat.', price=20)

-- CREATE DATABASE IF NOT EXISTS `roytuts`;
-- USE `roytuts`;

-- CREATE TABLE IF NOT EXISTS `user` (
--   `id` int unsigned NOT NULL AUTO_INCREMENT,
--   `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
--   `email` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
--   `phone` int unsigned NOT NULL,
--   `address` varchar(250) COLLATE utf8mb4_unicode_ci NOT NULL,
--   PRIMARY KEY (`id`)
-- ) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--CREATE TABLE IF NOT EXISTS `recipe` (
--  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
--  `time_minutes` int unsigned NOT NULL,
--  `ingredients` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL
--) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- INSERT INTO `user` (`id`, `name`, `email`, `phone`, `address`) VALUES
-- 	(1, 'Soumitra', 'soumitra@roytuts.com', 43256789, 'Earth'),
-- 	(2, 'Rahul', 'rahul@roytuts.com', 65465363, 'Mars'),
-- 	(3, 'Liton', 'liton.sarkar@email.com', 1407874760, 'Mars');