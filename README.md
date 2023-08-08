
# MTG Random Card Generator

Generate custom Magic: The Gathering cards. Use ChatGPT or another LLM to generate JSON card details, using existing cards as examples (and to cue the formatting). Then, use an image generation AI such as DALLE to generate art for the cards. Full cards are then rendered using the generated JSON and images. 

I hope you enjoy!

This project is very incomplete, so I welcome any contributions.

## Project Overview

The project is structured into these main parts:

1. **Set Generation (`set`)**: Attempt to generate a cohesive set, with themes and mechanics. 

1. **Card JSON Generation (`cards`)**: This part of the project generates the card details in a JSON format. It utilizes a pre-existing dataset, optionally allows for custom card names, and makes use of AI to generate card details.
   
1. **Image Generation (`images`)**: This step uses a generative graphics model to produce captivating images for the generated cards.

1. **Full Card Generation (`full`)**: This combines the card details with the generated images to render full Magic card designs.

## How to Run

1. **Prerequisites**:
   - Ensure Python is installed on your system.
   - Install required Python libraries by running:
     ```
     pip install -r requirements.txt
     ```
    - Download the [AtomicCards.json](https://mtgjson.com/downloads/all-files/) file from MTGJSON and place it in the root directory of the project.
    - Get an API key from Open AI and `export OPENAI_API_KEY=your_key_here`.

2. **Command Line Arguments**:
   The script accepts a range of command line arguments to customize the card generation process:
   - `action`: Choose which part of the process to run (choices: `cards`, `images`, `full`, `all`).
   - `--set-name`: Name of the set. Required.
   - `--set-description`: Description of the set. Required if generating a new set.
   - `--atomic-cards-file`: Path to AtomicCards.json.
   - `--number-of-cards-to-generate`: Number of cards to generate.
   - `--llm-model`: LLM model to use. Choices: gpt-3.5-turb, gpt-4
   - `--graphics-model`: Graphics model to use. NOT YET IMPLEMENTED.

3. **Execution**:

   - To generate a set:
     ```
        python main.py set --set-name "new_set" --set-description "This is a new set."
     ```
     or
     ```
        python main.py set --set-name "dune" --set-description "An MTG set inspired by Frank Herbert's Dune." --number-of-cards-to-generate 36
     ```
   
   - To generate card details in JSON format:
     ```
     python main.py cards --set-name "new_set" --number-of-cards-to-generate 5
     ```
     
   - To generate card images (for all cards in the set):
     ```
     python main.py images --set-name "new_set"
     ```
     
   - To render the complete cards with images (for all cards in the set):
     ```
     python main.py full --set-name "new_set"
     ```
   
   - To run all the above steps in sequence:
     ```
     python main.py all --set-name "new_set"
     ```

---

# TODO

This project isn't done. Here are the major things that could be improved:


- [ ] Improve the final card rendering. Right now they look quite ugly.
- [ ] In particular, mana symbols aren't rendering properly.
- [ ] Connect another image generator, like Midjourney. We can use [this one](https://github.com/yachty66/unofficial_midjourney_python_api). 
- [ ] It would be nice to generate mechanics for the set, and generally do some set design, before going in and generating cards.
- [ ] Right now cards are being generated from dumb names. It would be good to have a brainstorming phase where we think up cards before generating them.
- [ ] Balance cards for color and rarity. 
- [ ] Have the LLM think critically about the cards it's generating, and maybe do some revisions and edits. Right now some of them are broken or don't make sense.
- [ ] Review the set for synergies and combos.

