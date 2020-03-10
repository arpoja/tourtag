-- FULL OF BAD PRACTICES PLEASE DONT DO THIS 
SELECT json_object('Access',UserName)
FROM resusers
WHERE UserName = ?
AND PWD = ?;