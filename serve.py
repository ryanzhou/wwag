from wsgiref.handlers import CGIHandler
from wwag import app
CGIHandler().run(app)
