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
