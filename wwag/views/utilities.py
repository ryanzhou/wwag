from flask import render_template, request, flash, redirect, url_for, make_response, session, g
from wwag import app, database, forms

@app.route("/utilities")
def utilities():
  return render_template('utilities/index.html')

@app.route("/utilities/init_db", methods=['POST'])
def utilities_init_db():
  database.init_db()
  flash("Database schema loaded successfully.", 'notice')
  return redirect(url_for('utilities'))

@app.route("/utilities/seed_db", methods=['POST'])
def utilities_seed_db():
  database.seed_db()
  flash("Example data imported successfully.", 'notice')
  return redirect(url_for('utilities'))
