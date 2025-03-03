from app import db
from datetime import datetime
from app.models.reorder import Reorder
from app.models.product import Product

# Order model representing customer product orders
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)      # Customer who placed the order
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False) # Product being ordered
    quantity = db.Column(db.Integer, nullable=False)                               # Quantity ordered
    status = db.Column(db.String(20), default='pending')  # pending, approved, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)                   # When order was placed
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) # Last status update

    # Relationships with User and Product models
    user = db.relationship('User', backref='orders')      # Access orders via user.orders
    product = db.relationship('Product', backref='orders') # Access orders via product.orders

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure the product is loaded
        if self.product_id:
            self.product = Product.query.get(self.product_id)
        
        # Remove stock immediately when order is created
        if self.product:
            if self.product.stock_level >= self.quantity:
                self.product.stock_level -= self.quantity
            else:
                raise ValueError("Not enough stock available")
        
        # Check if reorder is needed
        self.check_stock_level()

    def check_stock_level(self):
        # Check if product exists
        if not self.product:
            raise ValueError(f"Product with ID {self.product_id} does not exist")
        
        # Check if stock level is below minimum threshold and create reorder if needed
        if self.product.stock_level - self.quantity < self.product.min_stock_level:
            # Calculate how much to reorder
            reorder_quantity = self.product.min_stock_level - (self.product.stock_level - self.quantity)
            reorder = Reorder(
                product_id=self.product_id,
                quantity=reorder_quantity
            )
            db.session.add(reorder) 