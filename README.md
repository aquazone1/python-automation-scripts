# 🐍 Python Business Automation Scripts

**Free Python scripts for automating common business tasks.**

No boilerplate. Drop them into your project and run.

---

## Free Scripts (this repo)

### [file_organizer.py](scripts/file_organizer.py)
Auto-sort any folder by file type or date. Zero external dependencies.

```python
from file_organizer import organize_by_type
organize_by_type("Downloads")
# → Images/, Videos/, Documents/, Code/, etc.
```

### [api_data_fetcher.py](scripts/api_data_fetcher.py)  
Fetch any REST API with auto-pagination and caching. Zero external dependencies.

```python
from api_data_fetcher import paginate, to_csv
items = paginate("https://api.example.com/products", max_pages=50, results_key="data")
to_csv(items, "products.csv")
```

---

## Full Bundle — 10 Scripts ($19)

The free scripts above are part of a larger bundle:

| # | Script | Description |
|---|--------|-------------|
| 1 | PDF Processor | Merge, split, extract text from PDFs |
| 2 | CSV Data Cleaner | Dedup, fix formats, validate emails/phones |
| 3 | Bulk Email Sender | Personalized email from CSV via Gmail |
| 4 | Price Tracker | Monitor any website, alert on price drop |
| 5 | **File Organizer** ← free | Sort files by type/date, bulk rename |
| 6 | Web Scraper | Any website → CSV/JSON |
| 7 | Invoice Generator | Professional PDF invoices |
| 8 | **API Data Fetcher** ← free | Paginate/cache any REST API |
| 9 | Report Generator | HTML reports + email delivery |
| 10 | Social Scheduler | Queue/schedule Twitter/X posts |

**Get the full bundle:** [`t.me/PyAutoPackBot`](https://t.me/PyAutoPackBot)  
Pay with USDT · Instant delivery · Python 3.9+

---

## Requirements

Free scripts: **zero dependencies** (Python stdlib only)

Full bundle dependencies:
```
pip install requests beautifulsoup4 lxml pandas openpyxl PyPDF2 reportlab tweepy schedule
```

---

## License

MIT for free scripts. Full bundle: personal and commercial use.
