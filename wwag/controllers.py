from flask import render_template, request, flash, redirect, url_for, make_response
from wwag import app, database

@app.route("/")
def index():
  players = database.execute('select * from Player;').fetchall()
  return render_template('index.html', players=players)

@app.route("/utilities/init_db", methods=['GET', 'POST'])
def utilities_init_db():
  database.init_db()
  return redirect(url_for('index'))
