import os
from app import create_app, db
from populate_products import create_sample_products
from init_test_accounts import create_test_data

def reset_and_populate():
    app = create_app()
    with app.app_context():
        # Drop all tables
        db.drop_all()
        print("Database cleared successfully!")

        # Create all tables
        db.create_all()
        print("Database recreated successfully!")

        # Populate products
        create_sample_products()

        # Initialize test accounts
        create_test_data()
        print("Test accounts initialized successfully!")

if __name__ == '__main__':
    reset_and_populate()
    app = create_app()
    app.run(debug=True) 