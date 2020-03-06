import flask
from flask import jsonify
from flask import request
import sqlite3
from sqlite3 import Error

db = '/home/jani/tourtag/tourtag.db'


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
    ret = 0
    fd = open('routeCTE.sql','r')
    query = fd.read()
    fd.close()
    cmds = query.split(';')
    cur = conn.cursor()
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

app.run(host='0.0.0.0', port=8080)
