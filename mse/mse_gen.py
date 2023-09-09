import json
import re
import zipfile
import os
from datetime import datetime


def write_set_file(cards, filename, set_name="my_set"):
    with open(filename, 'w') as f:
        # Writing set metadata
        f.write("mse_version: 2.0.2\ngame: magic\ngame_version: 2020-04-25\n")
        f.write("stylesheet: m15-altered\nstylesheet_version: 2020-09-04\n")
        f.write("set_info:\n\tsymbol:\n\tmasterpiece_symbol:\n")
        f.write("styling:\n\tmagic-m15-altered:\n")
        f.write("\t\tframes: puma\n")
        f.write("\t\ttext_box_mana_symbols: magic-mana-small.mse-symbol-font\n")
        f.write("\t\tlevel_mana_symbols: magic-mana-large.mse-symbol-font\n")
        f.write("\t\toverlay:\n")

        # Writing individual card data
        for idx, card in enumerate(cards):
            fixed_rule_text = card.get('rule_text', '').strip().replace('\n', '\n\t\t')
            fixed_rule_text = fixed_rule_text.replace('{T}', '<sym>T</sym>')
            fixed_rule_text = re.sub(r'\{(.)\}', r'<sym>\1</sym>', fixed_rule_text)

            f.write("card:\n")
            f.write(f"\thas_styling: false\n")
            f.write(f"\ttime_created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"\ttime_modified: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"\tname: {card['name'].strip()}\n")
            f.write(f"\timage: image{idx}\n")
            # TODO Need to split up type and supertype, e.g. "Creature - Human"
            f.write(f"\tsuper_type: <word-list-type>{card.get('type', '')}</word-list-type>\n")
            f.write(f"\tcasting_cost: {card.get('casting_cost', '')}\n")
            f.write(f"\trule_text:\n\t\t{fixed_rule_text}\n")
            f.write(f"\tflavor_text: <i-flavor>{card.get('flavor_text', '').strip()}</i-flavor>\n")
            f.write(f"\tpower: {card.get('power', '')}\n")
            f.write(f"\ttoughness: {card.get('toughness', '')}\n")
            f.write(f"\tloyalty: {card.get('loyalty', '')}\n")
            f.write(f"\tillustrator: {card.get('artist', 'midjourney')}\n")


def generate_mse_set(cards, set_name="my_set"):
    # Step 1: Create a temporary folder
    set_gen_loc = f"sets/{set_name}/msegen"

    os.makedirs(f"{set_gen_loc}/{set_name}", exist_ok=True)

    # Step 2: Write the set file
    write_set_file(cards, f"{set_gen_loc}/{set_name}/set")

    # Step 3: Copy the images
    for idx, card in enumerate(cards):
        image_path = card.get("image", "")
        if os.path.exists(image_path):
            os.makedirs(f"{set_name}", exist_ok=True)
            image_path = image_path.replace("'", "'\\''")
            os.system(f"cp '{image_path}' '{set_gen_loc}/{set_name}/image{idx}'")

    # Step 4: Zip everything into mse-set
    print(f"Zipping sets/{set_name}/{set_name}.mse-set ...")
    with zipfile.ZipFile(f"sets/{set_name}/{set_name}.mse-set", 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(f"{set_gen_loc}/{set_name}"):
            for file in files:
                # if "png" not in file:
                #     continue
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(os.path.join(root, file), set_name)
                if rel_path.startswith('../'):
                    rel_path = rel_path[3:]
                print("Writing", file_path, "to", rel_path)
                zipf.write(file_path, file)

def testing():
    # Example usage
    cards = [
        {
            "name": "Cool bird",
            "type": "Creature",
            "power": "2",
            "toughness": "2",
            "rule_text": """Flying""",
            "flavor_text": "It looks really cool",
            "image": "/home/keenan/Pictures/Art/n8ulzby8lpgb1.jpg",
            "casting_cost": "2RR"
        },
        # Add more card dictionaries here
    ]
    generate_mse_set(cards)

# TODO Do some command line stuff like this:
# mse --export-images my_set.mse-set


def run_export_images(set_name: str, mse_exe_location: str):
    # Remember the current working directory, so we can return to it later
    cwd = os.getcwd()

    # First, change the working directory to "sets/{set_name}/good_cards"
    os.makedirs(f"sets/{set_name}/good_cards", exist_ok=True)
    os.chdir(f"sets/{set_name}/good_cards")

    os.system(f"{mse_exe_location} --export-images ../{set_name}.mse-set")

    # Return to the original working directory
    os.chdir(cwd)


def load_and_create_set(set_name: str, mse_exe_location: str):
    # Load the cards.json file
    cards: list = []
    with open(f"sets/{set_name}/cards.jsonl", 'r') as f:
        for line in f.readlines():
            card = json.loads(line)

            # Reformat for MSE
            card["casting_cost"] = card["manaCost"] if "manaCost" in card else ""
            card["rule_text"] = card["text"]
            card["flavor_text"] = card["flavor"] if "flavor" in card else ""
            card["image"] = f"sets/{set_name}/images/{card['name']}.png"

            cards.append(card)

    # Generate the MSE set
    generate_mse_set(cards, set_name)

    # Export the images
    run_export_images(set_name, mse_exe_location)


if __name__ == "__main__":
    load_and_create_set("polynesia", "wine /home/keenan/Installs/M15-Magic-Pack-main/mse.exe")