from flask import render_template, request, flash, redirect, url_for, make_response, session, g
from wwag import app, database, forms

@app.route("/players")
def players():
  players = database.execute('select * from Player;').fetchall()
  return render_template('players.html', players=players)

@app.route("/players/<player_id>")
def players_show(player_id):
  player = database.execute("SELECT * FROM Player WHERE PlayerID = %s", (player_id,)).fetchone()
  return render_template('players/show.html', player=player)
