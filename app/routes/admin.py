from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.models.user import User
from app.models.product import Product
from app.models.category import Category
from app.models.order import Order
from app.models.stock_order import StockOrder
from app import db
import pandas as pd
import plotly.express as px
import json

bp = Blueprint('admin', __name__, url_prefix='/dashboard')

@bp.route('/')
@login_required
def index():
    if not current_user.is_admin():
        flash('You do not have permission to access the admin panel')
        return redirect(url_for('main.index'))
    
    total_products = Product.query.count()
    total_categories = Category.query.count()
    total_users = User.query.count()
    low_stock_products = Product.query.filter(Product.stock_level <= Product.min_stock_level).count()
    
    return render_template('admin/index.html',
                         total_products=total_products,
                         total_categories=total_categories,
                         total_users=total_users,
                         low_stock_products=low_stock_products)

@bp.route('/inventory')
@login_required
def inventory():
    if not current_user.can_manage_stock():
        abort(403)
    
    category_id = request.args.get('category_id', type=int)
    categories = Category.query.all()

    # Base query
    query = Product.query

    # Apply category filter if specified
    if category_id:
        query = query.filter_by(category_id=category_id)

    products = query.all()
    return render_template('admin/inventory.html', products=products, categories=categories, selected_category=category_id)

@bp.route('/users')
@login_required
def users():
    if not current_user.can_manage_users():
        abort(403)
    
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@bp.route('/users/<int:id>/role', methods=['POST'])
@login_required
def update_user_role(id):
    if not current_user.is_site_admin():
        flash('You do not have permission to update user roles')
        return redirect(url_for('main.index'))
    
    user = User.query.get_or_404(id)
    new_role = request.form.get('role')
    
    if new_role in ['user', 'admin', 'site_admin']:
        user.role = new_role
        db.session.commit()
        flash(f'Updated role for {user.username} to {new_role}')
    
    return redirect(url_for('admin.users'))

@bp.route('/orders')
@login_required
def orders():
    if not current_user.can_manage_stock():
        flash('You do not have permission to manage orders')
        return redirect(url_for('main.index'))
    
    status_filter = request.args.get('status')
    page = request.args.get('page', 1, type=int)
    
    query = Order.query
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    orders = query.order_by(Order.created_at.desc()).paginate(page=page, per_page=20)
    return render_template('admin/orders.html', orders=orders)

@bp.route('/stock-orders')
@login_required
def stock_orders():
    if not current_user.can_manage_stock():
        abort(403)
    
    selected_status = request.args.get('status', None)
    page = request.args.get('page', 1, type=int)
    per_page = 10

    # Base query
    query = StockOrder.query

    # Apply status filter if specified
    if selected_status:
        query = query.filter_by(status=selected_status)

    # Paginate the results
    stock_orders = query.order_by(StockOrder.created_at.desc()).paginate(page=page, per_page=per_page)

    return render_template('admin/stock_orders.html', stock_orders=stock_orders, selected_status=selected_status)

@bp.route('/stock-orders/create', methods=['GET', 'POST'])
@login_required
def create_stock_order():
    if not current_user.is_admin():
        flash('You do not have permission to create stock orders')
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        product_id = request.form.get('product_id', type=int)
        quantity = request.form.get('quantity', type=int)
        
        if not product_id or not quantity:
            flash('Invalid stock order data')
            return redirect(url_for('admin.create_stock_order'))
        
        stock_order = StockOrder(
            product_id=product_id,
            quantity=quantity
        )
        db.session.add(stock_order)
        db.session.commit()
        
        flash('Stock order created successfully')
        return redirect(url_for('admin.stock_orders'))
    
    products = Product.query.all()
    return render_template('admin/create_stock_order.html', products=products)

@bp.route('/stock-orders/<int:id>/approve', methods=['POST'])
@login_required
def approve_stock_order(id):
    if not current_user.is_admin():
        flash('You do not have permission to approve stock orders')
        return redirect(url_for('main.dashboard'))
    
    stock_order = StockOrder.query.get_or_404(id)
    stock_order.status = 'approved'
    db.session.commit()
    
    flash('Stock order approved successfully')
    return redirect(url_for('admin.stock_orders'))

@bp.route('/stock-orders/<int:id>/complete', methods=['POST'])
@login_required
def complete_stock_order(id):
    if not current_user.is_admin():
        flash('You do not have permission to complete stock orders')
        return redirect(url_for('main.dashboard'))
    
    stock_order = StockOrder.query.get_or_404(id)
    stock_order.product.stock_level += stock_order.quantity
    stock_order.status = 'completed'
    db.session.commit()
    
    flash('Stock order completed successfully')
    return redirect(url_for('admin.stock_orders'))

@bp.route('/stock-orders/<int:id>/delete', methods=['POST'])
@login_required
def delete_stock_order(id):
    if not current_user.is_site_admin():
        flash('You do not have permission to delete stock orders')
        return redirect(url_for('main.dashboard'))
    
    stock_order = StockOrder.query.get_or_404(id)
    db.session.delete(stock_order)
    db.session.commit()
    
    flash('Stock order deleted successfully')
    return redirect(url_for('admin.stock_orders')) 