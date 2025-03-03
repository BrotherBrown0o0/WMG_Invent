#!/usr/bin/env python
"""
Clean script for WMGInvent application.

This script removes Python cache files and directories to ensure a clean environment
for testing and development.
"""

import os
import shutil
import sys

def clean_cache():
    """Remove all __pycache__ directories and .pyc files."""
    count_dirs = 0
    count_files = 0
    
    # Walk through all directories
    for root, dirs, files in os.walk("."):
        # Remove __pycache__ directories
        for dir_name in dirs:
            if dir_name == "__pycache__":
                path = os.path.join(root, dir_name)
                print(f"Removing directory: {path}")
                shutil.rmtree(path)
                count_dirs += 1
        
        # Remove .pyc files
        for file_name in files:
            if file_name.endswith(".pyc") or file_name.endswith(".pyo"):
                path = os.path.join(root, file_name)
                print(f"Removing file: {path}")
                os.remove(path)
                count_files += 1
    
    return count_dirs, count_files

if __name__ == "__main__":
    print("Cleaning Python cache files...")
    dirs, files = clean_cache()
    print(f"Cleaned {dirs} __pycache__ directories and {files} .pyc/.pyo files.")
    print("Done!")
    sys.exit(0) 