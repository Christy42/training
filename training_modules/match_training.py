from random import randint
import yaml


def match_training(file_name, route_percentages, formation_percentages, position):
    with open(file_name, "r") as file:
        stats = yaml.safe_load(file)
    for element in route_percentages:
        stats[element] = min(500, route_increase(route_percentages[element]))

    for element in formation_percentages:
        stats[element] = min(500, formation_increase(formation_percentages[element]))
    stats[position] = min(500, stats[position] + randint(25, 35))
    with open(file_name, "w") as file:
        yaml.safe_dump(stats, file)


def route_increase(route_percentage):
    if route_percentage == 0:
        return 0
    elif route_percentage >= 80:
        return 30 + randint(-5, 5)
    elif route_percentage >= 50:
        return 20 + randint(-4, 4)
    elif route_percentage >= 30:
        return 15 + randint(-3, 3)
    elif route_percentage >= 20:
        return 6 + randint(-3, 3)
    elif route_percentage >= 10:
        return 3 + randint(-2, 2)
    else:
        return max(1 + randint(-3, 1), 0)


def formation_increase(formation_percentage):
    if formation_percentage == 0:
        return 0
    elif formation_percentage >= 50:
        return 30 + randint(-5, 5)
    elif formation_percentage >= 20:
        return 20 + randint(-4, 4)
    elif formation_percentage >= 15:
        return 8 + randint(-3, 3)
    elif formation_percentage >= 10:
        return 6 + randint(-3, 3)
    elif formation_percentage >= 5:
        return 3 + randint(-2, 2)
    elif formation_percentage >= 3:
        return 2 + randint(-1, 1)
    else:
        return max(0, 1 + randint(-3, 1))
