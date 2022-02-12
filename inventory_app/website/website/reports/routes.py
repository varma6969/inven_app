from flask import render_template, request, redirect, flash, url_for, session, send_file, Blueprint
from website import app, db
from website.reports.forms import ReportingForm
from website.models import Application, Jvm, User, Sops
from flask_login import login_user, current_user, logout_user, login_required
from io import BytesIO
import io
import xlwt


reports = Blueprint('reports', __name__)


@reports.route('/inventory/download/excel', methods=['GET'])
@login_required
def get_inventory_excel():
        apps= Application.query.all() 
        output = io.BytesIO()
        workbook = xlwt.Workbook()
        for app in apps:
            instances = app.jvms            
            # style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on')            
            sheet = workbook.add_sheet(app.app_name)            
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
            sn = 1
            for instance in instances:                
                sheet.write(idx+1, 0, str(sn))
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
                sn += 1
            
        workbook.save(output)
        output.seek(0)
        return send_file(output, as_attachment=True, mimetype="application/ms-excel", attachment_filename='inventory.xls')

@reports.route('/reports', methods=['GET','POST'])
@login_required
def get_reports():
    form = ReportingForm()
    app = form.app_name.data
    env = form.environment.data
    product = form.product_type.data
    version = form.product_version.data
    jdk = form.jdk_version.data
    patch = form.patch_level.data
    instances = Jvm.query.filter_by(application_name=app, environment_name=env, product_type=product, product_version=version, jdk_version=jdk, patch_level=patch).all()
    if form.is_submitted():
        output = io.BytesIO()
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet('data')
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
        return send_file(output, as_attachment=True, mimetype="application/ms-excel", attachment_filename='report.xls')       
        
    return render_template('reports.html', title='reports', form=form) 

