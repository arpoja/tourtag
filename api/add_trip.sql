-- THIS SCRIPT ADDS A NEW TRIP AND THE CORRESPONING FIRST "STOP" OF THE TRIP
DROP TABLE IF EXISTS temp.tvars;
CREATE TEMP TABLE tvars (Name TEXT PRIMARY KEY, Val TEXT);
--  3 params: 
--  Starting port NAME,
--  destination port NAME, 
--  route inbetween ports in form 'port,port2,port3', obtained from routeCTE.sql
INSERT OR REPLACE INTO tvars VALUES
     ('Start',?)
    ,('Dest',?)
    ,('Route',?);
INSERT INTO trips VALUES(
     (SELECT PortId FROM ports WHERE Name = (   -- Port Id where trip starts from
        SELECT Val FROM tvars WHERE Name = 'Start'))  
    ,(SELECT PortId FROM ports WHERE Name = (   -- Port Id where trip ends
        SELECT Val FROM tvars WHERE Name = 'Dest'))
    ,(SELECT IFNULL(MAX(TripId) + 1, 1) FROM trips) -- Increment TripId
    ,'PLANNED' -- Trip status
    ,(SELECT Val FROM tvars WHERE Name = 'Route')   -- Selected route from routeCTE.sql results
    ,(SELECT Val FROM tvars WHERE Name = 'Route')   -- Remaining route is the full route
);
INSERT INTO tripstops VALUES(
     (SELECT MAX(TripId) FROM Trips WHERE Status = 'PLANNED')
    ,(SELECT PortId FROM ports WHERE Name = (   -- First stop at start port
        SELECT Val FROM tvars WHERE Name = 'Start'))
    ,(SELECT datetime('now')) -- "arrived" at starting port
    ,(datetime('now',    -- default wait time from defvals, easy to demo other times
        time((SELECT Val FROM defvals WHERE Name = 'WaitTime'))))
    ,'ARRIVED'
    ,0
);

DROP TABLE IF EXISTS temp.tvars;