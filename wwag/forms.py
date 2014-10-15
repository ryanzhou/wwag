from wtforms import Form, BooleanField, StringField, PasswordField, SelectField, TextAreaField, DateTimeField, DateField, DecimalField, SelectMultipleField, validators
from wwag import app, database

def all_players():
  with app.app_context():
    try:
      players = database.execute("SELECT PlayerID, FirstName, LastName FROM Player").fetchall()
      return [(p['PlayerID'], "%s %s" % (p['FirstName'],p["LastName"])) for p in players]
    except:
      return []

def all_instance_runs():
  with app.app_context():
    try:
      instance_runs = database.execute("SELECT InstanceRunID, Name FROM InstanceRun").fetchall()
      return [(i['InstanceRunID'], i['Name']) for i in instance_runs]
    except:
      return []

def all_games():
  with app.app_context():
    try:
      games = database.execute("SELECT GameID, Genre FROM Game").fetchall()
      return [(g['GameID'], g['Genre']) for g in games]
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

class ViewerRegistrationForm(Form):
  email = StringField('Email', [validators.Email()])
  password = PasswordField('Password', [validators.Length(min=6, max=128), validators.EqualTo('password_confirmation', message='Passwords must match')])
  password_confirmation = PasswordField('Password Confirmation')
  date_of_birth = DateField('Date of Birth', [validators.required()])

class VideoForm(Form):
  name = StringField('Video Name', [validators.Length(min=3, max=50)])
  instance_run_id = SelectField('Instance Run', coerce=int, choices=all_instance_runs())
  game_id = SelectField('Game', coerce=int, choices=all_games())
  price = DecimalField('Price')
  url = StringField('URL', [validators.URL()])
  video_type = SelectField('Type', choices=[(c, c) for c in ["Just for Fun", "Achievement Attempt", "Role Playing", "Team Challenge"]])

class GameForm(Form):
  game_name = StringField('Game Name', [validators.Length(min=3, max=50)])
  genre = SelectField('Genre', choices=[(c, c) for c in ['Action', 'Adventure', 'Role-playing', 'Simulation', 'Sports']])
  review = StringField('Review', [validators.Length(min=3, max=50)])
  star_rating = DecimalField('StarRating', [validators.DataRequired()])
  classification_rating = SelectField ('ClassificationRating', choices=[(c, c) for c in ["PG", "M", "CTC", "G"]])
  platform_notes = SelectMultipleField('PlatformNotes', choices=[(c, c) for c in ["iOS", "Playstation", "PC", "Android", "Xbox", "Wii", "Ouya", "Steam Machine", "3DS"]])
  cost = DecimalField('Cost', [validators.DataRequired()])

class AchievementForm(Form):
  achievement_name = StringField('Name', [validators.Length(min=3, max=50)])
  reward_body = SelectField('RewardBody', choices=[(c,c) for c in [ "Microsoft", "Apple", "Blizzard", "made-up by WWAG"]])
