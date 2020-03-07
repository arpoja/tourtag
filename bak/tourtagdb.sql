/* qqqqry
select * 
from routes
inner join ports as beg on routes.portid = beg.portid
inner join ports as dest on routes.destid = dest.portid
where beg.name = 'Turku';
*/
create table ports(
	PortId int PRIMARY KEY,
	Name TEXT NOT NULL,
	SName TEXT NOT NULL
	);

create table routes(
	PortId int,
	DestId int,
	TravelTime time NOT NULL,
	FOREIGN KEY(PortId) REFERENCES ports (PortId),
	FOREIGN KEY(DestId) REFERENCES ports (PortId)
	);

create table users(
	UserId int PRIMARY KEY,
	UserName TEXT NOT NULL,
	UserRole TEXT NOT NULL,
	PWD varchar(64) NOT NULL
	);
	
create table tags(
	TagId INT PRIMARY KEY,
	UserId INT,
	FOREIGN KEY(UserId) References users (UserId)
	);
	
create table trips(
	BegId int,
	DestId int,
	TripId int PRIMARY KEY,
	Status varchar(16) NOT NULL,
	FOREIGN KEY(BegId) REFERENCES ports (PortId),
	FOREIGN KEY(DestId) REFERENCES ports (PortId)
	);
create table tripstops(
	TripId int,
	PortId int,
	ArrivalTime datetime,
	DepartureTime datetime,
	StopStatus varchar(16),
	FOREIGN KEY(TripId) REFERENCES trips (TripId),
	FOREIGN KEY(PortId) REFERENCES ports (PortId)
	);
	
	
/* data */
insert into ports values
(1,'Hamina','HMN'),
(2,'Helsinki','HKI'),
(3,'Turku','TKU'),
(4,'Åland','MHN'),
(5,'Pori','POR'),
(6,'Vaasa','VSA'),
(7,'Kokkola','KOK'),
(8,'Oulu','OUL');


insert into routes values
(2,1,'01:00:00');
insert into routes values
(2,3,'01:00:00');
insert into routes values
(3,2,'01:00:00');
insert into routes values
(4,3,'01:00:00');
insert into routes values
(5,3,'01:00:00');
insert into routes values
(5,4,'01:00:00');
insert into routes values
(3,5,'01:00:00');
insert into routes values
(5,6,'01:00:00');
insert into routes values
(6,5,'01:00:00');
insert into routes values
(6,7,'01:00:00');
insert into routes values
(7,8,'01:00:00');
insert into routes values
(7,6,'01:00:00');
insert into routes values
(8,7,'01:00:00');

