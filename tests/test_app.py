import unittest
from app import create_app, db
from app.models.user import User
from app.models.product import Product
from app.models.category import Category
from app.models.order import Order
from app.models.stock_order import StockOrder
from config import Config

# Test configuration overrides default settings for testing
class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Use in-memory database
    WTF_CSRF_ENABLED = False                        # Disable CSRF for testing

# Main test case class for the website application
class WebsiteTestCase(unittest.TestCase):
    def setUp(self):
        # Create test app and configure test environment
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        # Create test users with different roles
        self.admin = User(username='admin', email='admin@test.com', role='admin')
        self.admin.set_password('adminpass')
        self.customer = User(username='customer', email='customer@test.com', role='customer')
        self.customer.set_password('customerpass')
        
        # Create test category
        self.category = Category(name='Electronics', description='Electronic devices')
        db.session.add(self.category)
        db.session.commit()
        
        # Create test product with stock levels
        self.product = Product(
            name='Test Laptop',
            description='A test laptop',
            price=999.99,
            stock_level=10,
            min_stock_level=5,
            category_id=self.category.id
        )
        
        # Add all test objects to database
        db.session.add_all([self.admin, self.customer, self.product])
        db.session.commit()

    def tearDown(self):
        # Clean up after tests
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_basic_pages(self):
        # Test home page loads
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'WMGInvent', response.data)

        # Test login page loads
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

        # Test products page loads
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)

    def test_database_operations(self):
        # Test user creation
        self.assertEqual(User.query.count(), 2)  # admin and customer
        
        # Test category creation
        self.assertEqual(Category.query.count(), 1)
        self.assertEqual(Category.query.first().name, 'Electronics')
        
        # Test product creation
        self.assertEqual(Product.query.count(), 1)
        self.assertEqual(Product.query.first().name, 'Test Laptop')

    def test_authentication(self):
        # Test login with correct credentials
        response = self.client.post('/login', data={
            'username': 'customer',
            'password': 'customerpass'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_product_stock(self):
        # Test product stock level
        product = Product.query.first()
        self.assertEqual(product.stock_level, 10)
        self.assertEqual(product.min_stock_level, 5)
        
        # Test stock status
        self.assertTrue(product.stock_level >= product.min_stock_level)

if __name__ == '__main__':
    unittest.main(verbosity=2) 