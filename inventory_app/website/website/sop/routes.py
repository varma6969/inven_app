from flask import render_template, request, redirect, flash, url_for, session, send_file, Blueprint
from website import app, db
from website.sop.forms import FileUploadForm
from website.models import Sops
from flask_login import login_required
from io import BytesIO
import io
import xlwt

sops = Blueprint('sops', __name__)

@sops.route('/sops', methods=['GET','POST'])
@login_required
def get_sops(): 
    sops = Sops.query.all()
    sop_count = len(sops)   
    form = FileUploadForm()
    if form.is_submitted():
        if request.method == 'POST' and request.files:            
            f = form.file_data.data
            if f.filename != '':                
                new_file = Sops(f_name=f.filename, f_data=f.read())
                db.session.add(new_file)
                db.session.commit()
                flash(f'{f.filename} uploaded successfully..!', 'success')
                return redirect(url_for('sops.get_sops'))
            else:
                flash('No file selected..!', 'danger')
    return render_template('sops.html', title='SOPs', form=form, docs=sops, sop_count=sop_count)


@sops.route('/sops/<sop_name>/delete', methods=['GET','POST'])
@login_required
def sop_delete(sop_name):
    sop = Sops.query.filter_by(f_name=sop_name).first()    
    db.session.delete(sop)
    db.session.commit()
    flash(f'{sop_name} deleted successfully!', 'success')
    return redirect(url_for('sops.get_sops')) 


@sops.route('/sops/<sop_name>/download', methods=['GET','POST'])
@login_required
def sop_download(sop_name):
    sop = Sops.query.filter_by(f_name=sop_name).first()          
    return send_file(BytesIO(sop.f_data), as_attachment=True, attachment_filename=sop.f_name) 

