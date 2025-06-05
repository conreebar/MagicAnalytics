import json
import os
import re

# Folder containing JSON files
json_folder = f"MagicAnalytics\data"
print("Files in directory:", os.listdir(json_folder))
merged_data = []

# Regex pattern to match files named deck_json_X.json where X is a number
pattern = re.compile(r"^deck_json_\d+\.(json|txt)$")  # Match both .json and .txt

# Read and merge all matching JSON files
for filename in os.listdir(json_folder):
    if pattern.match(filename):  # Check if filename matches pattern
        with open(os.path.join(json_folder, filename), "r", encoding="utf-8") as file:
            merged_data.extend(json.load(file))  # Assuming each file contains a list of decks

# Save the merged data to deck_json_all.json
output_file = os.path.join(json_folder, "deck_json_all.json")
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(merged_data, file, indent=4)

print(f"Merged JSON saved as {output_file}")
