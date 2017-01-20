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
    for element in total:
        stats[element] += (element in group) + (element == focus) * 4 + randint(0, 2)
        stats[element] = min(stats[element], stats[element + "_max"])
    if not formation_route and group != ["blank"]:
        for element in group:
            stats[element] = min(stats[element] + randint(0, 5), stats["max_" + element])
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
