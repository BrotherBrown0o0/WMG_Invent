from app import create_app, db
from app.models.product import Product
from app.models.category import Category

def create_sample_products():
    app = create_app()
    with app.app_context():
        # Create the Electronics category
        electronics = Category(name='Electronics', description='Electronic devices and accessories')
        db.session.add(electronics)
        db.session.commit()

        # Sample products data
        products = [
            {
                'name': 'Apple iPad Pro 12.9"',
                'description': '12.9-inch Liquid Retina display, M1 chip, 5G capable',
                'price': 1099.99,
                'stock_level': 50,
                'min_stock_level': 10,
                'category_id': electronics.id
            },
            {
                'name': 'MacBook Pro 16"',
                'description': '16-inch Retina display, M1 Pro chip, 16GB RAM, 1TB SSD',
                'price': 2499.99,
                'stock_level': 30,
                'min_stock_level': 5,
                'category_id': electronics.id
            },
            {
                'name': 'iPhone 14 Pro',
                'description': '6.1-inch Super Retina XDR display, A16 Bionic chip, 5G',
                'price': 999.99,
                'stock_level': 100,
                'min_stock_level': 20,
                'category_id': electronics.id
            },
            {
                'name': 'Sony WH-1000XM5',
                'description': 'Noise cancelling wireless headphones with 30-hour battery life',
                'price': 399.99,
                'stock_level': 75,
                'min_stock_level': 15,
                'category_id': electronics.id
            },
            {
                'name': 'Samsung Galaxy Tab S8 Ultra',
                'description': '14.6-inch AMOLED display, Snapdragon 8 Gen 1, 5G',
                'price': 1099.99,
                'stock_level': 40,
                'min_stock_level': 10,
                'category_id': electronics.id
            },
            {
                'name': 'Dell XPS 15',
                'description': '15.6-inch 4K UHD display, Intel Core i7, 16GB RAM, 1TB SSD',
                'price': 1999.99,
                'stock_level': 25,
                'min_stock_level': 5,
                'category_id': electronics.id
            },
            {
                'name': 'Google Pixel 7 Pro',
                'description': '6.7-inch OLED display, Tensor G2 chip, 5G, 128GB',
                'price': 899.99,
                'stock_level': 60,
                'min_stock_level': 15,
                'category_id': electronics.id
            },
            {
                'name': 'Bose QuietComfort 45',
                'description': 'Noise cancelling headphones with 24-hour battery life',
                'price': 329.99,
                'stock_level': 80,
                'min_stock_level': 20,
                'category_id': electronics.id
            }
        ]

        # Add products to database
        for product_data in products:
            product = Product(**product_data)
            db.session.add(product)
        
        db.session.commit()
        print("Sample products added successfully!")

if __name__ == '__main__':
    create_sample_products() 