import json
import os
import re

# Folder containing match JSON files
json_folder = "MagicAnalytics\\data"

merged_matches = []

# Regex pattern to match files named matches_roundX_json.json where X is a number
pattern = re.compile(r"^matches_round\d+_json\.json$")

# Read and merge all matching JSON files
for filename in os.listdir(json_folder):
    if pattern.match(filename):  # Check if filename matches pattern
        with open(os.path.join(json_folder, filename), "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                merged_matches.extend(data)  # If it's a list, extend
            else:
                merged_matches.append(data)  # If it's a single object, append

# Save the merged data to matches_round_all.json
output_file = os.path.join(json_folder, "matches_round_all.json")
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(merged_matches, file, indent=4)

print(f"Merged match JSON saved as {output_file}")
