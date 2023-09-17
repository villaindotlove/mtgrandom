import json

from content_utils.gpt import prompt_completion_chat


def write_flavor_for_card(card_idea, card_json, story, llm_model):
    lines_remaining_for_flavor = 8

    flavorless_json = {k: v for k, v in card_json.items() if k != "flavor_text"}

    for line in card_json["rule_text"].split("\n"):
        lines_in_line = int(len(line) / 50) + 1
        lines_remaining_for_flavor -= lines_in_line

    if lines_remaining_for_flavor < 1:
        print("Not enough room for flavor text, skipping")
        return ""

    lines_guide = "a single line"
    if lines_remaining_for_flavor > 1:
        lines_guide = f"{lines_remaining_for_flavor} lines"

    len_advice = "keep your ideas short and sweet"
    if lines_remaining_for_flavor > 2:
        len_advice = "you have a few lines to work with"

    prompt = f"""I'd like help writing the flavor text for this Magic the Gathering card:
    
Here's the idea I had for the card:
    
{card_idea}
    
And here's the card's stats:
    
{card_json}
    
Here's the story of the set:
    
{story}
    
# Brainstorming
    
First, I want you to brainstorm some ideas for the flavor text. I'm not sure what the flavor text should be, so write out ideas in these styles:
* A quote attributed to character in the story about the card, like: "A quotation here" -- [Character Name]
* Poetry relevant to the card
* Something humorous
* Words that evoke the emotions of the card
* A single line describing a pivotal moment in the story
* A witty and cutting remark
* A quote from the character that illustrates their personality
* A quote that illustrates a surprising action like betrayal or sacrifice
* One of the other responses, but rhyming
* Free verse poetry

Because of the rules on the card, we only have about {lines_guide} of text or {lines_remaining_for_flavor * 40} characters to work with. So {len_advice}. Don't use quotation marks unless it's a quote from a character in the story.

# Final Flavor

Now, I want you to think about these options and choose one that best fits the theme and feeling of the card. Write out the flavor text for this card. It should be {lines_guide} of text that evokes the flavor of the card. It should be no more than {lines_guide} or {lines_remaining_for_flavor * 40} characters long.

Please write the flavor text on its own line, like this (no quotation marks unless it's a quote from a character in the story):
    
Flavor: [flavor text here]"""

    flavor_text = prompt_completion_chat(messages=[{"role": "system", "content": "You are a writer for Magic the Gathering cards. You love beautiful prose."}, {"role": "user", "content": prompt}], n=1, temperature=0.2, max_tokens=1000, model=llm_model)

    final_flavor = ""
    for line in flavor_text.split("\n"):
        if line.startswith("Flavor: "):
            final_flavor = line.replace("Flavor: ", "")
            break
        elif line.strip() != "":
            final_flavor = line  # If they didn't write "Flavor: " at the beginning, just take the last line

    print("Final flavor text:", final_flavor)
    return final_flavor


if __name__ == "__main__":
    idea = "Ereshkigal's Minions. Creature. Common. Black. These are the spirits and demons of the netherworld, called upon by Ereshkigal to wage war against the gods and the world of the living."
    card_json = json.loads("""{
    "name": "Ereshkigal's Minions",
    "supertype": "Creature",
    "subtype": "Spirit",
    "power": "2",
    "toughness": "2",
    "rule_text": "Deathtouch\\nWhen this creature dies, each opponent loses 1 life.",
    "flavor_text": "These are the spirits and demons of the netherworld, called upon by Ereshkigal to wage war against the gods and the world of the living.",
    "mana_cost": "{1}{B}",
    "rarity": "Common"
}""")

    story = """For thematic guidance, this set should evoke the grandeur and mystery of ancient Sumerian mythology. The gods should feel powerful and awe-inspiring, with mechanics like devotion and constellation representing their influence and authority. The netherworld should feel eerie and foreboding, with mechanics like embalm and sacrifice representing its dark and dangerous nature. The theme of creation should be represented through the creation of tokens and the growth of creatures, with mechanics like afterlife and devotion. The art and flavor text should further reinforce these themes, drawing from Sumerian myths and iconography to create a rich and immersive world."""

    flavor = write_flavor_for_card(idea, card_json, story, "gpt-4")
