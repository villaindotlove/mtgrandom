import random

from content_utils.text_utils import remove_bullet_etc, remove_bolding_and_stuff


class MTGCardMechanic:
    def __init__(self, card_text, complexity, flavor, synergy):
        self.card_text = card_text
        self.complexity = complexity
        self.flavor = flavor
        self.synergy = synergy

    def __repr__(self):
        return f"(Complexity: {self.complexity}, Flavor: {self.flavor}, Synergy: {self.synergy}) {self.card_text}"

    def nice_str(self):
        return f"{self.card_text}"  # (Complexity: {self.complexity}, Flavor: {self.flavor}, Synergy: {self.synergy})"


def parse_mechanics(mechanic_list):
    mechanics = []
    for line in mechanic_list:
        parts = line.split(".")

        complexity = 3
        flavor = 3
        synergy = 3
        card_text = ""

        parts_copy = parts.copy()
        for part in parts_copy:
            if "complexity" in part.lower():
                complexity = int(part.strip().split(" ")[1].strip())
                parts.remove(part)
            if "flavor" in part.lower():
                flavor = int(part.strip().split(" ")[1].strip())
                parts.remove(part)
            if "synergy" in part.lower():
                synergy = int(part.strip().split(" ")[1].strip())
                parts.remove(part)
            if "similar to" in part.lower():
                parts.remove(part)  # Don't care about this part
        card_text = remove_bolding_and_stuff(" ".join(parts).strip())  # Whatever's left is the card text
        if len(card_text) > 0 and card_text[0] == "\"":  # Not sure why this happens...
            card_text = card_text[1:]
        mechanics.append(MTGCardMechanic(card_text, complexity, flavor, synergy))
    return mechanics


def generate_sets_with_target_complexity(mechanics, target_complexity, num_sets=5):
    generated_sets = []

    # Calculate weights (sum of flavor and synergy) for each mechanic
    weights = [(mechanic.flavor + mechanic.synergy) ** 3 for mechanic in mechanics]
    weights = [w / sum(weights) for w in weights]

    for _ in range(num_sets):
        temp_mechanics = mechanics.copy()
        current_set = []
        current_complexity = 0
        i = 0
        while current_complexity < target_complexity and temp_mechanics and i < 10:
            i += 1

            # Pick a random mechanic based on weighted probabilities
            chosen_mechanic = random.choices(temp_mechanics, weights=weights, k=1)[0]

            if chosen_mechanic in current_set:
                continue  # Try again

            if current_complexity + chosen_mechanic.complexity <= target_complexity:
                current_set.append(chosen_mechanic)
                current_complexity += chosen_mechanic.complexity

        # Sort the current set by complexity, ascending
        current_set.sort(key=lambda x: x.complexity)

        generated_sets.append(current_set)

    return generated_sets


def generate_sets_with_target_complexity_str_to_strs(mechanic_list, target_complexity, num_sets=5):
    mechanics = parse_mechanics(mechanic_list)
    # print("Parsed Mechanics:")
    # for mechanic in mechanics:
    #     print(mechanic)
    mechanics_sets = generate_sets_with_target_complexity(mechanics, target_complexity, num_sets=num_sets)
    mechanics_sets_strs = []
    for mechanics_set in mechanics_sets:
        mechanics_sets_strs.append("\n".join([mechanic.nice_str() for mechanic in mechanics_set]))
    return mechanics_sets_strs


if __name__ == "__main__":
    mechanic_list = """
1. **Haste**. Similar to [Goblin Guide]. Complexity 1. Flavor 3. Synergy 4.
2. **Menace**. Similar to [Goblin King]. Complexity 1. Flavor 4. Synergy 3.
3. **Deathtouch**. Similar to [Vampire Nighthawk]. Complexity 1. Flavor 5. Synergy 2.
4. **First Strike**. Similar to [White Knight]. Complexity 1. Flavor 4. Synergy 3.
5. **Lifelink**. Similar to [Vampire Nighthawk]. Complexity 1. Flavor 3. Synergy 2.
6. **"When Nergal enters the battlefield, you may sacrifice a creature. If you do, Nergal deals damage equal to that creature's power to any target."** Similar to [Flayer of the Hatebound]. Complexity 3. Flavor 5. Synergy 5.
7. **"Whenever Nergal attacks, you may pay {2}. If you do, create a 2/2 black and red Warrior creature token that's tapped and attacking."** Similar to [Hero of Bladehold]. Complexity 3. Flavor 4. Synergy 4.
8. **"At the beginning of your upkeep, you may pay {2}. If you do, return a creature card from your graveyard to your hand."** Similar to [Oversold Cemetery]. Complexity 3. Flavor 5. Synergy 4.
9. **"Whenever a creature you control dies, put a +1/+1 counter on Nergal."** Similar to [Yahenni, Undying Partisan]. Complexity 3. Flavor 5. Synergy 5.
10. **"Whenever Nergal deals combat damage to a player, that player discards a card."** Similar to [Liliana's Reaver]. Complexity 3. Flavor 4. Synergy 3.
11. **"Whenever a creature you control dies, you may exile it. If you do, create a token that's a copy of that creature, except it's a 1/1 and it gains haste until end of turn."** Similar to [God-Pharaoh's Gift]. Complexity 5. Flavor 5. Synergy 5.
12. **"At the beginning of your end step, if a creature died this turn, you may pay {2}. If you do, draw a card."** Similar to [Dark Prophecy]. Complexity 4. Flavor 5. Synergy 4.
13. **"Whenever Nergal attacks, you may sacrifice another creature. If you do, Nergal gains indestructible until end of turn."** Similar to [Selfless Spirit]. Complexity 4. Flavor 5. Synergy 5.
14. **"Whenever a creature you control dies, you may pay {X}, where X is that creature's power. If you do, Nergal deals X damage to any target."** Similar to [Fling]. Complexity 5. Flavor 5. Synergy 5.
15. **"At the beginning of your upkeep, you may sacrifice a creature. If you do, reveal cards from the top of your library until you reveal a creature card. Put that card into your hand and the rest into your graveyard."** Similar to [Evolutionary Leap]. Complexity 5. Flavor 5. Synergy 5.""".strip().split("\n")

    mechanic_list = [remove_bullet_etc(line) for line in mechanic_list if line.strip() != ""]

    target_complexity = 7
    possible_mechanics_sets = generate_sets_with_target_complexity_str_to_strs(mechanic_list, target_complexity)

    print(f"\nGenerated Sets with Target Complexity {target_complexity}:")
    for i, card_set in enumerate(possible_mechanics_sets, 1):
        print(f"Set {i}: {card_set}")
    print("")
