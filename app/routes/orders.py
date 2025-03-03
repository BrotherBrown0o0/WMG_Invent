from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.order import Order
from app.models.product import Product
from app import db

# Create a blueprint for order-related routes with URL prefix
bp = Blueprint('orders', __name__, url_prefix='/orders')

@bp.route('/create', methods=['POST'])
@login_required
def create():
    # Get form data
    product_id = request.form.get('product_id', type=int)
    quantity = request.form.get('quantity', type=int)
    
    # Validate form data
    if not product_id or not quantity:
        flash('Invalid order data')
        return redirect(url_for('products.index'))
    
    # Get product by ID
    product = Product.query.get_or_404(product_id)
    
    # Check if enough stock is available
    if quantity > product.stock_level:
        flash('Not enough stock available')
        return redirect(url_for('products.detail', id=product_id))
    
    # Create new order
    order = Order(
        user_id=current_user.id,
        product_id=product_id,
        quantity=quantity,
        status='pending'
    )
    
    # Save to database
    db.session.add(order)
    db.session.commit()
    
    flash('Order placed successfully')
    return redirect(url_for('main.dashboard'))

@bp.route('/<int:id>/status', methods=['POST'])
@login_required
def update_status(id):
    # Check if user has permission to update order status
    if not current_user.can_manage_stock():
        flash('You do not have permission to update order status')
        return redirect(url_for('main.dashboard'))
    
    # Get order by ID
    order = Order.query.get_or_404(id)
    new_status = request.form.get('status')
    
    # Update status if valid
    if new_status in ['approved', 'completed', 'cancelled']:
        order.status = new_status
        db.session.commit()
        flash(f'Order status updated to {new_status}')
    
    return redirect(url_for('admin.orders'))

@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    # Check if user has permission to delete orders
    if not current_user.can_delete_orders():
        flash('You do not have permission to delete orders')
        return redirect(url_for('main.dashboard'))
    
    # Get order by ID
    order = Order.query.get_or_404(id)
    
    # Prevent deletion of completed orders
    if order.status == 'completed':
        flash('Cannot delete completed orders')
        return redirect(url_for('admin.orders'))
    
    # Return stock if order is pending or approved
    if order.status in ['pending', 'approved']:
        order.product.stock_level += order.quantity
    
    # Delete order and save changes
    db.session.delete(order)
    db.session.commit()
    
    flash('Order deleted successfully')
    return redirect(url_for('admin.orders')) 