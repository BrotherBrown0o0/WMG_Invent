from app import create_app, db
from app.models.product import Product

app = create_app()
with app.app_context():
    products = Product.query.all()
    if not products:
        print("No products found in the database!")
    else:
        print(f"Found {len(products)} products:")
        for product in products:
            print(f"Product: {product.name}, SKU: {product.sku}") 