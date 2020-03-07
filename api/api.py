import flask
from flask import jsonify
from flask import request
import sqlite3
from sqlite3 import Error

db = '/home/jani/tourtag/tourtag.db'


### SQL stuffs
# split query file to cmds
def split_query(query_file):
    fd = open(query_file,'r')
    query = fd.read()
    fd.close()
    return query.split(';')

# SQL connection
def create_conn(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


# GetAllPorts
def select_all_from_ports(conn):
    cur = conn.cursor()
    cur.execute("SELECT json_group_array(json_object('port',Name)) AS json_result " +
                "FROM (SELECT * FROM ports);")
    ret = cur.fetchall()
    return jsonify(ret[0][0])


# GetRouteToFrom
def select_route_to_from(conn,orig,dest):
    # too long query to keep in python code
    ret = "500"
    cur = conn.cursor()
    cmds = split_query('routeCTE.sql')
    for cmd in cmds:
        #print("\n***\nnow executing")
        #print(cmd)
        if cmd.count('?') == 2:
            #print("found 2 params")
            cur.execute(cmd,(orig,dest,))
        else:
            cur.execute(cmd)
        row = cur.fetchone()
        if not row:
            pass
        else:
            ret = row
    return jsonify(ret)

### Trip logics
# new trip from route 
# TODO: include departure time? -> change SQL script too
def create_new_trip(conn,r):
    print("adding new trip for route: " + r)
    ps = r.split(',')
    cur = conn.cursor()
    cmds = split_query('add_trip.sql')
    cur = conn.cursor()
    for cmd in cmds:
        print("\n\n*** running cmd:")
        print(cmd)
        if cmd.count('?') == 3:
            # params: orig port, dest port, full route comma separated
            cur.execute(cmd,(ps[0],ps[-1],r,))
        else:
            cur.execute(cmd)
    return "200"

# depart
# TODO: include settable departure time? -> change SQL script too
def update_trip_depart(conn):
    cmds = split_query('update_trip_DEPARTPORT.sql')
    cur = conn.cursor()
    for cmd in cmds:
        cur.execute(cmd)
    return "200"


# arrive
# TODO: include settable "waiting" time? -> change SQL script too
def update_trip_arrive(conn):
    cmds = split_query('update_trip_ARRIVEPORT.sql')
    cur = conn.cursor()
    for cmd in cmds:
        cur.execute(cmd)
    return "200"


### API
app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return "<h1>Bla bla</h1><p>This site is a prototoype API.</p>"


@app.route('/ports', methods=['GET'])
def get_ports():
    conn = None
    try:
        conn = sqlite3.connect(db)
    except Error as e:
        print(e)
    try:
        return select_all_from_ports(conn)
    finally:
        conn.close()


@app.route('/route',methods=['GET','POST'])
def route_to_from():
    orig = request.args.get('origin',default = None,type = str)
    dest = request.args.get('destination',default = None,type = str)
    if orig == None or dest == None:
        return -1
    conn = None
    try:
        conn = sqlite3.connect(db)
    except Error as e:
        print(e)
    try:
        return select_route_to_from(conn,orig,dest)
    finally:
        conn.close()


@app.route('/trip/new',methods=['GET','POST'])
def add_trip():
    # CSV route 'port1,port2,por3' returned by /route
    r = request.args.get('route',default = None, type = str)
    print("rest called, route")
    print(r)
    if not r: # is this correct way to do this?
        return "500"
    conn = None
    try:
        conn = sqlite3.connect(db)
    except Error as e:
        print(e)
    try:
        return create_new_trip(conn,r)
    finally:
        conn.close()


@app.route('/trip/depart',methods=['GET','POST'])    
def trip_depart():
    conn = None
    try:
        conn = sqlite3.connect(db)
    except Error as e:
        print(e)
    try:
        return update_trip_depart(conn)
    finally:
        conn.close()


@app.route('/trip/arrive',methods=['GET','POST'])    
def trip_arrive():
    conn = None
    try:
        conn = sqlite3.connect(db)
    except Error as e:
        print(e)
    try:
        return update_trip_arrive(conn)
    finally:
        conn.close()


    


app.run(host='0.0.0.0', port=8080)
