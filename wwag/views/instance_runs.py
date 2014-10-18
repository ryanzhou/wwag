from flask import render_template, request, flash, redirect, url_for, make_response, session, g
from wwag import app, database, forms
from wwag.decorators import player_login_required
from MySQLdb import IntegrityError
from datetime import datetime

@app.route("/instance_runs")
def instance_runs():
  instance_runs = database.execute("SELECT * FROM InstanceRun INNER JOIN Player ON InstanceRun.SupervisorID = Player.PlayerID ORDER BY RecordedTime DESC LIMIT 100").fetchall()
  return render_template('instance_runs/index.html', instance_runs=instance_runs)

@app.route("/instance_runs/<instance_run_id>")
def instance_runs_show(instance_run_id):
  instance_run_id = int(instance_run_id)
  instance_run = database.execute("SELECT * FROM InstanceRun INNER JOIN Player ON InstanceRun.SupervisorID = Player.PlayerID WHERE InstanceRunID = %s;", (instance_run_id,)).fetchone()
  instance_run_players = database.execute("SELECT * FROM InstanceRunPlayer NATURAL JOIN Player WHERE InstanceRunID = %s;", (instance_run_id,)).fetchall()
  achievements = database.execute("SELECT * FROM Achievement WHERE InstanceRunID = %s;", (instance_run_id,)).fetchall()
  add_player_form = forms.AddInstanceRunPlayerForm()
  add_player_form.set_choices()
  achievement_form = forms.AchievementForm()
  return render_template('instance_runs/show.html', instance_run=instance_run, instance_run_players=instance_run_players, achievements=achievements, add_player_form=add_player_form, achievement_form=achievement_form)

@app.route("/instance_runs/new")
@player_login_required
def instance_runs_new():
  instance_run_form = forms.InstanceRunForm(recorded_time=datetime.now())
  instance_run_form.set_choices()
  return render_template('instance_runs/new.html', instance_run_form=instance_run_form)

@app.route("/instance_runs/create", methods=['POST'])
@player_login_required
def instance_runs_create():
  instance_run_form = forms.InstanceRunForm(request.form)
  instance_run_form.set_choices()
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
  add_player_form.set_choices()
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

@app.route("/instance_runs/<instance_run_id>/achievements/create", methods=['GET', 'POST'])
@player_login_required
def instance_runs_achievements_create(instance_run_id):
  form = forms.AchievementForm(request.form)
  if request.method == "POST" and form.validate():
    lastrowid = database.execute("INSERT INTO Achievement (InstanceRunID, WhenAchieved, Name, RewardBody) VALUES (%s, %s, %s, %s);", (instance_run_id, datetime.now(), form.achievement_name.data, form.reward_body.data)).lastrowid
    database.commit()
    flash("You have created a new achievement successfully!", 'notice')
    return redirect(url_for('instance_runs_show', instance_run_id=instance_run_id))
  else:
    return render_template('instance_runs/show.html',instance_runs=instance_runs)

@app.route("/instance_runs/<instance_run_id>/achievements/<achievement_id>/update", methods=['GET', 'POST'])
@player_login_required
def instance_runs_achievements_update(instance_run_id, achievement_id):
  achievement = database.execute("SELECT * FROM Achievement WHERE AchievementID = %s AND InstanceRunID = %s", (achievement_id, instance_run_id)).fetchone()
  form = forms.AchievementForm(request.form, achievement_name=achievement['Name'], reward_body=achievement['RewardBody'])
  if request.method == "POST" and form.validate():
    database.execute("UPDATE Achievement SET Name = %s, RewardBody = %s WHERE InstanceRunID = %s AND AchievementID = %s;", (form.achievement_name.data, form.reward_body.data, instance_run_id, achievement_id))
    database.commit()
    flash("You have updated the achievement successfully!", 'notice')
    return redirect(url_for('instance_runs_show', instance_run_id=instance_run_id))
  else:
    return render_template('instance_runs/update_achievement.html', form=form, instance_run_id=instance_run_id, achievement_id=achievement_id)

@app.route("/instance_runs/<instance_run_id>/achievements/<achievement_id>/delete", methods=['POST'])
@player_login_required
def instance_runs_achievements_delete(instance_run_id, achievement_id):
  database.execute("DELETE FROM Achievement WHERE InstanceRunID = %s AND AchievementID = %s;", (instance_run_id, achievement_id))
  database.commit()
  flash("You have deleted the achievement.", 'notice')
  return redirect(url_for('instance_runs_show', instance_run_id=instance_run_id))
