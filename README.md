## Project Structure

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
├── run.py                  # Application entry point
├── clean_cache.py          # Script to remove Python cache files
├── clean_cache.bat         # Windows batch script for cache cleaning
└── clean_cache.sh          # Shell script for cache cleaning on Unix systems
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

4. Configure the application:
   - Create an `.env` file in the root directory with the following content:
   ```
   FLASK_APP=run.py
   FLASK_ENV=development
   ```
   - Or set these variables directly in your terminal session if preferred.

5. Initialize the database:
   ```
   python run.py
   ```

6. Install product images:
   ```
   # Run the provided script to download all product images
   python scripts/download_product_images.py
   ```

   *Note: Alternatively, you can manually download images and place them in `app/static/images/products/` 
   following the naming convention described in the "Product Images" section below.*

## Running the Application

Start the development server:
```
python run.py
```

Access the application at `http://localhost:5000`

## Testing

Run the tests with the standard Python unittest module:
```
python -m unittest tests/test_app.py
```

## Cleaning Cache Files

To remove Python cache files (`__pycache__` directories and `.pyc` files) and ensure a clean environment for development and testing:
```
python clean_cache.py
```

This is useful:
- Before running tests to ensure a clean test environment
- After making significant code changes
- When experiencing unexplained behavior that might be related to cached Python files

## Product Images

1. Products can be assigned direct image URLs through the `image_url` field when creating or editing products.

2. For products without a direct URL, the system falls back to matching the product name with corresponding image files in the `app/static/images/products/` directory.

3. The application includes a default mapping between product names and image filenames:
   ```
   'Apple iPad Pro 12.9"': 'ipad_pro.jpeg',
   'MacBook Pro 16"': 'macbook_pro.jpeg',
   'iPhone 14 Pro': 'iphone_14_pro.jpeg',
   'Sony WH-1000XM5': 'sony_headphones.jpeg',
   'Samsung Galaxy Tab S8 Ultra': 'galaxy_tab.jpeg',
   'Dell XPS 15': 'dell_xps.jpeg',
   'Google Pixel 7 Pro': 'pixel_7_pro.jpeg',
   'Bose QuietComfort 45': 'bose_headphones.jpeg'
   ```

4. If a product doesn't match any of the above, the system displays a generic `placeholder.png` image.

When restoring or setting up the application, make sure to populate the `app/static/images/products/` directory with the appropriate image files to ensure all products display correctly.