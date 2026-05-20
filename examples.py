"""
Usage examples for all free scripts.
"""

# File Organizer
from scripts.file_organizer import organize_by_type, organize_by_date, rename_bulk
organize_by_type("Downloads")            # sort by type
organize_by_type("Downloads", dry_run=True)  # preview only
organize_by_date("My Photos", fmt="%Y/%m")   # sort by date
rename_bulk("photos", prefix="vacation_2024_")

# API Data Fetcher
from scripts.api_data_fetcher import fetch, paginate, to_csv
data  = fetch("https://api.example.com/users", headers={"Authorization": "Bearer TOKEN"})
items = paginate("https://api.example.com/products", max_pages=50, results_key="data")
to_csv(items, "products.csv")
data  = fetch("https://api.example.com/catalog", cache_minutes=60)

# CSV Data Cleaner
from scripts.csv_data_cleaner import clean_csv, find_duplicates
stats = clean_csv("messy_data.csv")   # removes dupes, fixes columns
dupes = find_duplicates("data.csv", subset=["email"])
