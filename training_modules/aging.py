from random import randint
import yaml

from training_modules.training import focus_assignments


def aging(file_name):
    with open(file_name, "r") as file:
        stats = yaml.safe_load(file)

    groups, total = focus_assignments("")
    stats["strength basis"] += randint(0, 3)
    str_constant = stats["strength basis"] - stats["age factor"] ** 2 - 2 * 26 * stats["age factor"]
    str_mult = 52 + 2 * stats["age factor"]
    stats["strength"] = min(int((-stats["age"] ** 2 + str_mult * stats["age"] + str_constant)),
                            stats["max_strength"])
    stats["speed basis"] += randint(0, 3)
    spd_constant = stats["speed basis"] - stats["age factor"] ** 2 - 2 * 22 * stats["age factor"]
    spd_mult = 44 + 2 * stats["age factor"]
    stats["speed"] = min(int((-stats["age"] ** 2 + spd_mult * stats["age"] + spd_constant)),
                         stats["max_speed"])
    stats["fitness basis"] += randint(0, 3)
    fit_constant = stats["strength basis"] - stats["age factor"] ** 2 - 2 * 26 * stats["age factor"]
    fit_mult = 52 + 2 * stats["age factor"]
    stats["strength"] = min(int((-stats["age"] ** 2 + fit_mult * stats["age"] + fit_constant)),
                            stats["max_fitness"])
    if stats["age"] > 30:
        for element in total:
            if element not in ["fitness", "strength", "speed"]:
                stats[element] -= (stats["age"] - 29) * randint(1, 10)

    with open(file_name, "w") as file:
        yaml.safe_dump(stats, file)
