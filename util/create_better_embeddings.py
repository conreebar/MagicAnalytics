import openai
import json

# Initialize OpenAI client
openai_client = openai.OpenAI(api_key = "key")  # Create client

def get_embedding(text, model="text-embedding-ada-002"):
    response = openai_client.embeddings.create(
        input=[text],  # Must be a list
        model=model
    )
    return response.data[0].embedding

# Load JSON file
with open(f"MagicAnalytics\data\deck_json_all.json", "r") as file:
    data = json.load(file)  # Assuming the file contains a list of JSON objects

# Iterate through the list
compiled_data = []
count = 0

# Process each deck
for deck in data:
    deck_text = f"{deck['archetype']} deck by {deck['player_name']} (Rank {deck['rank']}, Record {deck['record']})\n"
    
    deck_text += "\nMainboard:\n"
    deck_text += "\n".join([f"{card['count']}x {card['name']} ({card['type']})" for card in deck["maindeck"]])
    
    deck_text += "\n\nSideboard:\n"
    deck_text += "\n".join([f"{card['count']}x {card['name']} ({card['type']})" for card in deck["sideboard"]])
    
    print(f"Processing deck {count + 1}: {deck['archetype']}")
    
    embedding = get_embedding(deck_text)
    
    # Store FULL deck data including the actual card lists
    compiled_data.append({
        "id": count,
        "archetype": deck["archetype"],
        "player_name": deck["player_name"],
        "rank": deck["rank"],
        "record": deck["record"],
        "maindeck": deck["maindeck"],  # Store actual maindeck
        "sideboard": deck["sideboard"],  # Store actual sideboard
        "deck_text": deck_text,  # Store formatted text for easy reading
        "embedding": embedding  # Store the embedding vector
    })

    count += 1

# Save enhanced data
with open("compiled_decks_full.json", "w") as file:
    json.dump(compiled_data, file, indent=4)

print("Enhanced JSON file with full deck data saved successfully!")