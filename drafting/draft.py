import json
import random

import pygame

# screen settings
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
CARD_WIDTH = 240
CARD_PADDING = 20
CARD_HEIGHT = 240
CARD_DISPLAY_POS = (0, 0)
CARD_NAME_POS = (SCREEN_WIDTH - 300, 0)
FONT_SIZE = 20
IMAGE_WIDTH = CARD_WIDTH
IMAGE_HEIGHT = CARD_WIDTH  # int(CARD_WIDTH * 2 / 3)  # 3:2 aspect ratio

# initialize pygame
pygame.init()

# setup screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# setup font
font = pygame.font.Font(None, FONT_SIZE)

# load the card database
with open("cards.json") as f:
    card_db = json.load(f)


def switch_keys_to_lower(dictionary):
    new_dictionary = {}
    for key, value in dictionary.items():
        new_key = key.lower().replace(" ", "_")
        new_dictionary[new_key] = value
    return new_dictionary


card_db = [switch_keys_to_lower(card) for card in card_db]

# load card images or create colored rectangles for missing ones
for card in card_db:
    try:
        card['image'] = pygame.image.load(card['image_path']).convert_alpha()
        card['image'] = pygame.transform.scale(card['image'], (IMAGE_WIDTH, IMAGE_HEIGHT))
    except FileNotFoundError:
        card_color = tuple((hash(card['name']) + i * 123456) % 256 for i in range(3))
        card['image'] = pygame.Surface((IMAGE_WIDTH, IMAGE_HEIGHT))
        card['image'].fill(card_color)

    # Default values for missing card attributes
    card['attack'] = card.get('attack', 0)
    card['health'] = card.get('health', 0)
    card['cost'] = card.get('mana_cost', "0")
    card['text'] = card.get('text', 'This is a card named ' + card['name'])

# player's deck
player_deck = []


def draw_card_names():
    y = CARD_NAME_POS[1]
    for card in player_deck:
        label = font.render(card['name'], True, (255, 255, 255))
        screen.blit(label, (CARD_NAME_POS[0], y))
        y += FONT_SIZE


def draw_card(card, x, y):
    screen.blit(card['image'], (x, y))
    y += IMAGE_HEIGHT
    name_label = font.render(card['name'], True, (255, 255, 255))
    screen.blit(name_label, (x, y))
    y += FONT_SIZE
    cost_label = font.render(str(card['cost']), True, (255, 255, 255))
    screen.blit(cost_label, (x, y))
    y += FONT_SIZE

    text_lines = text_wrap(card['text'], FONT_SIZE, CARD_WIDTH)  # Wrap the text lines
    rect_height = FONT_SIZE * len(text_lines)  # Calculate the height of the rectangle

    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(x, y, CARD_WIDTH, rect_height), 1)

    for line in text_lines:
        text_label = font.render(line, True, (255, 255, 255))
        screen.blit(text_label, (x, y))
        y += FONT_SIZE

    y += FONT_SIZE
    # attack_label = font.render(str(card['attack']), True, (255, 255, 255))
    # screen.blit(attack_label, (x, y))


def text_wrap(text, font_size, max_width):
    words = text.split(' ')
    lines = []
    current_line = words[0]
    for word in words[1:]:
        label = font.render(current_line + ' ' + word, True, (255, 255, 255))
        if label.get_width() <= max_width:
            current_line += ' ' + word
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)
    return lines


def draw_card_choices(card_choices):
    x = CARD_DISPLAY_POS[0]
    for card in card_choices:
        draw_card(card, x, CARD_DISPLAY_POS[1])
        x += CARD_WIDTH + CARD_PADDING  # added some padding between cards


while len(player_deck) < 10:
    # get 5 random cards
    card_choices = random.sample(card_db, 5)

    # main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                card_index = (mouse_pos[0] - CARD_DISPLAY_POS[0]) // (CARD_WIDTH + CARD_PADDING)
                if 0 <= card_index < len(card_choices):
                    player_deck.append(card_choices[card_index])
                    running = False

        # draw screen
        screen.fill((0, 0, 0))
        draw_card_names()
        draw_card_choices(card_choices)
        pygame.display.flip()

pygame.quit()
