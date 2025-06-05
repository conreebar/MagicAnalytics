import json
import ast

def process_match(match_text):
    """Process a single match string and return structured data."""
    # Parse the tuple string safely
    match_tuple = ast.literal_eval(match_text.strip())
    
    player_1, player_2, winner, match_record, round_info = match_tuple
    
    match_data = {
        "player_1": player_1,
        "player_2": player_2,
        "winner": winner,
        "match_record": match_record,
        "round": round_info
    }
    
    return match_data

def convert_matches_to_json(input_file, output_file):
    """Convert match file to JSON format."""
    with open(input_file, "r", encoding="utf-8") as file:
        match_texts = file.read().strip().split("\n")

    matches = [process_match(match) for match in match_texts if match.strip()]

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(matches, file, indent=4)

if __name__ == "__main__":
    # Replace with your actual file paths
    input_file = r"MagicAnalytics\data\matches_round1.txt"
    output_file = r"MagicAnalytics\data\matches_round1_json.json"
    
    convert_matches_to_json(input_file, output_file)
    print(f"Conversion complete! JSON saved to {output_file}")