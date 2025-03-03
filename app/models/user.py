from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# User model for authentication and authorization
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)  # Unique username for login
    email = db.Column(db.String(120), unique=True, nullable=False)    # Unique email for contact
    password_hash = db.Column(db.String(128))                         # Securely stored password hash
    role = db.Column(db.String(20), nullable=False, default='user')   # Role-based access control
    created_at = db.Column(db.DateTime, default=datetime.utcnow)      # When user account was created
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Last account update

    def set_password(self, password):
        # Generate and store password hash
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        # Verify password against stored hash
        return check_password_hash(self.password_hash, password)
    
    def can_manage_stock(self):
        # Check if user can manage inventory
        return self.role in ['admin', 'site_admin']
    
    def can_manage_users(self):
        # Check if user can manage other users
        return self.role == 'site_admin'
    
    def can_delete_orders(self):
        # Check if user can delete orders
        return self.role == 'site_admin'
    
    def is_admin(self):
        # Check if user has admin privileges
        return self.role in ['admin', 'site_admin']
    
    def is_site_admin(self):
        # Check if user has highest level of access
        return self.role == 'site_admin'

# User loader for Flask-Login
@login_manager.user_loader
def load_user(id):
    # Load user by ID for session management
    return User.query.get(int(id)) 