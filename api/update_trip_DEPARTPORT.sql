-- THIS SCRIPT UPDATES TRIP AND TRIPSTOPS WHEN DEPARTING PORT
DROP TABLE IF EXISTS temp.tvars;
CREATE TEMP TABLE tvars (Name TEXT PRIMARY KEY, Val TEXT);
-- 2 params: current port name and next port name.
INSERT OR REPLACE INTO tvars VALUES
     ('TripId',( -- Get current trip
         SELECT MAX(TripId) FROM trips WHERE Status <> 'FINISHED'))
     ,('CurPort',?)
     ,('NextPort',?);

-- update trips from PLANNED to STARTED
UPDATE trips
SET Status = 'STARTED'
WHERE TripId = (
    SELECT Val FROM tvars WHERE Name = 'TripId'
);

-- update last stop to DEPARTED state and give it a departure time.
UPDATE tripstops
SET  StopStatus = 'DEPARTED'
    ,DepartureTime = datetime('now')
WHERE TripId = (
    SELECT Val FROM tvars WHERE Name = 'TripId')
AND PortId = (
    SELECT Val FROM tvars WHERE Name = 'CurPort');

-- add next stop
INSERT INTO tripstops VALUES(
     (SELECT Val FROM tvars WHERE Name = 'TripId')
    ,(SELECT PortId FROM ports WHERE Name = (
        SELECT Val FROM tvars WHERE Name = 'NextPort'))
    ,datetime((SELECT TravelTime FROM routes    -- Give guess of arrival time based on traveltime
        WHERE PortId = (SELECT PortId FROM ports WHERE Name = (
            SELECT Val FROM tvars WHERE Name = 'CurPort'))
        AND   DestId = (SELECT PortId FROM ports WHERE Name = (
            SELECT Val FROM tvars WHERE Name = 'NextPort'))
        ))
    ,NULL -- Not departed yet
    ,'ON-THE-WAY'
    ,(SELECT StopCount FROM tripstops 
        WHERE TripId = (SELECT Val FROM tvars WHERE Name = 'TripId')
        AND PortId   = (SELECT Val FROM tvars WHERE Name = 'CurPort')
        ) + 1 -- increment stopcount
);
-- cleanup
DROP TABLE IF EXISTS temp.tvars;