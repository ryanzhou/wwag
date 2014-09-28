import MySQLdb
import MySQLdb.cursors
from wwag import app
from flask import g
import string

def connect_db():
  """Connects to the specific database."""
  conn = MySQLdb.connect(host=app.config['DB_HOST'], user=app.config['DB_USER'], passwd=app.config['DB_PASSWORD'], db=app.config['DB_DATABASE'], port=app.config['DB_PORT'], cursorclass=MySQLdb.cursors.DictCursor)
  return conn

def get_db():
  """Opens a new database connection if there is none yet for the
  current application context."""
  if not hasattr(g, 'mysql_conn'):
    g.mysql_conn = connect_db()
  return g.mysql_conn

def execute(query, args=()):
  """Execute a query in the database."""
  cursor = get_db().cursor()
  cursor.execute(query, args)
  return cursor

def init_db():
  """Initializes the application database with schema.sql."""
  db = get_db()
  with app.open_resource('../schema.sql', mode='r') as f:
    statements = string.split(f.read(), ";")
    for statement in statements[:-1]:
      db.cursor().execute(statement)
  db.commit()

def seed_db():
  """Seeds the application database with seeds.sql."""
  db = get_db()
  with app.open_resource('../seeds.sql', mode='r') as f:
    statements = string.split(f.read(), ";")
    for statement in statements[:-1]:
      db.cursor().execute(statement)
  db.commit()

def commit():
  db = get_db()
  db.commit()

@app.teardown_appcontext
def close_db(error):
  """Closes the database again at the end of the request."""
  if hasattr(g, 'mysql_conn'):
    g.mysql_conn.close()
