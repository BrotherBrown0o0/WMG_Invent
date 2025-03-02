# WMG INVENTORY MANAGEMENT SYSTEM REPORT

## Introduction

The WMG Inventory Management System (WMGInvent) is a web-based application designed to address the need for efficient inventory management in businesses dealing with physical goods. In today's competitive retail landscape, effective inventory management is crucial for maintaining healthy margins, ensuring product availability, and providing excellent customer service. The WMGInvent system has been developed to meet these needs through a user-friendly interface that allows for product browsing, stock tracking, order processing, and inventory reporting.

This report details the development, implementation, and testing of the WMGInvent system, following a structured approach to software development. The system is built using Python and the Flask web framework, providing a robust foundation for web-based applications. The report covers the system's requirements, design considerations, implementation details, testing strategies, and future development possibilities.

## General Description

### System Overview

The WMGInvent is a comprehensive inventory management solution that enables businesses to track their goods throughout the entire supply chain. The system is designed to provide real-time visibility of inventory levels, facilitate order processing, and offer statistical information for effective decision-making. The core functionalities include:

- Product listing and categorization
- Stock level tracking and management
- Order processing
- User and permission management
- Inventory reporting

### Product Category

This implementation focuses on a general inventory system capable of handling multiple product categories. The system supports various product types including electronics, books, health products, grocery items, and home appliances. Each product category can have specific attributes while sharing common properties such as name, description, price, and stock levels.

### Architecture

The application follows a Model-View-Controller (MVC) architecture, with Flask serving as the web framework. The system utilizes SQLAlchemy as the Object-Relational Mapping (ORM) tool, allowing for efficient database operations without writing raw SQL. The application's structure is organized into several key components:

- Models: Define the data structures and relationships
- Routes: Handle HTTP requests and responses
- Templates: Render the user interface
- Static Files: Contain CSS, JavaScript, and images

The system uses a SQLite database during development, which can be easily migrated to more robust database solutions like PostgreSQL or MySQL for production environments.

## Requirements

### Functional Requirements

1. User Authentication and Role Management
   - The system must support multiple user roles (customer, manager, admin, site admin)
   - Each role has specific permissions and access levels
   - Secure login and authentication processes

2. Product Management
   - Add, update, and delete product information
   - Categorize products into different types (electronics, books, etc.)
   - Track product stock levels and set minimum stock thresholds

3. Order Processing
   - Allow customers to place orders for products
   - Process orders based on stock availability
   - Update stock levels automatically after order placement

4. Stock Management
   - Monitor current stock levels for all products
   - Generate alerts when stock falls below minimum threshold
   - Process stock orders to replenish inventory

5. Inventory Reporting
   - Display stock status for products
   - Track order history
   - Generate reports on stock movements

### Non-Functional Requirements

1. Usability
   - Intuitive user interface
   - Responsive design for different screen sizes
   - Clear navigation between different sections

2. Performance
   - Fast page loading times
   - Efficient database queries
   - Responsive user interactions

3. Security
   - Role-based access control
   - Password hashing and secure authentication
   - CSRF protection

4. Maintainability
   - Modular code structure
   - Comprehensive documentation
   - Unit tests for key functionality

## Design

### Database Design

The database design of WMGInvent consists of several key entities and their relationships:

1. User: Stores user information and authentication details
2. Product: Contains product details, pricing, and stock levels
3. Category: Organizes products into different categories
4. Order: Tracks customer orders and order status
5. StockOrder: Manages inventory replenishment requests

The database schema implements relationships such as:
- One-to-many relationship between Category and Product
- One-to-many relationship between User and Order
- Many-to-one relationship between Product and Order

### Class Diagram

Below is a class diagram representing the key entities in the WMGInvent system and their relationships:

[Figure 1: Class Diagram for WMGInvent System]

```
+---------------+       +---------------+       +---------------+
|     User      |       |    Product    |       |   Category    |
+---------------+       +---------------+       +---------------+
| id            |       | id            |       | id            |
| username      |       | name          |       | name          |
| email         |       | description   |       | description   |
| password_hash |       | price         |       +---------------+
| role          |       | stock_level   |              ^
+---------------+       | min_stock_level|              |
       ^                | category_id    |-------------+
       |                | image_url      |
       |                +---------------+
       |                        ^
       |                        |
+------+------+        +--------+-------+       +---------------+
|    Order    |        |   StockOrder   |       |   Reorder     |
+-------------+        +----------------+       +---------------+
| id          |        | id             |       | id            |
| user_id     |--------| product_id     |-------| product_id    |
| product_id  |        | quantity       |       | quantity      |
| quantity    |        | status         |       | status        |
| status      |        | created_at     |       | created_at    |
| created_at  |        +----------------+       +---------------+
+-------------+
```

### User Interface Design

The user interface is designed to be intuitive and responsive, with clear separation between different functional areas:

- Main Dashboard: Provides an overview of key metrics and quick access to main functions
- Product Listing: Displays products organized by categories with filtering options
- Product Detail: Shows detailed information about a specific product
- Order Management: Interfaces for placing and tracking orders
- Admin Panel: Administrative tools for managing products, users, and stock

The interface utilizes modern web design principles, employing a clean and consistent layout across all pages to ensure a seamless user experience.

### Sequence Diagram

The following sequence diagram illustrates the order processing workflow in the WMGInvent system:

[Figure 2: Sequence Diagram for Order Processing]

```
User                  System               Product             Order             StockOrder
 |                      |                     |                  |                    |
 | Place Order          |                     |                  |                    |
 |--------------------->|                     |                  |                    |
 |                      | Check Stock         |                  |                    |
 |                      |-------------------->|                  |                    |
 |                      |                     |                  |                    |
 |                      | If Stock Available  |                  |                    |
 |                      |---------------------|                  |                    |
 |                      | Create Order        |                  |                    |
 |                      |-------------------------------->|      |                    |
 |                      |                     |           |      |                    |
 |                      | Update Stock Level  |           |      |                    |
 |                      |-------------------->|           |      |                    |
 |                      |                     |           |      |                    |
 |                      | Check Min Stock     |           |      |                    |
 |                      |-------------------->|           |      |                    |
 |                      |                     |           |      |                    |
 |                      | If Below Threshold  |           |      |                    |
 |                      |---------------------|           |      |                    |
 |                      | Create Stock Order  |           |      |                    |
 |                      |---------------------------------------------->|            |
 |                      |                     |           |      |                    |
 | Order Confirmation   |                     |           |      |                    |
 |<---------------------|                     |           |      |                    |
 |                      |                     |           |      |                    |
```

## Implementation Detail

### Technology Stack

The WMGInvent system is implemented using the following technologies:

- Backend: Python 3.x with Flask web framework
- Database: SQLite (development), with ORM provided by SQLAlchemy
- Frontend: HTML5, CSS, JavaScript with Tailwind CSS for styling
- Authentication: Flask-Login for user session management
- Forms: Flask-WTF for form handling and validation

### Key Components

#### User Authentication and Authorization

Table 1: User Model Implementation
| Code | Description |
|------|-------------|
| ```python
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), nullable=False, default='user')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        return self.role in ['admin', 'site_admin']
``` | The User model implements role-based access control with methods to validate passwords and check permissions. The model uses Werkzeug's password hashing functions to securely store passwords. User roles determine access levels to different functionalities within the system. |

[Figure 3: User Authentication Screen]
(Screenshot placeholder - User login interface)

#### Product Management

Table 2: Product Model Implementation
| Code | Description |
|------|-------------|
| ```python
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    stock_level = db.Column(db.Integer, default=0)
    min_stock_level = db.Column(db.Integer, default=10)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
``` | The Product model maintains essential information about each product, including stock levels. The model tracks both current stock level and minimum required stock level to facilitate automatic reordering. Products are associated with categories through a foreign key relationship. |

[Figure 4: Product Management Interface]
(Screenshot placeholder - Product management dashboard)

#### Order Processing

Table 3: Order Model Implementation
| Code | Description |
|------|-------------|
| ```python
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='pending')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove stock immediately
        if self.product:
            if self.product.stock_level >= self.quantity:
                self.product.stock_level -= self.quantity
            else:
                raise ValueError("Not enough stock available")
``` | The Order model handles the process of customer orders, automatically adjusting stock levels. When an order is created, it immediately checks product availability and updates the stock level. The model raises an exception if insufficient stock is available, preventing invalid orders. |

[Figure 5: Order Processing Flow]
(Screenshot placeholder - Order creation and processing interface)

### API Routes

The system implements various API endpoints to handle different functionalities:

#### Products
- GET /products/: List all products
- GET /products/<id>: View product details
- POST /products/create: Create new product (Admin only)
- POST /products/<id>/update: Update product (Admin only)
- POST /products/<id>/delete: Delete product (Admin only)

#### Orders
- GET /orders/: List user's orders
- POST /orders/create: Create new order
- GET /orders/<id>: View order details
- POST /orders/<id>/update: Update order status (Admin only)

#### Stock Management
- GET /admin/stock-orders/: List stock orders
- POST /admin/stock-orders/create: Create stock order
- POST /admin/stock-orders/<id>/approve: Approve stock order
- POST /admin/stock-orders/<id>/complete: Complete stock order

## Test Case Design

The application includes a comprehensive test suite to ensure the reliability and correctness of its core functionalities. The tests use Python's built-in unittest framework and are designed to validate different aspects of the system.

### Test Configuration

Table 4: Test Configuration Implementation
| Code | Description |
|------|-------------|
| ```python
class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
``` | The test configuration disables CSRF protection and uses an in-memory SQLite database to ensure tests run quickly and don't affect the production database. The TESTING flag enables Flask's testing mode, which provides additional debugging information. |

### Test Cases

#### Basic Page Tests

Table 5: Basic Page Test Implementation
| Code | Description |
|------|-------------|
| ```python
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
``` | The basic page test verifies that the main application pages load correctly. The test checks both the HTTP status code (200 for success) and the presence of expected content in the response. This ensures that the routing system and template rendering are working properly. |

#### Database Operation Tests

Table 6: Database Operation Test Implementation
| Code | Description |
|------|-------------|
| ```python
def test_database_operations(self):
    # Test user creation
    self.assertEqual(User.query.count(), 2)  # admin and customer
    
    # Test category creation
    self.assertEqual(Category.query.count(), 1)
    self.assertEqual(Category.query.first().name, 'Electronics')
    
    # Test product creation
    self.assertEqual(Product.query.count(), 1)
    self.assertEqual(Product.query.first().name, 'Test Laptop')
``` | The database operation test ensures that database models are functioning correctly. The test verifies that database records can be created and queried as expected. This validates both the model definitions and the SQLAlchemy ORM integration. |

#### Authentication Tests

Table 7: Authentication Test Implementation
| Code | Description |
|------|-------------|
| ```python
def test_authentication(self):
    # Test login with correct credentials
    response = self.client.post('/login', data={
        'username': 'customer',
        'password': 'customerpass'
    }, follow_redirects=True)
    self.assertEqual(response.status_code, 200)
``` | The authentication test validates the user login functionality. It submits login credentials to the login endpoint and verifies that the request succeeds. The test uses follow_redirects=True to follow any redirects after successful login, simulating a complete user journey. |

#### Stock Management Tests

Table 8: Stock Management Test Implementation
| Code | Description |
|------|-------------|
| ```python
def test_product_stock(self):
    # Test product stock level
    product = Product.query.first()
    self.assertEqual(product.stock_level, 10)
    self.assertEqual(product.min_stock_level, 5)
    
    # Test stock status
    self.assertTrue(product.stock_level >= product.min_stock_level)
``` | The stock management test verifies the stock level tracking functionality. It checks that product stock levels are correctly maintained and that stock status can be determined based on the relationship between current and minimum stock levels. This is crucial for the inventory management aspect of the system. |

## Code Management and Deployment

### Version Control

Although not explicitly implemented in the current project, a version control system like Git is recommended for tracking changes, collaborating with team members, and maintaining code history. The repository structure is designed to be compatible with Git, with clear separation of concerns and modular components.

The recommended code management workflow includes:
1. Feature branches for new development
2. Pull requests for code review
3. Continuous integration for automated testing
4. Tagged releases for versioning

### Deployment Strategy

The application is designed to be easily deployed to various environments. The recommended deployment process includes:

1. Environment Setup: Creating a virtual environment and installing dependencies
2. Configuration: Setting environment variables for production settings
3. Database Migration: Running migrations to set up the database schema
4. Server Configuration: Setting up a production web server like Gunicorn or uWSGI
5. Reverse Proxy: Configuring Nginx or Apache as a reverse proxy

### Running the Application

To run the application locally:

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python run.py
```

The application will be available at `http://localhost:5000`

## Progression of Work

The development of WMGInvent followed an iterative approach, with several key milestones:

1. Initial Setup and Planning:
   - Defined the project scope and requirements
   - Set up the basic Flask application structure
   - Created the database models

2. Core Functionality Implementation:
   - Developed user authentication system
   - Implemented product management features
   - Created order processing workflows

3. UI Development:
   - Designed responsive templates
   - Implemented Tailwind CSS for styling
   - Created admin dashboard interface

4. Testing and Refinement:
   - Developed unit tests for key functionality
   - Conducted user testing
   - Refined features based on feedback

5. Documentation:
   - Created comprehensive README
   - Documented API endpoints
   - Wrote installation and deployment instructions

The development process emphasized agility, with each iteration adding new features while refining existing ones. Regular testing was integrated throughout the development cycle to ensure stability and reliability.

## Current Status and Future Work

### Current Status

The WMGInvent system has successfully implemented all the core requirements specified in the project brief. The current version includes:

- Complete user authentication and role-based access control
- Comprehensive product management functionality
- Order processing with automatic stock level updates
- Stock order management for inventory replenishment
- Basic reporting and visualization features
- Responsive user interface

All key functionalities have been implemented and are working as expected. The system has been tested with unit tests to ensure reliability.

### Future Development

While the current implementation meets the basic requirements, several enhancements could be made in future iterations:

1. Advanced Reporting:
   - Implement more sophisticated reporting tools
   - Add data visualization with charts and graphs
   - Create exportable reports in various formats

2. Integration Capabilities:
   - Develop APIs for integration with other systems
   - Implement webhook functionality for real-time notifications
   - Support for barcode scanning or RFID

3. Performance Improvements:
   - Optimize database queries for larger datasets
   - Implement caching mechanisms
   - Add asynchronous processing for long-running tasks

4. Enhanced Security:
   - Implement two-factor authentication
   - Add more granular permission controls
   - Enhance audit logging for security events

5. Mobile Application:
   - Develop a companion mobile app for on-the-go inventory management
   - Implement push notifications for critical alerts

## Conclusion

The WMG Inventory Management System represents a successful implementation of a web-based inventory management solution. The system demonstrates how modern web technologies can be used to create efficient tools for business operations. By leveraging Python, Flask, and SQLAlchemy, the application provides a robust foundation that can be extended and customized to meet specific business needs.

The development process followed software engineering best practices, including requirements analysis, structured design, modular implementation, and comprehensive testing. The resulting system is not only functional but also maintainable and extensible.

Through the creation of WMGInvent, we have shown how a well-designed inventory management system can streamline operations, reduce costs, and improve customer satisfaction. The modular architecture and clear separation of concerns ensure that the system can evolve with changing business requirements and technological advancements.

As businesses continue to seek more efficient ways to manage their inventory, solutions like WMGInvent will play an increasingly important role in maintaining competitive advantage in the marketplace.

## Appendix

### Appendix A: Project Structure

The project follows a modular structure organized as follows:

```
WMG_Invent/
├── app/
│   ├── models/         # Database models
│   ├── routes/         # Route handlers
│   ├── templates/      # HTML templates
│   └── static/         # Static files (CSS, JS)
├── tests/             # Test files
├── requirements.txt   # Dependencies
└── run.py            # Application entry point
```

### Appendix B: Installation Guide

Detailed steps for installing and configuring the system:

1. Clone the repository
2. Create a virtual environment
3. Install dependencies from requirements.txt
4. Configure environment variables
5. Initialize the database
6. Run the application

### Appendix C: User Roles and Permissions

Detailed description of the different user roles and their permissions within the system:

| Role | Description | Permissions |
|------|-------------|------------|
| Customer | Regular user who places orders | Browse products, place orders, view order history |
| Manager | Manages products and orders | Customer permissions + update product info, process orders |
| Admin | Administrative access | Manager permissions + create/delete products, manage users |
| Site Admin | Complete system access | Admin permissions + system configuration, full data access | 