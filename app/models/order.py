from app import db
from datetime import datetime
from app.models.reorder import Reorder
from app.models.product import Product

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, approved, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref='orders')
    product = db.relationship('Product', backref='orders')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure the product is loaded
        if self.product_id:
            self.product = Product.query.get(self.product_id)
        
        # Remove stock immediately
        if self.product:
            if self.product.stock_level >= self.quantity:
                self.product.stock_level -= self.quantity
            else:
                raise ValueError("Not enough stock available")
        
        self.check_stock_level()

    def check_stock_level(self):
        if not self.product:
            raise ValueError(f"Product with ID {self.product_id} does not exist")
        
        if self.product.stock_level - self.quantity < self.product.min_stock_level:
            reorder_quantity = self.product.min_stock_level - (self.product.stock_level - self.quantity)
            reorder = Reorder(
                product_id=self.product_id,
                quantity=reorder_quantity
            )
            db.session.add(reorder) 