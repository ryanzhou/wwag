from wtforms import Form, BooleanField, StringField, PasswordField, SelectField, TextAreaField, validators
from wwag import app, database

def all_players():
  with app.app_context():
    players = database.execute("SELECT PlayerID, FirstName, LastName FROM Player").fetchall()
    return [(p['PlayerID'], "%s %s" % (p['FirstName'],p["LastName"])) for p in players]

class LoginForm(Form):
  email = StringField('Email', [validators.Email()])
  password = PasswordField('Password', [validators.Length(min=6, max=128)])

class AddInstanceRunPlayerForm(Form):
  player_id = SelectField('Player', coerce=int, choices=all_players())
  performance_notes = TextAreaField('Performance Notes', [validators.optional(), validators.length(max=200)])
