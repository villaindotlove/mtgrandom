
# MTG Random Card Generator

Generate custom Magic: The Gathering cards. Use ChatGPT or another LLM to generate JSON card details, using existing cards as examples (and to cue the formatting). Then, use an image generation AI such as DALLE to generate art for the cards. Full cards are then rendered using the generated JSON and images. 

I hope you enjoy!

## Project Overview

The project is structured into three main parts:

1. **Card JSON Generation (`cards`)**: This part of the project generates the card details in a JSON format. It utilizes a pre-existing dataset, optionally allows for custom card names, and makes use of AI to generate card details.
   
2. **Image Generation (`images`)**: This step uses a generative graphics model to produce captivating images for the generated cards.

3. **Full Card Generation (`full`)**: This combines the card details with the generated images to render full Magic card designs.

## How to Run

1. **Prerequisites**:
   - Ensure Python is installed on your system.
   - Install required Python libraries by running:
     ```
     pip install -r requirements.txt
     ```

2. **Command Line Arguments**:
   The script accepts a range of command line arguments to customize the card generation process:
   - `action`: Choose which part of the process to run (choices: `cards`, `images`, `full`, `all`).
   - `--set-name`: Name of the set.
   - `--set-description`: Description of the set.
   - `--card-names-file`: File with card names.
   - `--atomic-cards-file`: Path to AtomicCards.json.
   - `--number-of-cards-to-generate`: Number of cards to generate.
   - `--llm-model`: LLM model to use.
   - `--graphics-model`: Graphics model to use.

3. **Execution**:
   
   - To generate card details in JSON format:
     ```
     python your_script.py cards --set-name "new_set"
     ```
     
   - To generate card images:
     ```
     python your_script.py images --set-name "new_set"
     ```
     
   - To render the complete cards with images:
     ```
     python your_script.py full --set-name "new_set"
     ```
   
   - To run all the above steps in sequence:
     ```
     python your_script.py all --set-name "new_set"
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

