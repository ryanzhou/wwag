from flask import render_template
from wwag import app, database

@app.route("/")
def index():
  players = database.execute('select * from Player;').fetchall()
  videos = database.execute("SELECT * FROM Video NATURAL JOIN InstanceRun ORDER BY ViewCount DESC LIMIT 5;").fetchall()
  return render_template('index.html', players=players, videos=videos)
