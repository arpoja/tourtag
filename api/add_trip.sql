-- THIS SCRIPT ADDS A NEW TRIP AND THE CORRESPONING FIRST "STOP" OF THE TRIP
DROP TABLE IF EXISTS temp.tvars;
CREATE TEMP TABLE tvars (Name TEXT PRIMARY KEY, Val TEXT);
/* 4 params. 
    Starting and destination ports, 
    route inbetween ports in form 'port,port2,port3', obtained from routeCTE.sql
    departure time for when the trip starts
*/
INSERT OR REPLACE INTO tvars VALUES
     ('Start',?)
    ,('Dest',?)
    ,('Route',?)
    ,('Departing',?);

INSERT INTO trips VALUES(
     (SELECT PortId FROM ports WHERE Name = (   -- Port Id where trip starts from
        SELECT Val FROM tvars WHERE Name = 'Start'))  
    ,(SELECT PortId FROM ports WHERE Name = (   -- Port Id where trip ends
        SELECT Val FROM tvars WHERE Name = 'Dest'))
    ,(SELECT IFNULL(MAX(TripId) + 1, 1) FROM trips) -- Increment TripId
    ,'PLANNED' -- Trip status
    ,(SELECT Val FROM tvars WHERE Name = 'Route')   -- Selected route from routeCTE.sql results
);
INSERT INTO tripstops VALUES(
     (SELECT MAX(TripId) FROM Trips WHERE Status = 'PLANNED')
    ,(SELECT PortId FROM ports WHERE Name = (   -- First stop at start port
        SELECT Val FROM tvars WHERE Name = 'Start'))
    ,(SELECT datetime('now')) -- "arrived" at starting port
    ,(SELECT datetime((SELECT Val FROM tvars WHERE Name = 'Departing')))   -- departure time is NULL
    ,'ARRIVED'
    ,0
);

DROP TABLE IF EXISTS temp.tvars;