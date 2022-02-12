

from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField


class FileUploadForm(FlaskForm):    
    file_data = FileField('Upload File')
    submit = SubmitField('Upload') 