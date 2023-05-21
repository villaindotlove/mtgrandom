import random

import dalle
import render_full_card
from card_gen_tools import *

if __name__ == '__main__':
    all_cards = return_all_cards()
    new_card_names = load_card_names()
    # Randomize order of new_card_names to make it more interesting
    random.shuffle(new_card_names)
    for card_name in new_card_names:
        card = random.choice(all_cards)
        generated = generate_card(card, {"name": card_name})
        print(generated)
        generated_dict = generate_dict_given_text(generated)
        # Generate image
        flavor = generated_dict['flavor'] if 'flavor' in generated_dict else (generated_dict['text'] if 'text' in generated_dict else "No flavor text")
        # image_url = dalle.generate_image_and_return_url(f"{generated_dict['name']}, Magic the Gathering Art, Beautiful, Fantasy, Spec Art")
        image_path = f"images/{generated_dict['name']}.png"
        dalle.generate_image_and_save_to_file(f"{generated_dict['name']}, Magic the Gathering Art, Beautiful, Fantasy, Spec Art", image_path)
        # print(image_url)
        # generated_dict['image_url'] = image_url
        generated_dict['image_path'] = image_path
        print(generated_dict)
        print("-" * 80)

        # Render the card
        render_full_card.create_card(generated_dict)
