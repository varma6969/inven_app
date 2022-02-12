from website import db, login_manager, admin
from flask_login import UserMixin
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import LargeBinary


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    app_name = db.Column(db.String(20), nullable=False)
    app_manager = db.Column(db.String(20))
    support_group = db.Column(db.String(120))    
    additional_info = db.Column(db.Text)
    jvms = db.relationship('Jvm', backref='application', lazy=True)

    def __repr__(self):
        return f"Application('{self.app_name}', '{self.app_manager}', '{self.additional_info}')"

class Jvm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jvm_name = db.Column(db.String(20), nullable=False) 
    environment_name = db.Column(db.String(20), nullable=False) 
    #application_id = db.Column(db.Integer, db.ForeignKey('application.id'), nullable=False)  
    application_name = db.Column(db.String(20), db.ForeignKey('application.app_name'), nullable=False)
    host_name = db.Column(db.String(20), nullable=False)   
    ip_name = db.Column(db.Text(20), nullable=False)
    jdk_version = db.Column(db.String(20), nullable=False)
    product_type = db.Column(db.String(20), nullable=False)
    product_version = db.Column(db.String(20), nullable=False)  
    patch_level = db.Column(db.String(20), nullable=False) 
         

    def __repr__(self):
        return f"Instance('{self.jvm_name}', '{self.environment_name}', '{self.application_name}', '{self.host_name}', '{self.ip_name}', '{self.jdk_version}','{self.product_type}', '{self.product_version}')"
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)        
    role = db.Column(db.String(20), default='user')

    def __repr__(self):
        return f"User('{self.user_name}', '{self.email}', '{self.role}')"

class Sops(db.Model):
    id = db.Column(db.Integer, primary_key=True)    
    f_name =  db.Column(db.String(100))
    f_data = db.Column(db.LargeBinary)

    def __repr__(self):
        return f"Sops('{self.id}', '{self.f_name}')"


