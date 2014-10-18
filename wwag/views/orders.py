from flask import render_template, request, flash, redirect, url_for, make_response, session, g
from wwag import app, database, forms
from wwag.decorators import player_login_required, viewer_login_required

@app.route("/basket")
@viewer_login_required
def basket():
  return redirect(url_for('orders_show', order_id=g.open_order['ViewerOrderID']))

@app.route("/basket/checkout", methods=["POST"])
@viewer_login_required
def basket_checkout():
  database.execute("UPDATE ViewerOrder SET ViewedStatus = 'Pending' WHERE ViewerOrderID = %s", (g.open_order['ViewerOrderID'],))
  database.commit()
  flash("You have paid for this order! Now you can watch the videos.", 'notice')
  return redirect(url_for('orders_show', order_id=g.open_order['ViewerOrderID']))

@app.route("/orders/<order_id>")
@viewer_login_required
def orders_show(order_id):
  order = database.execute("SELECT * FROM ViewerOrder WHERE ViewerOrderID = %s AND ViewerID = %s;", (order_id, g.current_viewer['ViewerID'])).fetchone()
  order_lines = database.execute("SELECT * FROM ViewerOrderLine NATURAL JOIN Video WHERE ViewerOrderID = %s;", (order['ViewerOrderID'],)).fetchall()
  order_total = database.execute("SELECT SUM(Price) AS Total FROM ViewerOrderLine NATURAL JOIN Video WHERE ViewerOrderID = %s AND FlagPerk = '0'", (order['ViewerOrderID'],)).fetchone()["Total"]
  return render_template('orders/show.html', order=order, order_lines=order_lines, order_total=order_total)
