import os
import yaml
import unittest

from training_modules.aging import aging


class Test(unittest.TestCase):
    def test_aging(self):
        with open(os.path.join(os.path.dirname(__file__), "test_players/old_player.yaml")) as file:
            stats_initial = yaml.safe_load(file)
        aging(os.path.join(os.path.dirname(__file__), "test_players/old_player.yaml"))
        with open(os.path.join(os.path.dirname(__file__), "test_players/old_player.yaml")) as file:
            stats = yaml.safe_load(file)
        assert stats["positioning"] < 300
        assert stats["age"] == 33
        aging(os.path.join(os.path.dirname(__file__), "test_players/young_player.yaml"))
        with open(os.path.join(os.path.dirname(__file__), "test_players/young_player.yaml")) as file:
            stats = yaml.safe_load(file)
        assert stats["positioning"] == 300
        with open(os.path.join(os.path.dirname(__file__), "test_players/old_player.yaml"), "w") as file:
            yaml.safe_dump(stats_initial, file)


if __name__ == '__main__':
    unittest.main()
