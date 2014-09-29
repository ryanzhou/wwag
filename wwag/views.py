from flask import render_template, request, flash, redirect, url_for, make_response, session, g
from wwag import app, database, forms
from wwag.decorators import player_login_required, viewer_login_required
from MySQLdb import IntegrityError
import hashlib

@app.before_request
def before_request():
  if session.get('user_type') == "Player":
    player = database.execute("SELECT * FROM Player WHERE PlayerID = %s;", (session.get('user_id'),)).fetchone()
    g.current_player = player
  elif session.get('user_type') == "Viewer":
    viewer = database.execute("SELECT * FROM Viewer WHERE ViewerID = %s;", (session.get('user_id'),)).fetchone()
    g.current_viewer = viewer

def require_player_session():
  if not session.get('user_type') == "Player":
    return redirect

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
  flash("Database schema loaded successfully.", 'notice')
  return redirect(url_for('utilities'))

@app.route("/utilities/seed_db", methods=['POST'])
def utilities_seed_db():
  database.seed_db()
  flash("Example data imported successfully.", 'notice')
  return redirect(url_for('utilities'))

@app.route("/users/login")
def users_login():
  login_form = forms.LoginForm()

  return render_template('users/login.html', login_form=login_form, error=request.args.get('error'))

@app.route("/users/login_player", methods=['POST'])
def users_login_player():
  login_form = forms.LoginForm(request.form)
  if login_form.validate():
    hashed_password = hashlib.sha256(request.form['password']).hexdigest()
    player = database.execute("SELECT * FROM Player WHERE Email = %s AND HashedPassword = %s;", (request.form['email'], hashed_password)).fetchone()
    if player:
      session['user_type'] = "Player"
      session['user_id'] = player['PlayerID']
      flash("You have logged in successfully as a player.", 'notice')
      return redirect(url_for('dashboard'))
    else:
      return render_template('users/login.html', login_form=login_form, error="Email or password is incorrect.")
  else:
    return render_template('users/login.html', login_form=login_form)

@app.route("/users/login_viewer", methods=['POST'])
def users_login_viewer():
  login_form = forms.LoginForm(request.form)
  if login_form.validate():
    hashed_password = hashlib.sha256(login_form.password.data).hexdigest()
    viewer = database.execute("SELECT * FROM Viewer WHERE Email = %s AND HashedPassword = %s;", (login_form.email.data, hashed_password)).fetchone()
    if viewer:
      session['user_type'] = "Viewer"
      session['user_id'] = viewer['ViewerID']
      flash("You have signed in successfully as a viewer.", 'notice')
      return redirect(url_for('index'))
    else:
      return render_template('users/login.html', login_form=login_form, error="Email or password is incorrect.")
  else:
    return render_template('users/login.html', login_form=login_form)

@app.route("/users/logout")
def users_logout():
  session.pop('user_type')
  session.pop('user_id')
  flash("You have signed out successfully.", 'notice')
  return redirect(url_for('index'))

@app.route("/dashboard")
@player_login_required
def dashboard():
  return render_template('dashboard/index.html')

@app.route("/instance_runs")
def instance_runs():
  instance_runs = database.execute("SELECT * FROM InstanceRun INNER JOIN Player ON InstanceRun.SupervisorID = Player.PlayerID ORDER BY RecordedTime DESC LIMIT 100").fetchall()
  return render_template('instance_runs/index.html', instance_runs=instance_runs)

@app.route("/instance_runs/<instance_run_id>")
def instance_runs_show(instance_run_id):
  instance_run_id = int(instance_run_id)
  instance_run = database.execute("SELECT * FROM InstanceRun INNER JOIN Player ON InstanceRun.SupervisorID = Player.PlayerID WHERE InstanceRunID = %s;", (instance_run_id,)).fetchone()
  instance_run_players = database.execute("SELECT * FROM InstanceRunPlayer NATURAL JOIN Player WHERE InstanceRunID = %s;", (instance_run_id,)).fetchall()
  add_player_form = forms.AddInstanceRunPlayerForm()
  return render_template('instance_runs/show.html', instance_run=instance_run, instance_run_players=instance_run_players, add_player_form=add_player_form)

@app.route("/instance_runs/new")
@player_login_required
def instance_runs_new():
  instance_run_form = forms.InstanceRunForm()
  return render_template('instance_runs/new.html', instance_run_form=instance_run_form)

@app.route("/instance_runs/create", methods=['POST'])
@player_login_required
def instance_runs_create():
  instance_run_form = forms.InstanceRunForm(request.form)
  if instance_run_form.validate():
    lastrowid = database.execute("INSERT INTO InstanceRun (SupervisorID, Name, RecordedTime, CategoryName) VALUES (%s, %s, %s, %s);", (instance_run_form.supervisor_id.data, instance_run_form.name.data, instance_run_form.recorded_time.data, instance_run_form.category_name.data)).lastrowid
    database.commit()
    flash("You have created a new instance run successfully!", 'notice')
    return redirect(url_for('instance_runs_show', instance_run_id=lastrowid))
  else:
    return render_template('instance_runs/new.html', instance_run_form=instance_run_form)

@app.route("/instance_runs/<instance_run_id>/create_player", methods=['POST'])
@player_login_required
def instance_runs_create_player(instance_run_id):
  instance_run = database.execute("SELECT * FROM InstanceRun INNER JOIN Player ON InstanceRun.SupervisorID = Player.PlayerID WHERE InstanceRunID = %s;", (instance_run_id,)).fetchone()
  instance_run_players = database.execute("SELECT * FROM InstanceRunPlayer NATURAL JOIN Player WHERE InstanceRunID = %s;", (instance_run_id,)).fetchall()
  add_player_form = forms.AddInstanceRunPlayerForm(request.form)
  if g.current_player['PlayerID'] == instance_run['PlayerID']:
    if add_player_form.validate():
      try:
        database.execute("INSERT INTO InstanceRunPlayer (PlayerID, InstanceRunID, PerformanceNotes) VALUES (%s, %s, %s);", (add_player_form.player_id.data, instance_run_id, add_player_form.performance_notes.data))
        database.commit()
      except IntegrityError as e:
        return render_template('instance_runs/show.html', instance_run=instance_run, instance_run_players=instance_run_players, add_player_form=add_player_form, error=e[1])
      flash("Player performance tracked successfully!", 'notice')
      return redirect(url_for('instance_runs_show', instance_run_id=instance_run_id))
    else:
      return render_template('instance_runs/show.html', instance_run=instance_run, instance_run_players=instance_run_players, add_player_form=add_player_form)
  else:
    return redirect(url_for('instance_runs_show', instance_run_id=instance_run_id))

@app.route("/players")
def players():
  players = database.execute('select * from Player;').fetchall()
  return render_template('players.html', players=players)

@app.route("/players/<player_id>")
def players_show(player_id):
  player = database.execute("SELECT * FROM Player WHERE PlayerID = %s", (player_id,)).fetchone()
  return render_template('players/show.html', player=player)
