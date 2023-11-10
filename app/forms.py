from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import InputRequired, EqualTo


class SignUpForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    address = StringField('Physical Address', validators=[InputRequired()])
    phone_number = StringField('Phone Number', validators=[InputRequired()])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    body = TextAreaField('Body', validators=[InputRequired()])
    image_url = StringField('Image URL')
    submit = SubmitField('Create Post')
