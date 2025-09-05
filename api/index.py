import json
import requests
from bs4 import BeautifulSoup
import re

def scrape_auction_data(url):
    """Scrape auction data using requests and BeautifulSoup (Vercel compatible)"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
    except requests.RequestException as e:
        return {'error': f'Failed to fetch URL: {str(e)}'}
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Initialize result data
    result_data = {
        'success': True,
        'url': url,
        'lot_number': "Not found",
        'estimate': "Not found",
        'category': "Not found",
        'item_name': "Not found",
        'lead': "Not found",
        'description': "Not found",
        'auction_name': "Not found",
        'image_data': {
            'main_image_url': None,
            'gallery_image_urls': [],
            'thumbnail_urls': [],
            'all_gallery_images': [],
            'broad_search_images': []
        },
        'all_unique_image_urls': [],
        'total_unique_images': 0
    }
    
    # Extract auction name
    try:
        auction_elem = soup.find('th', string=re.compile(r'Name', re.I))
        if auction_elem and auction_elem.find_next_sibling('td'):
            result_data['auction_name'] = auction_elem.find_next_sibling('td').get_text(strip=True)
    except Exception:
        pass
    
    # Extract lot number
    try:
        lot_elem = soup.find('th', string=re.compile(r'Lot #', re.I))
        if lot_elem and lot_elem.find_next_sibling('td'):
            result_data['lot_number'] = lot_elem.find_next_sibling('td').get_text(strip=True)
    except Exception:
        pass
    
    # Extract estimate
    try:
        estimate_elem = soup.find('th', string=re.compile(r'Estimate', re.I))
        if estimate_elem and estimate_elem.find_next_sibling('td'):
            result_data['estimate'] = estimate_elem.find_next_sibling('td').get_text(strip=True)
    except Exception:
        pass
    
    # Extract category
    try:
        category_elem = soup.find('th', string=re.compile(r'Group.*Category', re.I))
        if category_elem and category_elem.find_next_sibling('td'):
            result_data['category'] = category_elem.find_next_sibling('td').get_text(strip=True)
    except Exception:
        pass
    
    # Extract item name from heading (e.g., "Lot # : 38 - Jaclyn Smith Watch/Pen Set")
    try:
        # First try to find the main heading with lot number and item name
        heading_elem = soup.find('h1')
        if heading_elem:
            heading_text = heading_elem.get_text(strip=True)
            # Check if it contains "Lot #" pattern
            if re.search(r'Lot\s*#\s*:\s*\d+', heading_text):
                result_data['item_name'] = heading_text
            else:
                # Fallback to table-based extraction
                item_elem = soup.find('th', string=re.compile(r'Item Name', re.I))
                if item_elem and item_elem.find_next_sibling('td'):
                    result_data['item_name'] = item_elem.find_next_sibling('td').get_text(strip=True)
        else:
            # Fallback to table-based extraction
            item_elem = soup.find('th', string=re.compile(r'Item Name', re.I))
            if item_elem and item_elem.find_next_sibling('td'):
                result_data['item_name'] = item_elem.find_next_sibling('td').get_text(strip=True)
    except Exception:
        pass
    
    # Extract lead
    try:
        lead_elem = soup.find('th', string=re.compile(r'Lead', re.I))
        if lead_elem and lead_elem.find_next_sibling('td'):
            result_data['lead'] = lead_elem.find_next_sibling('td').get_text(strip=True)
    except Exception:
        pass
    
    # Extract description
    try:
        desc_elem = soup.find('th', string=re.compile(r'Description', re.I))
        if desc_elem and desc_elem.find_next_sibling('td'):
            result_data['description'] = desc_elem.find_next_sibling('td').get_text(strip=True)
    except Exception:
        pass
    
    # Extract images
    all_images = []
    
    # Look for images in various places
    for img in soup.find_all('img'):
        src = img.get('src')
        if src:
            if src.startswith('//'):
                src = 'https:' + src
            elif src.startswith('/'):
                src = 'https://hibid.com' + src
            all_images.append(src)
    
    # Look for background images
    for element in soup.find_all(attrs={'style': True}):
        style = element.get('style', '')
        if 'background-image:' in style and 'hibid.com' in style:
            url_match = re.search(r"url\('([^']+)'\)", style)
            if url_match:
                img_url = url_match.group(1)
                img_url = img_url.replace("&amp;", "&")
                if img_url.startswith('//'):
                    img_url = 'https:' + img_url
                elif img_url.startswith('/'):
                    img_url = 'https://hibid.com' + img_url
                all_images.append(img_url)
    
    # Remove duplicates and filter
    unique_images = list(set(all_images))
    filtered_images = []
    
    for img in unique_images:
        if any(exclude in img.lower() for exclude in ["logo", "bbb", "privacy", "favicon", "icon"]):
            continue
        filtered_images.append(img)
    
    result_data['all_unique_image_urls'] = filtered_images
    result_data['total_unique_images'] = len(filtered_images)
    result_data['image_data']['gallery_image_urls'] = filtered_images[:10]  # First 10 as gallery
    
    return result_data

def handler(request):
    """Vercel handler function"""
    # Set CORS headers
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    
    # Handle preflight requests
    if request.method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': ''
        }
    
    try:
        # Parse the request
        path = request.path
        method = request.method
        
        # Route handling
        if path == '/' and method == 'GET':
            # API info endpoint
            response_data = {
                'name': 'Improved HiBid Scraper API',
                'version': '2.0',
                'description': 'Advanced auction data extraction API',
                'endpoints': {
                    '/extract-all': {
                        'method': 'POST',
                        'description': 'Extract all auction data from a single URL',
                        'body': {'url': 'auction_page_url'}
                    },
                    '/health': {
                        'method': 'GET',
                        'description': 'Health check endpoint'
                    }
                }
            }
            
        elif path == '/health' and method == 'GET':
            # Health check endpoint
            response_data = {
                'status': 'ok',
                'message': 'Improved HiBid Scraper API is running',
                'version': '2.0'
            }
            
        elif path == '/extract-all' and method == 'POST':
            # Main scraping endpoint
            try:
                body = request.body
                if isinstance(body, str):
                    data = json.loads(body)
                else:
                    data = body
                
                if not data or 'url' not in data:
                    response_data = {'error': 'URL is required in request body'}
                    status_code = 400
                else:
                    url = data['url']
                    result = scrape_auction_data(url)
                    
                    if 'error' in result:
                        response_data = result
                        status_code = 500
                    else:
                        response_data = result
                        status_code = 200
                        
            except Exception as e:
                response_data = {
                    'success': False,
                    'error': str(e)
                }
                status_code = 500
        else:
            # 404 for unknown routes
            response_data = {'error': 'Not found'}
            status_code = 404
            
        return {
            'statusCode': status_code if 'status_code' in locals() else 200,
            'headers': headers,
            'body': json.dumps(response_data)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({
                'error': f'Internal server error: {str(e)}'
            })
        }