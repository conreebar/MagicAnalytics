from collections import defaultdict
import redis

redis_client = redis.Redis(
    host="redis-13923.c259.us-central1-2.gce.redns.redis-cloud.com",
    port=13923,
    password="CThmL0km9GiObms9OSfZmRSFv3pHS3Fr",
    decode_responses=True
)
from collections import defaultdict

# Fetch matches and decks
matches = redis_client.json().get("matches")
decks = redis_client.json().get("decks")

# Track card win counts
card_usage = defaultdict(lambda: {"games": 0, "wins": 0})

# Iterate through matches
for match in matches:
    if match["winner"] == 0:  # Ignore ties
        continue

    winner = f"player_{match['winner']}"  # Either 'player_1' or 'player_2'
    winner_name = match[winner]

    # Find decks for both players
    for player_key in ["player_1", "player_2"]:
        player_name = match[player_key]
        player_deck = next((d for d in decks if d["player_name"] == player_name), None)

        if player_deck:
            for card in player_deck["maindeck"]:
                card_name = card["name"]
                card_usage[card_name]["games"] += 1  # Count how many games it appeared in
                if player_name == winner_name:
                    card_usage[card_name]["wins"] += 1  # Count wins

# Compute winrates
winrate_data = {card: (data["wins"] / data["games"] * 100) for card, data in card_usage.items() if data["games"] > 0}

# Find highest winrate card
highest_winrate_card = max(winrate_data, key=winrate_data.get)
highest_winrate = winrate_data[highest_winrate_card]

print(f"Highest maindeck winrate card: {highest_winrate_card} ({highest_winrate:.2f}% winrate)")


# Track usage of 'cardnamee'
card_name = "Basking Broodscale"
card_stats = {"games": 0, "wins": 0}

# Iterate through matches, excluding ties
for match in matches:
    if match["winner"] == 0:  # Ignore ties
        continue

    winner = f"player_{match['winner']}"  # Either 'player_1' or 'player_2'
    winner_name = match[winner]

    # Find decks for both players
    for player_key in ["player_1", "player_2"]:
        player_name = match[player_key]
        player_deck = next((d for d in decks if d["player_name"] == player_name), None)

        if player_deck:
            # Check if 'Consign to Memory' is in the maindeck or sideboard
            if any(card["name"] == card_name for card in player_deck["maindeck"] + player_deck["sideboard"]):
                card_stats["games"] += 1  # Count how many games this card appeared in
                if player_name == winner_name:
                    card_stats["wins"] += 1  # Count wins

# Compute winrate
winrate = (card_stats["wins"] / card_stats["games"] * 100) if card_stats["games"] > 0 else 0

print(f"Winrate for '{card_name}': {winrate:.2f}%")

# Fetch matches and decks
matches = redis_client.json().get("matches")
decks = redis_client.json().get("decks")

# Track win rates of sideboard cards
sideboard_stats = defaultdict(lambda: {"games": 0, "wins": 0})

# Iterate through matches, excluding ties
for match in matches:
    if match["winner"] == 0:  # Ignore ties
        continue

    winner = f"player_{match['winner']}"  # Either 'player_1' or 'player_2'
    winner_name = match[winner]

    # Process both players in each match
    for player_key in ["player_1", "player_2"]:
        player_name = match[player_key]
        player_deck = next((d for d in decks if d["player_name"] == player_name), None)

        if player_deck:
            for card in player_deck["sideboard"]:
                card_name = card["name"]
                sideboard_stats[card_name]["games"] += 1
                if player_name == winner_name:
                    sideboard_stats[card_name]["wins"] += 1

# Compute winrate for each sideboard card
winrate_data = {card: (data["wins"] / data["games"] * 100) for card, data in sideboard_stats.items() if data["games"] > 0}

# Find highest impact sideboard card
top_sideboard_card = max(winrate_data, key=winrate_data.get)
top_sideboard_winrate = winrate_data[top_sideboard_card]

print(f"Most impactful sideboard card: {top_sideboard_card} ({top_sideboard_winrate:.2f}% winrate)")



decks = redis_client.json().get("decks")
card_name = "Change the Equation" #change this 
matching_decks = [
    deck["deck_link"]
    for deck in decks
    if any(card["name"] == card_name for card in deck["maindeck"] + deck["sideboard"])
]

print(f"Decks containing '{card_name}':")
print("\n".join(matching_decks))

####

matches = redis_client.json().get("matches")
decks = redis_client.json().get("decks")

# Find players using each archetype
archetype1 = "Gruul Broodscale"
archetype2 = "Domain Zoo"

archetype1_players = {deck["player_name"] for deck in decks if deck["archetype"] == archetype1}
archetype2_players = {deck["player_name"] for deck in decks if deck["archetype"] == archetype2}

# Track wins and total matches
archetype1_stats = {"games": 0, "wins": 0}
archetype2_stats = {"games": 0, "wins": 0}

for match in matches:
    if match["winner"] == 0:  # Ignore ties
        continue

    player1 = match["player_1"]
    player2 = match["player_2"]
    winner = match[f"player_{match['winner']}"]

    # Check if both archetypes are present in the match
    if player1 in archetype1_players and player2 in archetype2_players:
        archetype1_stats["games"] += 1
        archetype2_stats["games"] += 1
        if winner == player1:
            archetype1_stats["wins"] += 1
        else:
            archetype2_stats["wins"] += 1

    elif player1 in archetype2_players and player2 in archetype1_players:
        archetype1_stats["games"] += 1
        archetype2_stats["games"] += 1
        if winner == player1:
            archetype2_stats["wins"] += 1
        else:
            archetype1_stats["wins"] += 1

# Compute winrates
archetype1_winrate = (archetype1_stats["wins"] / archetype1_stats["games"] * 100) if archetype1_stats["games"] > 0 else 0
archetype2_winrate = (archetype2_stats["wins"] / archetype2_stats["games"] * 100) if archetype2_stats["games"] > 0 else 0

print(f"{archetype1} winrate vs {archetype2}: {archetype1_winrate:.2f}%")
print(f"{archetype2} winrate vs {archetype1}: {archetype2_winrate:.2f}%")


###

    
decks = redis_client.json().get("decks")
card_name = "Basking Broodscale" #Phelia, Exuberant Shepherd
matching_archetypes = {
    deck["archetype"]
    for deck in decks
    if any(card["name"] == card_name for card in deck["maindeck"] + deck["sideboard"])
}

print(f"Archetypes containing '{card_name}':")
print("\n".join(matching_archetypes))


####

decks = redis_client.json().get("decks")
archetype_to_search = "Gruuln Broodscale"
matching_decks = [
    deck["deck_link"]
    for deck in decks
    if deck["archetype"] == archetype_to_search
]

print(f"Decks for '{archetype_to_search}':")
print("\n".join(matching_decks))

#### Reid's question
archetype = "Esper Reanimator"
opponent_archetypes = ["Amulet Titan", "Boros Energy"]
exclude_player = "Andrew Bailey"


matches = redis_client.json().get("matches")
decks = redis_client.json().get("decks")

# Find players using each archetype
archetype_players = {deck["player_name"] for deck in decks if deck["archetype"] == archetype}
opponent_players = {deck["player_name"] for deck in decks if deck["archetype"] in opponent_archetypes}

# Track win/loss data
stats = {opponent: {"games": 0, "wins": 0} for opponent in opponent_archetypes}

for match in matches:
    if match["winner"] == 0:  # Ignore ties
        continue

    player1 = match["player_1"]
    player2 = match["player_2"]
    winner = match[f"player_{match['winner']}"]

    # Skip matches involving excluded player
    if exclude_player in [player1, player2]:
        continue

    # Determine if match involves Esper Reanimator vs Amulet Titan or Boros Energy
    if player1 in archetype_players and player2 in opponent_players:
        stats[next(deck["archetype"] for deck in decks if deck["player_name"] == player2)]["games"] += 1
        if winner == player1:
            stats[next(deck["archetype"] for deck in decks if deck["player_name"] == player2)]["wins"] += 1

    elif player2 in archetype_players and player1 in opponent_players:
        stats[next(deck["archetype"] for deck in decks if deck["player_name"] == player1)]["games"] += 1
        if winner == player2:
            stats[next(deck["archetype"] for deck in decks if deck["player_name"] == player1)]["wins"] += 1

# Compute winrate per archetype
for opponent in opponent_archetypes:
    winrate = (stats[opponent]["wins"] / stats[opponent]["games"] * 100) if stats[opponent]["games"] > 0 else 0
    print(f"Esper Reanimator vs {opponent}: {winrate:.2f}% winrate")


## get one archetype
matches = redis_client.json().get("matches")
decks = redis_client.json().get("decks")

archetype = "Boros Energy" # Change this to see a different archetype winrate
archetype_players = {deck["player_name"] for deck in decks if deck["archetype"] == archetype}
archetype_stats = {"games": 0, "wins": 0}

for match in matches:
    if match["winner"] == 0:  # Ignore ties
        continue

    player1 = match["player_1"]
    player2 = match["player_2"]
    winner = match[f"player_{match['winner']}"]

    if player1 in archetype_players or player2 in archetype_players:
        archetype_stats["games"] += 1
        if winner in archetype_players:
            archetype_stats["wins"] += 1

# Compute winrate
winrate = (archetype_stats["wins"] / archetype_stats["games"] * 100) if archetype_stats["games"] > 0 else 0

print(f"{archetype} winrate: {winrate:.2f}%")