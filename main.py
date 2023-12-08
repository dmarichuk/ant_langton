import numpy as np
import time
from enum import Enum
from PIL import Image


WIDTH = 1024
HEIGHT = 1024
INIT_X = 512
INIT_Y = 512
INIT_VALUE = True
SAVE_RESULT = True


class OutOfBoundsError(Exception):
    pass


class CursorError(Exception):
    pass


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class Cursor:
    def __init__(self, x: int, y: int, direction: Direction):
        self.x = x
        self.y = y
        self.direction = direction

    @property
    def position(self):
        return (self.x, self.y)

    def move(self, direction: Direction):
        if direction == Direction.UP:
            self.y -= 1
        elif direction == Direction.RIGHT:
            self.x += 1
        elif direction == Direction.DOWN:
            self.y += 1
        elif direction == Direction.LEFT:
            self.x -= 1
        else:
            raise ValueError("Direction is not valid")
        self.direction = direction

    def choose_direction(self, flag: bool):
        if flag:
            if self.direction == Direction.UP:
                return Direction.RIGHT
            elif self.direction == Direction.RIGHT:
                return Direction.DOWN
            elif self.direction == Direction.DOWN:
                return Direction.LEFT
            elif self.direction == Direction.LEFT:
                return Direction.UP
        
        if self.direction == Direction.UP:
            return Direction.LEFT
        elif self.direction == Direction.RIGHT:
            return Direction.UP
        elif self.direction == Direction.DOWN:
            return Direction.RIGHT
        elif self.direction == Direction.LEFT:
            return Direction.DOWN

    def __repr__(self):
        return f"Cursor at ({self.x}, {self.y}) with direction {self.direction.name}"


class Board:
    def __init__(self, width: int, height: int, init_value: bool):
        self.width = width
        self.height = height
        self._matrix = np.array(
            [
                [init_value for _ in range(self.width)] 
                for _ in range(self.height)
            ]
        )
        self._cursor = None

    @property
    def cursor(self):
        return self._cursor
    
    @cursor.setter
    def cursor(self, cursor: Cursor):
        if not isinstance(cursor, Cursor):
            raise TypeError("Cursor must be of type Cursor")
        self._cursor = cursor

    def move_cursor(self):
        if self.cursor is None:
            raise CursorError("Cursor is not defined")

        x, y = self.cursor.position

        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            raise OutOfBoundsError
        
        direction = self.cursor.choose_direction(self._matrix[y][x])
        self.cursor.move(direction)
        self._matrix[y][x] = not self._matrix[y][x]
    
    def get_stats(self):
        return {
            "width": self.width,
            "height": self.height,
            "cursor": self.cursor,
            "black_cells": self.width * self.height - np.count_nonzero(self._matrix),
            "white_cells": np.count_nonzero(self._matrix),
        }


def main():
    try:
        board = Board(WIDTH, HEIGHT)
        board.cursor = Cursor(INIT_X, INIT_Y, Direction.UP)
        while True:
            board.move_cursor()
    except OutOfBoundsError:
        img = Image.fromarray(board._matrix)
        print("FINISHED: ", board.get_stats())
        if not SAVE_RESULT:
            img.show()
        else:
            img.save(f"images/{time.time()}.png")


if __name__ == "__main__":
    main()