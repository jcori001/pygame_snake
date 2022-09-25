from enum import Enum, auto


class Error(Exception):
    """Base class for other exceptions"""


class SnakeCollisionError(Error):
    """Raised when the snake bumps into itself"""


class Direction(Enum):
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    UP = auto()


class Snake:
    def __init__(self, starting_position: tuple[int, int], block_size: int) -> None:
        self._cur_head = starting_position
        self._block_size = block_size
        self._body: list[tuple[int, int]] = []
        self._cur_dir: tuple[int, int] = (0, 0)
        self._eating = False

    def block_size(self) -> int:
        return self._block_size

    def eat(self) -> None:
        self._eating = True

    def food_eaten(self) -> int:
        return len(self._body)

    def head(self) -> tuple[int, int]:
        return self._cur_head

    def move(self) -> None:
        new_head = (
            self._cur_head[0] + self._cur_dir[0] * self._block_size,
            self._cur_head[1] + self._cur_dir[1] * self._block_size,
        )
        self._demote_head()
        self._cur_head = new_head

        if self._eating:
            self._eating = False
        else:
            self._drop_tail()

        self._validate_snake()

    def set_direction(self, new_dir: Direction) -> None:
        d_map = {
            Direction.DOWN: (0, 1),
            Direction.LEFT: (-1, 0),
            Direction.RIGHT: (1, 0),
            Direction.UP: (0, -1),
        }
        self._cur_dir = d_map[new_dir]

    def _demote_head(self) -> None:
        self._body.append(self._cur_head)

    def _drop_tail(self) -> None:
        self._body.pop(0)

    def _full_snake(self) -> list[tuple[int, int]]:
        return self._body + [self._cur_head]

    def _validate_snake(self):
        if self._cur_head in self._body:
            raise SnakeCollisionError

    def __iter__(self):
        return iter(self._full_snake())
