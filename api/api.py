import flask
from flask import jsonify
from flask import request
import sqlite3
from sqlite3 import Error
import hashlib

db = '../tourtag.db'


# SQL stuffs
# split query file to cmds
def split_query(query_file):
    fd = open(query_file, 'r')
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
    cur.execute("SELECT json_object( 'port', json_group_array(Name)) AS json_result " +
                "FROM (SELECT * FROM ports);")
    ret = cur.fetchall()
    return jsonify(ret[0][0])


# GetRouteToFrom
def select_route_to_from(conn, orig, dest):
    # too long query to keep in python code
    ret = "500"
    cur = conn.cursor()
    cmds = split_query('routeCTE.sql')
    for cmd in cmds:
        #print("\n***\nnow executing")
        # print(cmd)
        if cmd.count('?') == 2:
            #print("found 2 params")
            cur.execute(cmd, (orig, dest,))
        else:
            cur.execute(cmd)
        row = cur.fetchone()
        if not row:
            pass
        else:
            ret = row
    return jsonify(ret)

# Trip logics
# new trip from route
def create_new_trip(conn, r):
    #print("adding new trip for route: " + r)
    ps = r.split(',')
    cur = conn.cursor()
    cmds = split_query('add_trip.sql')
    cur = conn.cursor()
    for cmd in cmds:
        print("\n\n*** running cmd:")
        print(cmd)
        if cmd.count('?') == 3:
            print("found 3 params")
            print(ps[0])
            print(ps[-1])
            print(r)
            
            cur.execute(cmd,(ps[0],ps[-1],r,))
            conn.commit()
        else:
            cur.execute(cmd)
            conn.commit()
    return "200"

# depart
def update_trip_depart(conn):
    cmds = split_query('update_trip_DEPARTPORT.sql')
    cur = conn.cursor()
    for cmd in cmds:
        cur.execute(cmd)
    return "200"


# arrive
def update_trip_arrive(conn):
    cmds = split_query('update_trip_ARRIVEPORT.sql')
    cur = conn.cursor()
    for cmd in cmds:
        cur.execute(cmd)
    return "200"


# trip state as json
def get_trip_state(conn):
    fd = open('trip_state.sql')
    cmd = fd.read()  # only one command in this file
    fd.close()
    cur = conn.cursor()
    cur.execute(cmd)
    return jsonify(cur.fetchone())


# BAD BAD BAD
def user_login_sql(conn, userName, hashedpw):
    cmd = "SELECT UserName FROM users WHERE UserName = ? AND PWD = ?;"
    cur = conn.cursor()
    cur.execute(cmd, (userName, hashedpw,))
    r = cur.fetchall()
    if len(r) > 0:
        if r[0][0] == userName:
            return "200"
    else:
        return "403"

# departure time setting. time in SQLITE acceptable time() format
def set_departure_time_sql(conn, time):
    fd = open('set_departure.sql')
    cmd = fd.read()
    fd.close()
    cur = conn.cursor()
    cur.execute(cmd,(time,))
    return "200"

# API
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


@app.route('/route', methods=['GET', 'POST'])
def route_to_from():
    orig = request.args.get('origin', default=None, type=str)
    dest = request.args.get('destination', default=None, type=str)
    if orig == None or dest == None:
        return "404"
    conn = None
    try:
        conn = sqlite3.connect(db)
    except Error as e:
        print(e)
    try:
        return select_route_to_from(conn, orig, dest)
    finally:
        conn.close()


@app.route('/trip/new', methods=['GET', 'POST'])
def add_trip():
    # CSV route 'port1,port2,por3' returned by /route
    r = request.args.get('route', default=None, type=str)
    #print("rest called, route")
    #print(r)
    if not r:  # is this correct way to do this?
        return "500"
    conn = None
    try:
        conn = sqlite3.connect(db)
    except Error as e:
        print(e)
    try:
        return create_new_trip(conn, r)
    finally:
        conn.close()


@app.route('/trip/depart', methods=['GET', 'POST'])
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


@app.route('/trip/arrive', methods=['GET', 'POST'])
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


@app.route('/trip/state', methods=['GET'])
def get_trip():
    conn = None
    try:
        conn = sqlite3.connect(db)
    except Error as e:
        print(e)
    try:
        return get_trip_state(conn)
    finally:
        conn.close()

# BAD BAD BAD
@app.route('/user/login', methods=['GET','POST'])
def user_login():
    username = request.args.get('user', default=None, type=str)
    password = request.args.get('pw', default=None, type=str)
    if username is None or  password is None:
        return "403"
    hashedpw = hashlib.sha256(password.encode(encoding='utf-8')).hexdigest()
    conn = None
    try:
        conn = sqlite3.connect(db)
    except Error as e:
        print(e)
    try:
        return user_login_sql(conn, username, hashedpw)
    finally:
        conn.close()


@app.route('/trip/departure_in', methods=['GET','POST'])
def set_departure_time():
    deptime = request.args.get('time', default='00:00:00', type=str)
    conn = None
    try:
        conn = sqlite3.connect(db)
    except Error as e:
        print(e)
    try:
        return set_departure_time_sql(conn, deptime)
    finally:
        conn.close()


app.run(host='0.0.0.0', port=8080)
