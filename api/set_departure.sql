-- SETS TIME FOR NEXT DEPARTURE
UPDATE tripstops 
SET DepartureTime = datetime('now',time(?))
WHERE StopStatus = 'ARRIVED'
AND TripId = (
    SELECT MAX(TripId)
    FROM trips
    WHERE status <> 'FINISHED'
);