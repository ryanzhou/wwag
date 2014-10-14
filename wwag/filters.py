from wwag import app

@app.template_filter('date')
def date_filter(s):
  return s.strftime("%d %B %Y")

@app.template_filter('youtube_thumbnail_url')
def youtube_thumbnail_url_filter(s):
  return "http://img.youtube.com/vi/" + s.split("/")[-1] + "/default.jpg"
