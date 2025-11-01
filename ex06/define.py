import sys
import requests
from bs4 import BeautifulSoup

def get_definition(word: str):
    url = f"https://www.oxfordlearnersdictionaries.com/definition/english/{word}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/115.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error: Unable to fetch definition for '{word}' (status code: {response.status_code})")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the first definition
    definition_tag = soup.find('span', class_='def')

    if not definition_tag:
        print(f"No definition found for '{word}'")
        return

    print(f"{definition_tag.text.strip()}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python oxford_dictionary.py <word>")
        sys.exit(1)

    word = sys.argv[1].lower()
    get_definition(word)
