import re

def remove_bullet_etc(mystr):
    debulleted_str = ""
    if len(mystr.strip()) == 0:
        return mystr
    if mystr.strip()[0] in ["*", "-", "#", "•", "‣", "◦"]:
        debulleted_str = mystr[1:]

    # Use re to check if the first character is a number followed by a period
    if re.match(r"^\d+\.", mystr.strip()):
        debulleted_str = mystr[mystr.find(".")+1:]
    if re.match(r"^\d+\)", mystr.strip()):
        debulleted_str = mystr[mystr.find(")")+1:]

    return debulleted_str.strip()

def remove_bolding_and_stuff(mystr):
    return mystr.replace("**", "")

