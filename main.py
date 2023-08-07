import os
import argparse
import json
import random
from graphics_utils import render_full_card
from content_utils.card_gen_tools import *


def parse_arguments():
    parser = argparse.ArgumentParser(description="Generate Cards")

    parser.add_argument('action', choices=['cards', 'images', 'full', 'all'], help='Action to be performed.')
    parser.add_argument('--set-name', default='testing', help='Name of the set.')
    parser.add_argument('--set-description', default='Cool fantasy world but with funny animals',
                        help='Description of the set.')
    parser.add_argument('--card-names-file', default=None, help='File with card names.')
    parser.add_argument('--atomic-cards-file', default='AtomicCards.json',
                        help='Path to AtomicCards.json.')
    parser.add_argument('--number-of-cards-to-generate', default=1, type=int, help='Number of cards to generate.')
    parser.add_argument('--llm-model', default='gpt-3.5-turbo', help='LLM model to use.')
    parser.add_argument('--graphics-model', default='dalle', help='Graphics model to use.')

    return parser.parse_args()


def generated_cards_json(args):
    all_cards = return_all_cards(args.atomic_cards_file)
    os.makedirs(f"sets/{args.set_name}", exist_ok=True)
    if args.card_names_file is not None:
        new_card_names = load_card_names(f"sets/{args.set_name}/{args.card_names_file}")
    else:
        adjectives = ["Cute", "Funny", "Silly", "Goofy", "Weird", "Strange", "Bizarre", "Unusual", "Quirky", "Odd", "Angry", "Sad", "Happy", "Frenzied", "Fantastic", "Questing", "Lost", "Forgotten", "Ancient", "Charming", "Enchanted", "Mysterious", "Running"]
        creatures = ["Badger", "Peacock", "Wizard", "Barbarian", "Emu", "Penguin", "Panda", "Wallaby", "Koala", "Kangaroo", "Dingo", "Dinosaur", "Dragon", "Unicorn", "Pegasus", "Griffin", "Phoenix", "Gryphon", "Goblin", "Orc", "Troll", "Ogre", "Elf", "Fairy", "Mermaid", "Centaur", "Minotaur", "Satyr", "Giant", "Gnome", "Golem", "Gargoyle", "Demon", "Angel", "Vampire", "Werewolf", "Zombie", "Skeleton", "Ghost", "Specter"]
        # TODO Use the LLM to generate these names
        new_card_names = [f"{random.choice(adjectives)} {random.choice(creatures)}" for _ in range(args.number_of_cards_to_generate)]
    random.shuffle(new_card_names)
    with open(f"sets/{args.set_name}/cards.jsonl", "a") as f:
        for card_name in new_card_names:
            card = random.choice(all_cards)
            generated = generate_card(card, args, {"name": card_name})
            print(generated)
            generated_dict = generate_dict_given_text(generated)
            f.write(json.dumps(generated_dict) + "\n")


def generated_cards_images(args):
    os.makedirs(f"sets/{args.set_name}/images", exist_ok=True)
    with open(f"sets/{args.set_name}/cards.jsonl", "r") as f:
        cards = [json.loads(line) for line in f.readlines()]
        for card in cards:
            flavor = card['flavor'] if 'flavor' in card else (
                card['text'] if 'text' in card else "")
            image_path = f"sets/{args.set_name}/images/{card['name']}.png"
            if not os.path.exists(image_path):
                dalle.generate_image_and_save_to_file(f"{card['name']}, Magic the Gathering Art, Beautiful, Fantasy, Spec Art. {flavor}", image_path)


def generate_full_card_images(args):
    os.makedirs(f"sets/{args.set_name}/cards", exist_ok=True)
    with open(f"sets/{args.set_name}/cards.jsonl", "r") as f:
        cards = [json.loads(line) for line in f.readlines()]
        for card in cards:
            image_path = f"sets/{args.set_name}/images/{card['name']}.png"
            card['image_path'] = image_path
            if not os.path.exists(f"sets/{args.set_name}/cards/{card['name']}.png"):
                print(card)
                print("-" * 80)
                render_full_card.create_magic_card(card, f"sets/{args.set_name}")


if __name__ == '__main__':
    args = parse_arguments()

    if args.action == "cards" or args.action == "all":
        print("Generating cards...")
        generated_cards_json(args)
    if args.action == "images" or args.action == "all":
        print("Generating images...")
        generated_cards_images(args)
    if args.action == "full" or args.action == "all":
        print("Generating full card images...")
        generate_full_card_images(args)