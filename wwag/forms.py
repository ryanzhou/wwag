from wtforms import Form, BooleanField, StringField, PasswordField, SelectField, TextAreaField, DateTimeField, validators
from wwag import app, database

def all_players():
  with app.app_context():
    try:
      players = database.execute("SELECT PlayerID, FirstName, LastName FROM Player").fetchall()
      return [(p['PlayerID'], "%s %s" % (p['FirstName'],p["LastName"])) for p in players]
    except:
      return []

class LoginForm(Form):
  email = StringField('Email', [validators.Email()])
  password = PasswordField('Password', [validators.Length(min=6, max=128)])

class InstanceRunForm(Form):
  supervisor_id = SelectField('Supervisor', coerce=int, choices=all_players())
  name = StringField('Name', [validators.Length(min=3, max=45)])
  recorded_time = DateTimeField('Recorded Time')
  category_name = SelectField('Category', choices=[(c, c) for c in ["Just for Fun", "Achievement Attempt", "Role Playing", "Team Challenge"]])

class AddInstanceRunPlayerForm(Form):
  player_id = SelectField('Player', coerce=int, choices=all_players())
  performance_notes = TextAreaField('Performance Notes', [validators.optional(), validators.length(max=200)])
