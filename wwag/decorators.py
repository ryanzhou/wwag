from functools import wraps
from flask import g, request, redirect, url_for

def player_login_required(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    if g.get('current_player') is None:
      return redirect(url_for('users_login', error="You must sign in as a Player to access this page."))
    return f(*args, **kwargs)
  return decorated_function

def viewer_login_required(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    if g.get('current_viewer') is None:
      return redirect(url_for('users_login', error="You must sign in as a Viewer to access this page."))
    return f(*args, **kwargs)
  return decorated_function

def staff_login_required(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    if g.get('current_player') is None or g.current_player['Type'] != "S":
      return redirect(url_for('users_login', error="You must sign in as a Player with staff permissions to access this page."))
    return f(*args, **kwargs)
  return decorated_function
