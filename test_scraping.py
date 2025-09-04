#!/usr/bin/env python3
"""
Test script to demonstrate the scraping issue
"""

import requests
from bs4 import BeautifulSoup

def test_url_response(url):
    """Test what a URL actually returns"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"URL: {response.url}")
        print(f"Content Length: {len(response.text)}")
        
        # Check if it's JSON (category tree)
        if response.text.strip().startswith('{'):
            print("❌ This URL returns JSON data (category tree), not an auction lot page")
            return False
        
        # Check for common auction page elements
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for auction-specific elements
        auction_indicators = [
            soup.find('title'),
            soup.find('h1'),
            soup.find('h2'),
            soup.find('h3'),
            soup.find('div', class_=lambda x: x and 'lot' in x.lower() if x else False),
            soup.find('div', class_=lambda x: x and 'auction' in x.lower() if x else False),
            soup.find('div', class_=lambda x: x and 'bid' in x.lower() if x else False),
        ]
        
        print("Page elements found:")
        for i, element in enumerate(auction_indicators):
            if element:
                print(f"  {i+1}. {element.name}: {element.get_text()[:100]}...")
            else:
                print(f"  {i+1}. None")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    test_url = "https://hibid.com/lot/322898g/antique-victorian-era-brass-candlestick-holder"
    print(f"Testing URL: {test_url}")
    print("=" * 60)
    
    test_url_response(test_url)
