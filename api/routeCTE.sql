-- Temp tables for queries and variables
DROP TABLE IF EXISTS temp.ttable;
DROP TABLE IF EXISTS temp.tvars;
CREATE TEMP TABLE ttable ([Route] TEXT, [PitStops] INT, [TravelTime] TIME);
CREATE TEMP TABLE tvars (Name TEXT PRIMARY KEY, Val TEXT);
INSERT OR REPLACE INTO tvars VALUES('Start',?),('Dest',?);

-- Form recursive query with CTE
    --Based on code by Vasyl Zvarydchuk: https://stackoverflow.com/a/41694077
WITH RoutesCTE AS (
    SELECT 
         o.[From] || ',' || o.[To] AS [Route] -- concat Route with ','
        ,0 AS PitStops -- count how many stops between points
        ,time(o.[TravelTime]) AS [TravelTime]
        ,o.[From]      -- from port
        ,o.[To]        -- to port
    FROM (  -- subquery to get port names instead of Id
        SELECT
             fp.Name as [From]
            ,dp.Name as [To]
            ,routes.TravelTime as [TravelTime]  -- keep track of traveltime
        FROM routes -- joins for translation
            LEFT JOIN ports fp ON routes.PortId = fp.PortId
            LEFT JOIN ports dp ON routes.DestId = dp.PortId
    ) o 
    -- RECURSION BEGINS
    UNION ALL

    SELECT 
         r.[Route] || ',' || r1.[To] -- Build route
        ,PitStops + 1   -- count up for each stop
        ,time(r.[TravelTime],r1.[TravelTime])
        ,r.[From]       
        ,r1.[To]
    FROM RoutesCTE r
        JOIN ( -- subqueyr to get port names instead of ID
            SELECT
                 fp.Name AS [From]
                ,dp.Name AS [To]
                ,routes.TravelTime as [TravelTime]
            FROM routes
                LEFT JOIN ports fp ON routes.PortId = fp.PortId
                LEFT JOIN ports dp ON routes.DestId = dp.PortId
        ) r1    
            ON r.[To] = r1.[From]   -- join to recursion
                AND r1.[To] <> r.[From] -- No backtracking
                AND INSTR(r.[Route],r1.[To]) = 0 -- only return routes that start with (recursion) destination
)
-- Put results into temp table
INSERT INTO ttable
SELECT [Route], PitStops, TravelTime
FROM RoutesCTE
WHERE [From] = (SELECT Val FROM tvars WHERE Name = 'Start') -- Starting port as Name
    AND [To] = (SELECT Val FROM tvars WHERE Name = 'Dest')  -- Destination port as Name
    AND PitStops <= 20; -- make sure recrusion ends 
SELECT 
    json_object(
        'from',         (SELECT Val FROM tvars WHERE Name = 'Start'),
        'destination',  (SELECT Val FROM tvars WHERE Name = 'Dest'),
        'routes',json_group_array(
            json_object(
                'route',[Route], 
                'stops', PitStops, 
                'traveltime',TravelTime
            )
        ) 
    ) AS json_result 
FROM ttable;

DROP TABLE IF EXISTS temp.ttable;
DROP TABLE IF EXISTS temp.tvars;
