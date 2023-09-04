from content_utils.gpt import prompt_completion_chat


def get_art_prompt(card, llm_model):
    name = card['name']
    flavor = card['flavor'] if 'flavor' in card else "I'm not sure"
    mechanics = card['text'] if 'text' in card else "I'm not sure"
    type_line = card['type'] if 'type' in card else "I'm not sure"

    prompt = f"""I'm generating art for a Magic the Gathering card. 

The details of the card are:
Name: {name}
Flavor Text: {flavor}
Mechanics: {mechanics}
Type: {type_line}

I'd like help generating a prompt to use to create art. First, I'd like you to brainstorm some options, and then I'd like you to write a prompt. 

The final prompt needs to be relatively short, so we'll brainstorm first and then distill it into a short prompt. 

Please fill out this form:

# Brainstorming

Central Figure: Describe what the card might feature
Action: What action or event could we depict on the card? Ideally this should suggest tension or arouse the viewer's curiosity
Style: List several stylistic influences we might choose
Medium: List several words to describe the visual medium
Artist: List several artists, living or dead, who might be appropriate to emulate for this art. Suggest at least one artist who has not worked with MTG before. 

# Decision

From the options that you've brainstormed, loosely describe the card art. Try to think of a way in which the scene will be exciting or memorable. Don't be afraid to make bold visual choices to ensure a beautiful card.

# Prompt

Final Prompt: \"[Card Name], Magic the Gathering art, spec art, [list several adjectives], [describe the scene in one sentence or less], in the style of [style], [visual medium], by [artist name]\""""

    temperature = 0.0

    # Try several times with increasing temperature
    for _ in range(3):
        response = prompt_completion_chat(messages=[{"role": "system", "content": "You are an artistic assistant who works with Magic the Gathering"}, {"role": "user", "content": prompt}], n=1, temperature=temperature, max_tokens=2048, model=llm_model)

        for line in response.split("\n"):
            if line.startswith("Final Prompt:") or "Magic the Gathering art, spec art," in line:
                found_prompt = line.replace("Final Prompt:", "").replace("\"", "").strip()
                print("Found a prompt!", found_prompt)
                return found_prompt

        temperature += 0.3

    raise ValueError("Prompt not found")