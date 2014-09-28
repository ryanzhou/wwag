from flask import render_template, request, flash, redirect, url_for, make_response
from wwag import app, database

@app.route("/")
def index():
  players = database.execute('select * from Player;').fetchall()
  return render_template('index.html', players=players)

@app.route("/utilities")
def utilities():
  return render_template('utilities/index.html')

@app.route("/utilities/init_db", methods=['POST'])
def utilities_init_db():
  database.init_db()
  flash("Database schema loaded successfully.")
  return redirect(url_for('utilities'))

@app.route("/utilities/seed_db", methods=['POST'])
def utilities_seed_db():
  database.seed_db()
  flash("Example data imported successfully.")
  return redirect(url_for('utilities'))

@app.route("/users/login")
def users_login():
  return render_template('users/login.html')

@app.route("/users/login_player", methods=['POST'])
def users_login_player():
  return redirect(url_for('dashboard'))

@app.route("/dashboard")
def dashboard():
  return

@app.route("/players")
def players():
  players = database.execute('select * from Player;').fetchall()
  return render_template('players.html', players=players)
