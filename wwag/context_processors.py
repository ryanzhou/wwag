from wwag import app
@app.context_processor
def templating_processor():
  def page_header(title, subtitle=''):
    return "<h1>%s<small>%s</small></h1>" % (title, subtitle)
  return dict(page_header=page_header)
