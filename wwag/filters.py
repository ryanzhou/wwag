from wwag import app

@app.template_filter('date')
def date_filter(s):
  return s.strftime("%d %B %Y")

@app.template_filter('youtube_thumbnail_url')
def youtube_thumbnail_url_filter(s):
  return "http://img.youtube.com/vi/" + s.split("/")[-1] + "/default.jpg"

@app.template_filter('price')
def price_filter(s):
  if s == None:
    return "Free"
  else:
    return "$%s" % s

@app.template_filter('viewer_type')
def viewer_type_filter(s):
  if s == "R":
    return "Regular"
  elif s == "P":
    return "Premium"
  elif s == "C":
    return "CrowdFunding"
