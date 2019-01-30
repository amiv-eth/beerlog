
# global imports
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, IntegerField, SelectField, HiddenField, TextAreaField
from wtforms.validators import DataRequired


class CredentialsLoginForm(FlaskForm):
    """
    Form for users to open new PresenceList
    """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    backend = SelectField('Event Type')
    submit = SubmitField('Login with Credentials')
    method_Cred = HiddenField('Credentials')
