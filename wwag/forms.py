from wtforms import Form, BooleanField, StringField, PasswordField, SelectField, TextAreaField, DateTimeField, DateField, DecimalField, SelectMultipleField, validators
from wwag import app, database

def all_players():
  players = database.execute("SELECT PlayerID, FirstName, LastName FROM Player;").fetchall()
  return [(p['PlayerID'], "%s %s" % (p['FirstName'],p["LastName"])) for p in players]

def all_instance_runs():
  instance_runs = database.execute("SELECT InstanceRunID, Name FROM InstanceRun;").fetchall()
  return [(i['InstanceRunID'], i['Name']) for i in instance_runs]

def all_games():
  games = database.execute("SELECT GameID, GameName FROM Game;").fetchall()
  return [(g['GameID'], g['GameName']) for g in games]

class LoginForm(Form):
  email = StringField('Email', [validators.Email()])
  password = PasswordField('Password', [validators.Length(min=6, max=128)])

class InstanceRunForm(Form):
  supervisor_id = SelectField('Supervisor', coerce=int)
  name = StringField('Name', [validators.Length(min=3, max=45)])
  recorded_time = DateTimeField('Recorded Time')
  category_name = SelectField('Category', choices=[(c, c) for c in ["Just for Fun", "Achievement Attempt", "Role Playing", "Team Challenge"]])

  def set_choices(self):
    self.supervisor_id.choices = all_players()

class AddInstanceRunPlayerForm(Form):
  player_id = SelectField('Player', coerce=int)
  performance_notes = TextAreaField('Performance Notes', [validators.optional(), validators.length(max=200)])

  def set_choices(self):
    self.player_id.choices = all_players()

class ViewerRegistrationForm(Form):
  email = StringField('Email', [validators.Email()])
  password = PasswordField('Password', [validators.Length(min=6, max=128), validators.EqualTo('password_confirmation', message='Passwords must match')])
  password_confirmation = PasswordField('Password Confirmation')
  date_of_birth = DateField('Date of Birth', [validators.required()])

class VideoForm(Form):
  name = StringField('Video Name', [validators.Length(min=3, max=50)])
  instance_run_id = SelectField('Instance Run', coerce=int)
  game_id = SelectField('Game', coerce=int)
  price = DecimalField('Price')
  url = StringField('URL', [validators.URL()])
  video_type = SelectField('Type', choices=[(c, c) for c in ["Just for Fun", "Achievement Attempt", "Role Playing", "Team Challenge"]])

  def set_choices(self):
    self.game_id.choices = all_games()
    self.instance_run_id.choices = all_instance_runs()

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
