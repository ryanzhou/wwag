from wwag import app

@app.template_filter('date')
def date_filter(s):
    return s.strftime("%d %B %Y")
