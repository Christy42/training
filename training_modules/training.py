import yaml
from random import randint


def training(file_name, focus, formation_route):
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
    with open(file_name, "w") as file:
        yaml.safe_dump(stats, file)


def focus_assignments(focus):
    # with open(os.path.join(os.path.dirname(__file__), "config/stat_groupings.yaml"), "r") as file:
    with open("C:\\Users\\Mark\\PycharmProjects\\training\\training_modules\\config\\stat_groupings.yaml", "r") as file:
        groupings = yaml.safe_load(file)
    total = groupings["total"]
    for group in groupings:
        if focus in group:
            return groupings[group].append(focus), total
    return ["blank"], total
