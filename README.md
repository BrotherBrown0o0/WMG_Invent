# WMG Inventory Management System

A comprehensive inventory management system built with Flask, designed to help businesses track products, manage stock levels, and process orders efficiently.

## Features

- **User Authentication**: Secure login and registration system with role-based access control
- **Product Management**: Add, edit, and delete products with detailed information
- **Order Processing**: Create and manage customer orders
- **Stock Level Monitoring**: Automatic tracking of inventory levels
- **Admin Dashboard**: Visualize sales data and inventory metrics
- **Reorder Automation**: Automatic reorder suggestions when stock is low

## Project Structure

The project follows a clean, modular structure:

```
wmg_invent/
├── app/                    # Application package
│   ├── models/             # Database models
│   ├── routes/             # Route blueprints
│   ├── static/             # Static assets (CSS, JS, images)
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   └── templates/          # HTML templates
├── instance/               # Instance-specific data
├── migrations/             # Database migrations
├── tests/                  # Test suite
├── config.py               # Configuration settings
├── requirements.txt        # Project dependencies
└── run.py                  # Application entry point
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd wmg_invent
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set environment variables:
   ```
   set FLASK_APP=run.py  # On Unix/Mac: export FLASK_APP=run.py
   set FLASK_ENV=development  # On Unix/Mac: export FLASK_ENV=development
   ```

5. Initialize the database:
   ```
   python run.py
   ```

## Running the Application

Start the development server:
```
flask run
```

Access the application at `http://localhost:5000`

## Testing

Run the test suite:
```
python -m unittest tests/test_app.py
```

## User Roles

- **Regular User**: Can browse products and place orders
- **Admin**: Can manage inventory and view orders
- **Site Admin**: Has full access to all features, including user management

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 