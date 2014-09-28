# Default users:
# jill@wwag.com.au  password
# charles.delaney@gmail.com  antood74
# davm1967@hotmail.com  password

INSERT INTO `Player` (PlayerID, SupervisorID, FirstName, LastName, Role, Type, ProfileDescription, Email, GameHandle, Phone, VoIP, HashedPassword)
VALUES
(1, 1, "Jill", "Williams", "MasterUser", "S", "System created",
  "jill@wwag.com.au", "jill", NULL, "jill", "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"),
(2, 1, "Charles", "Delaney", "Supervisor", "S", "Welcome to my profile",
  "charles.delaney@gmail.com", "charles", NULL, "antood74", "45601a7b9faa8c9958ab2a84b635e42cd632fffd1d8dac7cd76ae634a4cfebf9"),
(3, 2, "David", "Meldrum", "Player", "P", "I work at Pro Yard Services",
  "davm1967@hotmail.com", "david", NULL, "Wiself1967", "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8");

INSERT INTO `InstanceRun` (InstanceRunID, SupervisorID, Name, RecordedTime, CategoryName)
VALUES
(1, 1, "Attack on Zebras", "2002-11-19 19:34:20", "Role Playing"),
(2, 2, "Wrong Way Racer", "2003-06-04 12:00:09", "Role Playing"),
(3, 2, "Trial of the Champion", "2004-08-01 17:59:52", "Achievement Attempt");

INSERT INTO `InstanceRunPlayer` (PlayerID, InstanceRunID, PerformanceNotes)
VALUES
(1, 1, "Excellent! Jill definitely mastered this game."),
(2, 1, "Very effective and entertaining!"),
(1, 2, "Jill is very skillful, as usual."),
(2, 2, "Maybe Charles's internet wasn't working so well that day. His actions were a bit slow."),
(3, 2, "This was David's first play in WWAG. He definitely had a good time.");
