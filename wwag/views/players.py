from flask import render_template, request, flash, redirect, url_for, make_response, session, g
from wwag import app, database, forms
from wwag.decorators import player_login_required, staff_login_required
import hashlib

@app.route("/players")
def players():
  players = database.execute('select * from Player;').fetchall()
  return render_template('players/index.html', players=players)

@app.route("/players/<player_id>")
def players_show(player_id):
  player = database.execute("SELECT * FROM Player WHERE PlayerID = %s;", (player_id,)).fetchone()
  supervisor = database.execute("SELECT * FROM Player WHERE PlayerID = %s;", (player['SupervisorID'],)).fetchone()
  instance_runs = database.execute("SELECT * FROM InstanceRunPlayer NATURAL JOIN InstanceRun WHERE PlayerID = %s;", (player['PlayerID'],)).fetchall()
  return render_template('players/show.html', player=player, supervisor=supervisor, instance_runs=instance_runs)

@app.route("/players/create", methods=['GET', 'POST'])
@staff_login_required
def players_create():
  form = forms.PlayerForm(request.form)
  form.set_choices()
  if request.method == "POST" and form.validate():
    hashed_password = hashlib.sha256(form.password.data).hexdigest()
    lastrowid = database.execute("INSERT INTO Player (FirstName, LastName, SupervisorID, Role, Type, ProfileDescription, Email, GameHandle, Phone, VoIP, HashedPassword) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", (form.first_name.data, form.last_name.data, form.supervisor_id.data, form.role.data, form.type.data, form.profile_description.data, form.email.data, form.game_handle.data, form.phone.data, form.voip.data, hashed_password)).lastrowid
    database.commit()
    flash("You have created a new player successfully!", 'notice')
    return redirect(url_for('players_show', player_id=lastrowid))
  else:
    return render_template('players/new.html', form=form)

@app.route("/players/<player_id>/update", methods=['GET', 'POST'])
@player_login_required
def players_update(player_id):
  if (not g.get('current_staff')) and g.current_player['PlayerID'] != int(player_id):
    flash("You cannot update someone else's profile!", 'error')
    return redirect(url_for("users_login"))
  player = database.execute("SELECT * FROM Player WHERE PlayerID = %s", (player_id,)).fetchone()
  form = forms.PlayerForm(request.form, player_id=player['PlayerID'], supervisor_id=player['SupervisorID'], first_name=player['FirstName'], last_name=player['LastName'], role=player['Role'], type=player['Type'], profile_description=player['ProfileDescription'], email=player['Email'], game_handle=player['GameHandle'], phone=player['Phone'], voip=player['VoiP'])
  form.set_choices()
  if request.method == "POST" and form.validate():
    if form.password.data:
      hashed_password = hashlib.sha256(form.password.data).hexdigest()
      database.execute("UPDATE Player SET FirstName = %s, LastName = %s, SupervisorID = %s, Role = %s, Type = %s, ProfileDescription = %s, Email = %s, GameHandle = %s, Phone = %s, VoIP = %s, HashedPassword = %s WHERE PlayerID = %s;", (form.first_name.data, form.last_name.data, form.supervisor_id.data, form.role.data, form.type.data, form.profile_description.data, form.email.data, form.game_handle.data, form.phone.data, form.voip.data, hashed_password, player_id))
    else:
      database.execute("UPDATE Player SET FirstName = %s, LastName = %s, SupervisorID = %s, Role = %s, Type = %s, ProfileDescription = %s, Email = %s, GameHandle = %s, Phone = %s, VoIP = %s WHERE PlayerID = %s;", (form.first_name.data, form.last_name.data, form.supervisor_id.data, form.role.data, form.type.data, form.profile_description.data, form.email.data, form.game_handle.data, form.phone.data, form.voip.data, player_id))
    database.commit()
    flash("You have updated the player successfully!", 'notice')
    return redirect(url_for('players_show', player_id=player_id))
  else:
    return render_template('players/edit.html', form=form, player=player)
