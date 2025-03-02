from app import create_app, db
from app.models.user import User
from app.models.category import Category

def create_test_data():
    app = create_app()
    with app.app_context():
        # Create all categories
        categories = [
            {'name': 'Electronics', 'description': 'Electronic devices and accessories'},
            {'name': 'Books', 'description': 'Books and educational materials'},
            {'name': 'Health Products', 'description': 'Health and wellness products'},
            {'name': 'Grocery', 'description': 'Food and grocery items'},
            {'name': 'Home Appliances', 'description': 'Home and kitchen appliances'},
        ]

        for category_data in categories:
            if not Category.query.filter_by(name=category_data['name']).first():
                category = Category(**category_data)
                db.session.add(category)
        
        db.session.commit()

        # Create test users
        test_users = [
            {
                'username': 'basic_user',
                'email': 'user@test.com',
                'password': 'user123',
                'role': 'user'
            },
            {
                'username': 'admin_user',
                'email': 'admin@test.com',
                'password': 'admin123',
                'role': 'admin'
            },
            {
                'username': 'site_admin',
                'email': 'siteadmin@test.com',
                'password': 'siteadmin123',
                'role': 'site_admin'
            }
        ]

        for user_data in test_users:
            if not User.query.filter_by(username=user_data['username']).first():
                user = User(
                    username=user_data['username'],
                    email=user_data['email'],
                    role=user_data['role']
                )
                user.set_password(user_data['password'])
                db.session.add(user)
        
        db.session.commit()

if __name__ == '__main__':
    create_test_data() 