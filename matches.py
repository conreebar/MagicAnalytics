from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
import time
import re

tournament_url = "https://www.melee.gg/Tournament/View/285048"
driver = webdriver.Chrome()
driver.get(tournament_url)
wait = WebDriverWait(driver, 15)

#While this sleeps, click the cookie button so that the code can click the site
time.sleep(4)

#clicking inside pairings
matches_container = wait.until(EC.presence_of_element_located((By.ID, "pairings")))
round1_button = matches_container.find_element(By.CSS_SELECTOR, 'button.round-selector[data-id="992474"]')

# Scroll and click
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", round1_button)
actions = ActionChains(driver)
actions.move_to_element(round1_button).click().perform()

#sleeep to load
time.sleep(3)

# Now fetch the pairings container and parse rows
results = []
try:
    print("Found pairings container")
except Exception as e:
    print(f"Error finding pairings container: {e}")
    driver.quit()
    exit()

while True:
    print(f"Scraping next page...")
    
    pairings_container = wait.until(EC.presence_of_element_located((By.ID, "tournament-pairings-table")))
    match_rows = pairings_container.find_elements(By.CSS_SELECTOR, 'tr[role="row"]')[1:]  # Skip header
    for row in match_rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) < 4:
            continue  # skip malformed rows

        # Get player names
        player_links = cells[1].find_elements(By.TAG_NAME, "a")
        if len(player_links) != 2:
            continue  # skip unexpected structure

        player1 = player_links[0].text.strip()
        player2 = player_links[1].text.strip()

        # Get winner by checking if player2's name appears in the result
        result_text = cells[3].text.strip().lower()
        if player1.lower() in result_text:
            winner = 1
        elif player2.lower() in result_text:
            winner = 2
        else:
            winner = 0  # draw or unknown
        #record
        result_text = cells[3].text.strip()
        match = re.search(r'\b\d+-\d+-\d+\b', result_text)
        record = match.group(0) if match else ""

        if player1 == '𝕲𝖆𝖌𝖊 𝕬𝖑𝖇':
            player1 = 'Gage Ulb'
        if player2 == '𝕲𝖆𝖌𝖊 𝕬𝖑𝖇':
            player2 = 'Gage Ulb'
        if player1 == 'Kezia ⛏🐛':
            player1 = 'Kezia'
        if player2 == 'Kezia ⛏🐛':
            player2 = 'Kezia'

        results.append((player1, player2, winner, record, "Round 15"))
    
    print(f"Found {len(match_rows)} matches on page")
    
    # Try to find and click next button that's not disabled
    try:
        # Look for the next button only inside the "pairings" container
        matches_container = wait.until(EC.presence_of_element_located((By.ID, "pairings")))
        next_button = matches_container.find_element(By.CSS_SELECTOR, 'a.paginate_button.next:not(.disabled)')

        # Scroll and click
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_button)
        driver.execute_script("arguments[0].click();", next_button)
        time.sleep(3)  # Allow table to update
    except:
        print("Next button is disabled or not found — reached last page")
        break

print(len(results))

# Print all results
for r in results:
    print(r)

driver.quit()
