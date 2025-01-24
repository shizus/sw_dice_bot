import random
import re


def parse_dice_input(input_string):
    """Parses the input string to extract the dice pool.

    Args:
        input_string (str): Dice input string (e.g., "2ca,2pe,3di,1be,2co").

    Returns:
        dict: Parsed dice pool with counts by type.
    """
    dice_mapping = {
        "ca": "ability",
        "pe": "proficiency",
        "di": "difficulty",
        "de": "challenge",
        "be": "boost",
        "co": "setback",
        "fu": "force",
        "ab": "ability",
        "pr": "proficiency",
        "ch": "challenge",
        "bo": "boost",
        "se": "setback",
        "fo": "force",
    }

    dice_pool = {}
    for match in re.finditer(r"(\d+)([a-z]{2})", input_string):
        count, dice_type = match.groups()
        key = dice_mapping.get(dice_type)
        if key:
            dice_pool[key] = dice_pool.get(key, 0) + int(count)
        else:
            print(f"Unknown dice type: {dice_type}")

    return dice_pool


def roll_dice(dice_pool):
    """
    Simulates rolling a pool of Star Wars: Edge of the Empire dice.

    Args:
        dice_pool (dict): A dictionary representing the dice to roll, e.g.,
                         {"ability": 2, "difficulty": 1}

    Returns:
        tuple: (results, individual_rolls)
            results: dict with counts of symbols.
            individual_rolls: list of individual dice rolls.
    """
    dice_faces = {
        "ability": ["", "success", "success", "advantage", "success",
                    "advantage", "advantage", "advantage"],
        "proficiency": ["", "success", "success", "success", "success",
                        "advantage", "success+advantage", "success+advantage",
                        "advantage", "advantage", "advantage+advantage",
                        "triumph"],
        "difficulty": ["", "failure", "failure", "threat", "failure", "threat",
                       "threat", "threat+threat"],
        "challenge": ["", "failure", "failure", "failure", "failure", "threat",
                      "failure+threat", "failure+threat", "threat", "threat",
                      "threat+threat", "despair"],
        "boost": ["", "", "success", "success+advantage", "advantage",
                  "advantage"],
        "setback": ["", "", "failure", "failure", "threat", "threat"],
        "force": ["dark", "dark", "dark", "dark", "dark", "dark", "dark",
                  "dark", "light", "light", "light+light", "light+light"],
    }

    results = {
        "success": 0,
        "advantage": 0,
        "triumph": 0,
        "failure": 0,
        "threat": 0,
        "despair": 0,
        "light": 0,
        "dark": 0,
    }

    individual_rolls = []

    for dice_type, count in dice_pool.items():
        if dice_type not in dice_faces:
            print(f"Unknown dice type: {dice_type}")
            continue

        for _ in range(count):
            face = random.choice(dice_faces[dice_type])
            individual_rolls.append({"dice_type": dice_type, "result": face})
            for symbol in face.split('+'):
                if symbol:
                    results[symbol] += 1

    return results, individual_rolls


def roll_from_string(dice_input):
    """
    Parses the dice input string, rolls the dice, and returns the results.

    Args:
        dice_input (str): Dice input string (e.g., "2ca,2pe,3di,1be,2co").

    Returns:
        tuple: (results, individual_rolls)
            results: dict with counts of symbols.
            individual_rolls: list of individual dice rolls.
    """
    dice_pool = parse_dice_input(dice_input)
    return roll_dice(dice_pool)