from flask import render_template, request, flash, redirect, url_for, make_response, session, g
from wwag import app, database, forms
from wwag.decorators import player_login_required, viewer_login_required
from MySQLdb import IntegrityError
from datetime import datetime

@app.route("/videos")
def videos():
  videos = database.execute("SELECT * FROM Video NATURAL JOIN InstanceRun ORDER BY ViewCount DESC;").fetchall()
  return render_template('videos/index.html',videos=videos)

@app.route("/videos/<video_id>")
def videos_show(video_id):
  database.execute("UPDATE Video SET ViewCount = ViewCount+1 WHERE VideoID = %s;", (video_id,))
  database.commit()
  video = database.execute("SELECT * FROM Video NATURAL JOIN InstanceRun NATURAL JOIN Game WHERE VideoID = %s", (video_id,)).fetchone()
  if video['Price'] > 0 and not g.get('current_player'):
    if not g.get('current_viewer'):
      return redirect(url_for('users_login', error="You must sign in as a Viewer to access this page."))
    order_line = database.execute("SELECT * FROM ViewerOrderLine NATURAL JOIN ViewerOrder WHERE VideoID = %s AND ViewerID = %s AND ViewedStatus IN ('Pending', 'Viewed') LIMIT 1;", (video['VideoID'], g.current_viewer['ViewerID'])).fetchone()
    if order_line:
      database.execute("UPDATE ViewerOrder SET ViewedStatus = 'Viewed' WHERE ViewerOrderID = %s;",(order_line['ViewerOrderID'],))
      database.commit()
      return render_template('videos/show.html', video=video, order_line=order_line)
    else:
      return render_template('videos/purchase.html', video=video)
  else:
    return render_template('videos/show.html', video=video)

@app.route("/videos/create", methods=['GET', 'POST'])
@player_login_required
def videos_create():
  form = forms.VideoForm(request.form)
  form.set_choices()
  if request.method == "POST" and form.validate():
    lastrowid = database.execute("INSERT INTO Video (VideoName, InstanceRunID, GameID, Price, URL, VideoType, CreatedAt) VALUES (%s, %s, %s, %s, %s, %s, %s);", (form.name.data, form.instance_run_id.data, form.game_id.data, form.price.data, form.url.data, form.video_type.data, datetime.now())).lastrowid
    database.commit()
    flash("You have created a new video successfully!", 'notice')
    return redirect(url_for('videos'))
  else:
    return render_template('videos/new.html', form=form)

@app.route("/videos/<video_id>/update", methods=['GET', 'POST'])
@player_login_required
def videos_update(video_id):
  video = database.execute("SELECT * FROM Video WHERE VideoID = %s", (video_id,)).fetchone()
  form = forms.VideoForm(request.form, name=video['VideoName'], instance_run_id=video['InstanceRunID'], game_id=video['GameID'], price=video['Price'], url=video['URL'], video_type=video['VideoType'])
  form.set_choices()
  if request.method == "POST" and form.validate():
    database.execute("UPDATE Video SET VideoName = %s, InstanceRunID = %s, GameID = %s, Price = %s, URL = %s, VideoType = %s WHERE VideoID = %s", (form.name.data, form.instance_run_id.data, form.game_id.data, form.price.data, form.url.data, form.video_type.data, video['VideoID']))
    database.commit()
    flash("You have updated the video successfully!", 'notice')
    return redirect(url_for('videos'))
  else:
    return render_template('videos/edit.html', form=form, video=video)

@app.route("/videos/<video_id>/delete", methods=['POST'])
@player_login_required
def videos_delete(video_id):
  try:
    database.execute("DELETE FROM Video WHERE VideoID = %s", (video_id,))
    database.commit()
  except IntegrityError as e:
    flash("You cannot delete this video because some viewers have ordered it!", 'error')
    return redirect(url_for('videos_show', video_id=video_id))
  flash("You have deleted the video.", 'notice')
  return redirect(url_for('videos'))

@app.route("/videos/<video_id>/add_to_basket", methods=['POST'])
@viewer_login_required
def videos_add_to_basket(video_id):
  flag_perk = (g.current_viewer['ViewerType'] in ['C', 'P'])
  database.execute("INSERT INTO ViewerOrderLine (VideoID, ViewerOrderID, FlagPerk) VALUES (%s, %s, %s);", (video_id, g.open_order['ViewerOrderID'], flag_perk))
  database.commit()
  flash("Added video to basket!", 'notice')
  return redirect(url_for('basket'))

@app.route("/videos/<video_id>/remove_from_basket")
@viewer_login_required
def videos_remove_from_basket(video_id):
  database.execute("DELETE FROM ViewerOrderLine WHERE ViewerOrderID = %s AND VideoID = %s;", (g.open_order['ViewerOrderID'], video_id))
  database.commit()
  flash("The video item has been removed from your basket.", 'notice')
  return redirect(url_for('orders_show', order_id=g.open_order['ViewerOrderID']))
