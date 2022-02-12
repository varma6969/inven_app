
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length


class JvmRegistrationForm(FlaskForm):
    jvm_name = StringField('Instance Name', validators=[DataRequired(), Length(min=2, max=10)])
    # environment = StringField('Environment', validators=[DataRequired(), Length(min=2, max=10)])
    environment = SelectField('Environment', choices=['production', 'dr', 'newclient', 'uat', 'stage', 'qa', 'test', 'sit', 'dev'], validators=[DataRequired(), Length(min=2, max=10)])
    app_name = StringField('Application Name', validators=[DataRequired(), Length(min=2, max=10)])
    hostname = StringField('Hostname', validators=[DataRequired(), Length(min=2, max=10)])
    ip_address = StringField('IP Address', validators=[DataRequired(), Length(min=2, max=10)])
    jdk_version = StringField('JDK Version', validators=[DataRequired(), Length(min=2, max=10)])
    # product_type = StringField('Product Type', validators=[DataRequired(), Length(min=2, max=10)])
    product_type = SelectField('Product Type', choices=['weblogic', 'websphere', 'tomcat', 'jboss', 'nginx', 'mule'], validators=[DataRequired(), Length(min=2, max=10)])
    product_version = StringField('Product Version', validators=[DataRequired(), Length(min=2, max=10)])
    patch_level = StringField('Latest patch Applied', validators=[DataRequired(), Length(min=2, max=10)])
    submit = SubmitField('Submit')
