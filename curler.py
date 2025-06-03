import requests

url = "https://www.melee.gg/Decklist/View/d4e03bbb-6958-4041-ae18-b2ed01605955"
response = requests.get(url)

if response.status_code == 200:
    with open("decklist.html", "w", encoding="utf-8") as file:
        file.write(response.text)
    print("HTML saved successfully!")
else:
    print(f"Failed to retrieve page. Status code: {response.status_code}")
