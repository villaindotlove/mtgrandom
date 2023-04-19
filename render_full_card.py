from PIL import Image, ImageDraw, ImageFont


def create_card(card_info):
    # Load background image
    background = Image.open('card_background.png')

    # Get dimensions from the background
    width, height = background.size

    # Load card art
    card_art = Image.open(card_info['image_path'])
    card_art = card_art.resize((int(width * 0.6), int(width * 0.4)))  # Resize the card art to fit within the card
    background.paste(card_art, (25, 40))  # Paste the card art onto the background at a specific location

    # Set up fonts
    title_font = ImageFont.truetype('Arial.ttf', 24)
    text_font = ImageFont.truetype('Arial.ttf', 18)

    # Add card text
    draw = ImageDraw.Draw(background)
    draw.text((25, 10), card_info['name'], font=title_font, fill='black')
    draw.text((25, 170), card_info['text'], font=text_font, fill='black')
    draw.text((200, 200), f'{card_info["power"]}/{card_info["toughness"]}', font=text_font, fill='black')

    # Save generated card image
    background.save(f'cards/{card_info["name"]}.png')


if __name__ == "__main__":
    # Example usage:
    card_info = {
        'name': 'Sample Card',
        'text': 'This is a sample card description.',
        'power': 3,
        'toughness': 2,
        'image_path': 'images/Self Driving Car.png'
    }

    create_card(card_info)
