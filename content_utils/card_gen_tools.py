import json
import random

from graphics_utils import dalle
from content_utils.gpt import prompt_completion_chat

DETAILS_IN_ORDER = [
    'name',
    'manaCost',
    'rarity',
    'power',
    'toughness',
    'life',
    'loyalty',
    'defense',
    'attack',
    'type',
    # 'supertypes',
    # 'types',
    # 'subtypes',
    'text',
    'flavor',
    'artist']


def return_all_cards(atomic_cards_json):
    # Load the JSON file
    # Download this file from here: https://mtgjson.com/downloads/all-files/
    with open(atomic_cards_json, encoding='utf-8') as f:
        data = json.load(f)

    return list(data['data'].items())


def card_to_text(card):
    card_text = ''
    if 'rarity' not in card:
        card['rarity'] = 'Uncommon'
    for detail in DETAILS_IN_ORDER:
        if detail in card:
            det_text = card[detail]
            if isinstance(det_text, list):
                if not det_text:  # [] is falsey
                    continue
                det_text = ', '.join(det_text)
            det_text = det_text.strip()
            card_text += f'{detail}: {det_text}\n'
    return card_text


def generate_card(example, args, details=None):
    example_text = card_to_text(example[1][0]) + "\n"
    if details:
        messages = [{"role": "system", "content": f"You generate Magic the Gathering cards for a new set we're working on:\n\n{args.full_set_guidelines if args.full_set_guidelines else args.set_name}"},
                    {"role": "user", "content": f"Please generate a Magic the Gathering card named {example[1][0]['name']}"},
                    {"role": "assistant", "content": f"{example_text}"},
                    {"role": "user", "content": f"Please generate a card. Here's the idea I have for it: \n{details['idea']}"}, ]
    else:
        messages = [{"role": "system", "content": "You generate Magic the Gathering cards"},
                    {"role": "user", "content": f"Please generate a card"},
                    {"role": "assistant", "content": f"{example_text}"},
                    {"role": "user", "content": f"Please generate a card"}, ]
    suggested_card = prompt_completion_chat(messages=messages, n=1, temperature=0.0, max_tokens=512, model=args.llm_model)
    return suggested_card


def load_card_names(card_names_file):
    with open(card_names_file, encoding='utf-8') as f:
        card_names = f.readlines()
    return [x.strip() for x in card_names if x.strip() != ""]


def generate_dict_given_text(text):
    # TODO This needs to be improved. For example, sometimes it doesn't put everything on one line

    text = text.strip()
    if text == "":
        return {}
    lines = text.split("\n")
    details = {}
    for line in lines:
        line = line.strip()
        if line == "":
            continue
        if line.count(":") == 0:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if key in ["supertypes", "types", "subtypes"]:
            details[key] = value.split(",")
        else:
            details[key] = value

    # Try to fix it up
    # Lower case everything
    keys_copy = list(details.keys())
    for key in keys_copy:
        if key != key.lower():
            details[key.lower()] = details[key]
            del details[key]
    # Fix multi-word keys
    for flavor_synonym in ["flavor text", "flavortext"]:
        if flavor_synonym in details:
            details["flavor"] = details[flavor_synonym]
            del details[flavor_synonym]
    for artist_synonym in ["artist name", "artistname"]:
        if artist_synonym in details:
            details["artist"] = details[artist_synonym]
            del details[artist_synonym]
    for mana_synonym in ["mana cost", "manacost"]:
        if mana_synonym in details:
            details["manaCost"] = details[mana_synonym]
            del details[mana_synonym]

    # Should have power and toughness
    if "creature" in details["type"] and ("power" not in details or "toughness" not in details):
        raise Exception("Creature card without power and toughness")

    return details


def get_some_cards(num_new_cards=10, args=None):
    all_cards = return_all_cards()
    new_cards = []
    for _ in range(num_new_cards):
        example_card = random.choice(all_cards)
        generated = generate_card(example_card, args)
        print(generated)
        generated_dict = generate_dict_given_text(generated)
        if 'name' in generated_dict:
            gen_name = generated_dict['name']
        elif 'Name' in generated_dict:
            gen_name = generated_dict['Name']
        else:
            gen_name = "No Name"
        image_path = f"images/{gen_name}.png"
        dalle.generate_image_and_save_to_file(f"{gen_name}, Magic the Gathering Art, Beautiful, Fantasy, Spec Art", image_path)
        generated_dict['image_path'] = image_path
        # print(generated_dict)
        # print("-" * 80)
        new_cards.append(generated_dict)
    return new_cards


if __name__ == '__main__':
    cards = get_some_cards(10, args={'llm_model': 'gpt-3.5-turbo'})

    # Load cards.json as a list of dicts, append new cards, and save
    with open('../sets/default/cards.json', encoding='utf-8') as f:
        all_cards = json.load(f)
    all_cards.extend(cards)
    with open('../sets/default/cards.json', 'w', encoding='utf-8') as f:
        json.dump(all_cards, f, indent=4)
