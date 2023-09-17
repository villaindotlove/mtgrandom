import os
import re
from typing import Optional


def log_generation_step(step_name: str, prompt: str, ai_response: str, set_name: str, card_name: Optional[str] = None):
    if set_name is None:
        print(f"Skipping logging for step {step_name} because set_name is None.")
        return
    os.makedirs(f"sets/{set_name}/logs", exist_ok=True)
    if card_name is None:
        log_file = f"sets/{set_name}/logs/set.txt"
    else:
        # Remove all non-alphanumeric characters in card_idea
        # short_card_name = re.sub("[^\w\s]+", "", card_idea)[30]
        log_file = f"sets/{set_name}/logs/{card_name}.txt"
    with open(log_file, 'a') as f:
        f.write(f"**** STEP {step_name.upper()} ****\n\n")
        f.write(f"** PROMPT **\n\n{prompt}\n\n")
        f.write(f"** RESPONSE **\n\n{ai_response}\n\n")