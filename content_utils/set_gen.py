import os
import re

from content_utils.gpt import prompt_completion_chat


def generate_set_description(args):
    set_description_file_name = f"sets/{args.set_name}/set_description.txt"
    if os.path.exists(set_description_file_name):
        print(f"Set description file {set_description_file_name} already exists. Skipping.")
        return

    print(f"Generating set description for {args.set_name}")
    messages = [{"role": "system", "content": "You are a brilliant game designer"},
                {"role": "user", "content": f"""I'm an employee at Wizards of the Coast and I'm designing a new set of Magic: The Gathering cards.

The theme of the set is: {args.set_description}

To start with, let's describe some possible mechanics that this set might employ. First, brainstorm a brief list of 10 existing mechanics that might be appropriate for the setting.

Then briefly speculate on 4 new mechanics that we could introduce in the set.

Restrictions: No double sided cards such as werewolfs, no cards that transform, no cards that have a different back.

Next, please discuss how different themes and mechanics will be distributed on the Magic color pie, because we want the set to be balanced across colors. Write one line for each of the five colors describing their theme and mechanics.

If this set idea reminds you of any existing cards or mechanics, please mention them, but be brief."""},]
    first_description = prompt_completion_chat(messages=messages, n=1, temperature=0.0, max_tokens=3800, model=args.llm_model)

    messages.append({"role": "assistant", "content": f"{first_description}"})
    messages.append({"role": "user", "content": f"""That's great! I want to edit this down a bit though. Can you narrow it down to a shorter list of your top 6 favorite existing mechanics for this set theme? 
    
Then, list your top two new mechanics. For each new mechanic, give the Oracle rule text for that new mechanic. For example, the "scry" mechanic is defined as "To “scry N” means to look at the top N cards of your library, then put any number of them on the bottom of your library in any order and the rest on top of your library in any order.".

Remember, the set theme is: {args.set_description}

Again, please discuss how different themes and mechanics will be distributed on the Magic color pie, because we want the set to be balanced across colors.

Then write one paragraph giving thematic guidance for this set."""},)
    better_description = prompt_completion_chat(messages=messages, n=1, temperature=0.0, max_tokens=1000, model=args.llm_model)

    print("Here's the description we got:")
    print(better_description)

    args.set_description = better_description
    with open(set_description_file_name, "w", encoding="utf-8") as f:
        f.write(better_description)

def generate_card_suggestions(args):
    card_suggestions_file_name =  f"sets/{args.set_name}/card_suggestions.txt"
    if os.path.exists(card_suggestions_file_name):
        print(f"Card suggestions file {card_suggestions_file_name} already exists. Skipping.")
        return

    num_cards_to_generate = args.number_of_cards_to_generate
    cards_per_color = num_cards_to_generate // 6
    colorless_cards = num_cards_to_generate - (cards_per_color * 5)
    commons_per_color = cards_per_color // 2
    rares_per_color = (cards_per_color - commons_per_color) // 2
    uncommons_per_color = cards_per_color - commons_per_color - rares_per_color

    with open(card_suggestions_file_name, "a", encoding="utf-8") as f:
        for color in ["white", "blue", "black", "red", "green", "colorless"]:
            messages = [{"role": "system", "content": "You are a brilliant game designer"},
                        {"role": "user", "content": f"""Can you describe a cool Magic The Gathering set idea? It should have a cool theme and some matching mechanics. Please describe what each color is like in this set."""},
                        {"role": "assistant", "content": f"""{args.set_description}"""},
                        {"role": "user", "content": f"""That's great! 
                        
Now, I'd like some help brainstorming cards. Could you suggest some {color} cards for this set? Please brainstorm {commons_per_color} common cards, {uncommons_per_color} uncommon cards, and {rares_per_color} rare cards that are all {color}. 

Please write one per line, like this:
- Card Name (Rarity): Description of card goes here
- Another Card Name (Rarity): Give about one sentence describing the flavor and mechanics of this card

Please don't describe the full stats of each card, just give a few words to suggest what it does."""},]

            card_suggestions = prompt_completion_chat(messages=messages, n=1, temperature=0.2, max_tokens=1000, model=args.llm_model)

            print(f"Here are the {color} cards we got:")
            print(card_suggestions)

            # These look like cards I guess
            for line in card_suggestions.split("\n"):
                if line.startswith("-") or line.startswith("—") or line.startswith("*") or line.startswith("•") or line.startswith(">") or line.startswith("•"):
                    f.write(f"{line} ({color} card)\n")
                elif re.match(r"^\d+[.:)\]]", line):
                    f.write(f"{line} ({color} card)\n")
