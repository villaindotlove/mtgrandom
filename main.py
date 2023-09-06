import os
import argparse
import json
import random

from content_utils.art_director import get_art_prompt
from content_utils.set_gen import generate_set_description, generate_card_suggestions
from graphics_utils import render_full_card, midjourney
from content_utils.card_gen_tools import *


def parse_arguments():
    parser = argparse.ArgumentParser(description="Generate Cards")

    parser.add_argument('action', choices=['set', 'cards', 'images', 'full', 'all'], help='Action to be performed.')
    parser.add_argument('--set-name', default='testing', help='Name of the set.')
    parser.add_argument('--set-description', default='Cool fantasy world but with funny animals', help='Description of the set.')
    parser.add_argument('--card-names-file', default=None, help='File with card names.')
    parser.add_argument('--atomic-cards-file', default='AtomicCards.json', help='Path to AtomicCards.json.')
    parser.add_argument('--max-cards-generate', default=0, type=int, help='Maximum number of cards to generate. If zero, no max.')
    parser.add_argument('--set-size', default=18, type=int, help='The size of the set.')
    parser.add_argument('--llm-model', default='gpt-3.5-turbo', help='LLM model to use.')
    parser.add_argument('--graphics-model', default='dalle', help='Graphics model to use. Options: dalle, midjourney')

    return parser.parse_args()


def generate_set(args):
    set_description_file_name = f"sets/{args.set_name}/set_description.txt"
    if os.path.exists(set_description_file_name):
        print(f"Set description file {set_description_file_name} already exists. Skipping.")
    else:
        set_description = generate_set_description(args)
        args.set_description = set_description
        with open(set_description_file_name, "w", encoding="utf-8") as f:
            f.write(set_description)

    # Generate some card ideas
    card_suggestions_file_name = f"sets/{args.set_name}/card_suggestions.txt"
    num_cards_to_generate_suggestions_for = args.set_size
    if os.path.exists(card_suggestions_file_name):
        with open(card_suggestions_file_name, "r", encoding="utf-8") as f:
            card_suggestions = f.readlines()
            number_of_existing_suggestions = len([suggestion for suggestion in card_suggestions if suggestion.strip() != ""])
            num_cards_to_generate_suggestions_for = max(0, num_cards_to_generate_suggestions_for - number_of_existing_suggestions)
        print(f"Card suggestions file {card_suggestions_file_name} already exists. Generating {num_cards_to_generate_suggestions_for} more suggestions.")
    if num_cards_to_generate_suggestions_for > 0:
        card_suggestions = generate_card_suggestions(args, num_cards_to_generate_suggestions_for)
        with open(card_suggestions_file_name, "a", encoding="utf-8") as f:
            for card_suggestion in card_suggestions:
                f.write(card_suggestion + "\n")


def generated_cards_json(args):
    all_cards = return_all_cards(args.atomic_cards_file)
    card_suggestions_file = f"sets/{args.set_name}/card_suggestions.txt"
    num_generated_cards = 0
    if os.path.exists(card_suggestions_file):
        new_card_ideas = load_card_names(card_suggestions_file)
    else:
        adjectives = ["Cute", "Funny", "Silly", "Goofy", "Weird", "Strange", "Bizarre", "Unusual", "Quirky", "Odd", "Angry", "Sad", "Happy", "Frenzied", "Fantastic", "Questing", "Lost", "Forgotten", "Ancient", "Charming", "Enchanted", "Mysterious", "Running"]
        creatures = ["Badger", "Peacock", "Wizard", "Barbarian", "Emu", "Penguin", "Panda", "Wallaby", "Koala", "Kangaroo", "Dingo", "Dinosaur", "Dragon", "Unicorn", "Pegasus", "Griffin", "Phoenix", "Gryphon", "Goblin", "Orc", "Troll", "Ogre", "Elf", "Fairy", "Mermaid", "Centaur", "Minotaur", "Satyr", "Giant", "Gnome", "Golem", "Gargoyle", "Demon", "Angel", "Vampire", "Werewolf", "Zombie", "Skeleton", "Ghost", "Specter"]
        new_card_ideas = [f"{random.choice(adjectives)} {random.choice(creatures)}" for _ in range(args.number_of_cards_to_generate)]
        # random.shuffle(new_card_ideas)
    for i, card_idea in enumerate(new_card_ideas):
        if 0 <= args.max_cards_generate <= num_generated_cards:
            break
        approx_card_name = card_idea[2:card_idea.find("(")].strip()
        with open(f"sets/{args.set_name}/cards.jsonl", "r") as f:
            if f"name\": \"{approx_card_name}" in f.read():
                print(f"Skipping card {i + 1} (Already exists) out of {len(new_card_ideas)}: {card_idea}")
                continue
        example_card = random.choice(all_cards)
        generated = generate_card(example_card, args, {"idea": card_idea})
        print("-" * 80)
        print(f"Generated card {i+1} out of {len(new_card_ideas)}: {card_idea}")
        num_generated_cards += 1
        print(generated)
        generated_dict = generate_dict_given_text(generated)
        generated_dict = criticize_and_try_to_improve_card(generated_dict, args)
        generated_dict['art_prompt'] = get_art_prompt(generated_dict, args.llm_model)
        with open(f"sets/{args.set_name}/cards.jsonl", "a") as f:
            f.write(json.dumps(generated_dict) + "\n")


def generated_cards_images(args):
    os.makedirs(f"sets/{args.set_name}/images", exist_ok=True)
    generated_images = 0
    with open(f"sets/{args.set_name}/cards.jsonl", "r") as f:
        cards = [json.loads(line) for line in f.readlines()]
        for i, card in enumerate(cards):
            if 0 <= args.max_cards_generate <= generated_images:
                break
            # flavor = card['flavor'] if 'flavor' in card else (card['text'] if 'text' in card else "")
            image_path = f"sets/{args.set_name}/images/{card['name']}.png"
            # art_prompt = f"{card['name']}, Magic the Gathering Art, Beautiful, Fantasy, Spec Art. {flavor}"
            if not os.path.exists(image_path):
                print(f"Generating image for card {i+1} out of {len(cards)}:", card['name'])
                generated_images += 1
                if 'art_prompt' in card:
                    art_prompt = card['art_prompt']
                else:
                    art_prompt = get_art_prompt(card, args)
                if args.graphics_model == "dalle":
                    dalle.generate_image_and_save_to_file(art_prompt, image_path)
                elif args.graphics_model == "midjourney":
                    midjourney.generate_image_and_save_to_file(art_prompt, image_path)
                else:
                    print("Unknown graphics model.", args.graphics_model)
            else:
                print(f"Image already exists for card {i} of {len(cards)}:", card['name'])


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
    os.makedirs(f"sets/{args.set_name}", exist_ok=True)

    set_description_file_name = f"sets/{args.set_name}/set_description.txt"
    if os.path.exists(set_description_file_name):
        args.full_set_guidelines = open(set_description_file_name, "r", encoding="utf-8").read()

    if args.action == "set" or args.action == "all":
        print("Generating set...")
        generate_set(args)
    if args.action == "cards" or args.action == "all":
        print("Generating cards...")
        generated_cards_json(args)
    if args.action == "images" or args.action == "all":
        print("Generating images...")
        generated_cards_images(args)
    if args.action == "full" or args.action == "all":
        print("Generating full card images...")
        generate_full_card_images(args)