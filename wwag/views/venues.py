from flask import render_template, request, flash, redirect, url_for, make_response, session, g
from wwag import app, database, forms
from wwag.decorators import player_login_required, staff_login_required
from MySQLdb import IntegrityError
from datetime import datetime

@app.route("/venues")
def venues():
  venues = database.execute("SELECT * FROM Venue INNER JOIN Player ON Venue.SupervisorID = Player.PlayerID;").fetchall()
  return render_template('venues/index.html',venues=venues)

@app.route("/venues/create", methods=['GET', 'POST'])
@staff_login_required
def venues_create():
  form = forms.VenueForm(request.form)
  form.set_choices()
  if request.method == "POST" and form.validate():
    lastrowid = database.execute("INSERT INTO Venue (Name, VenueDescription, PowerOutlets, LightingNotes, SupervisorID) VALUES (%s, %s, %s, %s, %s);", (form.venue_name.data, form.description.data, form.power_outlets.data, form.light.data,  form.supervisor_id.data)).lastrowid
    database.commit()
    flash("You have successfully created a venue!", 'notice')
    return redirect(url_for('venues'))
  else:
    return render_template('venues/new.html', form=form)

@app.route("/venues/<venue_id>")
def venues_show(venue_id):
  venue = database.execute("SELECT * FROM Venue INNER JOIN Player ON Venue.SupervisorID = Player.PlayerID WHERE VenueID = %s", (venue_id,)).fetchone()
  equipment = database.execute("SELECT * FROM VenueEquipment NATURAL JOIN Equipment WHERE VenueID = %s ORDER BY FinancialYearStartingDate DESC LIMIT 1;", (venue['VenueID'],)).fetchone()
  form = forms.VenueEquipmentForm()
  form.set_choices()
  return render_template('venues/show.html', venue=venue, equipment=equipment, form=form)

@app.route("/venues/<venue_id>/update", methods=['GET', 'POST'])
@player_login_required
def venues_update(venue_id):
  venue = database.execute("SELECT * FROM Venue WHERE VenueID = %s", (venue_id,)).fetchone()
  if (not g.get('current_staff')) and venue['SupervisorID'] != g.current_player['PlayerID']:
    flash("You don't have the permission to update this venue!", 'error')
    return redirect(url_for('venues_show', venue_id=venue_id))
  form = forms.VenueForm(request.form, venue_name=venue['Name'], description=venue['VenueDescription'], power_outlets=venue['PowerOutlets'], light=venue['LightingNotes'], supervisor_id=venue['SupervisorID'])
  form.set_choices()
  if request.method == "POST" and form.validate():
    database.execute("UPDATE Venue SET Name = %s, VenueDescription = %s, PowerOutlets = %s, LightingNotes = %s, SupervisorID = %s WHERE VenueID = %s;", (form.venue_name.data, form.description.data, form.power_outlets.data, form.light.data, form.supervisor_id.data, venue['VenueID']))
    database.commit()
    flash("You have updated the venue successfully!",'notice')
    return redirect(url_for('venues'))
  else:
    return render_template('venues/edit.html', form=form, venue=venue)

@app.route("/venues/<venue_id>/delete", methods=['POST'])
@player_login_required
def venues_delete(venue_id):
  if (not g.get('current_staff')) and venue['SupervisorID'] != g.current_player['PlayerID']:
    flash("You don't have the permission to delete this venue!", 'error')
    return redirect(url_for('venues_show', venue_id=venue_id))
  database.execute("DELETE FROM VenueEquipment WHERE VenueID = %s;", (venue_id))
  database.execute("DELETE FROM Venue WHERE VenueID = %s;", (venue_id))
  database.commit()
  flash("You have deleted the venue.", 'notice')
  return redirect(url_for('venues'))

@app.route("/venues/<venue_id>/equipment/create", methods=['POST'])
@player_login_required
def venues_equipment_create(venue_id):
  venue = database.execute("SELECT * FROM Venue WHERE VenueID = %s", (venue_id,)).fetchone()
  equipment = database.execute("SELECT * FROM VenueEquipment NATURAL JOIN Equipment WHERE VenueID = %s ORDER BY FinancialYearStartingDate DESC LIMIT 1;", (venue['VenueID'],)).fetchone()
  if (not g.get('current_staff')) and venue['SupervisorID'] != g.current_player['PlayerID']:
    flash("You don't have the permission to repurpose this venue!", 'error')
    return redirect(url_for('venues_show', venue_id=venue_id))
  form = forms.VenueEquipmentForm(request.form)
  form.set_choices()
  if form.validate():
    try:
      lastrowid = database.execute("INSERT INTO VenueEquipment (VenueID, EquipmentID, FinancialYearStartingDate, SoftwareVersion) VALUES (%s, %s, %s, %s);", (venue['VenueID'], form.equipment_id.data, form.financial_year_starting_date.data, form.software_version.data)).lastrowid
    except IntegrityError as e:
      return render_template('venues/show.html', venue=venue, equipment=equipment, form=form, error=e[1])
    database.commit()
    flash("You have repurposed this venue successfully!", 'notice')
    return redirect(url_for("venues_show", venue_id=venue['VenueID']))
  else:
    return render_template("venues/show.html", venue=venue, equipment=equipment, form=form)
