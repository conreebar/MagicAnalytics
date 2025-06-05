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

print(f"Highest winrate card: {highest_winrate_card} ({highest_winrate:.2f}% winrate)")


# Track usage of 'Consign to Memory'
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