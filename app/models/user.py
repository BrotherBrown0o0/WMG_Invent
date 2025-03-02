from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), nullable=False, default='user')  # 'user', 'admin', 'site_admin'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def can_manage_stock(self):
        return self.role in ['admin', 'site_admin']
    
    def can_manage_users(self):
        return self.role == 'site_admin'
    
    def can_delete_orders(self):
        return self.role == 'site_admin'
    
    def is_admin(self):
        return self.role in ['admin', 'site_admin']
    
    def is_site_admin(self):
        return self.role == 'site_admin'

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id)) 