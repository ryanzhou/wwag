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
    if player and player['Type'] == "S":
      g.current_staff = player
  elif session.get('user_type') == "Viewer":
    viewer = fetch_viewer(session.get('user_id'))
    if viewer:
      if viewer['ViewerType'] == "P" and viewer['RenewalDate'] < datetime.today().date():
        database.execute("DELETE FROM PremiumViewer WHERE ViewerID = %s;", (viewer['ViewerID'],))
        database.execute("UPDATE Viewer SET ViewerType = 'R' WHERE ViewerID = %s;", (viewer['ViewerID'],))
        database.commit()
        viewer = fetch_viewer(session.get('user_id'))
      g.current_viewer = viewer
      g.open_order = open_order()

def fetch_viewer(viewer_id):
  return database.execute("SELECT * FROM Viewer LEFT JOIN PremiumViewer ON Viewer.ViewerID = PremiumViewer.ViewerID LEFT JOIN CrowdFundingViewer on Viewer.ViewerID = CrowdFundingViewer.ViewerID WHERE Viewer.ViewerID = %s;", (viewer_id,)).fetchone()

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
import wwag.views.venues
import wwag.views.equipment
