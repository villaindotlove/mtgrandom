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
        f.write("\t\ttext_box_mana_symbols: magic-mana-small.mse-symbol-font\n")
        f.write("\t\tlevel_mana_symbols: magic-mana-large.mse-symbol-font\n")
        f.write("\t\toverlay:\n")

        # Writing individual card data
        for idx, card in enumerate(cards):
            f.write("card:\n")
            f.write(f"\thas_styling: false\n")
            f.write(f"\ttime_created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"\ttime_modified: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"\tname: {card['name']}\n")
            f.write(f"\timage: image{idx}\n")
            f.write(f"\tsuper_type: <word-list-type>{card.get('type', '')}</word-list-type>\n")
            f.write(f"\tcasting_cost: {card.get('casting_cost', '')}\n")
            f.write(f"\trule_text:\n\t\t{card.get('rule_text', '')}\n")
            f.write(f"\tflavor_text: <i-flavor>{card.get('flavor_text', '')}</i-flavor>\n")


def generate_mse_set(cards, set_name="my_set"):
    # Step 1: Create a temporary folder
    os.makedirs(f"{set_name}", exist_ok=True)

    # Step 2: Write the set file
    write_set_file(cards, f"{set_name}/set")

    # Step 3: Copy the images
    for idx, card in enumerate(cards):
        image_path = card.get("image", "")
        if os.path.exists(image_path):
            os.makedirs(f"{set_name}", exist_ok=True)
            os.system(f"cp {image_path} {set_name}/image{idx}")

    # Step 4: Zip everything into mse-set
    with zipfile.ZipFile(f"{set_name}.mse-set", 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(set_name):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), set_name))


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

if __name__ == "__main__":
    generate_mse_set(cards)

# TODO Do some command line stuff like this:
# mse export-images my_set.mse-set
