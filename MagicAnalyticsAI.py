import json
import numpy as np
from sentence_transformers import SentenceTransformer, util
import openai
import torch
from collections import Counter

# Initialize OpenAI client
openai_client = openai.OpenAI(api_key = "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")

# Load stored deck embeddings with full data
with open(f"MagicAnalytics\data\compiled_decks_full.json", "r") as file:
    deck_data = json.load(file)

# Initialize embedding model for search queries
model = SentenceTransformer('all-mpnet-base-v2')

def get_embedding(text, model="text-embedding-ada-002"):
    response = openai_client.embeddings.create(
        input=[text],
        model=model
    )
    return response.data[0].embedding

def find_similar_decks(search_term, top_k=5):
    search_embedding = get_embedding(search_term)
    search_embedding = torch.tensor(search_embedding, dtype=torch.float32)
    
    similar_decks = []
    
    for deck in deck_data:
        deck_embedding = np.array(deck["embedding"])
        deck_embedding = torch.tensor(deck_embedding, dtype=torch.float32)
        
        similarity = util.cos_sim(search_embedding, deck_embedding).item()
        
        deck_info = {
            "archetype": deck["archetype"],
            "player_name": deck["player_name"],
            "rank": deck["rank"],
            "record": deck["record"],
            "maindeck": deck["maindeck"],
            "sideboard": deck["sideboard"],
            "deck_text": deck["deck_text"],
            "similarity": similarity
        }
        
        similar_decks.append(deck_info)
    
    # Sort by highest similarity
    return sorted(similar_decks, key=lambda x: x["similarity"], reverse=True)[:top_k]

def analyze_card_frequencies(decks):
    """Analyze card frequencies across similar decks"""
    maindeck_cards = Counter()
    sideboard_cards = Counter()
    
    for deck in decks:
        for card in deck["maindeck"]:
            maindeck_cards[card["name"]] += card["count"]
        for card in deck["sideboard"]:
            sideboard_cards[card["name"]] += card["count"]
    
    return maindeck_cards, sideboard_cards

def generate_optimal_decklist(search_term, top_decks):
    """Generate an optimal decklist based on similar decks"""
    
    # Analyze card frequencies
    maindeck_freq, sideboard_freq = analyze_card_frequencies(top_decks)
    
    # Format deck data for the prompt
    deck_analyses = []
    for i, deck in enumerate(top_decks, 1):
        deck_analysis = f"""
        Deck {i}: {deck['archetype']} by {deck['player_name']} (Rank {deck['rank']}, Record {deck['record']})
        Similarity Score: {deck['similarity']:.4f}
        
        Maindeck:
        {chr(10).join([f"{card['count']}x {card['name']}" for card in deck['maindeck']])}
        
        Sideboard:
        {chr(10).join([f"{card['count']}x {card['name']}" for card in deck['sideboard']])}
        """
        deck_analyses.append(deck_analysis)
    
    # Create comprehensive prompt
    prompt = f"""You are an expert Magic: The Gathering deck builder. Based on the following high-performing deck data, create an optimal decklist for: "{search_term}"

REFERENCE DECKS:
{''.join(deck_analyses)}

CARD FREQUENCY ANALYSIS:
Most common maindeck cards across these decks:
{chr(10).join([f"{name}: {count} total copies" for name, count in maindeck_freq.most_common(15)])}

Most common sideboard cards:
{chr(10).join([f"{name}: {count} total copies" for name, count in sideboard_freq.most_common(10)])}

INSTRUCTIONS:
1. Analyze the successful elements across these decks
2. Create an optimized 60-card maindeck and 15-card sideboard
3. Explain your card choices and synergies
4. Suggest any improvements or meta adaptations
5. Format the decklist clearly with card counts

Focus on creating a competitive, cohesive deck that learns from the best-performing examples while optimizing for the current meta."""

    response = openai_client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=2000
    )
    
    return response.choices[0].message.content

# Example usage
search_term = "Optimal Gruul Broodscale strategies"

print(f"Searching for: {search_term}")
print("="*50)

# Find similar decks
top_decks = find_similar_decks(search_term, top_k=5)

print("Top Similar Decks:")
for i, deck in enumerate(top_decks, 1):
    print(f"{i}. {deck['archetype']} by {deck['player_name']} (Rank {deck['rank']}) - Similarity: {deck['similarity']:.4f}")

print("\n" + "="*50)
print("GENERATING OPTIMAL DECKLIST...")
print("="*50)

# Generate optimal decklist
optimal_decklist = generate_optimal_decklist(search_term, top_decks)
print(optimal_decklist)