import sqlite3
from sqlite3 import Error

# connection 
def create_conn(db_file): 
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
        
    return conn

#def select_all_from_ports(conn):
#    cur = conn.cursor()
#    cur.execute("SELECT * FROM ports")
#    rows = cur.fetchall()
#    for row in rows:
#        print(row)

def select_all_from_ports(conn):
    cur = conn.cursor()
    cur.execute("SELECT json_group_array(json_object('port',Name)) AS json_result " + 
                "FROM (SELECT * FROM ports);")
    ret = cur.fetchall()
    print(ret[0][0])
    
def select_port_from_ports(conn, portid):
    cur = conn.cursor()
    cur.execute("SELECT * FROM ports WHERE PortId=?",(portid,))
    
    rows = cur.fetchall()
    
    for row in rows:
        print(row)


def select_route_to_from(conn,beg,dest):
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
            cur.execute(cmd,(beg,dest,))
        else:
            cur.execute(cmd)
        row = cur.fetchone()
        if not row:
            pass
        else:
            ret = row
    return jsonify(ret[0][0])


def split_query(query_file):
    fd = open(query_file,'r')
    query = fd.read()
    fd.close()
    return query.split(';')

### Trip logic
# new trip from route 
# TODO: include departure time? -> change SQL script too
def create_new_trip(conn,route):
    print("adding new trip for route: " + route)
    ports = route.split(',')
    cur = conn.cursor()
    cmds = split_query('add_trip.sql')
    cur = conn.cursor()
    for cmd in cmds:
        print("\n\n*** running cmd:")
        print(cmd)
        if cmd.count('?') == 3:
            # params: orig port, dest port, full route comma separated
            print("\tstart: " + ports[0])
            print("\tdest: " + ports[-1])
            print("\troute: "+ route)
            cur.execute(cmd,(ports[0],ports[-1],route,))
        else:
            cur.execute(cmd)
    return "200"
def get_trip_state(conn):
    #cmds = split_query('trip_state.sql')
    fd = open('trip_state.sql','r')
    cmd = fd.read()
    fd.close()
    cur = conn.cursor()
    cur.execute(cmd)
    rows = cur.fetchall()
    for row in rows:
        print(row)
    

def main():
    database = '/home/jani/tourtag/tourtag.db'
    
    conn = create_conn(database)
    with conn:
        #print("1. All ports:")
        #select_all_from_ports(conn)
        #print("2. Route")
        #select_route_to_from(conn,'Kokkola','Helsinki')
        #print("3: add trip")
        #create_new_trip(conn,'Hamina,Helsinki,Turku')
        print("trip state")
        get_trip_state(conn)
    conn.close()    
        #print("2. Port with id 1:")
        #select_port_from_ports(conn,1)
        
if __name__ == '__main__':
    main()
