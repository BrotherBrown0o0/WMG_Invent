from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.reorder import Reorder
from app.models.product import Product
from app import db

# Create a blueprint for reorder-related routes with URL prefix
bp = Blueprint('reorders', __name__, url_prefix='/reorders')

@bp.route('/')
@login_required
def index():
    # Check if user has admin permissions
    if not current_user.is_admin():
        flash('You do not have permission to view reorders')
        return redirect(url_for('main.dashboard'))
    
    # Get all reorder requests
    reorders = Reorder.query.all()
    return render_template('reorders/index.html', reorders=reorders)

@bp.route('/<int:id>/approve', methods=['POST'])
@login_required
def approve(id):
    # Check if user has admin permissions
    if not current_user.is_admin():
        flash('You do not have permission to approve reorders')
        return redirect(url_for('main.dashboard'))
    
    # Get reorder by ID and update status
    reorder = Reorder.query.get_or_404(id)
    reorder.status = 'approved'
    db.session.commit()
    
    flash('Reorder approved successfully')
    return redirect(url_for('reorders.index'))

@bp.route('/<int:id>/complete', methods=['POST'])
@login_required
def complete(id):
    # Check if user has admin permissions
    if not current_user.is_admin():
        flash('You do not have permission to complete reorders')
        return redirect(url_for('main.dashboard'))
    
    # Get reorder by ID, update product stock level, and mark as completed
    reorder = Reorder.query.get_or_404(id)
    reorder.product.stock_level += reorder.quantity
    reorder.status = 'completed'
    db.session.commit()
    
    flash('Reorder completed successfully')
    return redirect(url_for('reorders.index'))

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    # Check if user has admin permissions
    if not current_user.is_admin():
        flash('You do not have permission to create reorders')
        return redirect(url_for('main.dashboard'))
    
    # Process reorder creation form
    if request.method == 'POST':
        product_id = request.form.get('product_id', type=int)
        quantity = request.form.get('quantity', type=int)
        
        # Validate form data
        if not product_id or not quantity:
            flash('Invalid reorder data')
            return redirect(url_for('reorders.create'))
        
        # Get product by ID
        product = Product.query.get_or_404(product_id)
        
        # Create new reorder
        reorder = Reorder(
            product_id=product_id,
            quantity=quantity
        )
        db.session.add(reorder)
        db.session.commit()
        
        flash('Reorder created successfully')
        return redirect(url_for('reorders.index'))
    
    # Display reorder creation form
    products = Product.query.all()
    return render_template('reorders/create.html', products=products) 