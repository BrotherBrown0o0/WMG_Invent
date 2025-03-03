from app import db
from datetime import datetime

# Product model representing inventory items
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)                     # Product name (required)
    description = db.Column(db.Text)                                     # Product description
    price = db.Column(db.Float, nullable=False)                          # Product price (required)
    stock_level = db.Column(db.Integer, default=0)                       # Current inventory count
    min_stock_level = db.Column(db.Integer, default=10)                  # Threshold for reordering
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)  # Product category
    image_url = db.Column(db.String(512))                                # For storing direct image URLs
    created_at = db.Column(db.DateTime, default=datetime.utcnow)         # Creation timestamp
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Last update
    
    def __repr__(self):
        # String representation for debugging
        return f'<Product {self.name}>' 