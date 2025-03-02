# WMG Inventory Management System

A web-based inventory management system.

## Setup and Running

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python run.py
```

The application will be available at `http://localhost:5000`

## Testing

To run the unit tests:
```bash
python -m unittest tests/test_app.py -v
``` 

## User Roles

- **Customer**: Can browse products and place orders
- **Manager**: Can manage products and process orders
- **Admin**: Full access to all features including user management
- **Site Admin**: System-level access with additional privileges

## API Routes

### Products
- `GET /products/`: List all products
- `GET /products/<id>`: View product details
- `POST /products/create`: Create new product (Admin only)
- `POST /products/<id>/update`: Update product (Admin only)
- `POST /products/<id>/delete`: Delete product (Admin only)

### Orders
- `GET /orders/`: List user's orders
- `POST /orders/create`: Create new order
- `GET /orders/<id>`: View order details
- `POST /orders/<id>/update`: Update order status (Admin only)

### Stock Management
- `GET /admin/stock-orders/`: List stock orders
- `POST /admin/stock-orders/create`: Create stock order
- `POST /admin/stock-orders/<id>/approve`: Approve stock order
- `POST /admin/stock-orders/<id>/complete`: Complete stock order