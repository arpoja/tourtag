with cte as 
( 
    select   CAST(ff AS TEXT) || ',' || CAST(tt AS TEXT) as [Route]
            ,0 as Stops
            ,ff
            ,tt
    from routestest

    UNION ALL

    select   CAST(r.Route AS TEXT) || ',' || CAST(r1.tt AS TEXT) as [Route]
            ,Stops +1
            ,r.ff
            ,r1.tt
    FROM cte r
    JOIN routestest r1
        ON r.tt = r1.ff
        AND r1.tt <> r.ff
        AND INSTR(r.[Route],r1.tt) = 0
)
select [Route]
FROM cte
where   ff = 1
AND     tt = 4
AND Stops <= 5;



select  r1.PortId || ',' || r1.DestId || ',' || 
        IFNULL(r2.DestId, '') || ',' || 
        IFNULL(r3.DestId, '') || ',' || 
        IFNULL(r4.DestId, '') || ',' || 
        IFNULL(r5.DestId, '') || ',' || 
        IFNULL(r6.DestId, '') || ',' || 
        IFNULL(r7.DestId, '') || ',' || 
        IFNULL(r8.DestId, '') || ',' || 
        IFNULL(r9.DestId, '') AS [Route]
from routes r1
left join routes r2 on r1.DestId = r2.PortId
        AND r2.DestId <> r1.PortId
left join routes r3 on r2.DestId = r3.PortId
        AND r3.DestId <> r2.PortId
left join routes r4 on r3.DestId = r4.PortId
        AND r4.DestId <> r3.PortId
left join routes r5 on r4.DestId = r5.PortId
        AND r5.DestId <> r4.PortId
left join routes r6 on r5.DestId = r6.PortId
        AND r6.DestId <> r5.PortId
left join routes r7 on r6.DestId = r7.PortId
        AND r7.DestId <> r6.PortId
left join routes r8 on r7.DestId = r8.PortId
        AND r8.DestId <> r7.PortId
left join routes r9 on r8.DestId = r9.PortId
        AND r9.DestId <> r8.PortId
where r1.portId = 8
AND (
        r2.destId = 1 OR
        r3.destId = 1 OR
        r4.destId = 1 OR
        r5.destId = 1 OR
        r6.destId = 1 OR
        r7.destId = 1 OR
        r8.destId = 1 OR
        r9.destId = 1
)




SELECT 
    json_group_array(
        json_object(
            'route',[Route], 
            'stops', PitStops, 
            'traveltime',TravelTime
        )
    ) AS json_result 
FROM (
        