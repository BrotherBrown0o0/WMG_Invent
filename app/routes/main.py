import json
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.user import User
from app.models.product import Product
from app.models.category import Category
from app.models.order import Order
from app.models.stock_order import StockOrder
from sqlalchemy import desc

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    products = Product.query.order_by(Product.created_at.desc()).limit(10).all()
    categories = Category.query.all()
    return render_template('main/index.html', products=products, categories=categories)

@bp.route('/dashboard')
@login_required
def dashboard():
    # Common data for all users
    user_orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).limit(10).all()
    stock_orders = StockOrder.query.order_by(StockOrder.created_at.desc()).limit(10).all()
    
    # Data for admin and site_admin
    if current_user.can_manage_stock():
        total_products = Product.query.count()
        low_stock_products = Product.query.filter(Product.stock_level <= Product.min_stock_level).all()
        low_stock_count = len(low_stock_products)
        category_count = Category.query.count()
        total_value = sum(p.price * p.stock_level for p in Product.query.all())
        revenue = sum(o.total_price for o in Order.query.filter_by(status='Completed').all())
        
        # Get recent users for admin view (ordered by ID descending)
        recent_users = User.query.order_by(desc(User.id)).limit(5).all()
        
        # Prepare chart data in the format expected by Chart.js
        products = Product.query.all()
        chart_data = {
            'labels': [p.name for p in products],
            'current_stock': [p.stock_level for p in products],
            'min_stock': [p.min_stock_level for p in products]
        }
        
        return render_template('main/dashboard.html',
                             user_orders=user_orders,
                             stock_orders=stock_orders,
                             total_users=User.query.count(),
                             low_stock_count=low_stock_count,
                             revenue=revenue,
                             total_value=total_value,
                             recent_users=recent_users,
                             chart_json=json.dumps(chart_data))
    
    # For regular users
    return render_template('main/dashboard.html',
                         user_orders=user_orders) 