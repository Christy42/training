from random import randint
import yaml

from training_modules.training import focus_assignments


def aging(file_name):
    with open(file_name, "r") as file:
        stats = yaml.safe_load(file)

    groups, total = focus_assignments("")
    if stats["age"] < 30:
        return 0
    for element in total:
        stats[element] -= (stats["age"] - 29) * randint(1, 10)
    with open(file_name, "w") as file:
        yaml.safe_dump(stats, file)
