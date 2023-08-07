import os

from graphics_utils import render_full_card
from content_utils.card_gen_tools import *

# TODO Turn these into command line parameters
set_name = "testing"
set_description = "Cool fantasy world but with funny animals"
card_names_file = None # "card_names.txt"
# Download this file from here: https://mtgjson.com/downloads/all-files/
atomic_cards_file = "/home/keenan/Downloads/AtomicCards.json"
number_of_cards_to_generate = 3

# TODO Flags needed
llm_model = "gpt-3.5-turbo"
graphics_model = "dalle"

def generated_cards_json():
    all_cards = return_all_cards(atomic_cards_file)
    # Create folders if they don't exist
    os.makedirs(f"sets/{set_name}", exist_ok=True)
    if card_names_file is not None:
        new_card_names = load_card_names(f"sets/{set_name}/{card_names_file}")
    else:
        adjectives = ["Cute", "Funny", "Silly", "Goofy", "Weird", "Strange", "Bizarre", "Unusual", "Quirky", "Odd", "Angry"]
        creatures = ["Badger", "Peacock", "Wizard", "Barbarian", "Emu", "Penguin", "Panda", "Wallaby", "Koala", "Kangaroo", "Dingo", "Dinosaur", "Dragon", "Unicorn", "Pegasus", "Griffin", "Phoenix", "Gryphon", "Goblin", "Orc", "Troll", "Ogre", "Elf", "Fairy", "Mermaid", "Centaur", "Minotaur", "Satyr", "Giant", "Gnome", "Golem", "Gargoyle", "Demon", "Angel", "Vampire", "Werewolf", "Zombie", "Skeleton", "Ghost", "Specter"]
        # TODO Use the LLM to generate these names
        new_card_names = [f"{random.choice(adjectives)} {random.choice(creatures)}" for _ in range(number_of_cards_to_generate)]
    # Randomize order of new_card_names to make it more interesting
    random.shuffle(new_card_names)
    with open(f"sets/{set_name}/cards.jsonl", "a") as f:
        for card_name in new_card_names:
            card = random.choice(all_cards)
            generated = generate_card(card, {"name": card_name})
            print(generated)
            generated_dict = generate_dict_given_text(generated)

            # Append the card to cards.jsonl
            f.write(json.dumps(generated_dict) + "\n")

def generated_cards_images():
    os.makedirs(f"sets/{set_name}/images", exist_ok=True)
    # Load cards from cards.jsonl
    with open(f"sets/{set_name}/cards.jsonl", "r") as f:
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
    os.makedirs(f"sets/{set_name}/cards", exist_ok=True)
    # Load cards from cards.jsonl
    with open(f"sets/{set_name}/cards.jsonl", "r") as f:
        cards = [json.loads(line) for line in f.readlines()]
        for card in cards:
            image_path = f"sets/{set_name}/images/{card['name']}.png"
            card['image_path'] = image_path
            print(card)
            print("-" * 80)

            # Render the card
            render_full_card.create_magic_card(card, f"sets/{set_name}")

if __name__ == '__main__':
    # generated_cards_json()
    # generated_cards_images()
    generate_full_card_images()

