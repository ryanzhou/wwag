from wtforms import Form, BooleanField, StringField, PasswordField, validators

class LoginForm(Form):
  email = StringField('Email', [validators.Email()])
  password = PasswordField('Password', [validators.Length(min=6, max=128)])
