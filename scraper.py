from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Replace with your tournament URL
tournament_url = "https://www.melee.gg/Tournament/View/285048"

driver = webdriver.Chrome()
driver.get(tournament_url)

all_deck_urls = []
page = 1

while True:
    print(f"Scraping page {page}...")
    
    # Wait for deck links to load on current page
    wait = WebDriverWait(driver, 15)
    elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[data-type="decklist"][href*="/Decklist/View/"]')))
    
    # Get deck URLs from current page
    page_urls = []
    for element in elements:
        href = element.get_attribute('href')
        if href.startswith('/'):
            url = 'https://mtgmelee.com' + href
        else:
            url = href
        
        if url not in all_deck_urls:  # Avoid duplicates
            all_deck_urls.append(url)
            page_urls.append(url)
    
    print(f"Found {len(page_urls)} new deck URLs on page {page}")
    
    # Try to find and click next button that's not disabled
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, 'a.paginate_button.next:not(.disabled)')
        if next_button:
            driver.execute_script("arguments[0].click();", next_button)
            time.sleep(3)  # Wait for page to load
            page += 1
        else:
            print("Next button is disabled - reached last page")
            break
    except:
        print("No active next button found - reached last page")
        break

driver.quit()

# Write all URLs to file
with open('all_deck_urls.txt', 'w') as f:
    for url in all_deck_urls:
        f.write(url + '\n')

print(f"Found {len(all_deck_urls)} total unique deck URLs across {page} pages and saved to all_deck_urls.txt")