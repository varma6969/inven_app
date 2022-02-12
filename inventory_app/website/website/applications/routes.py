from flask import render_template, redirect, flash, url_for, session, Blueprint
from website import app, db
from website.applications.forms import ApplicationRegistrationForm
from website.models import Application, Jvm, Sops
from flask_login import login_required

apps = Blueprint('apps', __name__)



@apps.route('/applications')
@login_required
def get_applications():
    applications = Application.query.all()   
    def get_instances(app_name):
        app = Application.query.filter_by(app_name=app_name).first()
        instances = app.jvms
        number = len(instances)
        return number
    return render_template('applications.html', title='Applications', applications=applications, get_instances=get_instances)

@apps.route('/app_register', methods=['GET', 'POST'])
@login_required
def application_register():
    form = ApplicationRegistrationForm()
    if form.is_submitted():
        application = Application.query.filter_by(
            app_name=form.application_name.data).first()
        if application:
            flash(f'{form.application_name.data} alreaady existed.', 'danger')
            return redirect(url_for('apps.get_applications'))
        else:
            application = Application(app_name=form.application_name.data, app_manager=form.app_manager.data,
                                      support_group=form.support_group.data, additional_info=form.additionalInfo.data)
            db.session.add(application)
            db.session.commit()
            flash(f'{form.application_name.data} added successfully!', 'success')
            return redirect(url_for('apps.get_applications'))
    return render_template('app_register.html', title='Register Application', form=form)