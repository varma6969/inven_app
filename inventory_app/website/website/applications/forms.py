from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError
from website.models import Application


class ApplicationRegistrationForm(FlaskForm):
    application_name = StringField('Application Name', validators=[DataRequired(), Length(min=2, max=50)])
    app_manager = StringField('Application Manager', validators=[DataRequired(), Length(min=2, max=50)])
    support_group = StringField('Support Group', validators=[DataRequired(), Length(min=2, max=50)])
    additionalInfo = TextAreaField('Additional Information', validators=[DataRequired(), Length(min=2, max=1000)])
    submit = SubmitField('Add')
