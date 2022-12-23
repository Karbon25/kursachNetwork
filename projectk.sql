-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1
-- Время создания: Дек 20 2022 г., 21:26
-- Версия сервера: 10.4.24-MariaDB
-- Версия PHP: 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `projectk`
--

-- --------------------------------------------------------

--
-- Структура таблицы `clients`
--

CREATE TABLE `clients` (
  `idClient` int(11) NOT NULL,
  `fullName` varchar(255) NOT NULL,
  `address` text NOT NULL,
  `idTariff` int(5) NOT NULL,
  `tel` varchar(20) NOT NULL,
  `numberContract` varchar(20) NOT NULL,
  `idRouter` int(6) DEFAULT NULL,
  `ppoePassword` varchar(20) NOT NULL,
  `ConnectionDate` date NOT NULL,
  `state` int(1) NOT NULL,
  `active` int(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `clients`
--

INSERT INTO `clients` (`idClient`, `fullName`, `address`, `idTariff`, `tel`, `numberContract`, `idRouter`, `ppoePassword`, `ConnectionDate`, `state`, `active`) VALUES
(8, 'Кравченко Микола Іванович', 'Авіації 14', 2, '380678415691', '20221125001', 14, '123', '2022-11-22', 0, 0),
(9, 'Хоменко Лілія Василівна', 'Бобровицька 17', 3, '380661478234', '20221112002', 10, '123', '2022-11-12', 0, 0),
(10, 'Бойко Василь Іванович', 'Вишнева 140', 3, '380964311324', '20221112001', 9, '123', '2022-11-12', 0, 0),
(11, 'Ткаченко Володимир Іванович', 'Дачна 12', 1, '380637963425', '20221115001', 12, '123', '2022-11-15', 0, 0),
(12, 'Мороз Микола Іванович', 'Дружби 1', 3, '380507813799', '20221116001', 13, '123', '2022-11-16', 0, 0),
(13, 'Коваленко Юлія Володимирівна', 'Зелена 5', 1, '380737551155', '20221115002', 24, '123', '2022-11-15', 0, 0),
(14, 'Поліщук Олександра Миколаївна', 'Залічна 3', 3, '380638112591', '20221115003', 22, '123', '2022-11-15', 0, 0),
(15, 'Руденко Микола Іванович', 'Княжа 51', 1, '380991298871', '20221120003', 22, '123', '2022-11-20', 0, 0),
(16, 'Олійник Володимир Васильович', 'Козацька 91', 2, '380963172454', '20221119001', 21, '123', '2022-11-19', 0, 0),
(17, 'Литвиненко Юлія Іванівна', 'Кільцева 17', 2, '380501207771', '20221119002', 19, '123', '2022-11-19', 0, 0),
(18, 'Мельник Дар\'я Петрівна', 'Лісова 70', 3, '380661402593', '20221120001', 18, '123', '2022-11-20', 0, 0),
(19, 'Марченко Василь Іванович', 'Льотна 12', 1, '380631245972', '20221119003', 18, '123', '2022-12-19', 0, 0),
(20, 'Кузьменко Вікторія Миколаївна', 'Миру 12', 1, '380932452378', '20221120002', 17, '123', '2022-12-20', 0, 0);

-- --------------------------------------------------------

--
-- Структура таблицы `logspay`
--

CREATE TABLE `logspay` (
  `idPay` int(11) NOT NULL,
  `idClient` int(11) NOT NULL,
  `pay` float NOT NULL,
  `date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Структура таблицы `logsrouter`
--

CREATE TABLE `logsrouter` (
  `idLog` int(11) NOT NULL,
  `idRouter` int(11) NOT NULL,
  `text` text NOT NULL,
  `date` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `logsrouter`
--

INSERT INTO `logsrouter` (`idLog`, `idRouter`, `text`, `date`) VALUES
(1, 1, 'Роутер з ip адресою 10.1.0.1 під\'єднався. ', '2022-12-20 21:58:27'),
(2, 1, 'Роутер з ip адресою 10.1.1.0 під\'єднався. ', '2022-12-20 22:03:28');

-- --------------------------------------------------------

--
-- Структура таблицы `logsuser`
--

CREATE TABLE `logsuser` (
  `idLog` int(11) NOT NULL,
  `idUser` int(5) NOT NULL,
  `text` text NOT NULL,
  `date` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `logsuser`
--

INSERT INTO `logsuser` (`idLog`, `idUser`, `text`, `date`) VALUES
(1, 1, 'Перегляд сторінки Користувачі системи', '2022-12-20 21:31:18'),
(2, 1, 'Перегляд сторінки Клієнти', '2022-12-20 21:31:28'),
(3, 1, 'Перегляд стрінки Обладнення', '2022-12-20 21:32:19'),
(4, 1, 'Видалення обладнення id 2', '2022-12-20 21:32:26'),
(5, 1, 'Додання обладення IP адреса 10,1,0,1, присвоєно id 9', '2022-12-20 21:36:47'),
(6, 1, 'Отримання даних обладнення id 9', '2022-12-20 21:37:56'),
(7, 1, 'Додання обладення IP адреса 10.1.0.2, присвоєно id 10', '2022-12-20 21:38:45'),
(8, 1, 'Додання обладення IP адреса 10.1.0.3, присвоєно id 11', '2022-12-20 21:39:17'),
(9, 1, 'Додання обладення IP адреса 10.1.0.4, присвоєно id 12', '2022-12-20 21:39:38'),
(10, 1, 'Додання обладення IP адреса 10.1.0.5, присвоєно id 13', '2022-12-20 21:40:35'),
(11, 1, 'Додання обладення IP адреса 10.1.0.6, присвоєно id 14', '2022-12-20 21:41:16'),
(12, 1, 'Додання обладення IP адреса 10.1.0.7, присвоєно id 15', '2022-12-20 21:42:02'),
(13, 1, 'Додання обладення IP адреса 10.1.0.8, присвоєно id 16', '2022-12-20 21:42:26'),
(14, 1, 'Додання обладення IP адреса 10.1.0.9, присвоєно id 17', '2022-12-20 21:42:50'),
(15, 1, 'Додання обладення IP адреса 10.1.1.0, присвоєно id 18', '2022-12-20 21:43:19'),
(16, 1, 'Додання обладення IP адреса 10.1.1.1, присвоєно id 19', '2022-12-20 21:43:54'),
(17, 1, 'Додання обладення IP адреса 10.1.1.2, присвоєно id 20', '2022-12-20 21:44:36'),
(18, 1, 'Додання обладення IP адреса 10.1.1.3, присвоєно id 21', '2022-12-20 21:45:16'),
(19, 1, 'Додання обладення IP адреса 10.1.1.4, присвоєно id 22', '2022-12-20 21:46:18'),
(20, 1, 'Додання обладення IP адреса 10.1.1.5, присвоєно id 23', '2022-12-20 21:47:21'),
(21, 1, 'Додання обладення IP адреса 10.1.1.6, присвоєно id 24', '2022-12-20 21:48:11'),
(22, 1, 'Отримання даних обладнення id 9', '2022-12-20 21:48:31'),
(23, 1, 'Редагування даних обладнення id9', '2022-12-20 21:48:43'),
(24, 1, 'Перегляд стрінки Синхронізація', '2022-12-20 21:48:46'),
(25, 1, 'Видалення задачі синхронізації Додання роутера з ip адресою 10,1,0,1', '2022-12-20 21:48:58'),
(26, 1, 'Видалення задачі синхронізації Зміна ip адреси роутера з 10,1,0,1 на 10.1.0.1', '2022-12-20 21:49:08'),
(27, 1, 'Перегляд стрінки Обладнення', '2022-12-20 21:56:29'),
(28, 1, 'Отримання даних обладнення id 18', '2022-12-20 21:56:44'),
(29, 1, 'Редагування даних обладнення id18', '2022-12-20 21:56:57'),
(30, 1, 'Отримання даних обладнення id 18', '2022-12-20 21:58:13'),
(31, 1, 'Перегляд сторінки Списання з рахунків клієнтів', '2022-12-20 21:59:54'),
(32, 1, 'Перегляд стрінки Синхронізація', '2022-12-20 21:59:55'),
(33, 1, 'Перегляд сторінки Користувачі системи', '2022-12-20 21:59:59'),
(34, 1, 'Перегляд сторінки Баланс', '2022-12-20 22:00:18'),
(35, 1, 'Перегляд стрінки Синхронізація', '2022-12-20 22:00:25'),
(36, 1, 'Перегляд сторінки Користувачі системи', '2022-12-20 22:00:28'),
(37, 1, 'Перегляд сторінки Клієнти', '2022-12-20 22:00:31'),
(38, 1, 'Перегляд стрінки Обладнення', '2022-12-20 22:00:34'),
(39, 1, 'Відправка запиту перевірки доступності обладнення id 1', '2022-12-20 22:01:56'),
(40, 1, 'Перегляд сторінки Користувачі системи', '2022-12-20 22:03:16'),
(41, 1, 'Перегляд сторінки Клієнти', '2022-12-20 22:03:20'),
(42, 1, 'Користувач додав клієнта 20221125001. Присвоєне id 8', '2022-12-20 22:08:09'),
(43, 1, 'Користувач додав клієнта 20221112002. Присвоєне id 9', '2022-12-20 22:09:42'),
(44, 1, 'Користувач додав клієнта 20221112001. Присвоєне id 10', '2022-12-20 22:10:43'),
(45, 1, 'Користувач додав клієнта 20221115001. Присвоєне id 11', '2022-12-20 22:12:11'),
(46, 1, 'Користувач додав клієнта 20221116001. Присвоєне id 12', '2022-12-20 22:13:33'),
(47, 1, 'Користувач додав клієнта 20221115002. Присвоєне id 13', '2022-12-20 22:14:46'),
(48, 1, 'Користувач додав клієнта 20221115003. Присвоєне id 14', '2022-12-20 22:16:09'),
(49, 1, 'Користувач додав клієнта 20221120003. Присвоєне id 15', '2022-12-20 22:17:12'),
(50, 1, 'Користувач додав клієнта 20221119001. Присвоєне id 16', '2022-12-20 22:18:17'),
(51, 1, 'Користувач додав клієнта 20221119002. Присвоєне id 17', '2022-12-20 22:19:54'),
(52, 1, 'Користувач додав клієнта 20221120001. Присвоєне id 18', '2022-12-20 22:22:01'),
(53, 1, 'Користувач додав клієнта 20221119003. Присвоєне id 19', '2022-12-20 22:23:14'),
(54, 1, 'Користувач додав клієнта 20221120002. Присвоєне id 20', '2022-12-20 22:24:15'),
(55, 1, 'Перегляд сторінки Клієнти', '2022-12-20 22:24:48'),
(56, 1, 'Перегляд стрінки Синхронізація', '2022-12-20 22:25:05');

-- --------------------------------------------------------

--
-- Структура таблицы `pays`
--

CREATE TABLE `pays` (
  `idPays` int(11) NOT NULL,
  `idClient` int(11) NOT NULL,
  `price` float NOT NULL,
  `date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Структура таблицы `routers`
--

CREATE TABLE `routers` (
  `idRouter` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `address` text NOT NULL,
  `active` int(1) NOT NULL,
  `token` text NOT NULL,
  `ipAddress` text NOT NULL,
  `loginAccess` text NOT NULL,
  `passwordAccess` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `routers`
--

INSERT INTO `routers` (`idRouter`, `name`, `address`, `active`, `token`, `ipAddress`, `loginAccess`, `passwordAccess`) VALUES
(1, 'MainRouter', 'Головний офіс', 1, 'c91088f6dbcb0d46e0f5a838e8a1deb7', '10.0.0.1', 'userApi', '123'),
(9, 'Router15530_1', 'Шевченка 5', 1, 'e4faa2cb4572748d2cf0ef428fed253724f29276', '10.1.0.1', 'admin', 'admin'),
(10, 'Router15530_2', 'Комарова 9', 0, '56c58a687d3ab98ee28f732d91cca38a7c656931', '10.1.0.2', 'admin', 'admin'),
(11, 'Router15530_3', 'Сотницька 15', 0, '006cd9446234c346c9c7f0b8f0a8ab340328ffb3', '10.1.0.3', 'admin', 'admin'),
(12, 'Router15530_4', 'Польова 15', 0, '62af7cbce4108170082f1c5b6f45c614b336fe68', '10.1.0.4', 'admin', 'admin'),
(13, 'Router15530_5', '1 Травня 180', 0, 'ecfc4a7b2eee60a9fd2650251a1f043cc51b43ec', '10.1.0.5', 'admin', 'admin'),
(14, 'Router15530_6', 'Лютнева 12', 0, 'e4e831c01fa13c02b5e14bbd0eb7b6062d2c74aa', '10.1.0.6', 'admin', 'admin'),
(15, 'Router15530_7', 'Тероборони 16', 0, '0f709111ce2feebf471a8653b35ce0329098e5fc', '10.1.0.7', 'admin', 'admin'),
(16, 'Router15530_8', 'Піщана 71', 0, '25bd594a2bcaae257546e952790c56fbd7b2d653', '10.1.0.8', 'admin', 'admin'),
(17, 'Router15530_9', 'Реміснича 90', 0, '2899d918287e3f919b67402ec23f59b93a313a7d', '10.1.0.9', 'admin', 'admin'),
(18, 'Router15530_10', 'Ланова 43', 1, '7d1dfffa813cdd317b6dc5063e809d8b7d1fbfea', '10.1.1.0', 'userApi', 'admin'),
(19, 'Router15530_11', 'Героїв України 87', 0, '736f44e4b45752d6ee7b0887a981dd9cb2c136b5', '10.1.1.1', 'admin', 'admin'),
(20, 'Router15530_12', 'Василя Стуса 56', 0, 'b1f48e632523a74b3c0a89b013f5e12481b07dfa', '10.1.1.2', 'admin', 'admin'),
(21, 'Router15530_13', 'Святомиколаївська 7', 0, '8c63f4c5cb11b44737646c1d10b33e144cb4cb28', '10.1.1.3', 'admin', 'admin'),
(22, 'Router15530_14', 'Привокзальна 3', 0, 'f9631425c255a7a75c08a18383d788cba32a90d0', '10.1.1.4', 'admin', 'admin'),
(23, 'Router15530_15', 'Ялинкова 110', 0, '825d0f520c3507d38daac42eff817ceac3d5866a', '10.1.1.5', 'admin', 'admin'),
(24, 'Router15530_16', 'Чорнобаївська 81', 0, '7dd0d7acbc5e1f35941ba26f4ccd3604ac6746c2', '10.1.1.6', 'admin', 'admin');

-- --------------------------------------------------------

--
-- Структура таблицы `synchronizelist`
--

CREATE TABLE `synchronizelist` (
  `idTask` int(11) NOT NULL,
  `idRouter` int(11) NOT NULL,
  `jsonData` text NOT NULL,
  `synchronized` int(1) NOT NULL,
  `numberAttempts` int(5) NOT NULL,
  `nameTask` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `synchronizelist`
--

INSERT INTO `synchronizelist` (`idTask`, `idRouter`, `jsonData`, `synchronized`, `numberAttempts`, `nameTask`) VALUES
(1, 1, '{\"loadModule\": \"removeNetwatch\", \"paramModule\": {\"ipAddress\": \"10.1.0.1\"}}', 1, 1, 'Видалення роутера з ip адресою 10.1.0.1'),
(3, 1, '{\"loadModule\": \"addIpAddressNetwatch\", \"paramModule\": {\"ipAddress\": \"10.1.0.2\"}}', 1, 1, 'Додання роутера з ip адресою 10.1.0.2'),
(4, 1, '{\"loadModule\": \"addIpAddressNetwatch\", \"paramModule\": {\"ipAddress\": \"10.1.0.3\"}}', 1, 1, 'Додання роутера з ip адресою 10.1.0.3'),
(5, 1, '{\"loadModule\": \"addIpAddressNetwatch\", \"paramModule\": {\"ipAddress\": \"10.1.0.4\"}}', 1, 1, 'Додання роутера з ip адресою 10.1.0.4'),
(6, 1, '{\"loadModule\": \"addIpAddressNetwatch\", \"paramModule\": {\"ipAddress\": \"10.1.0.5\"}}', 1, 1, 'Додання роутера з ip адресою 10.1.0.5'),
(7, 1, '{\"loadModule\": \"addIpAddressNetwatch\", \"paramModule\": {\"ipAddress\": \"10.1.0.6\"}}', 1, 1, 'Додання роутера з ip адресою 10.1.0.6'),
(8, 1, '{\"loadModule\": \"addIpAddressNetwatch\", \"paramModule\": {\"ipAddress\": \"10.1.0.7\"}}', 1, 1, 'Додання роутера з ip адресою 10.1.0.7'),
(9, 1, '{\"loadModule\": \"addIpAddressNetwatch\", \"paramModule\": {\"ipAddress\": \"10.1.0.8\"}}', 1, 1, 'Додання роутера з ip адресою 10.1.0.8'),
(10, 1, '{\"loadModule\": \"addIpAddressNetwatch\", \"paramModule\": {\"ipAddress\": \"10.1.0.9\"}}', 1, 1, 'Додання роутера з ip адресою 10.1.0.9'),
(11, 1, '{\"loadModule\": \"addIpAddressNetwatch\", \"paramModule\": {\"ipAddress\": \"10.1.1.0\"}}', 1, 1, 'Додання роутера з ip адресою 10.1.1.0'),
(12, 1, '{\"loadModule\": \"addIpAddressNetwatch\", \"paramModule\": {\"ipAddress\": \"10.1.1.1\"}}', 1, 1, 'Додання роутера з ip адресою 10.1.1.1'),
(13, 1, '{\"loadModule\": \"addIpAddressNetwatch\", \"paramModule\": {\"ipAddress\": \"10.1.1.2\"}}', 1, 1, 'Додання роутера з ip адресою 10.1.1.2'),
(14, 1, '{\"loadModule\": \"addIpAddressNetwatch\", \"paramModule\": {\"ipAddress\": \"10.1.1.3\"}}', 1, 1, 'Додання роутера з ip адресою 10.1.1.3'),
(15, 1, '{\"loadModule\": \"addIpAddressNetwatch\", \"paramModule\": {\"ipAddress\": \"10.1.1.4\"}}', 1, 1, 'Додання роутера з ip адресою 10.1.1.4'),
(16, 1, '{\"loadModule\": \"addIpAddressNetwatch\", \"paramModule\": {\"ipAddress\": \"10.1.1.5\"}}', 1, 1, 'Додання роутера з ip адресою 10.1.1.5'),
(17, 1, '{\"loadModule\": \"addIpAddressNetwatch\", \"paramModule\": {\"ipAddress\": \"10.1.1.6\"}}', 1, 1, 'Додання роутера з ip адресою 10.1.1.6'),
(19, 1, '{\"loadModule\": \"changeIpAddressNetwatch\", \"paramModule\": {\"lastIpAddress\": \"10.1.1.0\", \"newIpAddress\": \"10.1.1.0\"}}', 1, 1, 'Зміна ip адреси роутера з 10.1.1.0 на 10.1.1.0'),
(20, 1, '{\"loadModule\": \"reloadNetwatch\", \"paramModule\": {\"ipAddress\": \"10.0.0.1\"}}', 1, 1, 'Оновлення стану роутера 10.0.0.1'),
(21, 14, '{\"loadModule\": \"addDataClients\", \"paramModule\": {\"idRouter\": \"14\", \"numberContract\": \"20221125001\", \"idTariff\": \"2\", \"ppoePassword\": \"123\"}}', 0, 0, 'Додання клієнта 20221125001'),
(22, 10, '{\"loadModule\": \"addDataClients\", \"paramModule\": {\"idRouter\": \"10\", \"numberContract\": \"20221112002\", \"idTariff\": \"3\", \"ppoePassword\": \"123\"}}', 0, 0, 'Додання клієнта 20221112002'),
(23, 9, '{\"loadModule\": \"addDataClients\", \"paramModule\": {\"idRouter\": \"9\", \"numberContract\": \"20221112001\", \"idTariff\": \"3\", \"ppoePassword\": \"123\"}}', 0, 0, 'Додання клієнта 20221112001'),
(24, 12, '{\"loadModule\": \"addDataClients\", \"paramModule\": {\"idRouter\": \"12\", \"numberContract\": \"20221115001\", \"idTariff\": \"1\", \"ppoePassword\": \"123\"}}', 0, 0, 'Додання клієнта 20221115001'),
(25, 13, '{\"loadModule\": \"addDataClients\", \"paramModule\": {\"idRouter\": \"13\", \"numberContract\": \"20221116001\", \"idTariff\": \"3\", \"ppoePassword\": \"123\"}}', 0, 0, 'Додання клієнта 20221116001'),
(26, 24, '{\"loadModule\": \"addDataClients\", \"paramModule\": {\"idRouter\": \"24\", \"numberContract\": \"20221115002\", \"idTariff\": \"1\", \"ppoePassword\": \"123\"}}', 0, 0, 'Додання клієнта 20221115002'),
(27, 22, '{\"loadModule\": \"addDataClients\", \"paramModule\": {\"idRouter\": \"22\", \"numberContract\": \"20221115003\", \"idTariff\": \"3\", \"ppoePassword\": \"123\"}}', 0, 0, 'Додання клієнта 20221115003'),
(28, 22, '{\"loadModule\": \"addDataClients\", \"paramModule\": {\"idRouter\": \"22\", \"numberContract\": \"20221120003\", \"idTariff\": \"1\", \"ppoePassword\": \"123\"}}', 0, 0, 'Додання клієнта 20221120003'),
(29, 21, '{\"loadModule\": \"addDataClients\", \"paramModule\": {\"idRouter\": \"21\", \"numberContract\": \"20221119001\", \"idTariff\": \"2\", \"ppoePassword\": \"123\"}}', 0, 0, 'Додання клієнта 20221119001'),
(30, 19, '{\"loadModule\": \"addDataClients\", \"paramModule\": {\"idRouter\": \"19\", \"numberContract\": \"20221119002\", \"idTariff\": \"2\", \"ppoePassword\": \"123\"}}', 0, 0, 'Додання клієнта 20221119002'),
(31, 18, '{\"loadModule\": \"addDataClients\", \"paramModule\": {\"idRouter\": \"18\", \"numberContract\": \"20221120001\", \"idTariff\": \"3\", \"ppoePassword\": \"123\"}}', 0, 0, 'Додання клієнта 20221120001'),
(32, 18, '{\"loadModule\": \"addDataClients\", \"paramModule\": {\"idRouter\": \"18\", \"numberContract\": \"20221119003\", \"idTariff\": \"1\", \"ppoePassword\": \"123\"}}', 0, 0, 'Додання клієнта 20221119003'),
(33, 17, '{\"loadModule\": \"addDataClients\", \"paramModule\": {\"idRouter\": \"17\", \"numberContract\": \"20221120002\", \"idTariff\": \"1\", \"ppoePassword\": \"123\"}}', 0, 0, 'Додання клієнта 20221120002');

-- --------------------------------------------------------

--
-- Структура таблицы `tariff`
--

CREATE TABLE `tariff` (
  `idTariff` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `price` int(6) NOT NULL,
  `rxLimit` int(11) NOT NULL,
  `txLimit` int(11) NOT NULL,
  `activeTariff` int(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `tariff`
--

INSERT INTO `tariff` (`idTariff`, `name`, `price`, `rxLimit`, `txLimit`, `activeTariff`) VALUES
(1, 'Безлімітна сотка', 240, 100, 100, 1),
(2, 'Шалена 50', 200, 50, 50, 1),
(3, 'Легка 20', 150, 20, 20, 1);

-- --------------------------------------------------------

--
-- Структура таблицы `users`
--

CREATE TABLE `users` (
  `idUser` int(5) NOT NULL,
  `fullName` varchar(255) NOT NULL,
  `login` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `permission` text NOT NULL,
  `authObject` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `users`
--

INSERT INTO `users` (`idUser`, `fullName`, `login`, `password`, `permission`, `authObject`) VALUES
(1, 'Administrator', 'admin', '40bd001563085fc35165329ea1ff5c5ecbdbbeef', 'users clients routers pays logRouter logUsers tariffs synchronizelist logPays', 'gASVngAAAAAAAABdlChLAYwNQWRtaW5pc3RyYXRvcpSMBWFkbWlulF2UKIwFdXNlcnOUjAdjbGll\nbnRzlIwHcm91dGVyc5SMBHBheXOUjAlsb2dSb3V0ZXKUjAhsb2dVc2Vyc5SMB3RhcmlmZnOUjA9z\neW5jaHJvbml6ZWxpc3SUjAdsb2dQYXlzlGVDGIXZlqgvevQd8KQE6Zk+kR4hHHyNwvMEVZRlLg==\n');

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `clients`
--
ALTER TABLE `clients`
  ADD PRIMARY KEY (`idClient`),
  ADD UNIQUE KEY `numberContract` (`numberContract`),
  ADD KEY `idTariff` (`idTariff`),
  ADD KEY `idRouter` (`idRouter`);

--
-- Индексы таблицы `logspay`
--
ALTER TABLE `logspay`
  ADD PRIMARY KEY (`idPay`);

--
-- Индексы таблицы `logsrouter`
--
ALTER TABLE `logsrouter`
  ADD PRIMARY KEY (`idLog`);

--
-- Индексы таблицы `logsuser`
--
ALTER TABLE `logsuser`
  ADD PRIMARY KEY (`idLog`);

--
-- Индексы таблицы `pays`
--
ALTER TABLE `pays`
  ADD PRIMARY KEY (`idPays`);

--
-- Индексы таблицы `routers`
--
ALTER TABLE `routers`
  ADD PRIMARY KEY (`idRouter`),
  ADD UNIQUE KEY `name` (`name`,`token`) USING HASH;

--
-- Индексы таблицы `synchronizelist`
--
ALTER TABLE `synchronizelist`
  ADD PRIMARY KEY (`idTask`);

--
-- Индексы таблицы `tariff`
--
ALTER TABLE `tariff`
  ADD PRIMARY KEY (`idTariff`);

--
-- Индексы таблицы `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`idUser`),
  ADD UNIQUE KEY `login` (`login`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `clients`
--
ALTER TABLE `clients`
  MODIFY `idClient` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT для таблицы `logspay`
--
ALTER TABLE `logspay`
  MODIFY `idPay` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `logsrouter`
--
ALTER TABLE `logsrouter`
  MODIFY `idLog` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT для таблицы `logsuser`
--
ALTER TABLE `logsuser`
  MODIFY `idLog` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=57;

--
-- AUTO_INCREMENT для таблицы `pays`
--
ALTER TABLE `pays`
  MODIFY `idPays` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `routers`
--
ALTER TABLE `routers`
  MODIFY `idRouter` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT для таблицы `synchronizelist`
--
ALTER TABLE `synchronizelist`
  MODIFY `idTask` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- AUTO_INCREMENT для таблицы `tariff`
--
ALTER TABLE `tariff`
  MODIFY `idTariff` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT для таблицы `users`
--
ALTER TABLE `users`
  MODIFY `idUser` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `clients`
--
ALTER TABLE `clients`
  ADD CONSTRAINT `clients_ibfk_1` FOREIGN KEY (`idRouter`) REFERENCES `routers` (`idRouter`) ON DELETE SET NULL ON UPDATE NO ACTION,
  ADD CONSTRAINT `clients_ibfk_2` FOREIGN KEY (`idTariff`) REFERENCES `tariff` (`idTariff`) ON DELETE NO ACTION ON UPDATE NO ACTION;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
