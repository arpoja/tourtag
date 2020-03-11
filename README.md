# tourtag
ESD miniproject stuff
Running:
1. run ./api/api.py in python 3.

**Update (running from base dir doesn't work anymore)**
```
cd api
python api.py
```
2. REST api order:
    - localhost:8080/ports  
        + returns all ports
    - localhost:8080/route?origin=Oulu&destination=Helsinki
        + returns all routes between 2 ports
    - localhost:8080/trip/new?route='Helsinki,Turku,Pori'
        + starts new trip and writes to tables:
            * trips
            * tripstops
     - localhost:8080/trip/depart
        + updates trip and tripstops
     - localhost:8080/trip/arrive
        + updates trip and tripstops, if destination port, resolves trip 
     - localhost:8080/trip/state
        + returns the most recent trip state as JSON
     - localhost:8080/user/login?user=someUser&pw=somePW
        + accepts user and pw in cleartext for login
        + returns 200 if succes
        + returns 403 if not succesful


Very bad code :)
