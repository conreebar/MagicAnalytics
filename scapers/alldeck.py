from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

def scrape_deck(deck_url):
    driver = webdriver.Chrome()
    driver.get(deck_url)
    
    # Wait for deck to load
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.decklist-category')))
    
    deck_data = []
    deck_info = {}
    
    # Get player stats (rank, record, points)
    deck_info = {'rank': 'N/A', 'record': 'N/A', 'points': 'N/A'} #doesnt work unless i do this lol idk it's 1:30 am
    try:
        stats_div = driver.find_element(By.CSS_SELECTOR, '.d-flex.flex-row.flex-gap-1.mb-3')
        spans = stats_div.find_elements(By.CSS_SELECTOR, 'span .text-muted')
        if len(spans) >= 3:
            deck_info['rank'] = spans[0].text.strip()
            deck_info['record'] = spans[1].text.strip()
            deck_info['points'] = spans[2].text.strip()
    except:
        deck_info = {'rank': 'N/A', 'record': 'N/A', 'points': 'N/A'}

    # Get deck owner
    try:
        owner_element = driver.find_element(By.CSS_SELECTOR, 'a.text-nowrap.text-muted span.text-nowrap')
        deck_info['owner'] = owner_element.text.strip()
    except:
        deck_info['owner'] = 'N/A'

    # Get deck archetype (title)
    try:
        title_element = driver.find_element(By.CSS_SELECTOR, '.decklist-title')
        deck_info['archetype'] = title_element.text.strip()
    except:
        deck_info['archetype'] = 'N/A'

    
    # Find all categories (Land, Creature, etc.)
    categories = driver.find_elements(By.CSS_SELECTOR, '.decklist-category')
    
    for category in categories:
        # Get category name and clean it up
        title_element = category.find_element(By.CSS_SELECTOR, '.decklist-category-title')
        category_name = title_element.text.strip()
        
        # Extract just the category type (remove the total category count in parentheses)
        if '(' in category_name:
            category_name = category_name.split('(')[0].strip()
        
        # Get all cards in this category
        cards = category.find_elements(By.CSS_SELECTOR, '.decklist-record')
        
        for card in cards:
            quantity = card.find_element(By.CSS_SELECTOR, '.decklist-record-quantity').text.strip()
            card_name = card.find_element(By.CSS_SELECTOR, '.decklist-record-name').text.strip()
            
            deck_data.append({
                'cardName': card_name,
                'cardNumber': quantity,
                'cardType': category_name
            })
    
    driver.quit()
    return deck_data, deck_info

# Read deck URLs from file
with open('all_deck_urls.txt', 'r') as f:
    deck_urls = [line.strip() for line in f.readlines()]

all_decks = []

# Scrape each deck

for i, url in enumerate(deck_urls[681:682]):
    print(f"Scraping deck {i+1}/{len(deck_urls)}: {url}")
    deck_data, deck_info = scrape_deck(url)  # Ensure both values are unpacked
    all_decks.append({
        'url': url,
        'cards': deck_data,
        'info': deck_info
    })
    #time.sleep(1)  # Optional: sleep to not overload server


# Write to file
with open('all_decks_7.txt', 'w') as f:
    for deck in all_decks:
        f.write(f"DECK: {deck['url']}\n")

        #check for bad user
        # TODO: fix this in a universal way and not a case by case
        if deck['info']['owner'] == '𝕬𝖑𝖇, 𝕲𝖆𝖌𝖊':
            deck['info']['owner'] = 'Ulb, Gage'
        if deck['info']['owner'] == '⛏🐛, Kezia':
            deck['info']['owner'] = 'Kezia'
        
        f.write(f"Player: {deck['info']['owner']}\n")
        f.write(f"Archetype:{deck['info']['archetype']}\n")
        f.write(f"Rank: {deck['info']['rank']} | Record: {deck['info']['record']} | Points: {deck['info']['points']}\n")
        for card in deck['cards']:
            f.write(f"{card['cardNumber']} {card['cardName']} ({card['cardType']})\n")
        f.write("\n---\n\n")

print(f"Scraping complete")