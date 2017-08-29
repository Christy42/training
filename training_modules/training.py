import os
import yaml
from random import randint


def training(file_name, focus, formation_route, weight_direction):
    with open(file_name, "r") as file:
        stats = yaml.safe_load(file)
    group, total = focus_assignments(focus)
    if focus == '':
        focus = "blank"
    if group is None:
        group = ["blank"]
    if focus not in ["strength", "speed", "fitness"]:
        for element in total:
            stats[element] += (element in group) + (element == focus) * 4 + randint(0, 2)
            stats[element] = min(stats[element], stats[element + "_max"])
    else:
        if stats[focus + " basis"] > stats[focus + " basis max"] - 80:
            stats[focus + " basis"] += min(randint(0, 3), randint(0, 3))
        elif stats[focus + " basis"] > stats[focus + " basis max"] - 50:
            stats[focus + " basis"] += min(randint(0, 2), randint(0, 2))
        elif stats[focus + " basis"] > stats[focus + " basis max"] - 30:
            stats[focus + " basis"] += min(randint(0, 1), randint(0, 1))
        elif stats[focus + " basis"] > stats[focus + " basis max"] - 1:
            stats[focus + " basis"] += 0
        else:
            stats[focus + " basis"] += randint(0, 3)
    str_constant = stats["strength basis"] - stats["age factor"] ** 2 - 2 * 26 * stats["age factor"]
    str_mult = 52 + 2 * stats["age factor"]
    stats["strength"] = min(int((-stats["age"] ** 2 + str_mult * stats["age"] + str_constant)),
                            stats["strength basis max"])
    spd_constant = stats["speed basis"] - stats["age factor"] ** 2 - 2 * 24 * stats["age factor"]
    spd_mult = 48 + 2 * stats["age factor"]
    stats["speed"] = min(int((-stats["age"] ** 2 + spd_mult * stats["age"] + spd_constant)),
                         stats["speed basis max"])
    fit_constant = stats["strength basis"] - stats["age factor"] ** 2 - 2 * 26 * stats["age factor"]
    fit_mult = 52 + 2 * stats["age factor"]
    stats["fitness"] = min(int((-stats["age"] ** 2 + fit_mult * stats["age"] + fit_constant)),
                           stats["fitness basis max"])
    if not formation_route and group != ["blank"]:
        if focus not in ["strength", "speed", "fitness"]:
            for element in group:
                stats[element] = min(stats[element] + randint(0, 1), stats["max_" + element])
    elif formation_route:
        for element in formation_route:
            stats[element] += randint(10, 20)
            stats[element] = min(stats[element], 500)
    stats["weight"] = amend_weight(weight_direction, stats["weight"], stats["base_weight"])
    with open(file_name, "w") as file:
        yaml.safe_dump(stats, file)


def focus_assignments(focus):
    with open(os.environ['FOOTBALL_HOME'] + "//training_config//stat_groupings.yaml") as file:
        groupings = yaml.safe_load(file)
    total = groupings["total"]
    for group in groupings:
        if focus in group:
            return groupings[group].append(focus), total
    return ["blank"], total


def amend_weight(direction, weight, base_weight):
    biggest_shift = 10
    direction_move = (direction == "up") - (direction == "down")
    weight = float(weight)
    base_weight = float(base_weight)

    max_move = biggest_shift * direction_move
    if direction not in ["up", "down"]:
        return int(max(base_weight * (100 - biggest_shift) / 100,
                   min(base_weight * (100 + biggest_shift) / 100,
                   weight + randint(-2, 2))))
    diff_to_go = ((base_weight * (100 + max_move) / 100 - weight) / base_weight)
    weight_move = diff_to_go * 10
    end_weight = weight + base_weight * weight_move / 100
    return int(max(base_weight * (100 - biggest_shift) / 100,
                   min(base_weight * (100 + biggest_shift) / 100,
                   end_weight + randint(-2, 2))))
