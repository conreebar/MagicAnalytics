import redis

redis_client = redis.Redis(
    host="redis-13923.c259.us-central1-2.gce.redns.redis-cloud.com",
    port=13923,
    password="CThmL0km9GiObms9OSfZmRSFv3pHS3Fr",
    decode_responses=True
)
import json
import os

json_folder = "MagicAnalytics\\data"

# Upload deck JSON
with open(os.path.join(json_folder, "deck_json_all.json"), "r", encoding="utf-8") as file:
    deck_data = json.load(file)
    redis_client.json().set("decks", "$", deck_data)

# Upload match JSON
with open(os.path.join(json_folder, "matches_round_all.json"), "r", encoding="utf-8") as file:
    match_data = json.load(file)
    redis_client.json().set("matches", "$", match_data)

print("Decks and matches successfully uploaded to Redis!")

decks = redis_client.json().get("decks")
matches = redis_client.json().get("matches")

print(f"Total decks uploaded: {len(decks)}")
print(f"Total matches uploaded: {len(matches)}")
