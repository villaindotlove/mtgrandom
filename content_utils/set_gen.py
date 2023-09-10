import os
import re

from content_utils.gpt import prompt_completion_chat


def generate_set_description(args):
    print(f"Generating set description for {args.set_name}")
    messages = [{"role": "system", "content": "You are a brilliant game designer"},
                {"role": "user", "content": f"""I'm an employee at Wizards of the Coast and I'm designing a new set of Magic: The Gathering cards.

The theme of the set is: {args.set_description}

To start with, let's describe some possible mechanics that this set might employ. First, brainstorm a brief list of 10 existing mechanics that might be appropriate for the setting. In one sentence or less, explain what the mechanic means.

Then, for each of those possible mechanics, describe a previous Magic the Gathering set that has used that mechanic. Describe how they used that mechanic, and what made it fun to draft and play.

Then describe some of the common mechanics that show up in Magic core sets, like flying or creature type synergies, and how they might be used in this set. You don't need to discuss all of them, but mention anything that you think is particularly relevant to the theme.

Then briefly speculate on 10 synergies or deck archetypes that the set might feature. Focus your description on the gameplay aspect here. For each synergy or archetype, describe how it played in a previous set. I want this to be a strong draft set, so focus your analysis on how these synergies and archetypes will play in draft.

Restrictions: No double sided cards such as werewolfs, no cards that transform, no cards that have a different back.

Next, please discuss how different themes and mechanics will be distributed on the Magic color pie, because we want the set to be balanced across colors. Write one line for each of the five colors describing their theme and mechanics.

Then, write one sentence giving guidance for each of the ten two-color pairs. I want each pair of colors to have a direction during the draft. That might be a mechanic like graveyard synergies, +1/+1 counters, "spells matter" or vehicles. These directions will help us design the cards.

If this set idea reminds you of any existing cards, please mention them, but be brief."""},]
    first_description = prompt_completion_chat(messages=messages, n=1, temperature=0.0, max_tokens=3800, model=args.llm_model)

    messages.append({"role": "assistant", "content": f"{first_description}"})
    messages.append({"role": "user", "content": f"""That's great! I want to edit this down a bit though. Can you narrow it down to a shorter list of your top 6 favorite existing mechanics for this set theme? These should be balanced and supportive of the draft archetypes we want. Explain how each mechanic works. Describe what makes the mechanic fun to play and draft.
    
Then, rewrite the 10 color-pair draft archetypes. Connect them to the mechanics you chose. Describe what each archetype is like to draft. What makes a card good for this archetype? Describe what makes the archetype fun to play.

Remember, the set theme is: {args.set_description}

Then write one paragraph giving thematic guidance for this set."""},)
    better_description = prompt_completion_chat(messages=messages, n=1, temperature=0.0, max_tokens=1000, model=args.llm_model)

    print("Here's the description we got:")
    print(better_description)

    return better_description


def generate_card_suggestions(args, num_cards_to_generate: int):
    # TODO: This doesn't hit num_cards_to_generate exactly, because it tries to cover the color pie
    cards_per_color = num_cards_to_generate // 6
    colorless_cards = num_cards_to_generate - (cards_per_color * 5)
    commons_per_color = cards_per_color // 2
    rares_per_color = (cards_per_color - commons_per_color) // 2
    uncommons_per_color = cards_per_color - commons_per_color - rares_per_color

    suggestions = []

    for color in ["white", "blue", "black", "red", "green", "colorless"]:
        messages = [{"role": "system", "content": "You are a brilliant game designer"},
                    {"role": "user", "content": f"""Can you describe a cool Magic The Gathering set idea? It should have a cool theme and some matching mechanics. Please describe what each color is like in this set."""},
                    {"role": "assistant", "content": f"""{args.set_description}"""},
                    {"role": "user", "content": f"""That's great! 
                    
Now, I'd like some help brainstorming cards. Could you suggest some {color} cards for this set? Please brainstorm {commons_per_color} common cards, {uncommons_per_color} uncommon cards, and {rares_per_color} rare cards that are all {color}. 

Please write one per line, like this:
- Card Name (Rarity): Description of card goes here
- Another Card Name (Rarity): One sentence describing the flavor and inspiration for the card. One sentence describing the mechanical archetype the card connects to. One sentence suggesting something the card might do mechanically. One sentence to mention any other cards that inspired this one.

Here's some advice about card ideas:
- Commons should be simple and easy to understand
- Uncommons should help support an archetype
- Rares can be more complex and powerful
- Many cards should connect to one of the mechanical archetypes
- It's okay if some cards are good and flavorful on their own, as long as they can stand alone mechanically

Please don't describe the full stats of each card, just give a few words to suggest what it does."""},]

        card_suggestions = prompt_completion_chat(messages=messages, n=1, temperature=0.2, max_tokens=1000, model=args.llm_model)

        print(f"Here are the {color} cards we got:")
        print(card_suggestions)

        # These look like cards I guess
        for line in card_suggestions.split("\n"):
            if line.startswith("-") or line.startswith("—") or line.startswith("*") or line.startswith("•") or line.startswith(">") or line.startswith("•"):
                suggestions.append(f"{line} ({color} card)")
            elif re.match(r"^\d+[.:)\]]", line):
                suggestions.append(f"{line} ({color} card)")

    return suggestions
