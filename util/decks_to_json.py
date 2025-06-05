import json
import re

def process_deck(deck_text):
    """Process a single deck text block and return structured data."""
    lines = deck_text.strip().split('\n')
    
    # Initialize deck data
    deck_data = {
        "deck_link": "",
        "player_name": "",
        "archetype": "",
        "rank": "",
        "record": "",
        "points": "",
        "maindeck": [],
        "sideboard": []
    }
    
    # Extract deck link
    if lines[0].startswith("DECK: "):
        deck_data["deck_link"] = lines[0].replace("DECK: ", "")
    
    # Extract player info and metadata
    for line in lines[1:]:
        if line.startswith("Player: "):
            player_name = line.replace("Player: ", "")
            # Handle "Lastname, Firstname" format
            if ", " in player_name:
                lastname, firstname = player_name.split(", ", 1)
                deck_data["player_name"] = f"{firstname} {lastname}"
            else:
                deck_data["player_name"] = player_name
        
        elif line.startswith("Archetype:"):
            deck_data["archetype"] = line.replace("Archetype:", "")
        
        elif line.startswith("Rank: "):
            # Parse "Rank: 372 | Record: 3-0-4 | Points: 9"
            parts = line.replace("Rank: ", "").split(" | ")
            deck_data["rank"] = parts[0]
            if len(parts) > 1:
                deck_data["record"] = parts[1].replace("Record: ", "")
            if len(parts) > 2:
                deck_data["points"] = parts[2].replace("Points: ", "")
    
    # Extract cards
    for line in lines:
        # Skip metadata lines
        if (line.startswith("DECK: ") or 
            line.startswith("Player: ") or 
            line.startswith("Archetype:") or 
            line.startswith("Rank: ") or
            line.strip() == ""):
            continue
        
        # Parse card lines (format: "4 Card Name (Type)")
        card_match = re.match(r'^(\d+)\s+(.+?)\s+\((.+?)\)(?:\s+\(Sideboard\))?$', line)
        if card_match:
            count = int(card_match.group(1))
            card_name = card_match.group(2)
            card_type = card_match.group(3)
            
            card_entry = {
                "count": count,
                "name": card_name,
                "type": card_type
            }
            
            # Check if it's a sideboard card
            if "(Sideboard)" in line:
                deck_data["sideboard"].append(card_entry)
            else:
                deck_data["maindeck"].append(card_entry)
    
    return deck_data

def convert_decks_to_json(input_file, output_file):
    """Convert deck file to JSON format."""
    with open(input_file, "r", encoding="utf-8") as file:
        deck_texts = file.read().strip().split("\n---\n")

    decks = [process_deck(deck) for deck in deck_texts]

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(decks, file, indent=4)

# Example usage
if __name__ == "__main__":
    # Replace with your actual file paths
    input_file = r"MagicAnalytics\data\all_decks_7.txt"
    output_file = r"MagicAnalytics\data\deck_json_7.txt"
    
    convert_decks_to_json(input_file, output_file)
    print(f"Conversion complete! JSON saved to {output_file}")

# Example of what the JSON output will look like:
example_output = {
    "deck_link": "https://www.melee.gg/Decklist/View/ff89d34b-cbd5-43fd-a9c5-b2ed006c0ed5",
    "player_name": "Sean Soper",
    "archetype": "Domain Zoo",
    "rank": "372",
    "record": "3-0-4",
    "points": "9",
    "maindeck": [
        {"count": 4, "name": "Phlage, Titan of Fire's Fury", "type": "Creature"},
        {"count": 4, "name": "Ragavan, Nimble Pilferer", "type": "Creature"},
        {"count": 4, "name": "Scion of Draco", "type": "Creature"},
        {"count": 4, "name": "Territorial Kavu", "type": "Creature"},
        {"count": 3, "name": "Tribal Flames", "type": "Sorcery"},
        {"count": 3, "name": "Lightning Bolt", "type": "Instant"},
        {"count": 2, "name": "Consign to Memory", "type": "Instant"},
        {"count": 2, "name": "Stubborn Denial", "type": "Instant"},
        {"count": 4, "name": "Leyline Binding", "type": "Enchantment"},
        {"count": 4, "name": "Leyline of the Guildpact", "type": "Enchantment"},
        {"count": 3, "name": "Fable of the Mirror-Breaker // Reflection of Kiki-Jiki", "type": "Enchantment"},
        {"count": 4, "name": "Arid Mesa", "type": "Land"},
        {"count": 4, "name": "Flooded Strand", "type": "Land"},
        {"count": 4, "name": "Wooded Foothills", "type": "Land"},
        {"count": 2, "name": "Arena of Glory", "type": "Land"},
        {"count": 1, "name": "Godless Shrine", "type": "Land"},
        {"count": 1, "name": "Indatha Triome", "type": "Land"},
        {"count": 1, "name": "Lush Portico", "type": "Land"},
        {"count": 1, "name": "Mountain", "type": "Land"},
        {"count": 1, "name": "Plains", "type": "Land"},
        {"count": 1, "name": "Sacred Foundry", "type": "Land"},
        {"count": 1, "name": "Steam Vents", "type": "Land"},
        {"count": 1, "name": "Temple Garden", "type": "Land"},
        {"count": 1, "name": "Thundering Falls", "type": "Land"}
    ],
    "sideboard": [
        {"count": 3, "name": "Wrath of the Skies", "type": "Sideboard"},
        {"count": 2, "name": "Consign to Memory", "type": "Sideboard"},
        {"count": 2, "name": "Mystical Dispute", "type": "Sideboard"},
        {"count": 2, "name": "Nihil Spellbomb", "type": "Sideboard"},
        {"count": 2, "name": "Wear // Tear", "type": "Sideboard"},
        {"count": 1, "name": "Clarion Conqueror", "type": "Sideboard"},
        {"count": 1, "name": "High Noon", "type": "Sideboard"},
        {"count": 1, "name": "Scavenging Ooze", "type": "Sideboard"},
        {"count": 1, "name": "Torpor Orb", "type": "Sideboard"}
    ]
}