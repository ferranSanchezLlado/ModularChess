from typing import Iterable

import numpy as np
import numpy.typing as npt


class Position(npt.NDArray[np.int64]):

    def __new__(cls, coord):
        if type(coord) is str:
            coord = [int(coord[1]) - 1, ord(coord[0]) - ord('a')]

        if any(not np.issubdtype(type(x), np.integer) for x in coord):
            raise Exception("all elements should be integers")

        position = np.asarray(coord).view(cls)

        if position.ndim != 1:
            raise Exception("position can only be a 1D array")
        return position

    # only called on str()
    def __str__(self) -> str:
        if self.shape[0] == 2 and min(self) >= 0:
            return chr(self[1] + ord('a')) + str(self[0] + 1)

        return "(" + ", ".join(map(str, self)) + ")"

    def create_lineal_path(self, destination: "Position") -> "Iterable[Position]":
        # DOES NOT RAISE UNTIL EVALUATED
        if self.shape != destination.shape:
            raise Exception("different dimensions.")

        diff: Position = destination - self
        abs_diff: Position = np.abs(diff)
        axis_diff = diff != 0
        not_linear = abs_diff != np.max(abs_diff)

        if np.any(not_linear, where=axis_diff):  # type: ignore
            raise Exception("destination path is not lineal.")

        direction = np.floor_divide(diff, np.abs(diff), out=np.zeros_like(diff), where=diff != 0)

        current_position = self
        while not np.array_equal(current_position, destination):
            current_position = current_position + direction
            yield current_position

    def copy_and_replace(self, key, new_value) -> "Position":
        new_coord = np.copy(self)
        new_coord[key] = new_value
        pos: Position = new_coord.view(Position)
        return pos
