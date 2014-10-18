from flask import render_template, request, flash, redirect, url_for, make_response, session, g
from wwag import app, database
from datetime import datetime

@app.before_request
def before_request():
  if '/static/' in request.path:
    return
  if session.get('user_type') == "Player":
    player = database.execute("SELECT * FROM Player WHERE PlayerID = %s;", (session.get('user_id'),)).fetchone()
    g.current_player = player
  elif session.get('user_type') == "Viewer":
    viewer = database.execute("SELECT * FROM Viewer WHERE ViewerID = %s;", (session.get('user_id'),)).fetchone()
    if viewer:
      g.current_viewer = viewer
      g.open_order = open_order()

def open_order():
  viewer_id = g.current_viewer['ViewerID']
  open_order = database.execute("SELECT * FROM ViewerOrder WHERE ViewerID = %s AND ViewedStatus = 'Open';", (viewer_id,)).fetchone()
  if open_order:
    return open_order
  else:
    lastrowid = database.execute("INSERT INTO ViewerOrder (OrderDate, ViewedStatus, ViewerID) VALUES (%s, %s, %s);", (datetime.now().date(), "Open", viewer_id)).lastrowid
    database.commit()
    return database.execute("SELECT * FROM ViewerOrder WHERE ViewerID = %s AND ViewedStatus = 'Open';", (viewer_id,)).fetchone()

import wwag.views.index
import wwag.views.instance_runs
import wwag.views.videos
import wwag.views.games
import wwag.views.users
import wwag.views.viewers
import wwag.views.utilities
import wwag.views.players
import wwag.views.orders
