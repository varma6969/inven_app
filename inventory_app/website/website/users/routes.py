from flask import render_template, request, redirect, flash, url_for, session, send_file, Blueprint
from website import app, db, bcrypt
from website.users.forms import UserLoginForm, UserRegistrationForm, SeperUserRegistrationForm, UserUpdateForm
from website.models import Application, Jvm, User, Sops
from flask_login import login_user, current_user, logout_user, login_required
from io import BytesIO
import io
import xlwt


users = Blueprint('users', __name__)


su_key = '$2a$04$6.4Vnon6XMy1tKI6B2CVreBHnZqIFVHcqikuztCUWcBVYBnfh2wbe'


@users.route('/', methods=['GET', 'POST'])
@users.route('/login', methods=['GET', 'POST'])
def user_login():  
    # if current_user.is_authenticated:
    #     return redirect(url_for('apps.home'))
    form = UserLoginForm()
    if form.is_submitted():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data): 
            login_user(user)
            next_page = request.args.get('next')
            flash(f' You have been logged in successfully..!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.home', current_user=user))        
        else:
            flash(f'Login unsuccessful..', 'danger')    
    return render_template('login.html', title='User Login', form=form)


@users.route('/logout')
def user_logout():
    logout_user()
    return redirect(url_for('users.user_login'))



@users.route('/user_register', methods=['GET', 'POST'])
def user_register():
    if current_user.is_authenticated:
        return redirect(url_for('apps.home'))
    form = UserRegistrationForm()    
    if form.is_submitted():
        mail = User.query.filter_by(email=form.email.data).first()
        if mail:
            flash(f'{form.email.data} alreaady Registered. Choose another one or contact Admin.', 'danger')
            return redirect(url_for('users.user_register'))
        else:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(user_name=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()        
            flash(f' Account created for {form.username.data} successfully..!', 'success')
            return redirect(url_for('users.user_login'))
    return render_template('user_register.html', title='User Registration', form=form)


@users.route('/su_r3gister', methods=['GET', 'POST'])
def su_register():
    form = SeperUserRegistrationForm()    
    if form.is_submitted():
        mail = User.query.filter_by(email=form.email.data).first()
        if bcrypt.check_password_hash(su_key, form.key.data):
            if mail:
                flash(f'{form.email.data} alreaady Registered. Choose another one or contact Admin.', 'danger')
                return redirect(url_for('users.su_register'))
            else:
                hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                s_user = User(user_name=form.username.data, email=form.email.data, password=hashed_password, role='super')
                db.session.add(s_user)
                db.session.commit()        
                flash(f' Account created for {form.username.data} successfully..!', 'success')
                return redirect(url_for('users.user_login'))
        else:
            flash(f'you entered a wrong key..', 'danger')
    return render_template('su_r3gister.html', title='SuperUser Registration', form=form)


@users.route('/adminpage/user_management', methods=['GET', 'POST'])
@login_required
def user_management():
    if current_user.is_authenticated and current_user.role == 'super':
        # return redirect(url_for('home'))
        users = User.query.all()
        return render_template('admin.html', title='Admin page', users=users)
    else:
        return redirect(url_for('users.user_login'))


@users.route('/<email>/edit', methods=['GET', 'POST'])
@login_required
def user_update(email):
    user = User.query.filter_by(email=email).first()    
    form = UserRegistrationForm()    
    if form.is_submitted():
        user.user_name=form.username.data
        user.email=form.email.data        
        user.role=form.role.data 
        db.session.commit()
        flash(f'{form.username.data} updated successfully!', 'success')
        return redirect(url_for('users.user_management'))  
    form.username.data = user.user_name
    form.email.data = user.email
    form.role.data = user.role     
    return render_template('update_user.html', title='Update user', form=form, legend='Update user')

@users.route('/<email>/delete', methods=['GET','POST'])
@login_required
def user_delete(email):
    user = User.query.filter_by(email=email).first()     
    db.session.delete(user)
    db.session.commit()
    flash(f'{user.user_name} deleted successfully!', 'success')
    return redirect(url_for('users.user_management')) 

@users.route('/account/<email>/edit', methods=['GET', 'POST'])
@login_required
def update_account(email):
    user = User.query.filter_by(email=email).first()    
    form = UserUpdateForm()    
    if form.is_submitted():
        if form.username.data != user.user_name:
            user.user_name=form.username.data
        if form.email.data != user.email:
            user.email=form.email.data  
        db.session.commit()
        flash(f'{form.username.data} Account updated successfully!', 'success')
        return redirect(url_for('apps.home'))  
    form.username.data = user.user_name
    form.email.data = user.email
    # form.role.data = user.role     
    return render_template('account.html', title='Edit user', form=form, legend='Edit user')

