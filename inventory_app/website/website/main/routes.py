
from flask import render_template, redirect, flash, url_for, session, Blueprint
from website import app, db
from website.applications.forms import ApplicationRegistrationForm
from website.models import Application, Jvm, Sops
from flask_login import login_required

main = Blueprint('main', __name__)


@main.route('/home')
@login_required
def home():
    jvms = Jvm.query.all()
    apps = Application.query.all()
    sops = Sops.query.all()
    total_apps = len(apps)
    total_jvms = len(jvms)
    total_sops = len(sops)
    return render_template('home.html', title='Home', app_count=total_apps, jvm_count=total_jvms, sop_count=total_sops)
