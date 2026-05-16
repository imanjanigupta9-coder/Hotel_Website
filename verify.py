#!/usr/bin/env python3
"""Quick verification script for the website"""
import os
import sys

# Check if key files exist
files_to_check = [
    'app.py',
    'templates/index.html',
    'static/css/style.css',
    'static/js/carousel.js'
]

print("Checking website files...")
all_exist = True
for file in files_to_check:
    path = os.path.join(os.path.dirname(__file__), file)
    exists = os.path.exists(path)
    status = "✓" if exists else "✗"
    print(f"{status} {file}")
    if not exists:
        all_exist = False

if all_exist:
    print("\n✓ All files exist!")
    print("\nTo start the server, run:")
    print("  python app.py")
    print("\nThen open http://localhost:5000 in your browser")
else:
    print("\n✗ Some files are missing!")
    sys.exit(1)
