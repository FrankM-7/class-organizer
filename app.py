import sys
from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
from sqlite3 import Error

app = Flask(__name__)
app_config = {"host": "0.0.0.0", "port": sys.argv[1]}

"""
---------------------- DEVELOPER MODE CONFIG -----------------------
"""
# Developer mode uses app.py
if "app.py" in sys.argv[0]:
  # Update app config
  app_config["debug"] = True

  # CORS settings
  cors = CORS(
    app,
    resources={r"/*": {"origins": "http://localhost*"}},
  )

  # CORS headers
  app.config["CORS_HEADERS"] = "Content-Type"


"""
--------------------------- REST CALLS -----------------------------
"""
# Remove and replace with your own
@app.route("/example")
def example():

  # See /src/components/App.js for frontend call
  return jsonify("Example response from Flask! Learn more in /app.py & /src/components/App.js")


"""
-------------------------- APP SERVICES ----------------------------
"""
# Quits Flask on Electron exit
@app.route("/quit")
def quit():
  shutdown = request.environ.get("werkzeug.server.shutdown")
  shutdown()

  return

# return all classes from the database
@app.route("/api/get_classes", methods=["GET"])
def get_classes():
    conn = create_connection(r"pythonsqlite.db")
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM classes")
        rows = cur.fetchall()

        # get class headers
        headers = [description[0] for description in cur.description]

        # convert to dictionary
        rows = [dict(zip(headers, row)) for row in rows]
        
        return jsonify({"classes" : rows, "status": "success"})

# add a class to the database
@app.route("/api/add_class", methods=["POST"])
def add_class():
    conn = create_connection(r"pythonsqlite.db")
    with conn:
        data = request.get_json()

        project = (data["name"]);

        class_id = create_class(conn, project)

        return jsonify({"status": "success", "id": class_id})
    
# add a classrow to the database
@app.route("/add_classrow", methods=["POST"])
def add_classrow():
    conn = create_connection(r"pythonsqlite.db")
    with conn:
        data = request.get_json()

        classrow = (data["name"], 1, data["project_id"])

        create_classrow(conn, classrow)
    return jsonify("Success")

"""
-------------------------- DATABASE ------------------------------
"""
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def create_class(conn, project):
    """
    Create a new class into the classes table
    :param conn: SQLite connection
    :param project: Project name
    :return: class id
    """

    sql = ''' INSERT INTO classes(name)
              VALUES(?) '''
    cur = conn.cursor()
    cur.execute(sql, (project,))
    conn.commit()
    return cur.lastrowid

def create_classrow(conn, task):
    """
    Create a new classrow
    :param conn: SQLite connection
    :param task: Tuple containing task details (name, priority, project_id)
    :return: Last inserted row ID
    """
    
    sql = ''' INSERT INTO classrows(name, priority, project_id)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()

    return cur.lastrowid

def main():
    database = r"pythonsqlite.db"

    sql_create_class_table = """ CREATE TABLE IF NOT EXISTS classes (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL
                                    ); """

    sql_create_classrow_table = """CREATE TABLE IF NOT EXISTS classrows (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    priority integer,
                                    project_id integer NOT NULL,
                                    FOREIGN KEY (project_id) REFERENCES projects (id)
                                );"""

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_class_table)

        # create tasks table
        create_table(conn, sql_create_classrow_table)
    else:
        print("Error! cannot create the database connection.")
    
    # with conn:
        # create a new project
        # project = ('Computer Animation');
        # project_id = create_class(conn, project)
        
    #     # tasks
    #     classrow_1 = ('syllabus link', 1, project_id)
    #     classrow_2 = ('assignments link', 1, project_id)

    #     # Assuming you have 'conn' defined as your SQLite connection object
    #     # create tasks
    #     create_classrow(conn, classrow_1)
    #     # create_classrow(conn, classrow_2)

if __name__ == "__main__":
  main()
  app.run(**app_config, use_reloader=False)
