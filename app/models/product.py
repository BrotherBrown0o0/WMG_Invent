from app import db
from datetime import datetime

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    stock_level = db.Column(db.Integer, default=0)
    min_stock_level = db.Column(db.Integer, default=10)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    image_url = db.Column(db.String(512))  # For storing direct image URLs
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Product {self.name}>' 