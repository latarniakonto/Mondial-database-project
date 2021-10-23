import sys
import psycopg2
import json

conn = None
def config():    
    global conn
    conn = psycopg2.connect(
        host = "localhost",
        dbname = "student",
        user = "app",
        password = "qwerty"
    )    

def return_output(status, data = None):
    output = {}
    if status == 0:
        if data is not None:
            output = {
                "status" : "OK",
                "data" : data
            }
        else:
            output = {
                "status" : "OK",                
            }
    elif status == 1:
        output = {
                "status" : "ERROR",                
            }
    output_json = json.dumps(output, ensure_ascii = False)
    print(output_json)
        
def init():
    print("Connecting to the PostGresSQL database student...")    
    
    global conn
    cur = conn.cursor()

    print("PostgreSQL database version:")
    cur.execute("SELECT version()")

    db_anwser = cur.fetchone()
    print(db_anwser[0])    

    psql_file = open("program-init.psql")
    psql_as_string = psql_file.read()    
    cur.execute(psql_as_string)
    conn.commit()

    cur.close()        

def flight(id, airports):

    global conn
    cur = conn.cursor()
    row = (
        id, 
        airports[0]["airport"], 
        airports[len(airports) - 1]["airport"], 
        airports[0]["takeoff_time"],
        airports[len(airports) - 1]["landing_time"]
    )
    cur.execute("""INSERT INTO flight(id, start_from, end_in, takeoff_time, landing_time) 
                   VALUES(%s, %s, %s, %s, %s)""",(row[0], row[1], row[2], row[3], row[4],))

    row = (
            id, #fid 
            airports[0]["airport"], 
            airports[0]["takeoff_time"],                        
        )
    cur.execute("""INSERT INTO flight_segment(fid, iatacode, takeoff_time) 
                       VALUES(%s, %s, %s)""",(row[0], row[1], row[2]))     

    for i in range(1,len(airports) - 1): 
        row = (
            id, #fid 
            airports[i]["airport"], 
            airports[i]["takeoff_time"],            
            airports[i]["landing_time"]
        )        
        cur.execute("""INSERT INTO flight_segment(fid, iatacode, takeoff_time, landing_time) 
                       VALUES(%s, %s, %s, %s)""",(row[0], row[1], row[2], row[3]))

    row = (
            id, #fid 
            airports[len(airports) - 1]["airport"], 
            airports[len(airports) - 1]["landing_time"],                        
        )
    cur.execute("""INSERT INTO flight_segment(fid, iatacode, landing_time) 
                       VALUES(%s, %s, %s)""",(row[0], row[1], row[2]))                        
        
    conn.commit()
    cur.close()
    return_output(0)    
    
def list_flights(id):

    global conn
    cur = conn.cursor()
    data = []
    cur.execute("SELECT get_overlapping_segments(%s)", (id,))
    cur.execute("""SELECT DISTINCT rid, start_from, end_in, takeoff_time::TEXT FROM ans_table
                    ORDER BY takeoff_time DESC, rid ASC""")
    db_answer = cur.fetchall()
    
    for i in db_answer:        
        temp = {
            "rid" : i[0],
            "from" : i[1],
            "to" : i[2],
            "takeoff_time" : i[3]
        }
        data.append(temp)
    return_output(0, data)

    cur.execute("TRUNCATE ans_table")    

def list_cities(id, dist):

    global conn
    cur = conn.cursor()
    data = []
    cur.execute("SELECT get_cities(%s, %s)", (id, dist,))
    cur.execute("""SELECT DISTINCT * FROM ans_table1
                    ORDER BY name ASC""")
    db_answer = cur.fetchall()
    
    for i in db_answer:        
        temp = {
            "name" : i[0],
            "prov" : i[1],
            "country" : i[2]            
        }
        data.append(temp)
    return_output(0, data)

    cur.execute("TRUNCATE ans_table1")    

def read_input():
    temp = input()
    parsed_json = json.loads(temp)

    if parsed_json["function"] == "flight":        
        flight(parsed_json["params"]["id"], parsed_json["params"]["airports"])
    elif parsed_json["function"] == "list_flights":
        list_flights(parsed_json["params"]["id"])
    elif parsed_json["function"] == "list_cities":
        list_cities(parsed_json["params"]["id"], parsed_json["params"]["dist"])
    elif parsed_json["function"] == "list_airport":
        print("list_airport")
    elif parsed_json["function"] == "list_city":
        print("list_city")
    elif parsed_json["function"] == "exit":
        return False                        
        
    return True    

def main(argv):
    global conn
    config()
    if len(argv) > 1 and argv[1] == "--init":
        init()
    elif len(argv) > 1 and argv[1] != "--init":
        print(argv[1] + " not supported!")
        exit(1)    
        
    if conn is None:
        exit(1)

    program_running = True
    while program_running:        
        program_running = read_input()
        
    conn.close()
                        
if __name__ == "__main__":
    try:
        main(sys.argv)
    except KeyboardInterrupt:
        print("\nInterrupted")
        return_output(0)
        exit(0)
