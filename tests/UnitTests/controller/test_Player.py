import unittest

from ModularChess.controller.Player import Player


class TestPlayer(unittest.TestCase):

    def setUp(self) -> None:
        self.players = []
        for i in range(4):
            self.players.append(Player(f"Player {i}", (i, i, i)))

        self.team1 = self.players[::2]
        self.team2 = self.players[1::2]

        Player.join_allies(self.team1, self.players)
        Player.join_allies(self.team2, self.players)

        self.main_player = self.players[0]
        self.main_player.name = "Main Player"

    def test_can_capture(self):
        for ally_player in self.team1:
            self.assertFalse(self.main_player.can_capture(ally_player))
        for enemy_player in self.team2:
            self.assertTrue(self.main_player.can_capture(enemy_player))

    def test_get_allies(self):
        self.assertListEqual(self.team1, self.main_player.allies)
        for team in [self.team1, self.team2]:
            for player in team:
                self.assertSetEqual(set(team), set(player.allies))

    def test_get_enemies(self):
        self.assertListEqual(self.team1, self.main_player.allies)
        for team, enemy_team in zip([self.team1, self.team2], [self.team2, self.team1]):
            for player in team:
                self.assertSetEqual(set(enemy_team), set(player.enemies))

    def test_join_allies(self):
        allies = self.players[1:]
        Player.join_allies(allies, self.players)
        for player in allies:
            self.assertSetEqual(set(allies), set(player.allies))
            self.assertSetEqual({self.players[0]}, set(player.enemies))


if __name__ == '__main__':
    unittest.main()
