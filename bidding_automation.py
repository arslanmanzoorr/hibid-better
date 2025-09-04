# # # # import time
# # # # import re
# # # # from selenium import webdriver
# # # # from selenium.webdriver.firefox.options import Options
# # # # from selenium.webdriver.common.by import By
# # # # from selenium.webdriver.support.ui import WebDriverWait
# # # # from selenium.webdriver.support import expected_conditions as EC
# # # # from selenium.common.exceptions import TimeoutException, NoSuchElementException

# # # # def scrape_auction_data():
# # # #     # Get user input
# # # #     url = input("Enter URL: ")
# # # #     platform_name = input("Enter Platform Name: ")
# # # #     auction_name = input("Enter Auction Name: ")
# # # #     lot_number = input("Enter Lot Number: ")

# # # #     # Configure Firefox options
# # # #     firefox_options = Options()
# # # #     firefox_options.add_argument("--width=1000")
# # # #     firefox_options.add_argument("--height=700")

# # # #     # Initialize Firefox driver
# # # #     driver = webdriver.Firefox(options=firefox_options)

# # # #     try:
# # # #         # Navigate to URL
# # # #         driver.get(url)

# # # #         # Wait for page to load
# # # #         WebDriverWait(driver, 10).until(
# # # #             EC.presence_of_element_located((By.TAG_NAME, "body"))
# # # #         )

# # # #         print(f"Navigated to: {url}")
# # # #         print(f"Platform: {platform_name}")
# # # #         print(f"Auction: {auction_name}")
# # # #         print(f"Lot: {lot_number}")
# # # #         print("\nScraping auction data...")

# # # #         # Wait for content to load
# # # #         time.sleep(3)

# # # #         scraped_data = {}

# # # #         # Get viewport height for scrolling
# # # #         viewport_height = driver.execute_script("return window.innerHeight")
# # # #         print(f"Viewport height: {viewport_height}px")

# # # #         # Scroll down by one screen height
# # # #         driver.execute_script(f"window.scrollBy(0, {viewport_height})")
# # # #         print(f"Scrolled down by {viewport_height}px")
        
# # # #         # Wait for any dynamic content to load after scrolling
# # # #         time.sleep(2)

# # # #         # Scrape the specific table structure after scrolling
# # # #         print("\n=== SCRAPING AFTER SCROLL ===")
# # # #         try:
# # # #             # Look for the specific table row with Description header
# # # #             description_rows = driver.find_elements(By.XPATH, "//tr[@class='row ng-star-inserted' and contains(@app-row-detail, '_nghost-hibid-c3894337431')]")
# # # #             print(f"Found {len(description_rows)} description rows")
            
# # # #             for i, row in enumerate(description_rows):
# # # #                 try:
# # # #                     # Extract the description header
# # # #                     desc_header = row.find_element(By.CSS_SELECTOR, "th.col-4.col-sm-3.col-md-2")
# # # #                     header_text = desc_header.text.strip()
                    
# # # #                     # Extract the description content
# # # #                     desc_content = row.find_element(By.CSS_SELECTOR, "td.col-8.col-sm-9.col-md-10.ng-star-inserted")
                    
# # # #                     # Look for the div with text-pre-line class inside the td
# # # #                     content_div = desc_content.find_element(By.CSS_SELECTOR, "div.text-pre-line")
# # # #                     content_text = content_div.text.strip()
                    
# # # #                     # Store in scraped data
# # # #                     key = f"scrolled_{header_text.lower().replace(' ', '_')}_row_{i+1}"
# # # #                     scraped_data[key] = content_text
# # # #                     print(f"Row {i+1} - {header_text}: {content_text}")
                    
# # # #                 except NoSuchElementException as e:
# # # #                     print(f"Could not extract data from row {i+1}: {e}")
# # # #                     continue
                    
# # # #         except NoSuchElementException:
# # # #             print("No matching table rows found after scrolling")
# # # #         except Exception as e:
# # # #             print(f"Error scraping after scroll: {e}")
        
# # # #         print("=== SCROLL SCRAPING COMPLETE ===\n")

# # # #         # Scrape lot number from table
# # # #         try:
# # # #             lot_element = driver.find_element(By.XPATH, "//th[contains(text(), 'Lot #')]/following-sibling::td")
# # # #             scraped_data['lot_number'] = lot_element.text.strip()
# # # #             print(f"Lot Number: {scraped_data['lot_number']}")
# # # #         except NoSuchElementException:
# # # #             scraped_data['lot_number'] = "Not found"
# # # #             print("Lot Number: Not found")

# # # #         # Scrape category/group information
# # # #         try:
# # # #             category_element = driver.find_element(By.XPATH, "//th[contains(text(), 'Group') or contains(text(), 'Category')]/following-sibling::td")
# # # #             scraped_data['category'] = category_element.text.strip()
# # # #             print(f"Category: {scraped_data['category']}")
# # # #         except NoSuchElementException:
# # # #             try:
# # # #                 # Alternative selector for category links
# # # #                 category_link = driver.find_element(By.CSS_SELECTOR, "a[href*='sporting-goods']")
# # # #                 scraped_data['category'] = category_link.get_attribute('href')
# # # #                 print(f"Category Link: {scraped_data['category']}")
# # # #             except NoSuchElementException:
# # # #                 scraped_data['category'] = "Not found"
# # # #                 print("Category: Not found")

# # # #         # Scrape item description/title
# # # #         try:
# # # #             description_element = driver.find_element(By.XPATH, "//th[contains(text(), 'Lead')]/following-sibling::td")
# # # #             scraped_data['description'] = description_element.text.strip()
# # # #             print(f"Description: {scraped_data['description']}")
# # # #         except NoSuchElementException:
# # # #             scraped_data['description'] = "Not found"
# # # #             print("Description: Not found")

# # # #         # Scrape auction details from accordion
# # # #         try:
# # # #             # Look for auction detail accordion
# # # #             accordion_button = driver.find_element(By.CSS_SELECTOR, "div[role='button'][aria-label*='Information']")
# # # #             if accordion_button.get_attribute('aria-expanded') == 'false':
# # # #                 accordion_button.click()
# # # #                 time.sleep(1)

# # # #             # Scrape additional information from the expanded accordion
# # # #             info_table = driver.find_element(By.CSS_SELECTOR, "table.table-no-border")
# # # #             rows = info_table.find_elements(By.TAG_NAME, "tr")

# # # #             for row in rows:
# # # #                 try:
# # # #                     header = row.find_element(By.TAG_NAME, "th").text.strip()
# # # #                     data = row.find_element(By.TAG_NAME, "td").text.strip()
# # # #                     scraped_data[header.lower().replace(' ', '_')] = data
# # # #                     print(f"{header}: {data}")
# # # #                 except NoSuchElementException:
# # # #                     continue

# # # #         except NoSuchElementException:
# # # #             print("Auction details accordion not found")

# # # #         # Enhanced image extraction with detailed debugging
# # # #         print("\n=== STARTING IMAGE EXTRACTION DEBUG ===")

# # # #         try:
# # # #             print("🔍 Step 1: Waiting for ngx-gallery to load...")
# # # #             WebDriverWait(driver, 10).until(
# # # #                 EC.presence_of_element_located((By.CSS_SELECTOR, "ngx-gallery"))
# # # #             )
# # # #             print("✅ ngx-gallery element found!")

# # # #             # Method 1: Extract from ngx-gallery-image with background-image style
# # # #             print("\n🔍 Step 2: Method 1 - Looking for div.ngx-gallery-image with background-image...")
# # # #             try:
# # # #                 gallery_image = driver.find_element(By.CSS_SELECTOR, "div.ngx-gallery-image[style*='background-image']")
# # # #                 print("✅ Found div.ngx-gallery-image with background-image style!")

# # # #                 style_attribute = gallery_image.get_attribute('style')
# # # #                 print(f"📝 Full style attribute: {style_attribute}")

# # # #                 # Extract URL from background-image: url("...") using regex
# # # #                 url_match = re.search(r'background-image:\surl\("([^"]+)"\)', style_attribute)
# # # #                 if url_match:
# # # #                     image_url = url_match.group(1)
# # # #                     scraped_data['main_image_url'] = image_url
# # # #                     print(f"✅ SUCCESS! Main Image URL extracted: {image_url}")
# # # #                 else:
# # # #                     print("❌ Could not extract URL from background-image style using regex")
# # # #                     # Try alternative regex patterns
# # # #                     alt_patterns = [
# # # #                         r'background-image:\surl\(([^)]+)\)',  # Without quotes
# # # #                         r'background-image:\s*url\(\'([^\']+)\'\)',  # Single quotes
# # # #                     ]
# # # #                     for pattern in alt_patterns:
# # # #                         alt_match = re.search(pattern, style_attribute)
# # # #                         if alt_match:
# # # #                             image_url = alt_match.group(1)
# # # #                             scraped_data['main_image_url'] = image_url
# # # #                             print(f"✅ SUCCESS with alternative pattern! Main Image URL: {image_url}")
# # # #                             break
# # # #                     else:
# # # #                         print("❌ All regex patterns failed")

# # # #             except NoSuchElementException:
# # # #                 print("❌ div.ngx-gallery-image with background-image not found")

# # # #                 # Debug: Check what ngx-gallery-image elements exist
# # # #                 try:
# # # #                     all_gallery_images = driver.find_elements(By.CSS_SELECTOR, "div.ngx-gallery-image")
# # # #                     print(f"🔍 Found {len(all_gallery_images)} div.ngx-gallery-image elements without background-image")
# # # #                     for i, elem in enumerate(all_gallery_images):
# # # #                         style = elem.get_attribute('style')
# # # #                         classes = elem.get_attribute('class')
# # # #                         print(f"  Element {i+1}: class='{classes}', style='{style}'")
# # # #                 except:
# # # #                     print("❌ No div.ngx-gallery-image elements found at all")

# # # #             # Method 2: Extract from ngx-gallery-image img tags
# # # #             print("\n🔍 Step 3: Method 2 - Looking for img tags in ngx-gallery-image...")
# # # #             try:
# # # #                 gallery_images = driver.find_elements(By.CSS_SELECTOR, "ngx-gallery-image img")
# # # #                 print(f"✅ Found {len(gallery_images)} img tags in ngx-gallery-image")

# # # #                 image_urls = []
# # # #                 for i, img in enumerate(gallery_images):
# # # #                     src = img.get_attribute('src')
# # # #                     alt = img.get_attribute('alt')
# # # #                     classes = img.get_attribute('class')
# # # #                     print(f"  Image {i+1}: src='{src}', alt='{alt}', class='{classes}'")
# # # #                     if src:
# # # #                         image_urls.append(src)

# # # #                 if image_urls:
# # # #                     scraped_data['gallery_image_urls'] = image_urls
# # # #                     scraped_data['image_count'] = len(image_urls)
# # # #                     print(f"✅ SUCCESS! Gallery Image URLs extracted: {image_urls}")
# # # #                 else:
# # # #                     print("❌ No valid src attributes found in img tags")

# # # #             except NoSuchElementException:
# # # #                 print("❌ No img tags found in ngx-gallery-image")

# # # #             # Method 3: Extract from thumbnails
# # # #             print("\n🔍 Step 4: Method 3 - Looking for thumbnail images...")
# # # #             try:
# # # #                 thumbnails = driver.find_elements(By.CSS_SELECTOR, "ngx-gallery-thumbnails img, .ngx-gallery-layout .thumbnails-bottom img")
# # # #                 print(f"✅ Found {len(thumbnails)} thumbnail images")

# # # #                 thumbnail_urls = []
# # # #                 for i, thumb in enumerate(thumbnails):
# # # #                     src = thumb.get_attribute('src')
# # # #                     print(f"  Thumbnail {i+1}: {src}")
# # # #                     if src:
# # # #                         thumbnail_urls.append(src)

# # # #                 if thumbnail_urls:
# # # #                     scraped_data['thumbnail_urls'] = thumbnail_urls
# # # #                     print(f"✅ SUCCESS! Thumbnail URLs extracted: {thumbnail_urls}")
# # # #                 else:
# # # #                     print("❌ No valid thumbnail URLs found")

# # # #             except NoSuchElementException:
# # # #                 print("❌ No thumbnail images found")

# # # #             # Method 4: Look for any images within the gallery container
# # # #             print("\n🔍 Step 5: Method 4 - Looking for ALL images in gallery container...")
# # # #             try:
# # # #                 gallery_container = driver.find_element(By.CSS_SELECTOR, "ngx-gallery")
# # # #                 all_images = gallery_container.find_elements(By.TAG_NAME, "img")
# # # #                 print(f"✅ Found {len(all_images)} total images in gallery container")

# # # #                 if all_images:
# # # #                     scraped_data['all_gallery_images'] = []
# # # #                     for i, img in enumerate(all_images):
# # # #                         img_data = {
# # # #                             'src': img.get_attribute('src'),
# # # #                             'alt': img.get_attribute('alt'),
# # # #                             'class': img.get_attribute('class'),
# # # #                             'style': img.get_attribute('style')
# # # #                         }
# # # #                         scraped_data['all_gallery_images'].append(img_data)
# # # #                         print(f"  Image {i+1}:")
# # # #                         print(f"    src: {img_data['src']}")
# # # #                         print(f"    alt: {img_data['alt']}")
# # # #                         print(f"    class: {img_data['class']}")
# # # #                         print(f"    style: {img_data['style']}")

# # # #                     print(f"✅ SUCCESS! All gallery images catalogued")
# # # #                 else:
# # # #                     print("❌ No images found in gallery container")

# # # #             except NoSuchElementException:
# # # #                 print("❌ Gallery container not found")

# # # #             # Method 5: Broad search for any divs with background-image containing hibid
# # # #             print("\n🔍 Step 6: Method 5 - Broad search for any background-image with hibid...")
# # # #             try:
# # # #                 all_bg_images = driver.find_elements(By.XPATH, "//*[contains(@style, 'background-image') and contains(@style, 'hibid')]")
# # # #                 print(f"✅ Found {len(all_bg_images)} elements with hibid background-images")

# # # #                 for i, elem in enumerate(all_bg_images):
# # # #                     tag_name = elem.tag_name
# # # #                     classes = elem.get_attribute('class')
# # # #                     style = elem.get_attribute('style')
# # # #                     print(f"  Element {i+1}: <{tag_name}> class='{classes}'")
# # # #                     print(f"    style: {style}")

# # # #                     # Extract URL
# # # #                     url_patterns = [
# # # #                         r'background-image:\surl\("([^"]+)"\)',
# # # #                         r'background-image:\surl\(([^)]+)\)',
# # # #                         r'background-image:\s*url\(\'([^\']+)\'\)'
# # # #                     ]

# # # #                     for pattern in url_patterns:
# # # #                         match = re.search(pattern, style)
# # # #                         if match:
# # # #                             url = match.group(1)
# # # #                             print(f"    ✅ Extracted URL: {url}")
# # # #                             if 'broad_search_images' not in scraped_data:
# # # #                                 scraped_data['broad_search_images'] = []
# # # #                             scraped_data['broad_search_images'].append(url)
# # # #                             break

# # # #             except Exception as e:
# # # #                 print(f"❌ Broad search failed: {e}")

# # # #         except TimeoutException:
# # # #             print("❌ Gallery did not load in time")
# # # #         except Exception as e:
# # # #             print(f"❌ Error extracting images: {e}")

# # # #         print("\n=== IMAGE EXTRACTION DEBUG COMPLETE ===\n")

# # # #         # Scrape any additional lot details
# # # #         try:
# # # #             lot_details_container = driver.find_element(By.CSS_SELECTOR, "div[class*='lot-details-container']")
# # # #             lot_info = lot_details_container.text.strip()
# # # #             scraped_data['lot_details'] = lot_info
# # # #             print(f"Additional lot details found: {len(lot_info)} characters")
# # # #         except NoSuchElementException:
# # # #             print("No additional lot details container found")

# # # #         print(f"\nScraping completed. Total data points collected: {len(scraped_data)}")

# # # #         # Print summary
# # # #         print("\n--- SCRAPED DATA SUMMARY ---")
# # # #         for key, value in scraped_data.items():
# # # #             if isinstance(value, list):
# # # #                 print(f"{key}: {len(value)} items")
# # # #                 for i, item in enumerate(value[:3]):  # Show first 3 items
# # # #                     print(f"  {i+1}: {item}")
# # # #                 if len(value) > 3:
# # # #                     print(f"  ... and {len(value)-3} more")
# # # #             else:
# # # #                 print(f"{key}: {value}")

# # # #         # Keep browser open
# # # #         input("\nPress Enter to close browser...")

# # # #     except TimeoutException:
# # # #         print("Page load timeout")
# # # #     except Exception as e:
# # # #         print(f"Error: {e}")
# # # #     finally:
# # # #         driver.quit()

# # # # if __name__ == "__main__":
# # # #     scrape_auction_data()




# # # import time
# # # import re
# # # from selenium import webdriver
# # # from selenium.webdriver.firefox.options import Options
# # # from selenium.webdriver.common.by import By
# # # from selenium.webdriver.support.ui import WebDriverWait
# # # from selenium.webdriver.support import expected_conditions as EC
# # # from selenium.common.exceptions import TimeoutException, NoSuchElementException

# # # def scrape_auction_data():
# # #     # Get user input
# # #     url = input("Enter URL: ")
# # #     platform_name = input("Enter Platform Name: ")
# # #     auction_name = input("Enter Auction Name: ")
# # #     lot_number = input("Enter Lot Number: ")

# # #     # Configure Firefox options
# # #     firefox_options = Options()
# # #     firefox_options.add_argument("--width=1000")
# # #     firefox_options.add_argument("--height=700")

# # #     # Initialize Firefox driver
# # #     driver = webdriver.Firefox(options=firefox_options)

# # #     try:
# # #         # Navigate to URL
# # #         driver.get(url)

# # #         # Wait for page to load
# # #         WebDriverWait(driver, 10).until(
# # #             EC.presence_of_element_located((By.TAG_NAME, "body"))
# # #         )

# # #         print(f"Navigated to: {url}")
# # #         print(f"Platform: {platform_name}")
# # #         print(f"Auction: {auction_name}")
# # #         print(f"Lot: {lot_number}")
# # #         print("\nScraping auction data...")

# # #         # Wait for content to load
# # #         time.sleep(3)

# # #         scraped_data = {}

# # #         # Get viewport height for scrolling
# # #         viewport_height = driver.execute_script("return window.innerHeight")
# # #         print(f"Viewport height: {viewport_height}px")

# # #         # Scroll down by one and a half screen heights
# # #         scroll_amount = int(viewport_height * 1.5)
# # #         driver.execute_script(f"window.scrollBy(0, {scroll_amount})")
# # #         print(f"Scrolled down by {scroll_amount}px")
        
# # #         # Wait for any dynamic content to load after scrolling
# # #         time.sleep(2)

# # #         # Scrape the specific table structure after scrolling
# # #         print("\n=== SCRAPING AFTER SCROLL ===")
# # #         try:
# # #             # Look for the specific table row with Description header
# # #             description_rows = driver.find_elements(By.XPATH, "//tr[@class='row ng-star-inserted' and contains(@app-row-detail, '_nghost-hibid-c3894337431')]")
# # #             print(f"Found {len(description_rows)} description rows")
            
# # #             for i, row in enumerate(description_rows):
# # #                 try:
# # #                     # Extract the description header
# # #                     desc_header = row.find_element(By.CSS_SELECTOR, "th.col-4.col-sm-3.col-md-2")
# # #                     header_text = desc_header.text.strip()
                    
# # #                     # Extract the description content
# # #                     desc_content = row.find_element(By.CSS_SELECTOR, "td.col-8.col-sm-9.col-md-10.ng-star-inserted")
                    
# # #                     # Look for the div with text-pre-line class inside the td
# # #                     content_div = desc_content.find_element(By.CSS_SELECTOR, "div.text-pre-line")
# # #                     content_text = content_div.text.strip()
                    
# # #                     # Store in scraped data
# # #                     key = f"scrolled_{header_text.lower().replace(' ', '_')}_row_{i+1}"
# # #                     scraped_data[key] = content_text
# # #                     print(f"Row {i+1} - {header_text}: {content_text}")
                    
# # #                 except NoSuchElementException as e:
# # #                     print(f"Could not extract data from row {i+1}: {e}")
# # #                     continue
                    
# # #         except NoSuchElementException:
# # #             print("No matching table rows found after scrolling")
# # #         except Exception as e:
# # #             print(f"Error scraping after scroll: {e}")
        
# # #         print("=== SCROLL SCRAPING COMPLETE ===\n")

# # #         # Scrape lot number from table
# # #         try:
# # #             lot_element = driver.find_element(By.XPATH, "//th[contains(text(), 'Lot #')]/following-sibling::td")
# # #             scraped_data['lot_number'] = lot_element.text.strip()
# # #             print(f"Lot Number: {scraped_data['lot_number']}")
# # #         except NoSuchElementException:
# # #             scraped_data['lot_number'] = "Not found"
# # #             print("Lot Number: Not found")

# # #         # Scrape category/group information
# # #         try:
# # #             category_element = driver.find_element(By.XPATH, "//th[contains(text(), 'Group') or contains(text(), 'Category')]/following-sibling::td")
# # #             scraped_data['category'] = category_element.text.strip()
# # #             print(f"Category: {scraped_data['category']}")
# # #         except NoSuchElementException:
# # #             try:
# # #                 # Alternative selector for category links
# # #                 category_link = driver.find_element(By.CSS_SELECTOR, "a[href*='sporting-goods']")
# # #                 scraped_data['category'] = category_link.get_attribute('href')
# # #                 print(f"Category Link: {scraped_data['category']}")
# # #             except NoSuchElementException:
# # #                 scraped_data['category'] = "Not found"
# # #                 print("Category: Not found")

# # #         # Scrape item description/title
# # #         try:
# # #             description_element = driver.find_element(By.XPATH, "//th[contains(text(), 'Lead')]/following-sibling::td")
# # #             scraped_data['description'] = description_element.text.strip()
# # #             print(f"Description: {scraped_data['description']}")
# # #         except NoSuchElementException:
# # #             scraped_data['description'] = "Not found"
# # #             print("Description: Not found")

# # #         # Scrape auction details from accordion
# # #         try:
# # #             # Look for auction detail accordion
# # #             accordion_button = driver.find_element(By.CSS_SELECTOR, "div[role='button'][aria-label*='Information']")
# # #             if accordion_button.get_attribute('aria-expanded') == 'false':
# # #                 accordion_button.click()
# # #                 time.sleep(1)

# # #             # Scrape additional information from the expanded accordion
# # #             info_table = driver.find_element(By.CSS_SELECTOR, "table.table-no-border")
# # #             rows = info_table.find_elements(By.TAG_NAME, "tr")

# # #             for row in rows:
# # #                 try:
# # #                     header = row.find_element(By.TAG_NAME, "th").text.strip()
# # #                     data = row.find_element(By.TAG_NAME, "td").text.strip()
# # #                     scraped_data[header.lower().replace(' ', '_')] = data
# # #                     print(f"{header}: {data}")
# # #                 except NoSuchElementException:
# # #                     continue

# # #         except NoSuchElementException:
# # #             print("Auction details accordion not found")

# # #         # Enhanced image extraction with detailed debugging
# # #         print("\n=== STARTING IMAGE EXTRACTION DEBUG ===")

# # #         try:
# # #             print("🔍 Step 1: Waiting for ngx-gallery to load...")
# # #             WebDriverWait(driver, 10).until(
# # #                 EC.presence_of_element_located((By.CSS_SELECTOR, "ngx-gallery"))
# # #             )
# # #             print("✅ ngx-gallery element found!")

# # #             # Method 1: Extract from ngx-gallery-image with background-image style
# # #             print("\n🔍 Step 2: Method 1 - Looking for div.ngx-gallery-image with background-image...")
# # #             try:
# # #                 gallery_image = driver.find_element(By.CSS_SELECTOR, "div.ngx-gallery-image[style*='background-image']")
# # #                 print("✅ Found div.ngx-gallery-image with background-image style!")

# # #                 style_attribute = gallery_image.get_attribute('style')
# # #                 print(f"📝 Full style attribute: {style_attribute}")

# # #                 # Extract URL from background-image: url("...") using regex
# # #                 url_match = re.search(r'background-image:\surl\("([^"]+)"\)', style_attribute)
# # #                 if url_match:
# # #                     image_url = url_match.group(1)
# # #                     scraped_data['main_image_url'] = image_url
# # #                     print(f"✅ SUCCESS! Main Image URL extracted: {image_url}")
# # #                 else:
# # #                     print("❌ Could not extract URL from background-image style using regex")
# # #                     # Try alternative regex patterns
# # #                     alt_patterns = [
# # #                         r'background-image:\surl\(([^)]+)\)',  # Without quotes
# # #                         r'background-image:\s*url\(\'([^\']+)\'\)',  # Single quotes
# # #                     ]
# # #                     for pattern in alt_patterns:
# # #                         alt_match = re.search(pattern, style_attribute)
# # #                         if alt_match:
# # #                             image_url = alt_match.group(1)
# # #                             scraped_data['main_image_url'] = image_url
# # #                             print(f"✅ SUCCESS with alternative pattern! Main Image URL: {image_url}")
# # #                             break
# # #                     else:
# # #                         print("❌ All regex patterns failed")

# # #             except NoSuchElementException:
# # #                 print("❌ div.ngx-gallery-image with background-image not found")

# # #                 # Debug: Check what ngx-gallery-image elements exist
# # #                 try:
# # #                     all_gallery_images = driver.find_elements(By.CSS_SELECTOR, "div.ngx-gallery-image")
# # #                     print(f"🔍 Found {len(all_gallery_images)} div.ngx-gallery-image elements without background-image")
# # #                     for i, elem in enumerate(all_gallery_images):
# # #                         style = elem.get_attribute('style')
# # #                         classes = elem.get_attribute('class')
# # #                         print(f"  Element {i+1}: class='{classes}', style='{style}'")
# # #                 except:
# # #                     print("❌ No div.ngx-gallery-image elements found at all")

# # #             # Method 2: Extract from ngx-gallery-image img tags
# # #             print("\n🔍 Step 3: Method 2 - Looking for img tags in ngx-gallery-image...")
# # #             try:
# # #                 gallery_images = driver.find_elements(By.CSS_SELECTOR, "ngx-gallery-image img")
# # #                 print(f"✅ Found {len(gallery_images)} img tags in ngx-gallery-image")

# # #                 image_urls = []
# # #                 for i, img in enumerate(gallery_images):
# # #                     src = img.get_attribute('src')
# # #                     alt = img.get_attribute('alt')
# # #                     classes = img.get_attribute('class')
# # #                     print(f"  Image {i+1}: src='{src}', alt='{alt}', class='{classes}'")
# # #                     if src:
# # #                         image_urls.append(src)

# # #                 if image_urls:
# # #                     scraped_data['gallery_image_urls'] = image_urls
# # #                     scraped_data['image_count'] = len(image_urls)
# # #                     print(f"✅ SUCCESS! Gallery Image URLs extracted: {image_urls}")
# # #                 else:
# # #                     print("❌ No valid src attributes found in img tags")

# # #             except NoSuchElementException:
# # #                 print("❌ No img tags found in ngx-gallery-image")

# # #             # Method 3: Extract from thumbnails
# # #             print("\n🔍 Step 4: Method 3 - Looking for thumbnail images...")
# # #             try:
# # #                 thumbnails = driver.find_elements(By.CSS_SELECTOR, "ngx-gallery-thumbnails img, .ngx-gallery-layout .thumbnails-bottom img")
# # #                 print(f"✅ Found {len(thumbnails)} thumbnail images")

# # #                 thumbnail_urls = []
# # #                 for i, thumb in enumerate(thumbnails):
# # #                     src = thumb.get_attribute('src')
# # #                     print(f"  Thumbnail {i+1}: {src}")
# # #                     if src:
# # #                         thumbnail_urls.append(src)

# # #                 if thumbnail_urls:
# # #                     scraped_data['thumbnail_urls'] = thumbnail_urls
# # #                     print(f"✅ SUCCESS! Thumbnail URLs extracted: {thumbnail_urls}")
# # #                 else:
# # #                     print("❌ No valid thumbnail URLs found")

# # #             except NoSuchElementException:
# # #                 print("❌ No thumbnail images found")

# # #             # Method 4: Look for any images within the gallery container
# # #             print("\n🔍 Step 5: Method 4 - Looking for ALL images in gallery container...")
# # #             try:
# # #                 gallery_container = driver.find_element(By.CSS_SELECTOR, "ngx-gallery")
# # #                 all_images = gallery_container.find_elements(By.TAG_NAME, "img")
# # #                 print(f"✅ Found {len(all_images)} total images in gallery container")

# # #                 if all_images:
# # #                     scraped_data['all_gallery_images'] = []
# # #                     for i, img in enumerate(all_images):
# # #                         img_data = {
# # #                             'src': img.get_attribute('src'),
# # #                             'alt': img.get_attribute('alt'),
# # #                             'class': img.get_attribute('class'),
# # #                             'style': img.get_attribute('style')
# # #                         }
# # #                         scraped_data['all_gallery_images'].append(img_data)
# # #                         print(f"  Image {i+1}:")
# # #                         print(f"    src: {img_data['src']}")
# # #                         print(f"    alt: {img_data['alt']}")
# # #                         print(f"    class: {img_data['class']}")
# # #                         print(f"    style: {img_data['style']}")

# # #                     print(f"✅ SUCCESS! All gallery images catalogued")
# # #                 else:
# # #                     print("❌ No images found in gallery container")

# # #             except NoSuchElementException:
# # #                 print("❌ Gallery container not found")

# # #             # Method 5: Broad search for any divs with background-image containing hibid
# # #             print("\n🔍 Step 6: Method 5 - Broad search for any background-image with hibid...")
# # #             try:
# # #                 all_bg_images = driver.find_elements(By.XPATH, "//*[contains(@style, 'background-image') and contains(@style, 'hibid')]")
# # #                 print(f"✅ Found {len(all_bg_images)} elements with hibid background-images")

# # #                 for i, elem in enumerate(all_bg_images):
# # #                     tag_name = elem.tag_name
# # #                     classes = elem.get_attribute('class')
# # #                     style = elem.get_attribute('style')
# # #                     print(f"  Element {i+1}: <{tag_name}> class='{classes}'")
# # #                     print(f"    style: {style}")

# # #                     # Extract URL
# # #                     url_patterns = [
# # #                         r'background-image:\surl\("([^"]+)"\)',
# # #                         r'background-image:\surl\(([^)]+)\)',
# # #                         r'background-image:\s*url\(\'([^\']+)\'\)'
# # #                     ]

# # #                     for pattern in url_patterns:
# # #                         match = re.search(pattern, style)
# # #                         if match:
# # #                             url = match.group(1)
# # #                             print(f"    ✅ Extracted URL: {url}")
# # #                             if 'broad_search_images' not in scraped_data:
# # #                                 scraped_data['broad_search_images'] = []
# # #                             scraped_data['broad_search_images'].append(url)
# # #                             break

# # #             except Exception as e:
# # #                 print(f"❌ Broad search failed: {e}")

# # #         except TimeoutException:
# # #             print("❌ Gallery did not load in time")
# # #         except Exception as e:
# # #             print(f"❌ Error extracting images: {e}")

# # #         print("\n=== IMAGE EXTRACTION DEBUG COMPLETE ===\n")

# # #         # Scrape any additional lot details
# # #         try:
# # #             lot_details_container = driver.find_element(By.CSS_SELECTOR, "div[class*='lot-details-container']")
# # #             lot_info = lot_details_container.text.strip()
# # #             scraped_data['lot_details'] = lot_info
# # #             print(f"Additional lot details found: {len(lot_info)} characters")
# # #         except NoSuchElementException:
# # #             print("No additional lot details container found")

# # #         print(f"\nScraping completed. Total data points collected: {len(scraped_data)}")

# # #         # Print summary
# # #         print("\n--- SCRAPED DATA SUMMARY ---")
# # #         for key, value in scraped_data.items():
# # #             if isinstance(value, list):
# # #                 print(f"{key}: {len(value)} items")
# # #                 for i, item in enumerate(value[:3]):  # Show first 3 items
# # #                     print(f"  {i+1}: {item}")
# # #                 if len(value) > 3:
# # #                     print(f"  ... and {len(value)-3} more")
# # #             else:
# # #                 print(f"{key}: {value}")

# # #         # Keep browser open
# # #         input("\nPress Enter to close browser...")

# # #     except TimeoutException:
# # #         print("Page load timeout")
# # #     except Exception as e:
# # #         print(f"Error: {e}")
# # #     finally:
# # #         driver.quit()

# # # if __name__ == "__main__":
# # #     scrape_auction_data()












# # import time
# # import re
# # from selenium import webdriver
# # from selenium.webdriver.firefox.options import Options
# # from selenium.webdriver.common.by import By
# # from selenium.webdriver.support.ui import WebDriverWait
# # from selenium.webdriver.support import expected_conditions as EC
# # from selenium.common.exceptions import TimeoutException, NoSuchElementException

# # def scrape_auction_data():
# #     # Get user input
# #     url = input("Enter URL: ")
# #     platform_name = input("Enter Platform Name: ")
# #     auction_name = input("Enter Auction Name: ")
# #     lot_number = input("Enter Lot Number: ")

# #     # Configure Firefox options
# #     firefox_options = Options()
# #     firefox_options.add_argument("--width=1000")
# #     firefox_options.add_argument("--height=700")

# #     # Initialize Firefox driver
# #     driver = webdriver.Firefox(options=firefox_options)

# #     try:
# #         # Navigate to URL
# #         driver.get(url)

# #         # Wait for page to load
# #         WebDriverWait(driver, 10).until(
# #             EC.presence_of_element_located((By.TAG_NAME, "body"))
# #         )

# #         print(f"Navigated to: {url}")
# #         print(f"Platform: {platform_name}")
# #         print(f"Auction: {auction_name}")
# #         print(f"Lot: {lot_number}")
# #         print("\nScraping auction data...")

# #         # Wait for content to load
# #         time.sleep(3)

# #         scraped_data = {}

# #         # Get viewport height for scrolling
# #         viewport_height = driver.execute_script("return window.innerHeight")
# #         print(f"Viewport height: {viewport_height}px")

# #         # Scroll down by one and a half screen heights
# #         scroll_amount = int(viewport_height * 1.5)
# #         driver.execute_script(f"window.scrollBy(0, {scroll_amount})")
# #         print(f"Scrolled down by {scroll_amount}px")
        
# #         # Wait for any dynamic content to load after scrolling
# #         time.sleep(5)  # Increased wait time

# #         # Scrape the specific table structure after scrolling
# #         print("\n=== SCRAPING AFTER SCROLL ===")
# #         try:
# #             # Look for the specific table row with Description header
# #             description_rows = driver.find_elements(By.XPATH, "//tr[@class='row ng-star-inserted' and contains(@app-row-detail, '_nghost-hibid-c3894337431')]")
# #             print(f"Found {len(description_rows)} description rows")
            
# #             for i, row in enumerate(description_rows):
# #                 try:
# #                     # Extract the description header
# #                     desc_header = row.find_element(By.CSS_SELECTOR, "th.col-4.col-sm-3.col-md-2")
# #                     header_text = desc_header.text.strip()
                    
# #                     if header_text.lower() == "description":  # Specifically target the Description row
# #                         # Extract the description content
# #                         desc_content = row.find_element(By.CSS_SELECTOR, "td.col-8.col-sm-9.col-md-10.ng-star-inserted")
# #                         # Try to find the div with text-pre-line, with a fallback to get all text
# #                         try:
# #                             content_div = desc_content.find_element(By.CSS_SELECTOR, "div.text-pre-line")
# #                             content_text = content_div.text.strip()
# #                         except NoSuchElementException:
# #                             content_text = desc_content.text.strip()  # Fallback to td text if div not found
                            
# #                         # Store in scraped data
# #                         key = f"scrolled_{header_text.lower().replace(' ', '_')}_row_{i+1}"
# #                         scraped_data[key] = content_text
# #                         print(f"Row {i+1} - {header_text}: {content_text}")
                        
# #                 except NoSuchElementException as e:
# #                     print(f"Could not extract data from row {i+1}: {e}")
# #                     continue
                    
# #         except NoSuchElementException:
# #             print("No matching table rows found after scrolling")
# #         except Exception as e:
# #             print(f"Error scraping after scroll: {e}")
        
# #         print("=== SCROLL SCRAPING COMPLETE ===\n")

# #         # Scrape lot number from table
# #         try:
# #             lot_element = driver.find_element(By.XPATH, "//th[contains(text(), 'Lot #')]/following-sibling::td")
# #             scraped_data['lot_number'] = lot_element.text.strip()
# #             print(f"Lot Number: {scraped_data['lot_number']}")
# #         except NoSuchElementException:
# #             scraped_data['lot_number'] = "Not found"
# #             print("Lot Number: Not found")

# #         # Scrape category/group information
# #         try:
# #             category_element = driver.find_element(By.XPATH, "//th[contains(text(), 'Group') or contains(text(), 'Category')]/following-sibling::td")
# #             scraped_data['category'] = category_element.text.strip()
# #             print(f"Category: {scraped_data['category']}")
# #         except NoSuchElementException:
# #             try:
# #                 # Alternative selector for category links
# #                 category_link = driver.find_element(By.CSS_SELECTOR, "a[href*='sporting-goods']")
# #                 scraped_data['category'] = category_link.get_attribute('href')
# #                 print(f"Category Link: {scraped_data['category']}")
# #             except NoSuchElementException:
# #                 scraped_data['category'] = "Not found"
# #                 print("Category: Not found")

# #         # Scrape item description/title
# #         try:
# #             description_element = driver.find_element(By.XPATH, "//th[contains(text(), 'Lead')]/following-sibling::td")
# #             scraped_data['description'] = description_element.text.strip()
# #             print(f"Description: {scraped_data['description']}")
# #         except NoSuchElementException:
# #             scraped_data['description'] = "Not found"
# #             print("Description: Not found")

# #         # Scrape auction details from accordion
# #         try:
# #             # Look for auction detail accordion
# #             accordion_button = driver.find_element(By.CSS_SELECTOR, "div[role='button'][aria-label*='Information']")
# #             if accordion_button.get_attribute('aria-expanded') == 'false':
# #                 accordion_button.click()
# #                 time.sleep(1)

# #             # Scrape additional information from the expanded accordion
# #             info_table = driver.find_element(By.CSS_SELECTOR, "table.table-no-border")
# #             rows = info_table.find_elements(By.TAG_NAME, "tr")

# #             for row in rows:
# #                 try:
# #                     header = row.find_element(By.TAG_NAME, "th").text.strip()
# #                     data = row.find_element(By.TAG_NAME, "td").text.strip()
# #                     scraped_data[header.lower().replace(' ', '_')] = data
# #                     print(f"{header}: {data}")
# #                 except NoSuchElementException:
# #                     continue

# #         except NoSuchElementException:
# #             print("Auction details accordion not found")

# #         # Enhanced image extraction with detailed debugging
# #         print("\n=== STARTING IMAGE EXTRACTION DEBUG ===")

# #         try:
# #             print("🔍 Step 1: Waiting for ngx-gallery to load...")
# #             WebDriverWait(driver, 10).until(
# #                 EC.presence_of_element_located((By.CSS_SELECTOR, "ngx-gallery"))
# #             )
# #             print("✅ ngx-gallery element found!")

# #             # Method 1: Extract from ngx-gallery-image with background-image style
# #             print("\n🔍 Step 2: Method 1 - Looking for div.ngx-gallery-image with background-image...")
# #             try:
# #                 gallery_image = driver.find_element(By.CSS_SELECTOR, "div.ngx-gallery-image[style*='background-image']")
# #                 print("✅ Found div.ngx-gallery-image with background-image style!")

# #                 style_attribute = gallery_image.get_attribute('style')
# #                 print(f"📝 Full style attribute: {style_attribute}")

# #                 # Extract URL from background-image: url("...") using regex
# #                 url_match = re.search(r'background-image:\surl\("([^"]+)"\)', style_attribute)
# #                 if url_match:
# #                     image_url = url_match.group(1)
# #                     scraped_data['main_image_url'] = image_url
# #                     print(f"✅ SUCCESS! Main Image URL extracted: {image_url}")
# #                 else:
# #                     print("❌ Could not extract URL from background-image style using regex")
# #                     # Try alternative regex patterns
# #                     alt_patterns = [
# #                         r'background-image:\surl\(([^)]+)\)',  # Without quotes
# #                         r'background-image:\s*url\(\'([^\']+)\'\)',  # Single quotes
# #                     ]
# #                     for pattern in alt_patterns:
# #                         alt_match = re.search(pattern, style_attribute)
# #                         if alt_match:
# #                             image_url = alt_match.group(1)
# #                             scraped_data['main_image_url'] = image_url
# #                             print(f"✅ SUCCESS with alternative pattern! Main Image URL: {image_url}")
# #                             break
# #                     else:
# #                         print("❌ All regex patterns failed")

# #             except NoSuchElementException:
# #                 print("❌ div.ngx-gallery-image with background-image not found")

# #                 # Debug: Check what ngx-gallery-image elements exist
# #                 try:
# #                     all_gallery_images = driver.find_elements(By.CSS_SELECTOR, "div.ngx-gallery-image")
# #                     print(f"🔍 Found {len(all_gallery_images)} div.ngx-gallery-image elements without background-image")
# #                     for i, elem in enumerate(all_gallery_images):
# #                         style = elem.get_attribute('style')
# #                         classes = elem.get_attribute('class')
# #                         print(f"  Element {i+1}: class='{classes}', style='{style}'")
# #                 except:
# #                     print("❌ No div.ngx-gallery-image elements found at all")

# #             # Method 2: Extract from ngx-gallery-image img tags
# #             print("\n🔍 Step 3: Method 2 - Looking for img tags in ngx-gallery-image...")
# #             try:
# #                 gallery_images = driver.find_elements(By.CSS_SELECTOR, "ngx-gallery-image img")
# #                 print(f"✅ Found {len(gallery_images)} img tags in ngx-gallery-image")

# #                 image_urls = []
# #                 for i, img in enumerate(gallery_images):
# #                     src = img.get_attribute('src')
# #                     alt = img.get_attribute('alt')
# #                     classes = img.get_attribute('class')
# #                     print(f"  Image {i+1}: src='{src}', alt='{alt}', class='{classes}'")
# #                     if src:
# #                         image_urls.append(src)

# #                 if image_urls:
# #                     scraped_data['gallery_image_urls'] = image_urls
# #                     scraped_data['image_count'] = len(image_urls)
# #                     print(f"✅ SUCCESS! Gallery Image URLs extracted: {image_urls}")
# #                 else:
# #                     print("❌ No valid src attributes found in img tags")

# #             except NoSuchElementException:
# #                 print("❌ No img tags found in ngx-gallery-image")

# #             # Method 3: Extract from thumbnails
# #             print("\n🔍 Step 4: Method 3 - Looking for thumbnail images...")
# #             try:
# #                 thumbnails = driver.find_elements(By.CSS_SELECTOR, "ngx-gallery-thumbnails img, .ngx-gallery-layout .thumbnails-bottom img")
# #                 print(f"✅ Found {len(thumbnails)} thumbnail images")

# #                 thumbnail_urls = []
# #                 for i, thumb in enumerate(thumbnails):
# #                     src = thumb.get_attribute('src')
# #                     print(f"  Thumbnail {i+1}: {src}")
# #                     if src:
# #                         thumbnail_urls.append(src)

# #                 if thumbnail_urls:
# #                     scraped_data['thumbnail_urls'] = thumbnail_urls
# #                     print(f"✅ SUCCESS! Thumbnail URLs extracted: {thumbnail_urls}")
# #                 else:
# #                     print("❌ No valid thumbnail URLs found")

# #             except NoSuchElementException:
# #                 print("❌ No thumbnail images found")

# #             # Method 4: Look for any images within the gallery container
# #             print("\n🔍 Step 5: Method 4 - Looking for ALL images in gallery container...")
# #             try:
# #                 gallery_container = driver.find_element(By.CSS_SELECTOR, "ngx-gallery")
# #                 all_images = gallery_container.find_elements(By.TAG_NAME, "img")
# #                 print(f"✅ Found {len(all_images)} total images in gallery container")

# #                 if all_images:
# #                     scraped_data['all_gallery_images'] = []
# #                     for i, img in enumerate(all_images):
# #                         img_data = {
# #                             'src': img.get_attribute('src'),
# #                             'alt': img.get_attribute('alt'),
# #                             'class': img.get_attribute('class'),
# #                             'style': img.get_attribute('style')
# #                         }
# #                         scraped_data['all_gallery_images'].append(img_data)
# #                         print(f"  Image {i+1}:")
# #                         print(f"    src: {img_data['src']}")
# #                         print(f"    alt: {img_data['alt']}")
# #                         print(f"    class: {img_data['class']}")
# #                         print(f"    style: {img_data['style']}")

# #                     print(f"✅ SUCCESS! All gallery images catalogued")
# #                 else:
# #                     print("❌ No images found in gallery container")

# #             except NoSuchElementException:
# #                 print("❌ Gallery container not found")

# #             # Method 5: Broad search for any divs with background-image containing hibid
# #             print("\n🔍 Step 6: Method 5 - Broad search for any background-image with hibid...")
# #             try:
# #                 all_bg_images = driver.find_elements(By.XPATH, "//*[contains(@style, 'background-image') and contains(@style, 'hibid')]")
# #                 print(f"✅ Found {len(all_bg_images)} elements with hibid background-images")

# #                 for i, elem in enumerate(all_bg_images):
# #                     tag_name = elem.tag_name
# #                     classes = elem.get_attribute('class')
# #                     style = elem.get_attribute('style')
# #                     print(f"  Element {i+1}: <{tag_name}> class='{classes}'")
# #                     print(f"    style: {style}")

# #                     # Extract URL
# #                     url_patterns = [
# #                         r'background-image:\surl\("([^"]+)"\)',
# #                         r'background-image:\surl\(([^)]+)\)',
# #                         r'background-image:\s*url\(\'([^\']+)\'\)'
# #                     ]

# #                     for pattern in url_patterns:
# #                         match = re.search(pattern, style)
# #                         if match:
# #                             url = match.group(1)
# #                             print(f"    ✅ Extracted URL: {url}")
# #                             if 'broad_search_images' not in scraped_data:
# #                                 scraped_data['broad_search_images'] = []
# #                             scraped_data['broad_search_images'].append(url)
# #                             break

# #             except Exception as e:
# #                 print(f"❌ Broad search failed: {e}")

# #         except TimeoutException:
# #             print("❌ Gallery did not load in time")
# #         except Exception as e:
# #             print(f"❌ Error extracting images: {e}")

# #         print("\n=== IMAGE EXTRACTION DEBUG COMPLETE ===\n")

# #         # Scrape any additional lot details
# #         try:
# #             lot_details_container = driver.find_element(By.CSS_SELECTOR, "div[class*='lot-details-container']")
# #             lot_info = lot_details_container.text.strip()
# #             scraped_data['lot_details'] = lot_info
# #             print(f"Additional lot details found: {len(lot_info)} characters")
# #         except NoSuchElementException:
# #             print("No additional lot details container found")

# #         print(f"\nScraping completed. Total data points collected: {len(scraped_data)}")

# #         # Print summary
# #         print("\n--- SCRAPED DATA SUMMARY ---")
# #         for key, value in scraped_data.items():
# #             if isinstance(value, list):
# #                 print(f"{key}: {len(value)} items")
# #                 for i, item in enumerate(value[:3]):  # Show first 3 items
# #                     print(f"  {i+1}: {item}")
# #                 if len(value) > 3:
# #                     print(f"  ... and {len(value)-3} more")
# #             else:
# #                 print(f"{key}: {value}")

# #         # Keep browser open
# #         input("\nPress Enter to close browser...")

# #     except TimeoutException:
# #         print("Page load timeout")
# #     except Exception as e:
# #         print(f"Error: {e}")
# #     finally:
# #         driver.quit()

# # if __name__ == "__main__":
# #     scrape_auction_data()











# # import time
# # import re
# # from selenium import webdriver
# # from selenium.webdriver.firefox.options import Options
# # from selenium.webdriver.common.by import By
# # from selenium.webdriver.support.ui import WebDriverWait
# # from selenium.webdriver.support import expected_conditions as EC
# # from selenium.common.exceptions import TimeoutException, NoSuchElementException

# # def scrape_auction_data():
# #     # Get user input
# #     url = input("Enter URL: ")
# #     platform_name = input("Enter Platform Name: ")
# #     auction_name = input("Enter Auction Name: ")
# #     lot_number = input("Enter Lot Number: ")

# #     # Configure Firefox options
# #     firefox_options = Options()
# #     firefox_options.add_argument("--width=1000")
# #     firefox_options.add_argument("--height=700")

# #     # Initialize Firefox driver
# #     driver = webdriver.Firefox(options=firefox_options)

# #     try:
# #         # Navigate to URL
# #         driver.get(url)

# #         # Wait for page to load
# #         WebDriverWait(driver, 10).until(
# #             EC.presence_of_element_located((By.TAG_NAME, "body"))
# #         )

# #         print(f"Navigated to: {url}")
# #         print(f"Platform: {platform_name}")
# #         print(f"Auction: {auction_name}")
# #         print(f"Lot: {lot_number}")
# #         print("\nScraping auction data...")

# #         # Wait for content to load
# #         time.sleep(3)

# #         scraped_data = {}

# #         # Get viewport height for scrolling
# #         viewport_height = driver.execute_script("return window.innerHeight")
# #         print(f"Viewport height: {viewport_height}px")

# #         # Scroll down by 1.2x screen heights (reduced from 1.5x)
# #         scroll_amount = int(viewport_height * 1.2)
# #         driver.execute_script(f"window.scrollBy(0, {scroll_amount})")
# #         print(f"Scrolled down by {scroll_amount}px")
        
# #         # Wait for any dynamic content to load after scrolling
# #         time.sleep(5)  # Increased wait time

# #         # Scrape the specific table structure after scrolling
# #         print("\n=== SCRAPING AFTER SCROLL ===")
# #         try:
# #             # Look for the specific table row with Description header
# #             description_rows = driver.find_elements(By.XPATH, "//tr[@class='row ng-star-inserted' and contains(@app-row-detail, '_nghost-hibid-c3894337431')]")
# #             print(f"Found {len(description_rows)} description rows")
            
# #             for i, row in enumerate(description_rows):
# #                 try:
# #                     # Extract the description header
# #                     desc_header = row.find_element(By.CSS_SELECTOR, "th.col-4.col-sm-3.col-md-2")
# #                     header_text = desc_header.text.strip()
# #                     print(f"DEBUG: Row {i+1} - Header found: {header_text}")
                    
# #                     if header_text.lower() == "description":  # Specifically target the Description row
# #                         print(f"DEBUG: Processing Description row {i+1}")
# #                         # Extract the description content
# #                         desc_content = row.find_element(By.CSS_SELECTOR, "td.col-8.col-sm-9.col-md-10.ng-star-inserted")
# #                         print(f"DEBUG: Found td content element: {desc_content.text[:50]}...")  # Print first 50 chars of td text
                        
# #                         # Try to find the div with text-pre-line, with detailed fallback
# #                         try:
# #                             content_div = desc_content.find_element(By.CSS_SELECTOR, "div.text-pre-line")
# #                             content_text = content_div.text.strip()
# #                             print(f"DEBUG: Successfully extracted div.text-pre-line content: {content_text[:50]}...")
# #                         except NoSuchElementException as e:
# #                             print(f"DEBUG: Failed to find div.text-pre-line: {e}")
# #                             try:
# #                                 content_text = desc_content.text.strip()
# #                                 print(f"DEBUG: Fallback to td text successful: {content_text[:50]}...")
# #                             except Exception as e2:
# #                                 print(f"DEBUG: Fallback to td text failed: {e2}")
# #                                 content_text = "Extraction failed"
                        
# #                         # Store in scraped data
# #                         key = f"scrolled_{header_text.lower().replace(' ', '_')}_row_{i+1}"
# #                         scraped_data[key] = content_text
# #                         print(f"DEBUG: Stored data for {key}: {content_text[:50]}...")
                        
# #                 except NoSuchElementException as e:
# #                     print(f"DEBUG: Could not extract data from row {i+1}: {e}")
# #                     continue
                    
# #         except NoSuchElementException:
# #             print("DEBUG: No matching table rows found after scrolling")
# #         except Exception as e:
# #             print(f"DEBUG: Error scraping after scroll: {e}")
        
# #         print("=== SCROLL SCRAPING COMPLETE ===\n")

# #         # Scrape lot number from table
# #         try:
# #             lot_element = driver.find_element(By.XPATH, "//th[contains(text(), 'Lot #')]/following-sibling::td")
# #             scraped_data['lot_number'] = lot_element.text.strip()
# #             print(f"Lot Number: {scraped_data['lot_number']}")
# #         except NoSuchElementException:
# #             scraped_data['lot_number'] = "Not found"
# #             print("Lot Number: Not found")

# #         # Scrape category/group information
# #         try:
# #             category_element = driver.find_element(By.XPATH, "//th[contains(text(), 'Group') or contains(text(), 'Category')]/following-sibling::td")
# #             scraped_data['category'] = category_element.text.strip()
# #             print(f"Category: {scraped_data['category']}")
# #         except NoSuchElementException:
# #             try:
# #                 # Alternative selector for category links
# #                 category_link = driver.find_element(By.CSS_SELECTOR, "a[href*='sporting-goods']")
# #                 scraped_data['category'] = category_link.get_attribute('href')
# #                 print(f"Category Link: {scraped_data['category']}")
# #             except NoSuchElementException:
# #                 scraped_data['category'] = "Not found"
# #                 print("Category: Not found")

# #         # Scrape item description/title
# #         try:
# #             description_element = driver.find_element(By.XPATH, "//th[contains(text(), 'Lead')]/following-sibling::td")
# #             scraped_data['description'] = description_element.text.strip()
# #             print(f"Description: {scraped_data['description']}")
# #         except NoSuchElementException:
# #             scraped_data['description'] = "Not found"
# #             print("Description: Not found")

# #         # Scrape auction details from accordion
# #         try:
# #             # Look for auction detail accordion
# #             accordion_button = driver.find_element(By.CSS_SELECTOR, "div[role='button'][aria-label*='Information']")
# #             if accordion_button.get_attribute('aria-expanded') == 'false':
# #                 accordion_button.click()
# #                 time.sleep(1)

# #             # Scrape additional information from the expanded accordion
# #             info_table = driver.find_element(By.CSS_SELECTOR, "table.table-no-border")
# #             rows = info_table.find_elements(By.TAG_NAME, "tr")

# #             for row in rows:
# #                 try:
# #                     header = row.find_element(By.TAG_NAME, "th").text.strip()
# #                     data = row.find_element(By.TAG_NAME, "td").text.strip()
# #                     scraped_data[header.lower().replace(' ', '_')] = data
# #                     print(f"{header}: {data}")
# #                 except NoSuchElementException:
# #                     continue

# #         except NoSuchElementException:
# #             print("Auction details accordion not found")

# #         # Enhanced image extraction with detailed debugging
# #         print("\n=== STARTING IMAGE EXTRACTION DEBUG ===")

# #         try:
# #             print("🔍 Step 1: Waiting for ngx-gallery to load...")
# #             WebDriverWait(driver, 10).until(
# #                 EC.presence_of_element_located((By.CSS_SELECTOR, "ngx-gallery"))
# #             )
# #             print("✅ ngx-gallery element found!")

# #             # Method 1: Extract from ngx-gallery-image with background-image style
# #             print("\n🔍 Step 2: Method 1 - Looking for div.ngx-gallery-image with background-image...")
# #             try:
# #                 gallery_image = driver.find_element(By.CSS_SELECTOR, "div.ngx-gallery-image[style*='background-image']")
# #                 print("✅ Found div.ngx-gallery-image with background-image style!")

# #                 style_attribute = gallery_image.get_attribute('style')
# #                 print(f"📝 Full style attribute: {style_attribute}")

# #                 # Extract URL from background-image: url("...") using regex
# #                 url_match = re.search(r'background-image:\surl\("([^"]+)"\)', style_attribute)
# #                 if url_match:
# #                     image_url = url_match.group(1)
# #                     scraped_data['main_image_url'] = image_url
# #                     print(f"✅ SUCCESS! Main Image URL extracted: {image_url}")
# #                 else:
# #                     print("❌ Could not extract URL from background-image style using regex")
# #                     # Try alternative regex patterns
# #                     alt_patterns = [
# #                         r'background-image:\surl\(([^)]+)\)',  # Without quotes
# #                         r'background-image:\s*url\(\'([^\']+)\'\)',  # Single quotes
# #                     ]
# #                     for pattern in alt_patterns:
# #                         alt_match = re.search(pattern, style_attribute)
# #                         if alt_match:
# #                             image_url = alt_match.group(1)
# #                             scraped_data['main_image_url'] = image_url
# #                             print(f"✅ SUCCESS with alternative pattern! Main Image URL: {image_url}")
# #                             break
# #                     else:
# #                         print("❌ All regex patterns failed")

# #             except NoSuchElementException:
# #                 print("❌ div.ngx-gallery-image with background-image not found")

# #                 # Debug: Check what ngx-gallery-image elements exist
# #                 try:
# #                     all_gallery_images = driver.find_elements(By.CSS_SELECTOR, "div.ngx-gallery-image")
# #                     print(f"🔍 Found {len(all_gallery_images)} div.ngx-gallery-image elements without background-image")
# #                     for i, elem in enumerate(all_gallery_images):
# #                         style = elem.get_attribute('style')
# #                         classes = elem.get_attribute('class')
# #                         print(f"  Element {i+1}: class='{classes}', style='{style}'")
# #                 except:
# #                     print("❌ No div.ngx-gallery-image elements found at all")

# #             # Method 2: Extract from ngx-gallery-image img tags
# #             print("\n🔍 Step 3: Method 2 - Looking for img tags in ngx-gallery-image...")
# #             try:
# #                 gallery_images = driver.find_elements(By.CSS_SELECTOR, "ngx-gallery-image img")
# #                 print(f"✅ Found {len(gallery_images)} img tags in ngx-gallery-image")

# #                 image_urls = []
# #                 for i, img in enumerate(gallery_images):
# #                     src = img.get_attribute('src')
# #                     alt = img.get_attribute('alt')
# #                     classes = img.get_attribute('class')
# #                     print(f"  Image {i+1}: src='{src}', alt='{alt}', class='{classes}'")
# #                     if src:
# #                         image_urls.append(src)

# #                 if image_urls:
# #                     scraped_data['gallery_image_urls'] = image_urls
# #                     scraped_data['image_count'] = len(image_urls)
# #                     print(f"✅ SUCCESS! Gallery Image URLs extracted: {image_urls}")
# #                 else:
# #                     print("❌ No valid src attributes found in img tags")

# #             except NoSuchElementException:
# #                 print("❌ No img tags found in ngx-gallery-image")

# #             # Method 3: Extract from thumbnails
# #             print("\n🔍 Step 4: Method 3 - Looking for thumbnail images...")
# #             try:
# #                 thumbnails = driver.find_elements(By.CSS_SELECTOR, "ngx-gallery-thumbnails img, .ngx-gallery-layout .thumbnails-bottom img")
# #                 print(f"✅ Found {len(thumbnails)} thumbnail images")

# #                 thumbnail_urls = []
# #                 for i, thumb in enumerate(thumbnails):
# #                     src = thumb.get_attribute('src')
# #                     print(f"  Thumbnail {i+1}: {src}")
# #                     if src:
# #                         thumbnail_urls.append(src)

# #                 if thumbnail_urls:
# #                     scraped_data['thumbnail_urls'] = thumbnail_urls
# #                     print(f"✅ SUCCESS! Thumbnail URLs extracted: {thumbnail_urls}")
# #                 else:
# #                     print("❌ No valid thumbnail URLs found")

# #             except NoSuchElementException:
# #                 print("❌ No thumbnail images found")

# #             # Method 4: Look for any images within the gallery container
# #             print("\n🔍 Step 5: Method 4 - Looking for ALL images in gallery container...")
# #             try:
# #                 gallery_container = driver.find_element(By.CSS_SELECTOR, "ngx-gallery")
# #                 all_images = gallery_container.find_elements(By.TAG_NAME, "img")
# #                 print(f"✅ Found {len(all_images)} total images in gallery container")

# #                 if all_images:
# #                     scraped_data['all_gallery_images'] = []
# #                     for i, img in enumerate(all_images):
# #                         img_data = {
# #                             'src': img.get_attribute('src'),
# #                             'alt': img.get_attribute('alt'),
# #                             'class': img.get_attribute('class'),
# #                             'style': img.get_attribute('style')
# #                         }
# #                         scraped_data['all_gallery_images'].append(img_data)
# #                         print(f"  Image {i+1}:")
# #                         print(f"    src: {img_data['src']}")
# #                         print(f"    alt: {img_data['alt']}")
# #                         print(f"    class: {img_data['class']}")
# #                         print(f"    style: {img_data['style']}")

# #                     print(f"✅ SUCCESS! All gallery images catalogued")
# #                 else:
# #                     print("❌ No images found in gallery container")

# #             except NoSuchElementException:
# #                 print("❌ Gallery container not found")

# #             # Method 5: Broad search for any divs with background-image containing hibid
# #             print("\n🔍 Step 6: Method 5 - Broad search for any background-image with hibid...")
# #             try:
# #                 all_bg_images = driver.find_elements(By.XPATH, "//*[contains(@style, 'background-image') and contains(@style, 'hibid')]")
# #                 print(f"✅ Found {len(all_bg_images)} elements with hibid background-images")

# #                 for i, elem in enumerate(all_bg_images):
# #                     tag_name = elem.tag_name
# #                     classes = elem.get_attribute('class')
# #                     style = elem.get_attribute('style')
# #                     print(f"  Element {i+1}: <{tag_name}> class='{classes}'")
# #                     print(f"    style: {style}")

# #                     # Extract URL
# #                     url_patterns = [
# #                         r'background-image:\surl\("([^"]+)"\)',
# #                         r'background-image:\surl\(([^)]+)\)',
# #                         r'background-image:\s*url\(\'([^\']+)\'\)'
# #                     ]

# #                     for pattern in url_patterns:
# #                         match = re.search(pattern, style)
# #                         if match:
# #                             url = match.group(1)
# #                             print(f"    ✅ Extracted URL: {url}")
# #                             if 'broad_search_images' not in scraped_data:
# #                                 scraped_data['broad_search_images'] = []
# #                             scraped_data['broad_search_images'].append(url)
# #                             break

# #             except Exception as e:
# #                 print(f"❌ Broad search failed: {e}")

# #         except TimeoutException:
# #             print("❌ Gallery did not load in time")
# #         except Exception as e:
# #             print(f"❌ Error extracting images: {e}")

# #         print("\n=== IMAGE EXTRACTION DEBUG COMPLETE ===\n")

# #         # Scrape any additional lot details
# #         try:
# #             lot_details_container = driver.find_element(By.CSS_SELECTOR, "div[class*='lot-details-container']")
# #             lot_info = lot_details_container.text.strip()
# #             scraped_data['lot_details'] = lot_info
# #             print(f"Additional lot details found: {len(lot_info)} characters")
# #         except NoSuchElementException:
# #             print("No additional lot details container found")

# #         print(f"\nScraping completed. Total data points collected: {len(scraped_data)}")

# #         # Print summary
# #         print("\n--- SCRAPED DATA SUMMARY ---")
# #         for key, value in scraped_data.items():
# #             if isinstance(value, list):
# #                 print(f"{key}: {len(value)} items")
# #                 for i, item in enumerate(value[:3]):  # Show first 3 items
# #                     print(f"  {i+1}: {item}")
# #                 if len(value) > 3:
# #                     print(f"  ... and {len(value)-3} more")
# #             else:
# #                 print(f"{key}: {value}")

# #         # Keep browser open
# #         input("\nPress Enter to close browser...")

# #     except TimeoutException:
# #         print("Page load timeout")
# #     except Exception as e:
# #         print(f"Error: {e}")
# #     finally:
# #         driver.quit()

# # if __name__ == "__main__":
# #     scrape_auction_data()


















# import time
# import re
# from selenium import webdriver
# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException, NoSuchElementException

# def scrape_auction_data():
#     # Get user input
#     url = input("Enter URL: ")
#     platform_name = input("Enter Platform Name: ")
#     auction_name = input("Enter Auction Name: ")
#     lot_number = input("Enter Lot Number: ")

#     # Configure Firefox options
#     firefox_options = Options()
#     firefox_options.add_argument("--width=1000")
#     firefox_options.add_argument("--height=700")

#     # Initialize Firefox driver
#     driver = webdriver.Firefox(options=firefox_options)

#     try:
#         # Navigate to URL
#         driver.get(url)

#         # Wait for page to load
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.TAG_NAME, "body"))
#         )

#         print(f"Navigated to: {url}")
#         print(f"Platform: {platform_name}")
#         print(f"Auction: {auction_name}")
#         print(f"Lot: {lot_number}")
#         print("\nScraping auction data...")

#         # Wait for content to load
#         time.sleep(3)

#         scraped_data = {}

#         # Get viewport height for scrolling
#         viewport_height = driver.execute_script("return window.innerHeight")
#         print(f"Viewport height: {viewport_height}px")

#         # Scroll down by 1.2x screen heights
#         scroll_amount = int(viewport_height * 1.2)
#         driver.execute_script(f"window.scrollBy(0, {scroll_amount})")
#         print(f"Scrolled down by {scroll_amount}px")
        
#         # Wait for any dynamic content to load after scrolling
#         time.sleep(5)

#         # Enhanced description scraping with multiple strategies
#         print("\n=== ENHANCED DESCRIPTION SCRAPING ===")
        
#         # Strategy 1: Look for the specific table structure you showed
#         try:
#             print("🔍 Strategy 1: Looking for Description in table rows...")
            
#             # Wait for the accordion to be expanded or expand it
#             try:
#                 accordion_button = driver.find_element(By.CSS_SELECTOR, "div[role='button'][aria-label*='Information']")
#                 if accordion_button.get_attribute('aria-expanded') == 'false':
#                     print("📝 Expanding accordion...")
#                     accordion_button.click()
#                     time.sleep(2)
#             except NoSuchElementException:
#                 print("📝 No accordion found or already expanded")

#             # Look for all table rows in the auction detail section
#             table_rows = driver.find_elements(By.CSS_SELECTOR, "tr.row.ng-star-inserted")
#             print(f"📊 Found {len(table_rows)} table rows")
            
#             for i, row in enumerate(table_rows):
#                 try:
#                     # Get the header cell
#                     header_cell = row.find_element(By.CSS_SELECTOR, "th")
#                     header_text = header_cell.text.strip()
#                     print(f"🏷️  Row {i+1}: Header = '{header_text}'")
                    
#                     if header_text.lower() == "description":
#                         print(f"✅ Found Description row!")
                        
#                         # Get the data cell
#                         data_cell = row.find_element(By.CSS_SELECTOR, "td")
                        
#                         # Try multiple methods to extract the description
#                         description_text = None
                        
#                         # Method 1: Look for div.text-pre-line
#                         try:
#                             desc_div = data_cell.find_element(By.CSS_SELECTOR, "div.text-pre-line")
#                             description_text = desc_div.text.strip()
#                             print(f"✅ Method 1 success - div.text-pre-line: {description_text[:100]}...")
#                         except NoSuchElementException:
#                             print("❌ Method 1 failed - no div.text-pre-line found")
                        
#                         # Method 2: Get all text from the td element
#                         if not description_text:
#                             try:
#                                 description_text = data_cell.text.strip()
#                                 print(f"✅ Method 2 success - td text: {description_text[:100]}...")
#                             except Exception as e:
#                                 print(f"❌ Method 2 failed: {e}")
                        
#                         # Method 3: Get innerHTML and clean it
#                         if not description_text:
#                             try:
#                                 inner_html = data_cell.get_attribute('innerHTML')
#                                 # Remove HTML tags and get clean text
#                                 clean_text = re.sub(r'<[^>]+>', '', inner_html).strip()
#                                 # Replace HTML entities
#                                 clean_text = clean_text.replace('&nbsp;', ' ').replace('&amp;', '&')
#                                 if clean_text:
#                                     description_text = clean_text
#                                     print(f"✅ Method 3 success - innerHTML cleaned: {description_text[:100]}...")
#                             except Exception as e:
#                                 print(f"❌ Method 3 failed: {e}")
                        
#                         if description_text:
#                             scraped_data['description_detailed'] = description_text
#                             print(f"✅ DESCRIPTION SUCCESSFULLY EXTRACTED: {len(description_text)} characters")
#                             break
#                         else:
#                             print("❌ All methods failed to extract description")
                            
#                 except NoSuchElementException as e:
#                     print(f"❌ Could not process row {i+1}: {e}")
#                     continue
                    
#         except Exception as e:
#             print(f"❌ Strategy 1 failed: {e}")

#         # Strategy 2: Alternative selectors for description
#         if 'description_detailed' not in scraped_data:
#             print("\n🔍 Strategy 2: Alternative description selectors...")
            
#             alternative_selectors = [
#                 "div.text-pre-line",
#                 "td.ng-star-inserted div.text-pre-line",
#                 "//th[contains(text(),'Description')]/following-sibling::td//div[@class='text-pre-line']",
#                 "//th[text()='Description']/following-sibling::td",
#                 "[class*='text-pre-line']"
#             ]
            
#             for selector in alternative_selectors:
#                 try:
#                     if selector.startswith("//"):
#                         elements = driver.find_elements(By.XPATH, selector)
#                     else:
#                         elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    
#                     print(f"📋 Selector '{selector}': Found {len(elements)} elements")
                    
#                     for element in elements:
#                         text = element.text.strip()
#                         if text and len(text) > 20:  # Assuming description should be meaningful
#                             scraped_data['description_detailed'] = text
#                             print(f"✅ DESCRIPTION FOUND with '{selector}': {text[:100]}...")
#                             break
                    
#                     if 'description_detailed' in scraped_data:
#                         break
                        
#                 except Exception as e:
#                     print(f"❌ Selector '{selector}' failed: {e}")

#         # Strategy 3: Broad search in the lot details container
#         if 'description_detailed' not in scraped_data:
#             print("\n🔍 Strategy 3: Broad search in lot details...")
#             try:
#                 lot_container = driver.find_element(By.CSS_SELECTOR, "div[id*='lot-details']")
#                 all_text_divs = lot_container.find_elements(By.CSS_SELECTOR, "div")
                
#                 for div in all_text_divs:
#                     text = div.text.strip()
#                     classes = div.get_attribute('class') or ''
                    
#                     # Look for divs with substantial text content
#                     if text and len(text) > 50 and ('text-pre-line' in classes or len(text) > 100):
#                         scraped_data['description_detailed'] = text
#                         print(f"✅ DESCRIPTION FOUND in broad search: {text[:100]}...")
#                         break
                        
#             except Exception as e:
#                 print(f"❌ Strategy 3 failed: {e}")

#         print("=== DESCRIPTION SCRAPING COMPLETE ===\n")

#         # Scrape lot number from table
#         try:
#             lot_element = driver.find_element(By.XPATH, "//th[contains(text(), 'Lot #')]/following-sibling::td")
#             scraped_data['lot_number'] = lot_element.text.strip()
#             print(f"Lot Number: {scraped_data['lot_number']}")
#         except NoSuchElementException:
#             scraped_data['lot_number'] = "Not found"
#             print("Lot Number: Not found")

#         # Scrape category/group information
#         try:
#             category_element = driver.find_element(By.XPATH, "//th[contains(text(), 'Group') or contains(text(), 'Category')]/following-sibling::td")
#             scraped_data['category'] = category_element.text.strip()
#             print(f"Category: {scraped_data['category']}")
#         except NoSuchElementException:
#             try:
#                 # Alternative selector for category links
#                 category_link = driver.find_element(By.CSS_SELECTOR, "a[href*='sporting-goods']")
#                 scraped_data['category'] = category_link.get_attribute('href')
#                 print(f"Category Link: {scraped_data['category']}")
#             except NoSuchElementException:
#                 scraped_data['category'] = "Not found"
#                 print("Category: Not found")

#         # Scrape item description/title (different from detailed description)
#         try:
#             title_element = driver.find_element(By.XPATH, "//th[contains(text(), 'Lead')]/following-sibling::td")
#             scraped_data['title'] = title_element.text.strip()
#             print(f"Title: {scraped_data['title']}")
#         except NoSuchElementException:
#             scraped_data['title'] = "Not found"
#             print("Title: Not found")

#         # Scrape auction details from accordion with enhanced approach
#         try:
#             # Ensure accordion is expanded
#             accordion_button = driver.find_element(By.CSS_SELECTOR, "div[role='button'][aria-label*='Information']")
#             if accordion_button.get_attribute('aria-expanded') == 'false':
#                 accordion_button.click()
#                 time.sleep(2)

#             # Scrape additional information from the expanded accordion
#             info_tables = driver.find_elements(By.CSS_SELECTOR, "table.table-no-border")
            
#             for table in info_tables:
#                 rows = table.find_elements(By.TAG_NAME, "tr")
                
#                 for row in rows:
#                     try:
#                         header = row.find_element(By.TAG_NAME, "th").text.strip()
#                         data = row.find_element(By.TAG_NAME, "td").text.strip()
                        
#                         if header and data:
#                             key = header.lower().replace(' ', '_').replace('#', 'number')
#                             scraped_data[key] = data
#                             print(f"{header}: {data}")
                            
#                     except NoSuchElementException:
#                         continue

#         except NoSuchElementException:
#             print("Auction details accordion not found")

#         # Enhanced image extraction (keeping your original detailed method)
#         print("\n=== STARTING IMAGE EXTRACTION DEBUG ===")

#         try:
#             print("🔍 Step 1: Waiting for ngx-gallery to load...")
#             WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located((By.CSS_SELECTOR, "ngx-gallery"))
#             )
#             print("✅ ngx-gallery element found!")

#             # Method 1: Extract from ngx-gallery-image with background-image style
#             print("\n🔍 Step 2: Method 1 - Looking for div.ngx-gallery-image with background-image...")
#             try:
#                 gallery_image = driver.find_element(By.CSS_SELECTOR, "div.ngx-gallery-image[style*='background-image']")
#                 print("✅ Found div.ngx-gallery-image with background-image style!")

#                 style_attribute = gallery_image.get_attribute('style')
#                 print(f"📝 Full style attribute: {style_attribute}")

#                 # Extract URL from background-image: url("...") using regex
#                 url_patterns = [
#                     r'background-image:\s*url\("([^"]+)"\)',
#                     r'background-image:\s*url\(([^)]+)\)',
#                     r'background-image:\s*url\(\'([^\']+)\'\)'
#                 ]
                
#                 for pattern in url_patterns:
#                     url_match = re.search(pattern, style_attribute)
#                     if url_match:
#                         image_url = url_match.group(1).strip('\'"')
#                         scraped_data['main_image_url'] = image_url
#                         print(f"✅ SUCCESS! Main Image URL extracted: {image_url}")
#                         break
#                 else:
#                     print("❌ Could not extract URL from background-image style")

#             except NoSuchElementException:
#                 print("❌ div.ngx-gallery-image with background-image not found")

#             # Method 2: Extract from ngx-gallery-image img tags
#             print("\n🔍 Step 3: Method 2 - Looking for img tags in ngx-gallery-image...")
#             try:
#                 gallery_images = driver.find_elements(By.CSS_SELECTOR, "ngx-gallery img")
#                 print(f"✅ Found {len(gallery_images)} img tags in ngx-gallery")

#                 image_urls = []
#                 for i, img in enumerate(gallery_images):
#                     src = img.get_attribute('src')
#                     if src:
#                         image_urls.append(src)
#                         print(f"  Image {i+1}: {src}")

#                 if image_urls:
#                     scraped_data['gallery_image_urls'] = image_urls
#                     scraped_data['image_count'] = len(image_urls)
#                     print(f"✅ SUCCESS! Gallery Image URLs extracted: {len(image_urls)} images")

#             except NoSuchElementException:
#                 print("❌ No img tags found in ngx-gallery")

#             # Method 3: Broad search for any images with hibid in the URL
#             print("\n🔍 Step 4: Method 3 - Broad search for hibid images...")
#             try:
#                 all_images = driver.find_elements(By.TAG_NAME, "img")
#                 hibid_images = []
                
#                 for img in all_images:
#                     src = img.get_attribute('src')
#                     if src and 'hibid' in src.lower():
#                         hibid_images.append(src)
#                         print(f"  Found hibid image: {src}")
                
#                 if hibid_images:
#                     scraped_data['hibid_images'] = hibid_images
#                     print(f"✅ SUCCESS! Found {len(hibid_images)} hibid images")

#             except Exception as e:
#                 print(f"❌ Broad image search failed: {e}")

#         except TimeoutException:
#             print("❌ Gallery did not load in time")
#         except Exception as e:
#             print(f"❌ Error extracting images: {e}")

#         print("\n=== IMAGE EXTRACTION DEBUG COMPLETE ===\n")

#         # Scrape any additional lot details
#         try:
#             lot_details_containers = driver.find_elements(By.CSS_SELECTOR, "div[class*='lot-details'], div[id*='lot-details']")
#             for container in lot_details_containers:
#                 lot_info = container.text.strip()
#                 if lot_info and len(lot_info) > 50:
#                     scraped_data['additional_lot_details'] = lot_info
#                     print(f"Additional lot details found: {len(lot_info)} characters")
#                     break
#         except NoSuchElementException:
#             print("No additional lot details container found")

#         print(f"\nScraping completed. Total data points collected: {len(scraped_data)}")

#         # Print summary
#         print("\n--- SCRAPED DATA SUMMARY ---")
#         for key, value in scraped_data.items():
#             if isinstance(value, list):
#                 print(f"{key}: {len(value)} items")
#                 for i, item in enumerate(value[:3]):  # Show first 3 items
#                     item_preview = str(item)[:100] + "..." if len(str(item)) > 100 else str(item)
#                     print(f"  {i+1}: {item_preview}")
#                 if len(value) > 3:
#                     print(f"  ... and {len(value)-3} more")
#             else:
#                 value_preview = str(value)[:200] + "..." if len(str(value)) > 200 else str(value)
#                 print(f"{key}: {value_preview}")

#         # Keep browser open
#         input("\nPress Enter to close browser...")

#     except TimeoutException:
#         print("Page load timeout")
#     except Exception as e:
#         print(f"Error: {e}")
#         import traceback
#         traceback.print_exc()
#     finally:
#         driver.quit()

# if __name__ == "__main__":
#     scrape_auction_data()




























# from flask import Flask, request, jsonify
# import time
# import re
# from selenium import webdriver
# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException, NoSuchElementException

# app = Flask(__name__)

# def create_driver():
#     """Create and configure Firefox driver"""
#     firefox_options = Options()
#     firefox_options.add_argument("--headless")  # Run in headless mode for API
#     firefox_options.add_argument("--width=1000")
#     firefox_options.add_argument("--height=700")
#     firefox_options.add_argument("--no-sandbox")
#     firefox_options.add_argument("--disable-dev-shm-usage")
    
#     return webdriver.Firefox(options=firefox_options)

# def navigate_and_scroll(driver, url):
#     """Navigate to URL and perform the scroll operation"""
#     driver.get(url)
    
#     # Wait for page to load
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.TAG_NAME, "body"))
#     )
    
#     # Wait for content to load
#     time.sleep(3)
    
#     # Get viewport height and scroll
#     viewport_height = driver.execute_script("return window.innerHeight")
#     scroll_amount = int(viewport_height * 1.2)
#     driver.execute_script(f"window.scrollBy(0, {scroll_amount})")
    
#     # Wait for dynamic content to load after scrolling
#     time.sleep(5)

# @app.route('/lot-number', methods=['POST'])
# def get_lot_number():
#     """Endpoint to get only the lot number from auction page"""
#     try:
#         # Get URL from request
#         data = request.json
#         if not data or 'url' not in data:
#             return jsonify({'error': 'URL is required in request body'}), 400
        
#         url = data['url']
        
#         # Initialize driver
#         driver = create_driver()
        
#         try:
#             # Navigate and scroll
#             navigate_and_scroll(driver, url)
            
#             # Scrape lot number
#             lot_number = "Not found"
#             try:
#                 lot_element = driver.find_element(By.XPATH, "//th[contains(text(), 'Lot #')]/following-sibling::td")
#                 lot_number = lot_element.text.strip()
#             except NoSuchElementException:
#                 pass
            
#             return jsonify({
#                 'success': True,
#                 'lot_number': lot_number,
#                 'url': url
#             })
            
#         finally:
#             driver.quit()
            
#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 500

# @app.route('/images', methods=['POST'])
# def get_all_images():
#     """Endpoint to get all image links from auction page"""
#     try:
#         # Get URL from request
#         data = request.json
#         if not data or 'url' not in data:
#             return jsonify({'error': 'URL is required in request body'}), 400
        
#         url = data['url']
        
#         # Initialize driver
#         driver = create_driver()
        
#         try:
#             # Navigate and scroll
#             navigate_and_scroll(driver, url)
            
#             image_data = {
#                 'main_image_url': None,
#                 'gallery_image_urls': [],
#                 'thumbnail_urls': [],
#                 'all_gallery_images': [],
#                 'broad_search_images': []
#             }
            
#             # Wait for gallery to load
#             try:
#                 WebDriverWait(driver, 10).until(
#                     EC.presence_of_element_located((By.CSS_SELECTOR, "ngx-gallery"))
#                 )
                
#                 # Method 1: Extract from ngx-gallery-image with background-image style
#                 try:
#                     gallery_image = driver.find_element(By.CSS_SELECTOR, "div.ngx-gallery-image[style*='background-image']")
#                     style_attribute = gallery_image.get_attribute('style')
                    
#                     # Extract URL from background-image using regex
#                     url_patterns = [
#                         r'background-image:\surl\("([^"]+)"\)',
#                         r'background-image:\surl\(([^)]+)\)',
#                         r'background-image:\s*url\(\'([^\']+)\'\)'
#                     ]
                    
#                     for pattern in url_patterns:
#                         url_match = re.search(pattern, style_attribute)
#                         if url_match:
#                             image_data['main_image_url'] = url_match.group(1)
#                             break
                            
#                 except NoSuchElementException:
#                     pass
                
#                 # Method 2: Extract from ngx-gallery-image img tags
#                 try:
#                     gallery_images = driver.find_elements(By.CSS_SELECTOR, "ngx-gallery-image img")
#                     for img in gallery_images:
#                         src = img.get_attribute('src')
#                         if src:
#                             image_data['gallery_image_urls'].append(src)
#                 except NoSuchElementException:
#                     pass
                
#                 # Method 3: Extract from thumbnails
#                 try:
#                     thumbnails = driver.find_elements(By.CSS_SELECTOR, "ngx-gallery-thumbnails img, .ngx-gallery-layout .thumbnails-bottom img")
#                     for thumb in thumbnails:
#                         src = thumb.get_attribute('src')
#                         if src:
#                             image_data['thumbnail_urls'].append(src)
#                 except NoSuchElementException:
#                     pass
                
#                 # Method 4: Look for any images within the gallery container
#                 try:
#                     gallery_container = driver.find_element(By.CSS_SELECTOR, "ngx-gallery")
#                     all_images = gallery_container.find_elements(By.TAG_NAME, "img")
                    
#                     for img in all_images:
#                         img_info = {
#                             'src': img.get_attribute('src'),
#                             'alt': img.get_attribute('alt'),
#                             'class': img.get_attribute('class')
#                         }
#                         if img_info['src']:
#                             image_data['all_gallery_images'].append(img_info)
                            
#                 except NoSuchElementException:
#                     pass
                
#                 # Method 5: Broad search for any divs with background-image containing hibid
#                 try:
#                     all_bg_images = driver.find_elements(By.XPATH, "//*[contains(@style, 'background-image') and contains(@style, 'hibid')]")
                    
#                     for elem in all_bg_images:
#                         style = elem.get_attribute('style')
#                         url_patterns = [
#                             r'background-image:\surl\("([^"]+)"\)',
#                             r'background-image:\surl\(([^)]+)\)',
#                             r'background-image:\s*url\(\'([^\']+)\'\)'
#                         ]
                        
#                         for pattern in url_patterns:
#                             match = re.search(pattern, style)
#                             if match:
#                                 image_url = match.group(1)
#                                 image_data['broad_search_images'].append(image_url)
#                                 break
                                
#                 except Exception:
#                     pass
                    
#             except TimeoutException:
#                 pass
            
#             # Create a consolidated list of all unique image URLs
#             all_image_urls = set()
            
#             if image_data['main_image_url']:
#                 all_image_urls.add(image_data['main_image_url'])
            
#             all_image_urls.update(image_data['gallery_image_urls'])
#             all_image_urls.update(image_data['thumbnail_urls'])
#             all_image_urls.update([img['src'] for img in image_data['all_gallery_images'] if img['src']])
#             all_image_urls.update(image_data['broad_search_images'])
            
#             return jsonify({
#                 'success': True,
#                 'url': url,
#                 'image_data': image_data,
#                 'all_unique_image_urls': list(all_image_urls),
#                 'total_unique_images': len(all_image_urls)
#             })
            
#         finally:
#             driver.quit()
            
#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 500

# @app.route('/health', methods=['GET'])
# def health_check():
#     """Health check endpoint"""
#     return jsonify({
#         'status': 'healthy',
#         'message': 'Auction scraper API is running'
#     })



# @app.route('/estimate', methods=['POST'])
# def get_estimate():
#     try:
#         data = request.json
#         if not data or 'url' not in data:
#             return jsonify({'error': 'URL is required in request body'}), 400

#         url = data['url']
#         driver = create_driver()

#         try:
#             navigate_and_scroll(driver, url)

#             estimate = "Not found"
#             try:
#                 estimate_elem = driver.find_element(
#                     By.XPATH,
#                     "//th[contains(text(), 'Estimate')]/following-sibling::td"
#                 )
#                 estimate = estimate_elem.text.strip()
#             except NoSuchElementException:
#                 pass

#             return jsonify({'success': True, 'estimate': estimate, 'url': url})

#         finally:
#             driver.quit()
#     except Exception as e:
#         return jsonify({'success': False, 'error': str(e)}), 500



# @app.route('/category', methods=['POST'])
# def get_category():
#     try:
#         data = request.json
#         if not data or 'url' not in data:
#             return jsonify({'error': 'URL is required in request body'}), 400

#         url = data['url']
#         driver = create_driver()

#         try:
#             navigate_and_scroll(driver, url)

#             category = "Not found"
#             try:
#                 category_elem = driver.find_element(
#                     By.XPATH,
#                     "//th[contains(text(), 'Group - Category')]/following-sibling::td"
#                 )
#                 category = category_elem.text.strip()
#             except NoSuchElementException:
#                 pass

#             return jsonify({'success': True, 'category': category, 'url': url})

#         finally:
#             driver.quit()
#     except Exception as e:
#         return jsonify({'success': False, 'error': str(e)}), 500




# @app.route('/item-name', methods=['POST'])
# def get_item_name():
#     try:
#         data = request.json
#         if not data or 'url' not in data:
#             return jsonify({'error': 'URL is required in request body'}), 400

#         url = data['url']
#         driver = create_driver()

#         try:
#             navigate_and_scroll(driver, url)

#             item_name = "Not found"
#             try:
#                 name_elem = driver.find_element(
#                     By.XPATH,
#                     "//div[contains(@class, 'page-header')]/h1/span"
#                 )
#                 item_name = name_elem.text.strip()
#             except NoSuchElementException:
#                 pass

#             return jsonify({'success': True, 'item_name': item_name, 'url': url})

#         finally:
#             driver.quit()
#     except Exception as e:
#         return jsonify({'success': False, 'error': str(e)}), 500



# @app.route('/lead', methods=['POST'])
# def get_lead():
#     try:
#         data = request.json
#         if not data or 'url' not in data:
#             return jsonify({'error': 'URL is required in request body'}), 400

#         url = data['url']
#         driver = create_driver()

#         try:
#             navigate_and_scroll(driver, url)

#             lead = "Not found"
#             try:
#                 lead_elem = driver.find_element(
#                     By.XPATH,
#                     "//th[contains(text(), 'Lead')]/following-sibling::td"
#                 )
#                 lead = lead_elem.text.strip()
#             except NoSuchElementException:
#                 pass

#             return jsonify({'success': True, 'lead': lead, 'url': url})

#         finally:
#             driver.quit()
#     except Exception as e:
#         return jsonify({'success': False, 'error': str(e)}), 500




# @app.route('/description', methods=['POST'])
# def get_description():
#     """Endpoint to get the item description from auction page"""
#     try:
#         # Get URL from request
#         data = request.json
#         if not data or 'url' not in data:
#             return jsonify({'error': 'URL is required in request body'}), 400

#         url = data['url']

#         # Initialize driver
#         driver = create_driver()

#         try:
#             # Navigate and scroll
#             navigate_and_scroll(driver, url)

#             description = "Not found"
#             try:
#                 desc_element = driver.find_element(
#                     By.XPATH,
#                     "//th[contains(text(), 'Description')]/following-sibling::td//div[contains(@class, 'text-pre-line')]"
#                 )
#                 description = desc_element.text.strip()
#             except NoSuchElementException:
#                 pass

#             return jsonify({
#                 'success': True,
#                 'description': description,
#                 'url': url
#             })

#         finally:
#             driver.quit()

#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 500




# @app.route('/', methods=['GET'])
# def home():
#     """Home endpoint with API documentation"""
#     return jsonify({
#         'message': 'Auction Scraper API',
#         'endpoints': {
#             '/lot-number': {
#                 'method': 'POST',
#                 'description': 'Get lot number from auction page',
#                 'body': {'url': 'auction_page_url'}
#             },
#             '/images': {
#                 'method': 'POST', 
#                 'description': 'Get all image links from auction page',
#                 'body': {'url': 'auction_page_url'}
#             },
#             '/health': {
#                 'method': 'GET',
#                 'description': 'Health check endpoint'
#             }
#         }
#     })


# if __name__ == '__main__':
#     import argparse
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--port', type=int, default=8000)
#     args = parser.parse_args()
    
#     app.run(debug=True, host='0.0.0.0', port=args.port)





# # if __name__ == '__main__':
# #     app.run(debug=True, host='0.0.0.0', port=5000)























from flask import Flask, request, jsonify
import time
import re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

app = Flask(__name__)

def create_driver():
    """Create and configure Firefox driver"""
    firefox_options = Options()
    firefox_options.add_argument("--headless")  # Run in headless mode for API
    firefox_options.add_argument("--width=1000")
    firefox_options.add_argument("--height=700")
    firefox_options.add_argument("--no-sandbox")
    firefox_options.add_argument("--disable-dev-shm-usage")
    
    return webdriver.Firefox(options=firefox_options)

def navigate_and_scroll(driver, url):
    """Navigate to URL and perform the scroll operation"""
    driver.get(url)
    
    # Wait for page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    
    # Wait for content to load
    time.sleep(3)
    
    # Get viewport height and scroll
    viewport_height = driver.execute_script("return window.innerHeight")
    scroll_amount = int(viewport_height * 1.2)
    driver.execute_script(f"window.scrollBy(0, {scroll_amount})")
    
    # Wait for dynamic content to load after scrolling
    time.sleep(5)

# @app.route('/extract-all', methods=['POST'])
# def extract_all_data():
#     """Combined endpoint to extract all data from auction page"""
#     try:
#         # Get URL from request
#         data = request.json
#         if not data or 'url' not in data:
#             return jsonify({'error': 'URL is required in request body'}), 400
        
#         url = data['url']
        
#         # Initialize driver
#         driver = create_driver()
        
#         try:
#             # Navigate and scroll
#             navigate_and_scroll(driver, url)
            
#             # Initialize result data
#             result_data = {
#                 'success': True,
#                 'url': url,
#                 'lot_number': "Not found",
#                 'estimate': "Not found",
#                 'category': "Not found",
#                 'item_name': "Not found",
#                 'lead': "Not found",
#                 'description': "Not found",
#                 'image_data': {
#                     'main_image_url': None,
#                     'gallery_image_urls': [],
#                     'thumbnail_urls': [],
#                     'all_gallery_images': [],
#                     'broad_search_images': []
#                 },
#                 'all_unique_image_urls': [],
#                 'total_unique_images': 0
#             }
            
#             # Extract lot number
#             try:
#                 lot_element = driver.find_element(By.XPATH, "//th[contains(text(), 'Lot #')]/following-sibling::td")
#                 result_data['lot_number'] = lot_element.text.strip()
#             except NoSuchElementException:
#                 pass
            
#             # Extract estimate
#             try:
#                 estimate_elem = driver.find_element(By.XPATH, "//th[contains(text(), 'Estimate')]/following-sibling::td")
#                 result_data['estimate'] = estimate_elem.text.strip()
#             except NoSuchElementException:
#                 pass
            
#             # Extract category
#             try:
#                 category_elem = driver.find_element(By.XPATH, "//th[contains(text(), 'Group - Category')]/following-sibling::td")
#                 result_data['category'] = category_elem.text.strip()
#             except NoSuchElementException:
#                 pass
            
#             # Extract item name
#             try:
#                 name_elem = driver.find_element(By.XPATH, "//div[contains(@class, 'page-header')]/h1/span")
#                 result_data['item_name'] = name_elem.text.strip()
#             except NoSuchElementException:
#                 pass
            
#             # Extract lead
#             try:
#                 lead_elem = driver.find_element(By.XPATH, "//th[contains(text(), 'Lead')]/following-sibling::td")
#                 result_data['lead'] = lead_elem.text.strip()
#             except NoSuchElementException:
#                 pass
            
#             # Extract description
#             try:
#                 desc_element = driver.find_element(By.XPATH, "//th[contains(text(), 'Description')]/following-sibling::td//div[contains(@class, 'text-pre-line')]")
#                 result_data['description'] = desc_element.text.strip()
#             except NoSuchElementException:
#                 pass
            
#             # Extract images
#             try:
#                 WebDriverWait(driver, 10).until(
#                     EC.presence_of_element_located((By.CSS_SELECTOR, "ngx-gallery"))
#                 )
                
#                 # Method 1: Extract from ngx-gallery-image with background-image style
#                 try:
#                     gallery_image = driver.find_element(By.CSS_SELECTOR, "div.ngx-gallery-image[style*='background-image']")
#                     style_attribute = gallery_image.get_attribute('style')
                    
#                     # Extract URL from background-image using regex
#                     url_patterns = [
#                         r'background-image:\surl\("([^"]+)"\)',
#                         r'background-image:\surl\(([^)]+)\)',
#                         r'background-image:\s*url\(\'([^\']+)\'\)'
#                     ]
                    
#                     for pattern in url_patterns:
#                         url_match = re.search(pattern, style_attribute)
#                         if url_match:
#                             result_data['image_data']['main_image_url'] = url_match.group(1)
#                             break
                            
#                 except NoSuchElementException:
#                     pass
                
#                 # Method 2: Extract from ngx-gallery-image img tags
#                 try:
#                     gallery_images = driver.find_elements(By.CSS_SELECTOR, "ngx-gallery-image img")
#                     for img in gallery_images:
#                         src = img.get_attribute('src')
#                         if src:
#                             result_data['image_data']['gallery_image_urls'].append(src)
#                 except NoSuchElementException:
#                     pass
                
#                 # Method 3: Extract from thumbnails
#                 try:
#                     thumbnails = driver.find_elements(By.CSS_SELECTOR, "ngx-gallery-thumbnails img, .ngx-gallery-layout .thumbnails-bottom img")
#                     for thumb in thumbnails:
#                         src = thumb.get_attribute('src')
#                         if src:
#                             result_data['image_data']['thumbnail_urls'].append(src)
#                 except NoSuchElementException:
#                     pass
                
#                 # Method 4: Look for any images within the gallery container
#                 try:
#                     gallery_container = driver.find_element(By.CSS_SELECTOR, "ngx-gallery")
#                     all_images = gallery_container.find_elements(By.TAG_NAME, "img")
                    
#                     for img in all_images:
#                         img_info = {
#                             'src': img.get_attribute('src'),
#                             'alt': img.get_attribute('alt'),
#                             'class': img.get_attribute('class')
#                         }
#                         if img_info['src']:
#                             result_data['image_data']['all_gallery_images'].append(img_info)
                            
#                 except NoSuchElementException:
#                     pass
                
#                 # Method 5: Broad search for any divs with background-image containing hibid
#                 try:
#                     all_bg_images = driver.find_elements(By.XPATH, "//*[contains(@style, 'background-image') and contains(@style, 'hibid')]")
                    
#                     for elem in all_bg_images:
#                         style = elem.get_attribute('style')
#                         url_patterns = [
#                             r'background-image:\surl\("([^"]+)"\)',
#                             r'background-image:\surl\(([^)]+)\)',
#                             r'background-image:\s*url\(\'([^\']+)\'\)'
#                         ]
                        
#                         for pattern in url_patterns:
#                             match = re.search(pattern, style)
#                             if match:
#                                 image_url = match.group(1)
#                                 result_data['image_data']['broad_search_images'].append(image_url)
#                                 break
                                
#                 except Exception:
#                     pass
                    
#             except TimeoutException:
#                 pass
            
#             # Create a consolidated list of all unique image URLs
#             all_image_urls = set()
            
#             if result_data['image_data']['main_image_url']:
#                 all_image_urls.add(result_data['image_data']['main_image_url'])
            
#             all_image_urls.update(result_data['image_data']['gallery_image_urls'])
#             all_image_urls.update(result_data['image_data']['thumbnail_urls'])
#             all_image_urls.update([img['src'] for img in result_data['image_data']['all_gallery_images'] if img['src']])
#             all_image_urls.update(result_data['image_data']['broad_search_images'])
            
#             result_data['all_unique_image_urls'] = list(all_image_urls)
#             result_data['total_unique_images'] = len(all_image_urls)
            
#             return jsonify(result_data)
            
#         finally:
#             driver.quit()
            
#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 500




@app.route('/extract-all', methods=['POST'])
def extract_all_data():
    """Combined endpoint to extract all data from auction page"""
    try:
        # Get URL from request
        data = request.json
        if not data or 'url' not in data:
            return jsonify({'error': 'URL is required in request body'}), 400
        
        url = data['url']
        print(url)
        
        # Initialize driver
        driver = create_driver()
        
        try:
            # Navigate and scroll
            navigate_and_scroll(driver, url)
            
            # Click Auction Information accordion
            try:
                auction_info_header = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and @aria-label='Auction Information']"))
                )
                auction_info_header.click()
                time.sleep(1.5)
            except Exception:
                pass

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
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//th[normalize-space(text())='Name']/following-sibling::td"))
                )
                auction_elem = driver.find_element(By.XPATH, "//th[normalize-space(text())='Name']/following-sibling::td")
                result_data['auction_name'] = driver.execute_script("return arguments[0].innerText;", auction_elem).strip()
            except Exception:
                pass

            # Extract lot number
            try:
                lot_element = driver.find_element(By.XPATH, "//th[contains(text(), 'Lot #')]/following-sibling::td")
                result_data['lot_number'] = lot_element.text.strip()
            except NoSuchElementException:
                pass
            
            # Extract estimate
            try:
                estimate_elem = driver.find_element(By.XPATH, "//th[contains(text(), 'Estimate')]/following-sibling::td")
                result_data['estimate'] = estimate_elem.text.strip()
            except NoSuchElementException:
                pass
            
            # Extract category
            try:
                category_elem = driver.find_element(By.XPATH, "//th[contains(text(), 'Group - Category')]/following-sibling::td")
                result_data['category'] = category_elem.text.strip()
            except NoSuchElementException:
                pass
            
            # Extract item name
            try:
                name_elem = driver.find_element(By.XPATH, "//div[contains(@class, 'page-header')]/h1/span")
                result_data['item_name'] = name_elem.text.strip()
            except NoSuchElementException:
                pass
            
            # Extract lead
            try:
                lead_elem = driver.find_element(By.XPATH, "//th[contains(text(), 'Lead')]/following-sibling::td")
                result_data['lead'] = lead_elem.text.strip()
            except NoSuchElementException:
                pass
            
            # Extract description
            try:
                desc_element = driver.find_element(By.XPATH, "//th[contains(text(), 'Description')]/following-sibling::td//div[contains(@class, 'text-pre-line')]")
                result_data['description'] = desc_element.text.strip()
            except NoSuchElementException:
                pass
            
            # Extract images
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "ngx-gallery"))
                )
                
                try:
                    gallery_image = driver.find_element(By.CSS_SELECTOR, "div.ngx-gallery-image[style*='background-image']")
                    style_attribute = gallery_image.get_attribute('style')
                    url_patterns = [
                        r'background-image:\surl\("([^"]+)"\)',
                        r'background-image:\surl\(([^)]+)\)',
                        r'background-image:\s*url\(\'([^\']+)\'\)'
                    ]
                    for pattern in url_patterns:
                        url_match = re.search(pattern, style_attribute)
                        if url_match:
                            result_data['image_data']['main_image_url'] = url_match.group(1)
                            break
                except NoSuchElementException:
                    pass
                
                try:
                    gallery_images = driver.find_elements(By.CSS_SELECTOR, "ngx-gallery-image img")
                    for img in gallery_images:
                        src = img.get_attribute('src')
                        if src:
                            result_data['image_data']['gallery_image_urls'].append(src)
                except NoSuchElementException:
                    pass
                
                try:
                    thumbnails = driver.find_elements(By.CSS_SELECTOR, "ngx-gallery-thumbnails img, .ngx-gallery-layout .thumbnails-bottom img")
                    for thumb in thumbnails:
                        src = thumb.get_attribute('src')
                        if src:
                            result_data['image_data']['thumbnail_urls'].append(src)
                except NoSuchElementException:
                    pass
                
                try:
                    gallery_container = driver.find_element(By.CSS_SELECTOR, "ngx-gallery")
                    all_images = gallery_container.find_elements(By.TAG_NAME, "img")
                    for img in all_images:
                        img_info = {
                            'src': img.get_attribute('src'),
                            'alt': img.get_attribute('alt'),
                            'class': img.get_attribute('class')
                        }
                        if img_info['src']:
                            result_data['image_data']['all_gallery_images'].append(img_info)
                except NoSuchElementException:
                    pass
                
                try:
                    all_bg_images = driver.find_elements(By.XPATH, "//*[contains(@style, 'background-image') and contains(@style, 'hibid')]")
                    for elem in all_bg_images:
                        style = elem.get_attribute('style')
                        url_patterns = [
                            r'background-image:\surl\("([^"]+)"\)',
                            r'background-image:\surl\(([^)]+)\)',
                            r'background-image:\s*url\(\'([^\']+)\'\)'
                        ]
                        for pattern in url_patterns:
                            match = re.search(pattern, style)
                            if match:
                                image_url = match.group(1)
                                result_data['image_data']['broad_search_images'].append(image_url)
                                break
                except Exception:
                    pass
                    
            except TimeoutException:
                pass
            
            all_image_urls = set()
            if result_data['image_data']['main_image_url']:
                all_image_urls.add(result_data['image_data']['main_image_url'])
            all_image_urls.update(result_data['image_data']['gallery_image_urls'])
            all_image_urls.update(result_data['image_data']['thumbnail_urls'])
            all_image_urls.update([img['src'] for img in result_data['image_data']['all_gallery_images'] if img['src']])
            all_image_urls.update(result_data['image_data']['broad_search_images'])
            result_data['all_unique_image_urls'] = list(all_image_urls)
            result_data['total_unique_images'] = len(all_image_urls)
            
            return jsonify(result_data)
            
        finally:
            driver.quit()
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500






# Keep all the individual endpoints for backward compatibility
@app.route('/lot-number', methods=['POST'])
def get_lot_number():
    """Endpoint to get only the lot number from auction page"""
    try:
        # Get URL from request
        data = request.json
        if not data or 'url' not in data:
            return jsonify({'error': 'URL is required in request body'}), 400
        
        url = data['url']
        
        # Initialize driver
        driver = create_driver()
        
        try:
            # Navigate and scroll
            navigate_and_scroll(driver, url)
            
            # Scrape lot number
            lot_number = "Not found"
            try:
                lot_element = driver.find_element(By.XPATH, "//th[contains(text(), 'Lot #')]/following-sibling::td")
                lot_number = lot_element.text.strip()
            except NoSuchElementException:
                pass
            
            return jsonify({
                'success': True,
                'lot_number': lot_number,
                'url': url
            })
            
        finally:
            driver.quit()
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/images', methods=['POST'])
def get_all_images():
    """Endpoint to get all image links from auction page"""
    try:
        # Get URL from request
        data = request.json
        if not data or 'url' not in data:
            return jsonify({'error': 'URL is required in request body'}), 400
        
        url = data['url']
        
        # Initialize driver
        driver = create_driver()
        
        try:
            # Navigate and scroll
            navigate_and_scroll(driver, url)
            
            image_data = {
                'main_image_url': None,
                'gallery_image_urls': [],
                'thumbnail_urls': [],
                'all_gallery_images': [],
                'broad_search_images': []
            }
            
            # Wait for gallery to load
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "ngx-gallery"))
                )
                
                # Method 1: Extract from ngx-gallery-image with background-image style
                try:
                    gallery_image = driver.find_element(By.CSS_SELECTOR, "div.ngx-gallery-image[style*='background-image']")
                    style_attribute = gallery_image.get_attribute('style')
                    
                    # Extract URL from background-image using regex
                    url_patterns = [
                        r'background-image:\surl\("([^"]+)"\)',
                        r'background-image:\surl\(([^)]+)\)',
                        r'background-image:\s*url\(\'([^\']+)\'\)'
                    ]
                    
                    for pattern in url_patterns:
                        url_match = re.search(pattern, style_attribute)
                        if url_match:
                            image_data['main_image_url'] = url_match.group(1)
                            break
                            
                except NoSuchElementException:
                    pass
                
                # Method 2: Extract from ngx-gallery-image img tags
                try:
                    gallery_images = driver.find_elements(By.CSS_SELECTOR, "ngx-gallery-image img")
                    for img in gallery_images:
                        src = img.get_attribute('src')
                        if src:
                            image_data['gallery_image_urls'].append(src)
                except NoSuchElementException:
                    pass
                
                # Method 3: Extract from thumbnails
                try:
                    thumbnails = driver.find_elements(By.CSS_SELECTOR, "ngx-gallery-thumbnails img, .ngx-gallery-layout .thumbnails-bottom img")
                    for thumb in thumbnails:
                        src = thumb.get_attribute('src')
                        if src:
                            image_data['thumbnail_urls'].append(src)
                except NoSuchElementException:
                    pass
                
                # Method 4: Look for any images within the gallery container
                try:
                    gallery_container = driver.find_element(By.CSS_SELECTOR, "ngx-gallery")
                    all_images = gallery_container.find_elements(By.TAG_NAME, "img")
                    
                    for img in all_images:
                        img_info = {
                            'src': img.get_attribute('src'),
                            'alt': img.get_attribute('alt'),
                            'class': img.get_attribute('class')
                        }
                        if img_info['src']:
                            image_data['all_gallery_images'].append(img_info)
                            
                except NoSuchElementException:
                    pass
                
                # Method 5: Broad search for any divs with background-image containing hibid
                try:
                    all_bg_images = driver.find_elements(By.XPATH, "//*[contains(@style, 'background-image') and contains(@style, 'hibid')]")
                    
                    for elem in all_bg_images:
                        style = elem.get_attribute('style')
                        url_patterns = [
                            r'background-image:\surl\("([^"]+)"\)',
                            r'background-image:\surl\(([^)]+)\)',
                            r'background-image:\s*url\(\'([^\']+)\'\)'
                        ]
                        
                        for pattern in url_patterns:
                            match = re.search(pattern, style)
                            if match:
                                image_url = match.group(1)
                                image_data['broad_search_images'].append(image_url)
                                break
                                
                except Exception:
                    pass
                    
            except TimeoutException:
                pass
            
            # Create a consolidated list of all unique image URLs
            all_image_urls = set()
            
            if image_data['main_image_url']:
                all_image_urls.add(image_data['main_image_url'])
            
            all_image_urls.update(image_data['gallery_image_urls'])
            all_image_urls.update(image_data['thumbnail_urls'])
            all_image_urls.update([img['src'] for img in image_data['all_gallery_images'] if img['src']])
            all_image_urls.update(image_data['broad_search_images'])
            
            return jsonify({
                'success': True,
                'url': url,
                'image_data': image_data,
                'all_unique_image_urls': list(all_image_urls),
                'total_unique_images': len(all_image_urls)
            })
            
        finally:
            driver.quit()
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Auction scraper API is running'
    })

@app.route('/estimate', methods=['POST'])
def get_estimate():
    try:
        data = request.json
        if not data or 'url' not in data:
            return jsonify({'error': 'URL is required in request body'}), 400

        url = data['url']
        driver = create_driver()

        try:
            navigate_and_scroll(driver, url)

            estimate = "Not found"
            try:
                estimate_elem = driver.find_element(
                    By.XPATH,
                    "//th[contains(text(), 'Estimate')]/following-sibling::td"
                )
                estimate = estimate_elem.text.strip()
            except NoSuchElementException:
                pass

            return jsonify({'success': True, 'estimate': estimate, 'url': url})

        finally:
            driver.quit()
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/category', methods=['POST'])
def get_category():
    try:
        data = request.json
        if not data or 'url' not in data:
            return jsonify({'error': 'URL is required in request body'}), 400

        url = data['url']
        driver = create_driver()

        try:
            navigate_and_scroll(driver, url)

            category = "Not found"
            try:
                category_elem = driver.find_element(
                    By.XPATH,
                    "//th[contains(text(), 'Group - Category')]/following-sibling::td"
                )
                category = category_elem.text.strip()
            except NoSuchElementException:
                pass

            return jsonify({'success': True, 'category': category, 'url': url})

        finally:
            driver.quit()
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/item-name', methods=['POST'])
def get_item_name():
    try:
        data = request.json
        if not data or 'url' not in data:
            return jsonify({'error': 'URL is required in request body'}), 400

        url = data['url']
        driver = create_driver()

        try:
            navigate_and_scroll(driver, url)

            item_name = "Not found"
            try:
                name_elem = driver.find_element(
                    By.XPATH,
                    "//div[contains(@class, 'page-header')]/h1/span"
                )
                item_name = name_elem.text.strip()
            except NoSuchElementException:
                pass

            return jsonify({'success': True, 'item_name': item_name, 'url': url})

        finally:
            driver.quit()
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/lead', methods=['POST'])
def get_lead():
    try:
        data = request.json
        if not data or 'url' not in data:
            return jsonify({'error': 'URL is required in request body'}), 400

        url = data['url']
        driver = create_driver()

        try:
            navigate_and_scroll(driver, url)

            lead = "Not found"
            try:
                lead_elem = driver.find_element(
                    By.XPATH,
                    "//th[contains(text(), 'Lead')]/following-sibling::td"
                )
                lead = lead_elem.text.strip()
            except NoSuchElementException:
                pass

            return jsonify({'success': True, 'lead': lead, 'url': url})

        finally:
            driver.quit()
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    
@app.route('/auction-name', methods=['POST'])
def get_auction_name():
    """Endpoint to get only the Auction Name from the auction page"""
    try:
        data = request.json
        print(data)
        if not data or 'url' not in data:
            return jsonify({'error': 'URL is required in request body'}), 400

        url = data['url']
        print(url)
        driver = create_driver()

        try:
            navigate_and_scroll(driver, url)

            # Step 1: Click the "Auction Information" accordion
            try:
                print("[DEBUG] Clicking Auction Info panel...")
                auction_info_header = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//div[@role='button' and @aria-label='Auction Information']")
                    )
                )
                auction_info_header.click()
                time.sleep(1.5)  # Wait briefly for the panel to expand
            except Exception as e:
                print(f"[DEBUG] Failed to click auction info panel: {e}")

            # Step 2: Wait for the <td> next to "Name" to appear
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//th[normalize-space(text())='Name']/following-sibling::td")
                )
            )

            # Step 3: Extract the auction name
            try:
                auction_elem = driver.find_element(
                    By.XPATH, "//th[normalize-space(text())='Name']/following-sibling::td"
                )
                auction_name = driver.execute_script("return arguments[0].innerText;", auction_elem).strip()
                print("Auction Name:", auction_name)
            except NoSuchElementException:
                auction_name = "Not found"

            return jsonify({
                'success': True,
                'auction_name': auction_name,
                'url': url
            })

        finally:
            driver.quit()

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500





    
# @app.route('/auction-name', methods=['POST'])
# def get_auction_name():
#     """Endpoint to get only the Auction Name from the auction page"""
#     try:
#         data = request.json
#         print(data)
#         if not data or 'url' not in data:
#             return jsonify({'error': 'URL is required in request body'}), 400

#         url = data['url']
#         print(url)
#         driver = create_driver()

#         try:
#             navigate_and_scroll(driver, url)

#             # Wait for the "Name" row to be visible
#             WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located((By.XPATH, "//th[normalize-space(text())='Name']/following-sibling::td"))
#             )

#             # Now extract the auction name
#             try:
#                 print("About to search")
#                 auction_elem = driver.find_element(
#                     By.XPATH, "//th[normalize-space(text())='Name']/following-sibling::td"
#                 )

#                 print(auction_elem.text)

#                 auction_name = auction_elem.text.strip()
#                 print("Auction Name")
#                 print(auction_name)
#             except NoSuchElementException:
#                 auction_name = "Not found"

#             return jsonify({
#                 'success': True,
#                 'auction_name': auction_name,
#                 'url': url
#             })

#         finally:
#             driver.quit()

#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 500




@app.route('/description', methods=['POST'])
def get_description():
    """Endpoint to get the item description from auction page"""
    try:
        # Get URL from request
        data = request.json
        if not data or 'url' not in data:
            return jsonify({'error': 'URL is required in request body'}), 400

        url = data['url']

        # Initialize driver
        driver = create_driver()

        try:
            # Navigate and scroll
            navigate_and_scroll(driver, url)

            description = "Not found"
            try:
                desc_element = driver.find_element(
                    By.XPATH,
                    "//th[contains(text(), 'Description')]/following-sibling::td//div[contains(@class, 'text-pre-line')]"
                )
                description = desc_element.text.strip()
            except NoSuchElementException:
                pass

            return jsonify({
                'success': True,
                'description': description,
                'url': url
            })

        finally:
            driver.quit()

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/', methods=['GET'])
def home():
    """Home endpoint with API documentation"""
    return jsonify({
        'message': 'Auction Scraper API',
        'endpoints': {
            '/extract-all': {
                'method': 'POST',
                'description': 'Extract all data from auction page in one call',
                'body': {'url': 'auction_page_url'}
            },
            '/lot-number': {
                'method': 'POST',
                'description': 'Get lot number from auction page',
                'body': {'url': 'auction_page_url'}
            },
            '/images': {
                'method': 'POST', 
                'description': 'Get all image links from auction page',
                'body': {'url': 'auction_page_url'}
            },
            '/estimate': {
                'method': 'POST',
                'description': 'Get estimate from auction page',
                'body': {'url': 'auction_page_url'}
            },
            '/category': {
                'method': 'POST',
                'description': 'Get category from auction page',
                'body': {'url': 'auction_page_url'}
            },
            '/item-name': {
                'method': 'POST',
                'description': 'Get item name from auction page',
                'body': {'url': 'auction_page_url'}
            },
            '/lead': {
                'method': 'POST',
                'description': 'Get lead from auction page',
                'body': {'url': 'auction_page_url'}
            },
            '/description': {
                'method': 'POST',
                'description': 'Get description from auction page',
                'body': {'url': 'auction_page_url'}
            },
            '/health': {
                'method': 'GET',
                'description': 'Health check endpoint'
            }
        }
    })

# For Vercel deployment
app = app

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8000)
    args = parser.parse_args()
    
    app.run(debug=True, host='0.0.0.0', port=args.port)