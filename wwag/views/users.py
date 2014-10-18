from flask import render_template, request, flash, redirect, url_for, make_response, session, g
from wwag import app, database, forms
import hashlib
from datetime import datetime

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
      return redirect(url_for('index'))
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

@app.route("/users/update_address", methods=['GET', 'POST'])
def users_update_address():
  if g.get('current_player'):
    address_relation = database.execute("SELECT * FROM PlayerAddress WHERE PlayerID = %s AND EndDate IS NULL;", (g.current_player['PlayerID'],)).fetchone()
  elif g.get('current_viewer'):
    address_relation = database.execute("SELECT * FROM ViewerAddress WHERE ViewerID = %s AND EndDate IS NULL;", (g.current_viewer['ViewerID'],)).fetchone()
  else:
    flash("You must be logged in as either Player or Viewer to access this page.", 'error')
    return redirect(url_for('users_login'))
  if address_relation:
    address = database.execute("SELECT * FROM Address WHERE AddressID = %s;", (address_relation['AddressID'],)).fetchone()
    form = forms.AddressForm(request.form, street_number=address['StreetNumber'], street_number_suffix=address['StreetNumberSuffix'], street_name=address['StreetName'], street_type=address['StreetType'], major_municipality=address['MajorMunicipality'], governing_district=address['GoverningDistrict'], postal_area=address['PostalArea'], country=address['Country'])
  else:
    form = forms.AddressForm(request.form)
  if request.method == "POST" and form.validate():
    lastrowid = database.execute("INSERT INTO Address (StreetNumber, StreetNumberSuffix, StreetName, StreetType, MajorMunicipality, GoverningDistrict, PostalArea, Country) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);", (form.street_number.data, form.street_number_suffix.data, form.street_name.data, form.street_type.data, form.major_municipality.data, form.governing_district.data, form.postal_area.data, form.country.data)).lastrowid
    if g.get('current_player'):
      database.execute("UPDATE PlayerAddress SET EndDate = %s WHERE PlayerID = %s AND EndDate IS NULL;", (datetime.today().date(), g.current_player['PlayerID']))
      database.execute("INSERT INTO PlayerAddress (AddressID, PlayerID, StartDate, EndDate) VALUES (%s, %s, %s, NULL);", (lastrowid, g.current_player['PlayerID'], datetime.today().date()))
    elif g.get('current_viewer'):
      database.execute("UPDATE ViewerAddress SET EndDate = %s WHERE ViewerID = %s AND EndDate IS NULL;", (datetime.today().date(), g.current_viewer['ViewerID']))
      database.execute("INSERT INTO ViewerAddress (AddressID, ViewerID, StartDate, EndDate) VALUES (%s, %s, %s, NULL);", (lastrowid, g.current_viewer['ViewerID'], datetime.today().date()))
    database.commit()
    flash("You have updated your address successfully!", 'notice')
    return redirect(url_for('index'))
  else:
    return render_template('users/update_address.html', form=form)
