from app import create_app, db
from app.models.category import Category

app = create_app()
with app.app_context():
    electronics = Category.query.filter_by(name='Electronics').first()
    if electronics:
        print(f"Electronics category found with ID: {electronics.id}")
    else:
        print("Electronics category not found!") 