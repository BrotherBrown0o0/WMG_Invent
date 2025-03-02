from flask import Blueprint, render_template, redirect, url_for, flash, request, send_from_directory, jsonify
from flask_login import login_required, current_user
from app.models.product import Product
from app.models.category import Category
from app import db
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, IntegerField, SelectField, URLField
from wtforms.validators import DataRequired, NumberRange, URL, Optional
import os

bp = Blueprint('products', __name__, url_prefix='/products')

class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0)])
    stock_level = IntegerField('Initial Stock Level', validators=[DataRequired(), NumberRange(min=0)])
    min_stock_level = IntegerField('Minimum Stock Level', validators=[DataRequired(), NumberRange(min=0)])
    category_id = SelectField('Category', coerce=int, validators=[DataRequired()])
    image_url = URLField('Image URL', validators=[Optional(), URL()])

@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 12
    category_id = request.args.get('category_id', type=int)
    search_query = request.args.get('q', '')

    # Get all categories for the filter dropdown
    categories = Category.query.all()

    # Base query
    query = Product.query

    # Apply search filter if specified
    if search_query:
        query = query.filter(Product.name.ilike(f'%{search_query}%'))

    # Apply category filter if specified
    if category_id:
        query = query.filter_by(category_id=category_id)

    # Paginate the results
    products = query.paginate(page=page, per_page=per_page)

    return render_template('products/index.html', products=products, categories=categories, selected_category=category_id, search_query=search_query)

@bp.route('/<int:id>')
def detail(id):
    product = Product.query.get_or_404(id)
    return render_template('products/detail.html', product=product)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if current_user.role not in ['admin', 'manager', 'site_admin']:
        flash('You do not have permission to create products')
        return redirect(url_for('products.index'))

    form = ProductForm()
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]

    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            stock_level=form.stock_level.data,
            min_stock_level=form.min_stock_level.data,
            category_id=form.category_id.data,
            image_url=form.image_url.data
        )
        db.session.add(product)
        db.session.commit()
        flash('Product created successfully')
        return redirect(url_for('products.detail', id=product.id))

    return render_template('products/create.html', form=form, categories=Category.query.all())

@bp.route('/<int:id>/edit', methods=['POST'])
@login_required
def edit(id):
    if current_user.role not in ['admin', 'site_admin']:
        return jsonify({'success': False, 'message': 'You do not have permission to edit products'}), 403

    product = Product.query.get_or_404(id)
    
    product.name = request.form['name']
    product.description = request.form['description']
    product.price = float(request.form['price'])
    product.stock_level = int(request.form['stock_level'])
    product.min_stock_level = int(request.form['min_stock_level'])
    product.category_id = int(request.form['category_id'])
    
    db.session.commit()
    return jsonify({'success': True, 'message': 'Product updated successfully'})

@bp.route('/images/products/<filename>')
def serve_image(filename):
    image_dir = os.path.abspath('C:/images/products')
    return send_from_directory(image_dir, filename)

@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    if not current_user.is_site_admin():
        flash('You do not have permission to delete products')
        return redirect(url_for('products.index'))
    
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    
    flash('Product deleted successfully')
    return redirect(url_for('admin.inventory'))

@bp.route('/<int:id>/update_stock', methods=['POST'])
@login_required
def update_stock(id):
    if current_user.role not in ['admin', 'manager', 'site_admin']:
        flash('You do not have permission to update stock')
        return redirect(url_for('products.detail', id=id))

    product = Product.query.get_or_404(id)
    quantity = int(request.form['quantity'])
    action = request.form['action']

    if action == 'add':
        product.stock_level += quantity
    elif action == 'remove':
        if product.stock_level - quantity < 0:
            flash('Cannot remove more stock than available')
            return redirect(url_for('products.detail', id=id))
        product.stock_level -= quantity

    db.session.commit()
    flash('Stock updated successfully')
    return redirect(url_for('products.detail', id=id)) 