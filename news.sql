CREATE TABLE `news` (
  `Date` date NOT NULL,
  `source` varchar(45) NOT NULL,
  `Fund` varchar(45) NOT NULL,
  `Title` varchar(45) NOT NULL,
  `Link` varchar(45) NOT NULL,
  PRIMARY KEY (`Title`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
