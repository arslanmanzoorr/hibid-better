# Improved HiBid Scraper API

A more advanced auction data extraction API with multiple endpoints for comprehensive data scraping.

## 🚀 Vercel Deployment

This API is optimized for Vercel deployment with serverless functions.

### Files for Vercel:
- `app_vercel.py` - Main Flask app (Vercel compatible)
- `vercel.json` - Vercel configuration
- `requirements_vercel.txt` - Simplified dependencies
- `.vercelignore` - Files to ignore

### Files for Local Development:
- `bidding_automation.py` - Full Selenium automation (requires browser)
- `requirements.txt` - Full dependencies including Selenium

## 📡 API Endpoints

### Health Check
```bash
GET /
GET /health
```

### Extract All Data
```bash
POST /extract-all
Content-Type: application/json

{
  "url": "https://hibid.com/lot/..."
}
```

## 🔧 Local Development

### With Selenium (Full Features)
```bash
pip install -r requirements.txt
python bidding_automation.py --port 8000
```

### Vercel Compatible (Limited Features)
```bash
pip install -r requirements_vercel.txt
python app_vercel.py
```

## 📊 Response Format

```json
{
  "success": true,
  "url": "https://hibid.com/lot/...",
  "lot_number": "123",
  "estimate": "$100-200",
  "category": "Collectibles",
  "item_name": "Vintage Item",
  "lead": "Lead description",
  "description": "Full description",
  "auction_name": "Auction Name",
  "image_data": {
    "main_image_url": "https://...",
    "gallery_image_urls": ["https://...", "https://..."],
    "thumbnail_urls": ["https://..."],
    "all_gallery_images": ["https://..."],
    "broad_search_images": ["https://..."]
  },
  "all_unique_image_urls": ["https://...", "https://..."],
  "total_unique_images": 5
}
```

## 🌐 Deployment

### Vercel
1. Upload files to GitHub
2. Import repository in Vercel
3. Deploy automatically

### Docker (Full Features)
```bash
docker-compose up --build -d
```

## ⚠️ Limitations

- **Vercel Version**: No Selenium automation, uses requests/BeautifulSoup
- **Selenium Version**: Requires browser installation, not suitable for Vercel
- **Timeout**: Vercel functions have 30-second timeout limit
