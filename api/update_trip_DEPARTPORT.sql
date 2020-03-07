-- THIS SCRIPT UPDATES TRIP AND TRIPSTOPS WHEN DEPARTING PORT
DROP TABLE IF EXISTS temp.tvars;
CREATE TEMP TABLE tvars (Name TEXT PRIMARY KEY, Val TEXT);
-- 2 params: current port name and next port name.
INSERT OR REPLACE INTO tvars VALUES
     ('TripId',( -- Get current trip
         SELECT MAX(TripId) FROM trips WHERE Status <> 'FINISHED'))
     ,('CurPort',(
        -- latest port NAME from tripstops
         (SELECT Name FROM ports WHERE PortId = (
             SELECT PortId FROM tripstops 
             WHERE TripId = (SELECT MAX(TripId) FROM trips WHERE Status <> 'FINISHED')
             AND StopStatus = 'ARRIVED'))
     ))
     ,('NextPort',(
         -- last remainig route, drop first item
         (SELECT substr( 
            (SELECT substr(
                (SELECT remainingroute FROM trips WHERE TripId = (SELECT MAX(TripID) FROM trips WHERE Status <> 'FINISHED')) || ','
                ,INSTR( -- find first comma
                    (SELECT remainingroute FROM trips WHERE TripId = (SELECT MAX(TripID) FROM trips WHERE Status <> 'FINISHED'))
                    ,',') + 1 --instr ends
                ,999))-- hardcode length, wont exceed this
         ,0 
         ,INSTR( -- find second comma
             (SELECT substr(
                (SELECT remainingroute FROM trips WHERE TripId = (SELECT MAX(TripID) FROM trips WHERE Status <> 'FINISHED')) || ','
                ,INSTR( -- find first comma
                    (SELECT remainingroute FROM trips WHERE TripId = (SELECT MAX(TripID) FROM trips WHERE Status <> 'FINISHED'))
                    ,',') + 1 --instr ends
                ,999))-- hardcode length, wont exceed this
             ,',')
         ))));
-- update trips from PLANNED to STARTED
UPDATE trips
SET  Status = 'STARTED'
    ,remainingroute = ( -- shorten remaining route by removing the port we just arrived at
        SELECT substr(
             (SELECT remainingroute FROM trips WHERE TripId = (SELECT Val FROM tvars WHERE Name = 'TripId'))
            ,INSTR(
                 (SELECT remainingroute FROM trips WHERE TripId = (SELECT Val FROM tvars WHERE Name = 'TripId'))
                ,','
            ) + 1 
            ,999 --hardcode length, will never exceed this
            ) -- susbtr ends
    ) -- remainingroute
WHERE TripId = (
    SELECT Val FROM tvars WHERE Name = 'TripId'
);

-- update last stop to DEPARTED state and give it a departure time.
UPDATE tripstops
SET  StopStatus = 'DEPARTED'
    ,DepartureTime = datetime('now')
WHERE TripId = (
    SELECT Val FROM tvars WHERE Name = 'TripId')
AND PortId = ( SELECT PortId FROM ports WHERE Name = ( -- convert name to id
    SELECT Val FROM tvars WHERE Name = 'CurPort'));

-- add next stop
INSERT INTO tripstops VALUES(
     (SELECT Val FROM tvars WHERE Name = 'TripId')
    ,(SELECT PortId FROM ports WHERE Name = (
        SELECT Val FROM tvars WHERE Name = 'NextPort'))
    ,datetime('now',time(
        (SELECT TravelTime FROM routes    -- Give guess of arrival time based on traveltime
        WHERE PortId = (SELECT PortId FROM ports WHERE Name = (
            SELECT Val FROM tvars WHERE Name = 'CurPort'))
        AND   DestId = (SELECT PortId FROM ports WHERE Name = (
            SELECT Val FROM tvars WHERE Name = 'NextPort'))
        )))
    ,NULL -- Not arrived yet, so no departure time
    ,'ON-THE-WAY'
    ,(SELECT StopCount FROM tripstops 
        WHERE TripId = (SELECT Val FROM tvars WHERE Name = 'TripId')
        AND PortId   = (SELECT PortId FROM ports WHERE Name = (SELECT Val FROM tvars WHERE Name = 'CurPort'))
        ) + 1 -- increment stopcount
);
-- cleanup
DROP TABLE IF EXISTS temp.tvars; 