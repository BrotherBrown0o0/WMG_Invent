from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.order import Order
from app.models.product import Product
from app import db

bp = Blueprint('orders', __name__, url_prefix='/orders')

@bp.route('/create', methods=['POST'])
@login_required
def create():
    product_id = request.form.get('product_id', type=int)
    quantity = request.form.get('quantity', type=int)
    
    if not product_id or not quantity:
        flash('Invalid order data')
        return redirect(url_for('products.index'))
    
    product = Product.query.get_or_404(product_id)
    
    if quantity > product.stock_level:
        flash('Not enough stock available')
        return redirect(url_for('products.detail', id=product_id))
    
    order = Order(
        user_id=current_user.id,
        product_id=product_id,
        quantity=quantity,
        status='pending'
    )
    
    db.session.add(order)
    db.session.commit()
    
    flash('Order placed successfully')
    return redirect(url_for('main.dashboard'))

@bp.route('/<int:id>/status', methods=['POST'])
@login_required
def update_status(id):
    if not current_user.can_manage_stock():
        flash('You do not have permission to update order status')
        return redirect(url_for('main.dashboard'))
    
    order = Order.query.get_or_404(id)
    new_status = request.form.get('status')
    
    if new_status in ['approved', 'completed', 'cancelled']:
        order.status = new_status
        db.session.commit()
        flash(f'Order status updated to {new_status}')
    
    return redirect(url_for('admin.orders'))

@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    if not current_user.can_delete_orders():
        flash('You do not have permission to delete orders')
        return redirect(url_for('main.dashboard'))
    
    order = Order.query.get_or_404(id)
    
    # Prevent deletion of completed orders
    if order.status == 'completed':
        flash('Cannot delete completed orders')
        return redirect(url_for('admin.orders'))
    
    # Return stock if order is pending or approved
    if order.status in ['pending', 'approved']:
        order.product.stock_level += order.quantity
    
    db.session.delete(order)
    db.session.commit()
    
    flash('Order deleted successfully')
    return redirect(url_for('admin.orders')) 