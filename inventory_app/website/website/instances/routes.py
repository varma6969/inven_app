from flask import render_template, request, redirect, flash, url_for, session, send_file, Blueprint
from website import app, db
from website.instances.forms import  JvmRegistrationForm
from website.models import Application, Jvm, User
from flask_login import login_user, current_user, logout_user, login_required
from io import BytesIO
import io
import xlwt


instances = Blueprint('instances', __name__)


@instances.route('/<app_name>/download/excel', methods=['GET', 'POST'])
@login_required
def get_instances_excel(app_name):
        app = Application.query.filter_by(app_name=app_name).first()  
        instances = app.jvms
        output = io.BytesIO()
        # style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on')
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet(app_name)
        sheet.write(0, 0, 'S.no')
        sheet.write(0, 1, 'JVM Name')
        sheet.write(0, 2, 'Environment')
        sheet.write(0, 3, 'Application Name')
        sheet.write(0, 4, 'Host Name')
        sheet.write(0, 5, 'IP Address')
        sheet.write(0, 6, 'JDK Version')
        sheet.write(0, 7, 'Product Type')
        sheet.write(0, 8, 'Product Version')
        sheet.write(0, 9, 'Latest patch')

        idx = 0
        for instance in instances:
            sheet.write(idx+1, 0, str(instance.id))
            sheet.write(idx+1, 1, instance.jvm_name)
            sheet.write(idx+1, 2, instance.environment_name)
            sheet.write(idx+1, 3, instance.application_name)
            sheet.write(idx+1, 4, instance.host_name)
            sheet.write(idx+1, 5, instance.ip_name)
            sheet.write(idx+1, 6, instance.jdk_version)
            sheet.write(idx+1, 7, instance.product_type)
            sheet.write(idx+1, 8, instance.product_version)
            sheet.write(idx+1, 9, instance.patch_level)
            idx += 1
        
        workbook.save(output)
        output.seek(0)
        return send_file(output, as_attachment=True, mimetype="application/ms-excel", attachment_filename=app_name+'.xls')

@instances.route('/instances/<app_name>/<env>', methods=['GET', 'POST'])
@login_required
def get_instances_env(app_name, env):
    app = Application.query.filter_by(app_name=app_name).first()
    instances = Jvm.query.filter_by(application_name=app_name, environment_name=env).all()    
    print(instances)    
    return render_template('application.html', title='Application', jvms=instances, app=app)


@instances.route('/instance_register/<app_name>', methods=['GET', 'POST'])
@login_required
def instance_register(app_name):
    form = JvmRegistrationForm()
    app = Application.query.filter_by(app_name=app_name).first()
    if form.is_submitted():
        jvm = Jvm(jvm_name=form.jvm_name.data,
                    environment_name=form.environment.data,
                    application_name=app.app_name,
                    host_name=form.hostname.data,
                    ip_name=form.ip_address.data,
                    jdk_version=form.jdk_version.data,
                    product_type=form.product_type.data,
                    product_version=form.product_version.data,
                    patch_level=form.patch_level.data
                    )
        db.session.add(jvm)
        db.session.commit()
        flash(f'{form.jvm_name.data} added successfully!', 'success')
        return redirect(url_for('instances.get_instances_env', app_name=app_name, env=form.environment.data))
    return render_template('instance_register.html', title='Register Instance', form=form, app_name=app_name, legend='Register Instance')


@instances.route('/weblogic')
@login_required
def get_weblogic():
    page = request.args.get('page', 1, type=int)
    wl_instances = Jvm.query.filter_by(product_type='weblogic').paginate(page=page, per_page=15)
    wl_count = wl_instances.total   
    return render_template('weblogic.html', title='WebLogic', jvms=wl_instances, count=wl_count)


@instances.route('/websphere')
@login_required
def get_websphere():
    page = request.args.get('page', 1, type=int)
    was_instances = Jvm.query.filter_by(product_type='websphere').paginate(page=page, per_page=15)
    was_count = was_instances.total
    return render_template('websphere.html', title='WebSphere', jvms=was_instances, count=was_count)


@instances.route('/tomcat')
@login_required
def get_tomcat():
    page = request.args.get('page', 1, type=int)
    tc_instances = Jvm.query.filter_by(product_type='tomcat').paginate(page=page, per_page=15)
    tc_count = tc_instances.total
    return render_template('tomcat.html', title='Tomcat', jvms=tc_instances, count=tc_count)


@instances.route('/jboss')
@login_required
def get_jboss():
    page = request.args.get('page', 1, type=int)
    jb_instances = Jvm.query.filter_by(product_type='jboss').paginate(page=page, per_page=15)
    jb_count = jb_instances.total
    return render_template('jboss.html', title='JBoss', jvms=jb_instances, count=jb_count)


@instances.route('/nginx')
@login_required
def get_nginx():
    page = request.args.get('page', 1, type=int)
    ng_instances = Jvm.query.filter_by(product_type='nginx').paginate(page=page, per_page=15)
    ng_count = ng_instances.total
    return render_template('nginx.html', title='Nginx', jvms=ng_instances, count=ng_count)



@instances.route('/<app_name>/<env>/<jvm>/edit', methods=['GET', 'POST'])
@login_required
def instance_update(app_name, env, jvm):
    app = Application.query.filter_by(app_name=app_name).first()
    instance = Jvm.query.filter_by(jvm_name=jvm, environment_name=env, application_name=app.app_name).first()
    form = JvmRegistrationForm()    
    if form.is_submitted():
        instance.jvm_name=form.jvm_name.data
        instance.environment_name=form.environment.data
        instance.application_name=app.app_name
        instance.host_name=form.hostname.data
        instance.ip_name=form.ip_address.data
        instance.jdk_version=form.jdk_version.data
        instance.product_type=form.product_type.data
        instance.product_version=form.product_version.data
        instance.patch_level=form.patch_level.data                
        #db.session.add(jvm)
        db.session.commit()
        flash(f'{form.jvm_name.data} updated successfully!', 'success')
        return redirect(url_for('instances.get_instances_env', app_name=app_name, env=env))  
    form.jvm_name.data = instance.jvm_name
    form.environment.data = instance.environment_name
    form.hostname.data = instance.host_name
    form.ip_address.data = instance.ip_name
    form.jdk_version.data = instance.jdk_version
    form.product_type.data = instance.product_type
    form.product_version.data = instance.product_version
    form.patch_level.data = instance.patch_level  
    return render_template('instance_register.html', title='Update Instance', form=form, app_name=app_name, legend='Update Instance')


@instances.route('/<app_name>/<env>/<jvm>/delete', methods=['GET', 'POST'])
@login_required
def instance_delete(app_name, env, jvm):
    app = Application.query.filter_by(app_name=app_name).first()
    instance = Jvm.query.filter_by(jvm_name=jvm, environment_name=env, application_name=app.app_name).first()
    db.session.delete(instance)
    db.session.commit()
    flash(f'{instance.jvm_name} deleted successfully!', 'success')
    return redirect(url_for('instances.get_instances_env', app_name=app_name, env=env)) 

