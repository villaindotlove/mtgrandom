import json
import os
import random
import re

import requests

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
    if not os.path.exists(atomic_cards_json):
        # Download the file if it doesn't exist
        url = 'https://mtgjson.com/api/v5/AtomicCards.json'
        response = requests.get(url)
        with open(atomic_cards_json, 'wb') as f:
            f.write(response.content)

    with open(atomic_cards_json, encoding='utf-8') as f:
        data = json.load(f)

    return list(data['data'].items())


def get_fake_example_card():
    # TODO I think the order of this is getting rearranged, which might matter for prompt engineering reasons
    return {
        "name": "Name of card",
        "supertype": "Sorcery, Land, Creature, Legendary Artifact, Enchantment, etc",
        "subtype": "Human, Elf, Warrior, etc",
        "power": "2",
        "toughness": "4",
        "rule_text": """Flying, Indestructible
{T}: Example tap ability
{1}{R}: Example mana ability""",
        "flavor_text": "A quote or vignette that adds flavor to the card",
        "mana_cost": "{2}{R}{W}",
        "rarity": "Common, Uncommon, or Rare",
    }


def generate_card(example, args, details=None):
    if example is None:
        example = get_fake_example_card()
        example_text = card_to_text(example, False)
    else:
        example_text = card_to_text(example[1][0], True)
    if details:
        # This is the most common case
        messages = [{"role": "system", "content": f"You generate Magic the Gathering cards for a new set we're working on:\n\n{getattr(args, 'full_set_guidelines', args.set_name)}"},
                    {"role": "user", "content": f"Please show me the format for a Magic the Gathering card."},
                    {"role": "assistant", "content": f"```json\n{example_text}\n```"},
                    {"role": "user", "content": f"Please generate a card. Here's the idea I have for it: \n{details['idea']}\n\nFirst describe a coherent idea for the card, then describe how mechanics could capture that idea. \n\nThen, write out the details in the JSON format I showed you. Don't forget to include the mana cost (unless it's a land)"}, ]
    else:
        messages = [{"role": "system", "content": "You generate Magic the Gathering cards"},
                    {"role": "user", "content": f"Please show me the format for a Magic the Gathering card."},
                    {"role": "assistant", "content": f"```json\n{example_text}\n```"},
                    {"role": "user", "content": f"Please generate a card"}, ]
    suggested_card = prompt_completion_chat(messages=messages, n=1, temperature=0.0, max_tokens=512, model=args.llm_model)
    return suggested_card


def criticize_and_try_to_improve_card(card, args):
    # TODO I think I need to totally redo this prompt.
    # It should first focus on missing content and rules issues, which are the most serious problems.
    # I should include a list of the most common design issues, like parasitic mechanics, and ask it to identify those
    # I should include a scoring system like "Rate complexity on a scale of 1-5" and "Rate power level on a scale of 1-5"
    # I should give it clear rules for when to accept or reject a card based on those scores, like commons should be a 1-3 on both, uncommons should be a 2-4, and rares should be a 3-5
    messages = [{"role": "system", "content": f"You generate Magic the Gathering cards. You are not afraid to be critical."},
                {"role": "user", "content": f"""I want help designing a Magic the Gathering card. Here are the details:

```json
{card_to_text(card)}
```

Please answer these questions about this card, and give constructive criticism:

* Name one or two cards that are mechanically similar to this card, for reference.

* Is it missing any important details like mana cost, or power and toughness if it's a creature? If so, write "Needs work: Missing details" and write what's missing

* Does the text on the card make sense mechanically? Is it possible to do what the card says? If not, write "Needs work: Mechanical Issues"

* Is it written in the right style for MTG? Would a judge have trouble interpreting it? If it's not written in the style of Oracle text, write "Needs work: Wrong Style"

Rate the power level of the card on a scale from 0-6, where 0 is unplayable, 1 is very weak, like a bad common, 5 is very strong, like a bomb rare, and 6 is super overpowered like a black lotus. We're aiming for these power levels:
Commons: 1-3
Uncommons: 2-4
Rares: 3-5

Rate the complexity of the card on a scale from 0-6, where 0 is a vanilla creature, 1 is very simple, 5 is very complex, like a planeswalker, and 6 is way too confusingly complicated. We're aiming for these complexity levels:
Commons: 1-3
Uncommons: 2-4
Rares: 3-5

If we're not within those ranges, write "Needs work: Power Level too [high, low]" or "Needs work: [Too complex, too simple]"

Rate the flavor of the card and the match between the flavor and the mechanics on a scale from 1-5, where 1 is a boring card or a card whose theme is not at all reflected in the mechanics, and 5 is a card with a very interesting theme that is well reflected in the mechanics. If the card is a 1 or a 2, write "Needs work: Flavor".

If the card passes all these tests, then great! Please write "Looks good".

For now, just answer the questions."""},]
    criticism = prompt_completion_chat(messages=messages, n=1, temperature=0.0, max_tokens=512, model=args.llm_model)

    looks_good: bool = False
    if "looks good" in criticism.lower():
        looks_good = True

    if "needs work" in criticism.lower():
        looks_good = False
        for line in criticism.split("\n"):
            if "needs work" in line.lower():
                print("Fixing:", line)
                break

    if not looks_good:
        messages = [{"role": "system",
                     "content": f"You generate Magic the Gathering cards. You are not afraid to be critical."},
                    {"role": "user", "content": f"""I want help designing a Magic the Gathering card. Here are the details I have for the card:

```json
{card_to_text(card)}
```

What do you think of this card?"""},
                    {"role": "assistant", "content": f"{criticism}"},
                    {"role": "user", "content": f"Given your feedback, please try to improve the card. Please output JSON for the improved card."}]
        improved_card = prompt_completion_chat(messages=messages, n=1, temperature=0.0, max_tokens=512, model=args.llm_model)
        improved_card_dict = generate_dict_given_text(improved_card)
        return improved_card_dict, False
    else:
        return card, True


def load_card_ideas(card_names_file):
    with open(card_names_file, encoding='utf-8') as f:
        card_names = f.readlines()
    return [x.strip() for x in card_names if x.strip() != ""]


def card_to_text(card, fix_inclusions=False):
    if fix_inclusions:
        if 'rarity' not in card:
            card['rarity'] = 'Uncommon'
        simpler_card = {}
        for detail in DETAILS_IN_ORDER:
            if detail in card:
                simpler_card[detail] = card[detail]
    else:
        simpler_card = card
    s = json.dumps(simpler_card, indent=4)
    return s


def generate_dict_given_text(text):
    # TODO This needs to be improved. For example, sometimes it doesn't put everything on one line

    text = text.strip()
    if text == "":
        return {}
    details = {}
    try:
        if "```json" in text:
            potential_json = text[text.find("```json")+7:text.rfind("```")]
        else:
            potential_json = text[text.find('{'):text.rfind('}')+1]
        details = json.loads(potential_json)
        print(details)
    except:
        print("SAD! Couldn't parse as JSON: ", text)
        lines = text.split("\n")
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

    # For some reason it sometimes has "abilities" instead of "rule_text"
    if "abilities" in details:
        print("Got abilities, trying to repair:", details)
        if "rule_text" in details:
            print("Weird, found both abilities and rule_text")
        else:
            ability_texts = []
            for ability in details["abilities"]:
                if ability is str:
                    details["rule_text"] += ability
                elif ability is dict:
                    main_ability = ability["text"] if "text" in ability else ability["effect"] if "effect" in ability else ability["description"] if "description" in ability else ""
                    if "cost" in ability:
                        if ability["cost"] in main_ability:
                            # The text is duplicated
                            ability_texts.append(main_ability)
                        else:
                            ability_texts.append(ability["cost"] + ": " + main_ability)
                    else:
                        ability_texts.append(main_ability)
            details["rule_text"] = "\n".join(ability_texts)

    # Should have power and toughness
    is_creature = False
    if "type" in details:
        is_creature = "creature" in details["type"]
    elif "supertype" in details:
        is_creature = "creature" in details["supertype"]
    if is_creature and ("power" not in details or "toughness" not in details):
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
