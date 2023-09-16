import re

from collections import Counter


class MTGCard:
    def __init__(self, name, card_type, rarity, colors, coolness):
        self.name = name
        self.card_type = card_type
        self.rarity = rarity
        self.colors = colors  # Set of colors
        self.is_creature = card_type == "Creature" or "Creature" in card_type
        self.coolness = coolness

    def __repr__(self):
        color_str = "/".join(self.colors)
        return f"{self.name}. {self.card_type}. {self.rarity}. {color_str}. Coolness {self.coolness}."

def parse_card_list(card_list):
    cards = []
    for line in card_list:
        name, card_type, rarity, color, coolness = line.split('. ')
        coolness = int(re.search(r'Coolness (\d+)', line).group(1))  # Extract the number from "Coolness X"
        colors = set()

        for clr in ["white", "blue", "black", "red", "green"]:
            if clr in color.lower():
                colors.add(clr.capitalize())

        if "all colors" in color.lower():
            colors = {"White", "Blue", "Black", "Red", "Green"}

        if "colorless" in color.lower():
            colors = {}

        if "Rare" in rarity or "Mythic" in rarity:
            rarity = "Rare"

        cards.append(MTGCard(name, card_type, rarity, colors, coolness))
    return cards

from collections import defaultdict
import random

def calculate_potential(card, color_count, rarity_count, creature_count, other_count, set_size):
    potential = card.coolness

    for clr in card.colors:
        potential += ((set_size / 5) - color_count[clr])

    potential += ((set_size / 3) - rarity_count[card.rarity])

    if card.is_creature:
        potential += ((set_size / 2) - creature_count)
    else:
        potential += ((set_size / 2) - other_count)

    return potential

def create_balanced_set(cards, set_size=60):
    balanced_set = []

    color_count = defaultdict(int)
    rarity_count = defaultdict(int)
    creature_count = 0
    other_count = 0

    while len(balanced_set) < set_size:
        for card in cards:
            card.potential = calculate_potential(card, color_count, rarity_count, creature_count, other_count, set_size)

        cards.sort(key=lambda x: x.potential, reverse=True)

        card_to_add = None

        for card in cards:
            if card in balanced_set:
                continue
            can_add = True

            for clr in card.colors:
                if color_count[clr] >= set_size / 5:
                    can_add = False
                    break

            if rarity_count[card.rarity] >= set_size / 3:
                can_add = False

            if card.is_creature and creature_count >= set_size / 2:
                can_add = False

            if not card.is_creature and other_count >= set_size / 2:
                can_add = False

            if can_add:
                card_to_add = card
                break

        if card_to_add is None:
            # Be greedy
            print(f"Could not find a card to add. Adding the highest potential card: {cards[0].name}")
            card_to_add = cards[0]

        balanced_set.append(card_to_add)
        print(f"Added {card_to_add.name} to the set.")
        for clr in card_to_add.colors:
            color_count[clr] += 1
        rarity_count[card_to_add.rarity] += 1
        creature_count += card_to_add.is_creature
        other_count += not card_to_add.is_creature

    return balanced_set

def summarize_set(balanced_set):
    color_counter = Counter()
    rarity_counter = Counter()
    type_counter = Counter()

    for card in balanced_set:
        for color in card.colors:
            color_counter[color] += 1
        rarity_counter[card.rarity] += 1
        type_counter[card.card_type] += 1

    print("=== Summary Statistics ===")

    print("\nColor Distribution:")
    for color, count in color_counter.items():
        print(f"{color}: {count}")

    print("\nRarity Distribution:")
    for rarity, count in rarity_counter.items():
        print(f"{rarity}: {count}")

    print("\nType Distribution:")
    for card_type, count in type_counter.items():
        print(f"{card_type}: {count}")


if __name__ == '__main__':
    card_list_text = """
Enki, Lord of Water and Wisdom. Legendary Creature. Mythic. Blue. Coolness 10.
Inanna, Goddess of Love and War. Legendary Creature. Mythic. White/Red. Coolness 9.
Ninsun, the Seeress. Legendary Creature. Rare. White/Blue. Coolness 8.
Ereshkigal, Queen of the Netherworld. Legendary Creature. Mythic. Black. Coolness 9.
Lugal, the Mortal King. Legendary Creature. Rare. White/Red. Coolness 7.
Anzu, the Thunderbird. Creature. Rare. Blue/Red. Coolness 8.
Basmu, the Venomous Serpent. Creature. Uncommon. Green/Black. Coolness 7.
Lilitu, the Night Spirit. Creature. Uncommon. Black. Coolness 6.
Ugallu, the Great Lion. Creature. Uncommon. Green/White. Coolness 7.
Enlil, the God of Air. Legendary Creature. Rare. Blue/White. Coolness 8.
Nanna, the God of the Moon. Legendary Creature. Rare. White/Blue. Coolness 8.
Tablets of Fate. Artifact. Mythic. Colorless. Coolness 10.
Crown of Heaven. Artifact. Rare. Colorless. Coolness 9.
Rod of Power. Artifact. Rare. Colorless. Coolness 8.
Heartstone, Core of Zunaria. Legendary Artifact. Mythic. Colorless. Coolness 10.
Scribe’s Quill. Artifact. Uncommon. Colorless. Coolness 6.
Enchanter's Loom. Artifact. Uncommon. Colorless. Coolness 5.
Ritual Dagger. Artifact. Uncommon. Colorless. Coolness 6.
The Offering. Artifact. Common. Colorless. Coolness 4.
Uruk-Kala, the Divine City. Land. Rare. Colorless. Coolness 9.
Zunaria, the Realm of Gods. Land. Mythic. Colorless. Coolness 10.
Heaven’s Gate. Land. Rare. Colorless. Coolness 8.
The Abyss, Gateway to the Netherworld. Land. Uncommon. Colorless. Coolness 7.
Rivers of Enki. Land. Uncommon. Colorless. Coolness 7.
Fields of the Damned. Land. Uncommon. Colorless. Coolness 6.
Desert of Forgotten Souls. Land. Common. Colorless. Coolness 5.
Caverns of Despair. Land. Common. Colorless. Coolness 4.
Forest of Whispers. Land. Common. Colorless. Coolness 5.
Hallowed Sanctuary. Land. Common. Colorless. Coolness 5.
The Uprising of Lugal. Sorcery. Rare. Red/White. Coolness 8.
The Final Confrontation. Instant. Mythic. All Colors. Coolness 10.
Dance of Inanna. Enchantment. Uncommon. Red/White. Coolness 6.
Nightfall, Ereshkigal's Dominion. Enchantment. Rare. Black. Coolness 8.
Moonrise, Nanna’s Blessing. Instant. Rare. Blue/White. Coolness 7.
Thunderstorm, Wrath of Anzu. Sorcery. Uncommon. Blue/Red. Coolness 7.
Rebellion, Mortal's Revolt. Sorcery. Rare. Red. Coolness 9.
The Gathering, Council of Gods. Enchantment. Mythic. All Colors. Coolness 10.
Serpent's Venom, Basmu’s Curse. Instant. Uncommon. Black/Green. Coolness 6.
Lion's Roar, Ugallu’s Might. Instant. Uncommon. Green/White. Coolness 7.
Divine Intervention. Instant. Rare. White. Coolness 8.
Ancestral Spirits. Enchantment. Uncommon. White/Blue. Coolness 6.
Will of the Seeress. Enchantment. Rare. Blue. Coolness 8.
Seal of Authority. Enchantment. Rare. White. Coolness 7.
The Reckoning, Final Judgment. Sorcery. Rare. Black/White. Coolness 9.
Cosmic Alignment. Enchantment. Rare. Blue. Coolness 8.
Whispering Shadows. Instant. Common. Black. Coolness 5.
The Cosmic Wheel. Artifact. Rare. Colorless. Coolness 9.""".strip().split("\n")

    cards = parse_card_list(card_list_text)
    balanced_set = create_balanced_set(cards, set_size=24)
    for card in balanced_set:
        print(card)

    summarize_set(balanced_set)

