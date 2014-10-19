from wtforms import Form, BooleanField, StringField, PasswordField, SelectField, TextAreaField, DateTimeField, DateField, DecimalField, SelectMultipleField, validators, IntegerField, RadioField
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

def all_equipment():
  equipment = database.execute("SELECT EquipmentID, ModelAndMake FROM Equipment;").fetchall()
  return [(e['EquipmentID'], e['ModelAndMake']) for e in equipment]

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
  star_rating = SelectField('Star Rating', coerce=int, choices=[(0,0), (1,1), (2,2), (3,3), (4,4), (5,5)])
  classification_rating = SelectField ('Classification Rating', choices=[(c, c) for c in ["PG", "M", "CTC", "G"]])
  platform_notes = SelectMultipleField('Platform Notes', choices=[(c, c) for c in ["iOS", "Playstation", "PC", "Android", "Xbox", "Wii", "Ouya", "Steam Machine", "3DS"]])
  cost = DecimalField('Cost', [validators.DataRequired()])

class AchievementForm(Form):
  achievement_name = StringField('Name', [validators.Length(min=3, max=50)])
  reward_body = SelectField('Reward Body', choices=[(c,c) for c in [ "Microsoft", "Apple", "Blizzard", "WWAG"]])

class VenueForm(Form):
  venue_name = StringField('Name', [validators.Length(min=3, max=50)])
  description = TextAreaField('Venue Description', [validators.Length(min=2, max=65535)])
  power_outlets = IntegerField('Power Outlets', [validators.DataRequired()])
  light = TextAreaField('Lighting Notes', [validators.Length(min=3, max=65535)])
  supervisor_id = SelectField('Supervisor', coerce=int)

  def set_choices(self):
    self.supervisor_id.choices = all_players()

class EquipmentForm(Form):
  model = SelectField('Model and Make', choices=[(c, c) for c in["iOS", "Playstation", "PC", "Android", "Xbox", "Wii", "Ouya", "Steam Machine", "3DS"]])
  review = StringField('Equipment Review', [validators.Length(min=3, max=50)])
  speed = StringField('Processor Speed', [validators.Length(min=0, max=50)])

class AddressForm(Form):
  street_number = StringField('Street Number', [validators.DataRequired()])
  street_number_suffix = StringField('Suffix')
  street_name = StringField('Street Name', [validators.DataRequired()])
  street_type = StringField('Street Type', [validators.DataRequired()])
  major_municipality = StringField('Suburb', [validators.DataRequired()])
  governing_district = StringField('State', [validators.DataRequired()])
  postal_area = StringField('Postcode', [validators.Length(min=2, max=8)])
  country = SelectField('Country', choices=[(c,c) for c in ["Australia", "Canada", "United States", "India", "Russia", "France", "Germany", "China", "Indonesia", "Japan", "United Kingdom", "South Korea"]])

class PlayerForm(Form):
  email = StringField('Email', [validators.Length(min=3, max=50)])
  password = PasswordField('Password', [validators.Length(min=6, max=128), validators.EqualTo('password_confirmation', message='Passwords must match'), validators.Optional()])
  password_confirmation = PasswordField('Password Confirmation')
  supervisor_id = SelectField('Supervisor', coerce=int)
  first_name = StringField('First Name', [validators.Length(min=3, max=50)])
  last_name = StringField('Last Name', [validators.Length(min=3, max=50)])
  role = SelectField('Role', choices=[(c, c) for c in ['Master User', 'Supervisor', 'Player']])
  type = SelectField('Type', choices=[('P', 'Regular Player'), ('S', 'Staff Member')])
  profile_description = TextAreaField('Profile Description', [validators.Length(min=3, max=65535)])
  game_handle = StringField('Game Handle', [validators.Length(min=3, max=50)])
  phone = StringField('Phone', [validators.Length(min=3, max=14)])
  voip = StringField('VoIP', [validators.Length(min=3, max=30)])

  def set_choices(self):
    self.supervisor_id.choices = all_players()

class VenueEquipmentForm(Form):
  equipment_id = SelectField('Equipment', coerce=int)
  financial_year_starting_date = DateField('Financial Year Starting Date', [validators.DataRequired()])
  software_version = StringField('Software Version', [validators.DataRequired()])

  def set_choices(self):
    self.equipment_id.choices = all_equipment()
