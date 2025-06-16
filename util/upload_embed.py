import redis
import json
import os
redis_client = redis.Redis(
    host="redis-13923.c259.us-central1-2.gce.redns.redis-cloud.com",
    port=13923,
    password="CThmL0km9GiObms9OSfZmRSFv3pHS3Fr",
    decode_responses=True
)

json_folder = "MagicAnalytics\\data"

with open(os.path.join(json_folder, "compiled_decks.json"), "r", encoding="utf-8") as file:
    embed_data = json.load(file)
    redis_client.json().set("embeddings", "$", embed_data)

embeddings = redis_client.json().get("embeddings")
print(len(embeddings))