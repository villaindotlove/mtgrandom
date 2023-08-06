from graphics_utils import render_full_card
from content_utils.card_gen_tools import *

# TODO Turn these into command line parameters
set_name = "default"
set_description = "Comedy set about San Francisco"
card_names_file = "card_names.txt"
# Download this file from here: https://mtgjson.com/downloads/all-files/
atomic_cards_file = "/home/keenan/Downloads/AtomicCards.json"

def generated_cards_json():
    all_cards = return_all_cards(atomic_cards_file)
    if card_names_file is not None:
        new_card_names = load_card_names(f"../sets/{set_name}/{card_names_file}")
    else:
        raise Exception("No card names file specified")
    # Randomize order of new_card_names to make it more interesting
    random.shuffle(new_card_names)
    with open(f"../sets/{set_name}/cards.jsonl", "a") as f:
        for card_name in new_card_names:
            card = random.choice(all_cards)
            generated = generate_card(card, {"name": card_name})
            print(generated)
            generated_dict = generate_dict_given_text(generated)

            # Append the card to cards.jsonl
            f.write(json.dumps(generated_dict) + "\n")

def generated_cards_images():
    # Load cards from cards.jsonl
    with open(f"../sets/{set_name}/cards.jsonl", "r") as f:
        cards = [json.loads(line) for line in f.readlines()]
        for card in cards:
            # Generate image
            flavor = card['flavor'] if 'flavor' in card else (
                card['text'] if 'text' in card else "")
            # image_url = dalle.generate_image_and_return_url(f"{generated_dict['name']}, Magic the Gathering Art, Beautiful, Fantasy, Spec Art")
            image_path = f"sets/{set_name}/images/{card['name']}.png"
            dalle.generate_image_and_save_to_file(
                f"{card['name']}, Magic the Gathering Art, Beautiful, Fantasy, Spec Art. {flavor}", image_path)
            # print(image_url)
            # generated_dict['image_url'] = image_url

def generate_full_card_images():
    # Load cards from cards.jsonl
    with open(f"../sets/{set_name}/cards.jsonl", "r") as f:
        cards = [json.loads(line) for line in f.readlines()]
        for card in cards:
            image_path = f"sets/{set_name}/images/{card['name']}.png"
            card['image_path'] = image_path
            print(card)
            print("-" * 80)

            # Render the card
            render_full_card.create_magic_card(card)

if __name__ == '__main__':
    generated_cards_json()

