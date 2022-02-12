
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, FileField
from wtforms.validators import DataRequired, Length, ValidationError, Email, EqualTo


class UserRegistrationForm(FlaskForm):
    username = StringField('UserName', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=2, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = StringField('Role', validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Submit')    

class SeperUserRegistrationForm(FlaskForm):
    username = StringField('UserName', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=2, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    key = PasswordField('Key', validators=[DataRequired()])
    role = StringField('Role', validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Sign Up')  

class UserLoginForm(FlaskForm):    
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=2, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])    
    submit = SubmitField('Login')

class UserUpdateForm(FlaskForm):
    username = StringField('UserName', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=2, max=50)])       
    submit = SubmitField('Update') 
