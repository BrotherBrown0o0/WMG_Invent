import os
import sys
from app import create_app

def test_app_creation():
    """Test that the app can be created successfully."""
    try:
        app = create_app()
        print("✅ App created successfully!")
        return app
    except Exception as e:
        print(f"❌ Error creating app: {e}")
        return None

def test_routes(app):
    """Test that the routes are registered correctly."""
    if not app:
        return
    
    try:
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append(f"{rule.endpoint}: {rule.rule}")
        
        print(f"✅ Found {len(routes)} routes:")
        for route in sorted(routes):
            print(f"  - {route}")
    except Exception as e:
        print(f"❌ Error checking routes: {e}")

def test_static_folder(app):
    """Test that the static folder is configured correctly."""
    if not app:
        return
    
    try:
        static_folder = app.static_folder
        print(f"✅ Static folder: {static_folder}")
        
        # Check if the static folder exists
        if os.path.exists(static_folder):
            print(f"✅ Static folder exists!")
            
            # Count files in static folder
            css_files = len(os.listdir(os.path.join(static_folder, 'css')))
            js_files = len(os.listdir(os.path.join(static_folder, 'js')))
            image_files = len(os.listdir(os.path.join(static_folder, 'images')))
            
            print(f"  - CSS files: {css_files}")
            print(f"  - JS files: {js_files}")
            print(f"  - Image files: {image_files}")
        else:
            print(f"❌ Static folder does not exist!")
    except Exception as e:
        print(f"❌ Error checking static folder: {e}")

def main():
    """Main function to test the new structure."""
    print("Testing new structure...")
    
    # Change to the new structure directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Add the current directory to the path
    sys.path.insert(0, os.getcwd())
    
    # Test app creation
    app = test_app_creation()
    
    # Test routes
    test_routes(app)
    
    # Test static folder
    test_static_folder(app)
    
    print("Testing completed!")

if __name__ == "__main__":
    main() 