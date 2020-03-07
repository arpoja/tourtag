-- THIS SCRIPT UPDATES TRIP AND TRIPSTOPS WHEN ARRIVING TO A PORT
DROP TABLE IF EXISTS temp.tvars;
CREATE TEMP TABLE tvars (Name TEXT PRIMARY KEY, Val TEXT);
-- 3 params: Last and arrival port names, when departing to next?
INSERT OR REPLACE INTO tvars VALUES
     ('TripId',( -- Get current trip
         SELECT MAX(TripId) FROM trips WHERE Status <> 'FINISHED'))
     ,('LastPort',?)
     ,('ArrPort',?)
     ,('Departing',?);

-- update trips from STARTED to FINISHED if destination = the same port we're arriving at.
UPDATE trips
SET Status = 'FINISHED'
WHERE TripId = (SELECT Val FROM tvars WHERE Name = 'TripId')
AND DestId = (SELECT Val FROM tvars WHERE Name = 'ArrPort');

-- update new stop to ARRIVED state and give it an arrival time.
UPDATE tripstops
SET  StopStatus = 'ARRIVED'
    ,ArrivalTime = datetime('now')
    ,DepartureTime = datetime((SELECT Val FROM tvars WHERE Name = 'Departing'))
WHERE TripId = (
    SELECT Val FROM tvars WHERE Name = 'TripId')
AND PortId = (
    SELECT Val FROM tvars WHERE Name = 'ArrPort');

-- cleanup
DROP TABLE IF EXISTS temp.tvars;