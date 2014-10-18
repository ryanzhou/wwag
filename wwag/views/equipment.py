from flask import render_template, request, flash, redirect, url_for, make_response, session, g
from wwag import app, database, forms
from wwag.decorators import player_login_required, viewer_login_required

@app.route("/equipment")
def equipment():
  equipment = database.execute("SELECT * FROM Equipment").fetchall()
  return render_template("equipment/index.html", equipment=equipment)

@app.route("/equipment/create", methods=['GET', 'POST'])
@player_login_required
def equipment_create():
  form = forms.EquipmentForm(request.form)
  if request.method == "POST" and form.validate():
    lastrowid = database.execute("INSERT INTO Equipment (ModelAndMake, EquipmentReview, ProcessorSpeed) VALUES (%s, %s, %s);", (form.name.data, form.review.data, form.speed.data)).lastrowid
    database.commit()
    flash("You have created the equipment successfully!", 'notice')
    return redirect(url_for('equipment'))
  else:
    return render_template('equipment/new.html', form=form)

@app.route("/equipment/update/<equipment_id>", methods=['GET', 'POST'])
@player_login_required
def equipment_update(equipment_id):
  equipment = database.execute("SELECT * FROM Equipment WHERE EquipmentID = %s", (equipment_id)).fetchone()
  form = forms.EquipmentForm(request.form, model=equipment['ModelAndMake'], review=equipment['Review'], speed=equipment['ProcessorSpeed'])
  if request.method == "POST" and form.validate():
    database.execute("UPDATE Equipment SET ModelAndMake = %s, Review = %s, ProcessorSpeed = %s;", (form.model.data, form.review.data, form.speed.data))
    database.commit()
    flash("You have successfully updated the equipment!", 'notice')
    return redirect(url_for('equipment'))
  else:
    return render_template('equipment/edit.html', form=form, equipment=equipment)

@app.route("/equipment/<equipment_id>/delete", methods=['POST'])
@player_login_required
def equipment_delete(equipment_id):
  database.execute("DELETE FROM Equipment WHERE EquipmentID = %s", (equipment_id,))
  database.commit()
  flash("You have deleted the equipment!", 'notice')
  return redirect(url_for('equipment'))
