import json


def write_flavor_for_card(card_idea, card_json, story):
    lines_remaining_for_flavor = 5

    for line in card_json["rule_text"].split("\n"):
        lines_in_line = int(len(line) / 40) + 1
        lines_remaining_for_flavor -= lines_in_line

    prompt = f"""I'd like help writing the flavor text for this Magic the Gathering card:
    
Here's the idea I had for the card:
    
{card_idea}
    
And here's the card's stats:
    
{card_json}
    
Here's the story of the set:
    
{story}
    
# Brainstorming
    
First, I want you to brainstorm some ideas for the flavor text. I'm not sure what the flavor text should be, so write out ideas in these styles:
* A quote from a character in the story about the card
* Poetry relevant to the card
* Something humorous
* Words that evoke the emotions of the card
* A single line describing a pivotal moment in the story

Because of the rules on the card, we only have about {lines_remaining_for_flavor} lines of text or {lines_remaining_for_flavor * 40} characters to work with. So keep your ideas short and sweet.

# Final Flavor

Now, I want you to think about these options and write out the flavor text for this card. It should be a single line of text that evokes the flavor of the card. It should be no more than {lines_remaining_for_flavor} lines or {lines_remaining_for_flavor * 40} characters long.

Please write the flavor text on its own line, like this:
    
Flavor: [flavor text here]"""

    print(prompt)

    return ""


if __name__ == "__main__":
    idea = "Ereshkigal's Minions. Creature. Common. Black. These are the spirits and demons of the netherworld, called upon by Ereshkigal to wage war against the gods and the world of the living."
    cardjson = json.loads("""{
    "name": "Ereshkigal's Minions",
    "supertype": "Creature",
    "subtype": "Spirit",
    "power": "2",
    "toughness": "2",
    "rule_text": "Deathtouch\nWhen this creature dies, each opponent loses 1 life.",
    "flavor_text": "These are the spirits and demons of the netherworld, called upon by Ereshkigal to wage war against the gods and the world of the living.",
    "mana_cost": "{1}{B}",
    "rarity": "Common"
}""")

    story = """For thematic guidance, this set should evoke the grandeur and mystery of ancient Sumerian mythology. The gods should feel powerful and awe-inspiring, with mechanics like devotion and constellation representing their influence and authority. The netherworld should feel eerie and foreboding, with mechanics like embalm and sacrifice representing its dark and dangerous nature. The theme of creation should be represented through the creation of tokens and the growth of creatures, with mechanics like afterlife and devotion. The art and flavor text should further reinforce these themes, drawing from Sumerian myths and iconography to create a rich and immersive world."""

    flavor = write_flavor_for_card(idea, cardjson, story)