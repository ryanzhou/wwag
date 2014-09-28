# Default users:
# jill@wwag.com.au  password
# charles.delaney@gmail.com  antood74

INSERT INTO `Player` (PlayerID, SupervisorID, FirstName, LastName, Role, Type, ProfileDescription, Email, GameHandle, Phone, VoIP, HashedPassword)
VALUES
(1, 1, "Jill", "Williams", "MasterUser", "S", "System created",
  "jill@wwag.com.au", "jill", NULL, "jill", "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"),
(2, 1, "Charles", "Delaney", "Supervisor", "S", "Welcome to my profile",
  "charles.delaney@gmail.com", "charles", NULL, "antood74", "45601a7b9faa8c9958ab2a84b635e42cd632fffd1d8dac7cd76ae634a4cfebf9");
