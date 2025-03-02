from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.product import Product
from app.models.category import Category
from app.models.order import Order
from app.models.user import User
from app.models.stock_order import StockOrder
import json

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
        
        # Create simple chart data without pandas
        products = Product.query.all()
        chart_data = {
            'data': [{
                'type': 'bar',
                'x': [p.name for p in products],
                'y': [p.stock_level for p in products],
                'name': 'Current Stock'
            }, {
                'type': 'bar',
                'x': [p.name for p in products],
                'y': [p.min_stock_level for p in products],
                'name': 'Minimum Stock'
            }],
            'layout': {
                'title': 'Stock Levels by Product',
                'barmode': 'group'
            }
        }
        chart_json = json.dumps(chart_data)
    else:
        total_products = low_stock_count = category_count = total_value = revenue = None
        chart_json = None
        
    # Data for site_admin only
    if current_user.can_manage_users():
        total_users = User.query.count()
        recent_users = User.query.order_by(User.id.desc()).limit(5).all()
    else:
        total_users = recent_users = None
    
    return render_template('main/dashboard.html',
                         user_orders=user_orders,
                         stock_orders=stock_orders,
                         total_products=total_products,
                         low_stock_count=low_stock_count,
                         category_count=category_count,
                         total_value=total_value,
                         revenue=revenue,
                         chart_json=chart_json,
                         total_users=total_users,
                         recent_users=recent_users) 