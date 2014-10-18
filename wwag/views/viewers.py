from flask import render_template, request, flash, redirect, url_for, make_response, session, g
from wwag import app, database, forms

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
