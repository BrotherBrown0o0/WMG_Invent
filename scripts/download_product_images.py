import os
import requests
import shutil

# Define the directory where images will be saved
target_dir = 'app/static/images/products'

# Create the directory if it doesn't exist
os.makedirs(target_dir, exist_ok=True)

# Dictionary mapping product image filenames to URLs
image_urls = {
    'ipad_pro.jpeg': 'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=500&q=80',
    'macbook_pro.jpeg': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=500&q=80',
    'iphone_14_pro.jpeg': 'https://images.unsplash.com/photo-1591337676887-a217a6970a8a?w=500&q=80',
    'sony_headphones.jpeg': 'https://images.unsplash.com/photo-1618366712010-f4ae9c647dcb?w=500&q=80',
    'galaxy_tab.jpeg': 'https://images.pexels.com/photos/1334597/pexels-photo-1334597.jpeg?w=500&q=80',
    'dell_xps.jpeg': 'https://images.unsplash.com/photo-1593642532973-d31b6557fa68?w=500&q=80',
    'pixel_7_pro.jpeg': 'https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=500&q=80',
    'bose_headphones.jpeg': 'https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=500&q=80',
}

# Function to download an image
def download_image(url, filename):
    file_path = os.path.join(target_dir, filename)
    
    # Skip if file already exists
    if os.path.exists(file_path):
        print(f"File {filename} already exists, skipping...")
        return
    
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                shutil.copyfileobj(response.raw, f)
            print(f"Downloaded {filename}")
        else:
            print(f"Failed to download {filename}")
    except Exception as e:
        print(f"Error downloading {filename}: {e}")

# Create a placeholder image
placeholder_path = os.path.join(target_dir, 'placeholder.png')
if not os.path.exists(placeholder_path):
    download_image('https://via.placeholder.com/500x500.png?text=Product+Image', 'placeholder.png')

# Download all product images
for filename, url in image_urls.items():
    download_image(url, filename)

print("Product images download completed!")
print(f"Images are stored in: {os.path.abspath(target_dir)}") 