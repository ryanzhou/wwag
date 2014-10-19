from flask import render_template, request, flash, redirect, url_for, make_response, session, g
from wwag import app, database, forms
from wwag.decorators import staff_login_required
from MySQLdb import OperationalError
import hashlib

@app.route("/viewers/new")
def viewers_new():
  form = forms.ViewerRegistrationForm()
  return render_template('viewers/new.html', form=form)

@app.route("/viewers/register", methods=['POST'])
def viewers_register():
  form = forms.ViewerRegistrationForm(request.form)
  if form.validate():
    hashed_password = hashlib.sha256(form.password.data).hexdigest()
    database.execute("INSERT INTO Viewer (Email, DateOfBirth, HashedPassword, ViewerType) VALUES (%s, %s, %s, 'R');", (form.email.data, form.date_of_birth.data, hashed_password))
    database.commit()
    flash("You have successfully registered as a viewer!", 'notice')
    return redirect(url_for('users_login'))
  else:
    return render_template('viewers/new.html', form=form)

@app.route("/viewers")
@staff_login_required
def viewers():
  viewers = database.execute("SELECT * FROM Viewer ORDER BY ViewerID DESC;").fetchall()
  return render_template("viewers/index.html", viewers=viewers)

@app.route("/viewers/<viewer_id>/update", methods=['GET', 'POST'])
@staff_login_required
def viewers_update(viewer_id):
  viewer = database.execute("SELECT * FROM Viewer LEFT JOIN PremiumViewer ON Viewer.ViewerID = PremiumViewer.ViewerID LEFT JOIN CrowdFundingViewer on Viewer.ViewerID = CrowdFundingViewer.ViewerID WHERE Viewer.ViewerID = %s;", (viewer_id,)).fetchone()
  form = forms.ViewerEditForm(request.form, email=viewer['Email'], date_of_birth=viewer['DateOfBirth'], viewer_type=viewer['ViewerType'], first_name=viewer['FirstName'], last_name=viewer['LastName'], total_amount_donated=viewer['TotalAmountDonated'], renewal_date=viewer['RenewalDate'])
  if request.method == "POST" and form.validate():
    if form.password.data:
      hashed_password = hashlib.sha256(form.password.data).hexdigest()
      database.execute("UPDATE Viewer SET Email = %s, DateOfBirth = %s, ViewerType = %s, HashedPassword = %s WHERE ViewerID = %s", (form.email.data, form.date_of_birth.data, form.viewer_type.data, hashed_password, viewer['ViewerID']))
    else:
      database.execute("UPDATE Viewer SET Email = %s, DateOfBirth = %s, ViewerType = %s WHERE ViewerID = %s", (form.email.data, form.date_of_birth.data, form.viewer_type.data, viewer['ViewerID']))
    database.execute("DELETE FROM PremiumViewer WHERE ViewerID = %s;", (viewer['ViewerID'],))
    database.execute("DELETE FROM CrowdFundingViewer WHERE ViewerID = %s;", (viewer['ViewerID'],))
    try:
      if form.viewer_type.data == "P":
        database.execute("INSERT INTO PremiumViewer (ViewerID, RenewalDate) VALUES (%s, %s);", (viewer['ViewerID'], form.renewal_date.data))
      elif form.viewer_type.data == "C":
        database.execute("INSERT INTO CrowdFundingViewer (ViewerID, FirstName, LastName, TotalAmountDonated) VALUES (%s, %s, %s, %s);", (viewer['ViewerID'], form.first_name.data, form.last_name.data, form.total_amount_donated.data))
    except OperationalError as e:
      return render_template('viewers/edit.html', form=form, error=e[1])
    database.commit()
    flash("You have updated the viewer successfully!", 'notice')
    return redirect(url_for('viewers_update', viewer_id=viewer['ViewerID']))
  else:
    return render_template("viewers/edit.html", form=form)
