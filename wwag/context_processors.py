from wwag import app
@app.context_processor
def templating_processor():
  def button_to(url, text):
    return "<form action='%s' method='POST'><input type='submit' value='%s' class='btn btn-sm btn-primary'></input></form>" % (url, text)
  return dict(button_to=button_to)
