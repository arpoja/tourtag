-- THIS SCRIPT UPDATES TRIP AND TRIPSTOPS WHEN ARRIVING TO A PORT
DROP TABLE IF EXISTS temp.tvars;
CREATE TEMP TABLE tvars (Name TEXT PRIMARY KEY, Val TEXT);
-- No params
INSERT OR REPLACE INTO tvars VALUES
     ('TripId',( -- Get current trip
         SELECT MAX(TripId) FROM trips WHERE Status <> 'FINISHED'))
     ,('LastPort',( -- get last port from tripstops where tripid is the above.
         SELECT PortId FROM tripstops
         WHERE StopStatus = 'DEPARTED'
         AND TripId = (
             SELECT MAX(TripId) FROM trips WHERE Status <> 'FINISHED')
         ORDER BY DepartureTime DESC -- select latest departed boat for this tripid
         LIMIT 1))
     ,('ArrPort',(
         -- port from trips with status ON-THE-WAY
         SELECT PortId FROM tripstops 
         WHERE StopStatus = 'ON-THE-WAY' 
         AND TripId = (
             SELECT MAX(TripId) FROM trips WHERE Status <> 'FINISHED')));

-- update trips from STARTED to FINISHED if destination = the same port we're arriving at.
UPDATE trips
SET Status = 'FINISHED'
WHERE TripId = (SELECT Val FROM tvars WHERE Name = 'TripId')
AND DestId = (SELECT Val FROM tvars WHERE Name = 'ArrPort');

-- update new stop to ARRIVED state and give it an arrival time.
UPDATE tripstops
SET  StopStatus = 'ARRIVED'
    ,ArrivalTime = datetime('now')
    ,DepartureTime = datetime('now',    -- default wait time from defvals, easy to demo other times
        time((SELECT Val FROM defvals WHERE Name = 'WaitTime')))
WHERE TripId = (
    SELECT Val FROM tvars WHERE Name = 'TripId')
AND PortId = (
    SELECT Val FROM tvars WHERE Name = 'ArrPort');

-- cleanup
DROP TABLE IF EXISTS temp.tvars;
