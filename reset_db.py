import os
from app import create_app, db
from app.models import user, product, category, order

def reset_database():
    app = create_app()
    with app.app_context():
        # Drop all tables
        db.drop_all()
        # Create all tables
        db.create_all()
        print("Database recreated successfully!")

if __name__ == '__main__':
    reset_database() 