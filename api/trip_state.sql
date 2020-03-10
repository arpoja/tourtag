-- THIS SCRIPT SELECTS THE CURRENT STATE FOR THE TRIP
WITH all_stops AS (
    SELECT 
     t.TripId       AS TripId
    ,bp.Name        AS TripFrom
    ,dp.Name        AS TripDest
    ,t.Status       AS TripStatus
    ,t.Route        AS TripRoute
    ,t.RemainingRoute   AS TripRemaining
    ,p.Name         AS StopName
    ,s.StopStatus   AS StopStatus
    ,s.StopCount    AS StopCount
    ,s.ArrivalTime  AS StopArrivalTime
    ,s.DepartureTime    AS StopDepartureTime
    FROM trips t
    LEFT JOIN tripstops s ON t.TripId = s.TripId
         JOIN ports p ON s.PortId = p.PortId
         JOIN ports bp ON t.BegId = bp.PortId
         JOIN ports dp ON t.DestId = dp.PortId
)

SELECT 
    json_object(
         'trip', TripId
        ,'from', TripFrom
        ,'destination', TripDest
        ,'route',TripRoute
        ,'remainingroute',TripRemaining
        ,'status',TripStatus
        ,'stops',json_group_array(
            json_object(
                 'Stop',StopName
                ,'Status',StopStatus
                ,'Order',StopCount
                ,'ArrivalTime',StopArrivalTime
                ,'DepartureTime',StopDepartureTime
            )
        )
    ) AS json_result
 FROM all_stops
 ORDER BY TripId DESC
 LIMIT 1;