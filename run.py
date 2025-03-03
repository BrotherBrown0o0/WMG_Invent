import os
from app import create_app, db
from populate_products import create_sample_products
from init_test_accounts import create_test_data

def reset_and_populate():
    # Create Flask application instance
    app = create_app()
    with app.app_context():
        # Drop all tables to start with a clean database
        db.drop_all()
        print("Database cleared successfully!")

        # Create all tables based on models
        db.create_all()
        print("Database recreated successfully!")

        # Populate products with sample data
        create_sample_products()

        # Initialize test accounts with various roles
        create_test_data()
        print("Test accounts initialized successfully!")

if __name__ == '__main__':
    # Reset database and populate with initial data
    reset_and_populate()
    
    # Create Flask application instance
    app = create_app()
    
    # Run the application in debug mode
    app.run(debug=True) 