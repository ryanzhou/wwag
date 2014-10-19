from flask import render_template, request, flash, redirect, url_for, make_response, session, g
from wwag import app, database, forms
from wwag.decorators import player_login_required, viewer_login_required, staff_login_required

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
def orders_show(order_id):
  order = database.execute("SELECT * FROM ViewerOrder WHERE ViewerOrderID = %s;", (order_id,)).fetchone()
  if not g.get('current_staff') and not (g.get('current_viewer') and g.current_viewer['ViewerID'] == order['ViewerID']):
    return redirect(url_for('users_login', error="You need to be a staff member or you can only view your own orders."))
  order_lines = database.execute("SELECT * FROM ViewerOrderLine NATURAL JOIN Video WHERE ViewerOrderID = %s;", (order['ViewerOrderID'],)).fetchall()
  order_total = database.execute("SELECT SUM(Price) AS Total FROM ViewerOrderLine NATURAL JOIN Video WHERE ViewerOrderID = %s AND FlagPerk = '0'", (order['ViewerOrderID'],)).fetchone()["Total"]
  return render_template('orders/show.html', order=order, order_lines=order_lines, order_total=order_total)

@app.route("/orders")
def orders():
  if not g.get('current_staff') and not g.get('current_viewer'):
    return redirect(url_for('users_login', error="You need to be a staff member or viewer to list orders"))
  if g.get('current_staff'):
    orders = database.execute("SELECT ViewerOrder.ViewerOrderID, OrderDate, ViewedStatus, SUM(CASE WHEN FlagPerk = 1 THEN 0 ELSE Price END) AS OrderTotal FROM ViewerOrder LEFT JOIN ViewerOrderLine ON ViewerOrder.ViewerOrderID = ViewerOrderLine.ViewerOrderID LEFT JOIN Video ON ViewerOrderLine.VideoID = Video.VideoID WHERE ViewedStatus IN ('Pending', 'Viewed', 'Fraud') GROUP BY ViewerOrderID ORDER BY ViewerOrderID DESC;").fetchall()
  else:
    orders = database.execute("SELECT ViewerOrder.ViewerOrderID, OrderDate, ViewedStatus, SUM(CASE WHEN FlagPerk = 1 THEN 0 ELSE Price END) AS OrderTotal FROM ViewerOrder LEFT JOIN ViewerOrderLine ON ViewerOrder.ViewerOrderID = ViewerOrderLine.ViewerOrderID LEFT JOIN Video ON ViewerOrderLine.VideoID = Video.VideoID WHERE ViewerID = %s AND ViewedStatus IN ('Pending', 'Viewed') GROUP BY ViewerOrderID ORDER BY ViewerOrderID DESC;", (g.current_viewer['ViewerID'],)).fetchall()
  return render_template('orders/index.html', orders=orders)

@app.route("/orders/<order_id>/mark_as_fraud", methods=['POST'])
@staff_login_required
def orders_mark_as_fraud(order_id):
  database.execute("UPDATE ViewerOrder SET ViewedStatus = 'Fraud' WHERE ViewerOrderID = %s;", (order_id,))
  database.commit()
  flash("Marked this order as fraud. :-(", 'notice')
  return redirect(url_for('orders_show', order_id=order_id))
