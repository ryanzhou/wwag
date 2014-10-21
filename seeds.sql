# Default users:
# jill@wwag.com.au  password
# charles.delaney@gmail.com  antood74
# davm1967@hotmail.com  password

INSERT INTO `Player` (`PlayerID`, `SupervisorID`, `FirstName`, `LastName`, `Role`, `Type`, `ProfileDescription`, `Email`, `GameHandle`, `Phone`, `VoiP`, `HashedPassword`)
VALUES
	(1,1,'Jill','Williams','Master User','S','System created','jill@wwag.com.au','jill','079 3251 3581','jill','5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'),
	(2,1,'Charles','Delaney','Player','P','Welcome to my profile','charles.delaney@gmail.com','charles','070 7720 8527','antood74','5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'),
	(3,2,'David','Meldrum','Player','P','I work at Pro Yard Services','davm1967@hotmail.com','david','078 6663 5818','Wiself1967','5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'),
	(4,3,'Adam','Agee','Player','P','Hello world','Adam@hotmail.com','adam','0410238839','chee63','5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'),
	(5,5,'Perry','Leigh','Supervisor','S','I am a star','Perry1897@yahoo.cn','perry','0319234567','perrr23','5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'),
	(6,4,'Patrick','Gable','MasterUser','S','game is fun!','Patrick234@gmail.com','patrick','0357893214','ptky227','5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'),
	(7,6,'Steven','Lee','Player','P','I am a student','Steven@hotmail.com','steven','(02) 4917 1444','steven007','5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'),
	(8,7,'Hannah','Layne','Master User','S','Life is wonderful','hannah@wwag.com.au','hannah','0420345567','Hannah','5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'),
	(9,9,'Peter','Ferry','Supervisor','S','Hi, everyone','peter@wwag.com.au','peter','(02) 4917 1444','peter1','5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'),
	(10,8,'Max','Bravo','Player','P','I\'m good thank you!','Maxxx@yahoo.com','max','(02) 6191 1709','max345','5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8');

INSERT INTO `InstanceRun` (`InstanceRunID`, `SupervisorID`, `Name`, `RecordedTime`, `CategoryName`)
VALUES
	(1,1,'Attack on Zebras','2002-11-19 19:34:20','Role Playing'),
	(2,2,'Wrong Way Racer','2003-06-04 12:00:09','Role Playing'),
	(3,2,'Trial of the Champion','2004-08-01 17:59:52','Achievement Attempt'),
	(4,3,'World of Warcraft','2005-09-10 13:57:00','Role Playing'),
	(5,4,'Guild Wars 2','2006-07-08 10:22:20','Role Playing'),
	(6,6,'Doom','2006-02-11 11:24:30','Achievement Attempt'),
	(7,5,'Black & White','2007-06-01 14:34:00','Role Playing'),
	(8,6,'Stronghold','2008-05-15 23:17:02','Achievement Attempt'),
	(9,9,'Deer Hunter','2012-08-11 20:45:00','Role Playing'),
	(10,8,'Return to Zork','2012-10-03 09:23:12','Achievement Attempt');

INSERT INTO `InstanceRunPlayer` (`PlayerID`, `InstanceRunID`, `PerformanceNotes`)
VALUES
	(1,1,'Excellent! Jill definitely mastered this game.'),
	(1,2,'Jill is very skillful, as usual.'),
	(2,1,'Very effective and entertaining!'),
	(2,2,'Maybe Charles\'s internet wasn\'t working so well that day. His actions were a bit slow.'),
	(2,9,'Charles is very good at this game. Obviously!'),
	(3,2,'This was David\'s first play in WWAG. He definitely had a good time.'),
	(4,3,'Adam is the youngest player in this game.'),
	(5,4,'Perry played really well today!'),
	(6,5,'Patrick just took part in this game today!'),
	(7,3,'The scores of Steven and Adam are same now.'),
	(7,6,'Steven just joined us at that time.'),
	(8,3,'good job, Hannah!!!'),
	(8,8,'Hannah is a talent!'),
	(9,4,'Peter always a strong competitor.'),
	(9,9,'Peter is doing this for the first time, but he\'s doing it pretty well!'),
	(10,10,'Max\'s rank raised in this game.');

INSERT INTO `Game` (`GameName`, `GameID`, `Genre`, `Review`, `StarRating`, `ClassificationRating`, `PlatformNotes`, `PromotionLink`, `Cost`)
VALUES
	('Ace Ventura',1,'Action','This is excellent',4,'G','Xbox Wii','http://www.lol.com',49.99),
	('Damage Incorporated',2,'Action','This is scary',4,'M','Android','http://www.lol.com',39.99),
	('Dark Messiah of Might and Magic',3,'War','This is scary and interesting',5,'PG','All platforms','http://www.lol.com',69.99),
	('Darkness Within 2: The Dark Lineage',4,'Action','This is cool',5,'CTC','Xbox Wii 3DS','http://www.lol.com',39.99),
	('Dead to Rights II',5,'Simulation','This is awesome',2,'PG','iOS Playstation','http://www.lol.com',69.99),
	('G-Police',6,'Action','A new game',4,'PG','Ouya Steam Machine','http://www.lol.com',49.99),
	('Galactic Civilizations II: Endless Universe',7,'Action','This is scary',3,'M','Android','http://www.lol.com',39.99),
	('Machine Hunter',8,'Action RPG','This is popular',5,'PG','Windows only','http://www.lol.com',49.99),
	('Massive Assault',9,'Action','This is excellent',4,'PG','iOS PC','http://www.lol.com',39.99),
	('Ripley\'s Believe It or Not!',10,'Action','This is cool',4,'EG','All platforms','http://www.lol.com',59.99);

INSERT INTO `Video` (`VideoID`, `VideoName`, `CreatedAt`, `ViewCount`, `URL`, `Price`, `VideoType`, `InstanceRunID`, `GameID`)
VALUES
	(1,'The Walking Dead Survival Instinct','2012-11-19 19:34:20',137,'http://www.youtube.com/embed/3pfJzK1tdR0',4.99,'Role Playing',1,1),
	(2,'Minecraft Xbox - Big Board Game','2012-11-20 19:34:20',46,'http://www.youtube.com/embed/r7gC7-loff8',0.00,'Role Playing',2,1),
	(3,'The Amazing Spider-Man 2','2013-10-22 09:12:21',200,'http://www.youtube.com/embed/o9kr9ZhydK0',5.60,'Role Playing',3,1),
	(4,'The LEGO Movie Videogame','2014-05-02 09:12:21',202,'http://www.youtube.com/embed/cufUOd29f8U',0.00,'Role Playing',2,1),
	(5,'Pichachu','2014-09-12 08:11:33',290,'http://www.youtube.com/embed/2W4fC0OknHA',9.10,'Role Playing',1,1),
	(6,'Pichachu2','2014-09-12 08:11:33',2292,'http://www.youtube.com/embed/SvRCsUcyHhg',199.99,'Role Playing',1,1),
	(7,'World of Warcraft','2005-09-10 07:59:19',100,'http://www.youtube.com/embed/TLzhlsEFcVQ',4.99,'Role Playing',4,4),
	(8,'Guild Wars 2','2006-07-08 10:22:20',122,'http://www.youtube.com/embed/dtopEsHspCk',5.60,'Role Playing',5,8),
	(9,'Doom 1','2006-02-11 11:24:30',202,'http://www.youtube.com/embed/nio1jZUaLL0',0.00,'Achievement Attempt',6,7),
	(10,'Doom 2','2007-02-11 11:24:30',158,'http://www.youtube.com/embed/uI0DC91r_9g',5.60,'Achievement Attempt',6,7),
	(11,'Black & White','2007-06-01 14:34:00',20,'http://www.youtube.com/embed/yvrwokNrMIQ',4.99,'Role Playing',7,5),
	(12,'Stronghold','2008-05-15 23:17:02',300,'http://www.youtube.com/embed/DdUQJTGsFYs',8.00,'Achievement Attempt',8,2),
	(13,'Deer Hunter','2012-08-11 21:45:00',68,'http://www.youtube.com/embed/a8T41MDu7jc',0.00,'Role Playing',9,9),
	(14,'Return to Zork','2012-10-03 11:23:12',430,'http://www.youtube.com/embed/ouTRmfrBjOw',0.00,'Achievement Attempt',10,10);

INSERT INTO `Address` (`AddressID`, `StreetNumber`, `StreetNumberSuffix`, `StreetName`, `StreetType`, `AddressType`, `AddressTypeIdentifier`, `MinorMunicipality`, `MajorMunicipality`, `GoverningDistrict`, `PostalArea`, `Country`)
VALUES
	(1,339,'SW','Spring','Avenue','Home','H',NULL,'Geelong','Victoria','3000','Australia'),
	(2,118,'SW','Swanston','Main Street','Home','H',NULL,'Sydney','New South Wales','4602','Australia'),
	(3,445,'SW','William','Main Street','Home','H',NULL,'Melbourne','Victoria','2283','Australia'),
	(4,234,'SE','Queensland','Avenue','Home','H',NULL,'Perth','Queensland','2009','Australia'),
	(5,246,'SE','Russell','Main Street','Home','H',NULL,'Chicago','Illinois','2000','United States'),
	(6,536,'NE','Victoria','Main Street','Home','H',NULL,'Los Angeles','Los Angeles','5342','United States'),
	(7,235,'NE','Moray','Avenue','Home','H',NULL,'New York','New York','1235','United States'),
	(8,355,'CN','Walsh','Avenue','Home','H',NULL,'Liverpool','Merseyside','LL13 0JH','United Kingdom'),
	(9,643,'CN','Leslie','Main Street','Home','H',NULL,'Bristol','Bristol','GU34 3QA','United Kingdom'),
	(10,287,'CN','Youyi','Main Street','Home','H',NULL,'Beijing','Beijing','100016','China');

INSERT INTO `Viewer` (`ViewerID`, `ViewerType`, `DateOfBirth`, `Email`, `HashedPassword`)
VALUES
	(1,'C','1994-12-09','anthony.davies@gmail.com','5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'),
	(2,'R','1988-02-04','carmentorres@teleworm.us','5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'),
	(3,'R','1996-01-23','cancest@yahoo.com','5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'),
	(4,'P','1998-12-05','sposee@hotmail.com','5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'),
	(5,'R','1968-04-01','beeldrer@yahoo.com','5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'),
	(6,'P','1988-10-17','adaamorgan@outlook.com','5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'),
	(7,'R','1993-02-24','17265EGJ@hotmail.com','5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'),
	(8,'C','1994-10-15','lily_s@hotmail.com','5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'),
	(9,'C','1992-08-22','jjones@gmail.com','5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'),
	(10,'P','1994-12-11','asdo1245@qq.com','5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8');

INSERT INTO `CrowdFundingViewer` (`ViewerID`, `FirstName`, `LastName`, `TotalAmountDonated`)
VALUES
	(1,'Anthony','Davies',100.00),
	(8,'Lily','Smith',400.00),
	(9,'James','Jones',345.00);

INSERT INTO `PremiumViewer` (`ViewerID`, `RenewalDate`)
VALUES
	(4,'2014-11-24'),
	(6,'2014-12-31'),
	(10,'2014-11-15');

INSERT INTO `Equipment` (`EquipmentID`, `ModelAndMake`, `EquipmentReview`, `ProcessorSpeed`)
VALUES
	(1,'iOS','Very good','1.5 GHz'),
	(2,'Playstation','A bit old','280 MHz'),
	(3,'PC','Not bad','3.2 GHz'),
	(4,'Android','Modern configuration','1.2 GHz'),
	(5,'Xbox','The newest model','2 GHz'),
	(6,'Wii','Almost outdated','500 MHz'),
	(7,'Ouya','Still working','100 MHz'),
	(8,'Steam Machine','Great Platform','N/A'),
	(9,'3DS','The old model','400 MHz');

INSERT INTO `Venue` (`VenueID`, `Name`, `VenueDescription`, `PowerOutlets`, `LightingNotes`, `SupervisorID`)
VALUES
	(1,'WWAG Tower','The exclusive in-house venue for gamers.',20,'Natural lighting',1),
	(2,'Central','Not a bad place for entertainment.',10,'Good',2),
	(3,'Bunker','Small but nice.',8,'OK lighting.',4),
	(4,'Cuban Bar','Not usually a gaming venue but we sometimes hold exclusive events there.',10,'Pretty dark inside. But it\'s very fancy place!',8);

INSERT INTO `VenueEquipment` (`VenueID`, `EquipmentID`, `FinancialYearStartingDate`, `SoftwareVersion`)
VALUES
	(1,2,'2012-07-01','2.0'),
	(1,5,'2014-07-01','3.0.2'),
	(2,1,'2013-07-01','6.1.2'),
	(3,6,'2012-07-01','12.0'),
	(3,8,'2014-07-01','12.0');

INSERT INTO `Achievement` (`AchievementID`, `InstanceRunID`, `WhenAchieved`, `Name`, `RewardBody`)
VALUES
	(1,1,'2014-10-19 20:24:09','First Instance Run Award','Microsoft'),
	(2,10,'2014-10-19 20:25:05','Apple Design Award','Apple'),
	(3,9,'2014-10-19 20:25:35','Great Players Award','Blizzard'),
	(4,9,'2014-10-19 20:25:51','Best Team','WWAG');

INSERT INTO `PlayerAddress` (`PlayerID`, `AddressID`, `StartDate`, `EndDate`)
VALUES
	(1,1,'2012-01-01',NULL),
	(2,2,'2012-01-02',NULL),
  (3,3,'2012-01-02',NULL),
  (4,4,'2012-01-02',NULL),
  (5,5,'2012-01-02',NULL);

INSERT INTO `ViewerAddress` (`ViewerID`, `AddressID`, `StartDate`, `EndDate`)
VALUES
  (1,6,'2012-01-01',NULL),
  (2,7,'2012-01-02',NULL),
  (3,8,'2012-01-02',NULL),
  (4,9,'2012-01-02',NULL),
  (5,10,'2012-01-02',NULL);

INSERT INTO `ViewerOrder` (`ViewerOrderID`, `OrderDate`, `ViewedStatus`, `ViewerID`)
VALUES
	(1,'2014-10-19','Viewed',1),
	(2,'2014-10-19','Pending',1),
	(3,'2014-10-19','Open',1),
	(4,'2014-10-19','Viewed',3),
	(5,'2014-10-19','Fraud',3),
	(6,'2014-10-19','Open',3),
	(7,'2014-10-19','Viewed',4),
	(8,'2014-10-19','Open',4),
	(9,'2014-10-19','Open',5),
	(10,'2014-10-19','Viewed',6),
	(11,'2014-10-19','Viewed',6),
	(12,'2014-10-19','Open',6),
	(13,'2014-10-19','Viewed',7),
	(14,'2014-10-19','Pending',7),
	(15,'2014-10-19','Open',7),
	(16,'2014-10-19','Viewed',8),
	(17,'2014-10-19','Open',8),
	(18,'2014-10-19','Viewed',9),
	(19,'2014-10-19','Open',9),
	(20,'2014-10-19','Viewed',10),
	(21,'2014-10-19','Open',10);

INSERT INTO `ViewerOrderLine` (`VideoID`, `ViewerOrderID`, `FlagPerk`)
VALUES
	(1,6,0),
	(3,2,1),
	(5,1,1),
	(5,10,1),
	(6,4,0),
	(6,7,1),
	(6,18,1),
	(6,21,1),
	(7,9,0),
	(7,16,1),
	(8,11,1),
	(10,14,0),
	(10,16,1),
	(11,10,1),
	(11,16,1),
	(12,1,1),
	(12,5,0),
	(12,13,0),
	(12,16,1),
	(12,20,1);
