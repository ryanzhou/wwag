from flask import g
from wwag import app, database

@app.context_processor
def templating_processor():
  def button_to(url, text):
    return "<form action='%s' method='POST'><input type='submit' value='%s' class='btn btn-sm btn-primary'></input></form>" % (url, text)
  return dict(button_to=button_to)

@app.context_processor
def open_order_items_count():
  if g.get('open_order'):
    viewer_order_id = g.open_order['ViewerOrderID']
    result = database.execute("SELECT COUNT(*) AS COUNT FROM ViewerOrderLine WHERE ViewerOrderID = %s;", (viewer_order_id,)).fetchone()["COUNT"]
    return dict(open_order_items_count=result)
  else:
    return dict()
