from flask import render_template, redirect, url_for, flash
from wwag import app, database
from MySQLdb import ProgrammingError

@app.route("/")
def index():
  try:
    videos = database.execute("SELECT * FROM Video NATURAL JOIN InstanceRun ORDER BY ViewCount DESC LIMIT 5;").fetchall()
    instance_runs = database.execute("SELECT * FROM InstanceRun ORDER BY RecordedTime DESC LIMIT 5;").fetchall()
  except ProgrammingError:
    flash("Please initialize the database first.", 'error')
    return redirect(url_for('utilities'))
  return render_template('index.html', videos=videos, instance_runs=instance_runs)
