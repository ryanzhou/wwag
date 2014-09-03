create table Player (
  PlayerID smallint auto_increment,
  SupervisorID smallint not null,
  FirstName varchar(50) not null,
  LastName varchar(50) not null,
  Role varchar(50) not null,
  Type varchar(1) not null,
  ProfileDescription text,
  Email varchar(50) not null,
  GameHandle varchar(50) not null,
  Phone varchar(14),
  VoIP varchar(30) not null,

  primary key (PlayerID, SupervisorID),
  foreign key (SupervisorID) references Player(PlayerID)
) ENGINE=InnoDB;

create table ViewerAddress (
  ViewerID smallint not null,
  AddressID smallint not null,
  StartDate date not null,
  EndDate date,

  primary key (ViewerID, AddressID, StartDate),
  foreign key (ViwerID) references Viewer(ViewerID),
  foreign key (AddressID) references Address(AddressID)
) ENGINE=InnoDB;
