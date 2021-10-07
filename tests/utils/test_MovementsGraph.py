import unittest

from ModularChess.utils.Movement import Movement
from ModularChess.utils.MovementsGraph import MovementsGraph, MovementsNode


class FakeMovement(Movement):
    def __init__(self, _id: int):
        self._id = _id

    def __eq__(self, other: "FakeMovement"):
        return self._id == other._id


class TestMovementsGraph(unittest.TestCase):

    def setUp(self) -> None:

        self.move = FakeMovement(0)
        self.node = MovementsNode(None, self.move)
        self.graph = MovementsGraph(self.node, self.node, True, 1)

    def test_add(self):
        move1 = FakeMovement(1)
        node = self.graph.add(move1)
        self.assertEqual(move1, node.move)
        self.assertEqual(self.graph.root, node.parent)
        self.assertEqual(self.graph.root.children[0], node)

        same_node = self.graph.add(move1)
        self.assertEqual(node, same_node)

        move2 = FakeMovement(2)
        node = self.graph.add(move2)
        self.assertEqual(move2, node.move)
        self.assertEqual(self.graph.root, node.parent)
        self.assertEqual(self.graph.root.children[1], node)

    @unittest.skip("TO IMPLEMENT")
    def test_next(self):
        self.fail()

    @unittest.skip("TO IMPLEMENT")
    def test_add_and_next(self):
        self.fail()

    @unittest.skip("TO IMPLEMENT")
    def test_remove(self):
        self.fail()

    @unittest.skip("TO IMPLEMENT")
    def test_get_moves(self):
        self.fail()


if __name__ == '__main__':
    unittest.main()
