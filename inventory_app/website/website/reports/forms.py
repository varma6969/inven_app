
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length
from website.models import Application

app_names = []

def apps():
    apps = Application.query.all()
    for app in apps:
        app_names.append(app.app_name)
    return app_names

class ReportingForm(FlaskForm):
    app_name = SelectField('Application', choices=apps(), validators=[DataRequired(), Length(min=2, max=10)])
    # host_name = SelectField('Host', choices=['weblogic', 'websphere', 'tomcat', 'jboss', 'nginx', 'mule'], validators=[DataRequired(), Length(min=2, max=10)])
    environment = SelectField('Environment', choices=['production', 'dr', 'newclient', 'uat', 'stage', 'qa', 'test', 'sit', 'dev'], validators=[DataRequired(), Length(min=2, max=10)])
    product_type = SelectField('Product Type', choices=['weblogic', 'websphere', 'tomcat', 'jboss', 'nginx', 'mule'], validators=[DataRequired(), Length(min=2, max=10)])
    product_version = SelectField('Product Version', choices=['12.1.3.0', '12.2.1.3', '12.2.1.4', '14.1.1.0'], validators=[DataRequired(), Length(min=2, max=10)])
    jdk_version = SelectField('JDK', choices=['1.8.0_221', '1.8.0_281', '1.8.0_291'], validators=[DataRequired(), Length(min=2, max=10)])
    patch_level = SelectField('Patches', choices=['q1_2021', 'q2_2021', 'q3_2021', 'q4_2021'], validators=[DataRequired(), Length(min=2, max=10)])
    submit = SubmitField('Run')
