import random

import pygame


class Error(Exception):
    """Base class for other exceptions"""

    pass


class SnakeCollisionError(Error):
    """Raised when the snake bumps into itself"""

    pass


class Snake:

    BLOCK_SIZE = 10

    def __init__(
        self, starting_position: tuple[int, int], block_size: int = BLOCK_SIZE
    ) -> None:
        self.cur_head = starting_position
        self.block_size = block_size
        self.body: list[tuple[int, int]] = []
        self.dir = (0, 0)
        self.eating = False

    def move(self) -> None:
        new_head = (
            self.cur_head[0] + self.dir[0] * self.block_size,
            self.cur_head[1] + self.dir[1] * self.block_size,
        )
        self._demote_head()
        self.cur_head = new_head

        if self.eating:
            self.eating = False
        else:
            self._drop_tail()

        self._validate_snake()

    def eat(self) -> None:
        self.eating = True

    def update_direction(self, new_dir: tuple[int, int]) -> None:
        self.dir = new_dir

    def _demote_head(self) -> None:
        self.body.append(self.cur_head)

    def _drop_tail(self) -> None:
        self.body.pop(0)

    def _validate_snake(self):
        if self.cur_head in self.body:
            raise SnakeCollisionError


TITLE = "Snake"
BLOCK_SIZE = 10
DISPLAY_HEIGHT = 400
DISPLAY_WIDTH = 600
GAME_SPEED = 15


class COLOR:
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 102)
    BLUE = (50, 153, 213)
    RED = (213, 50, 80)
    GREEN = (0, 255, 0)
    BLACK = (0, 0, 0)


pygame.init()
pygame.display.set_caption(TITLE)

dis = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
clock = pygame.time.Clock()


def draw_text(text, font, color, position, antialiasing=True):
    text_image = font.render(text, antialiasing, color)
    dis.blit(text_image, position)


def center_coordinates():
    return (DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2)


def random_coordinates():
    return (
        round(random.randrange(0, DISPLAY_WIDTH - BLOCK_SIZE) / 10.0) * 10.0,
        round(random.randrange(0, DISPLAY_HEIGHT - BLOCK_SIZE) / 10.0) * 10.0,
    )


def spawn_new_food():
    x, y = random_coordinates()
    return show_food(x, y)


def show_food(x, y):
    rectangle = [x, y, BLOCK_SIZE, BLOCK_SIZE]
    pygame.draw.rect(dis, COLOR.GREEN, rectangle)
    return x, y


def show_game_close_menu():
    font = pygame.font.SysFont("bahnschrift", 25)
    position = [DISPLAY_WIDTH / 6, DISPLAY_HEIGHT / 3]
    text = "You Lost! Press C-Play Again or Q-Quit"
    draw_text(text, font, COLOR.RED, position)


def show_score(score):
    font = pygame.font.SysFont("comicsansms", 35)
    position = [0, 0]
    text = f"Your Score: {score}"
    draw_text(text, font, COLOR.YELLOW, position)


def show_snake(snake):
    for block in snake:
        x, y = block
        rectangle = [x, y, BLOCK_SIZE, BLOCK_SIZE]
        pygame.draw.rect(dis, COLOR.BLACK, rectangle)


def within_bounds(x, y):
    return 0 < x < DISPLAY_WIDTH and 0 < y < DISPLAY_HEIGHT


def gameLoop():
    game_over = False
    game_close = False

    x, y = center_coordinates()
    dir = (0, 0)
    food_x, food_y = random_coordinates()

    snake = []
    length_of_snake = 1

    while not game_over:

        while game_close == True:
            dis.fill(COLOR.BLUE)
            show_game_close_menu()
            show_score(length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dir = (-1, 0)
                elif event.key == pygame.K_RIGHT:
                    dir = (1, 0)
                elif event.key == pygame.K_UP:
                    dir = (0, -1)
                elif event.key == pygame.K_DOWN:
                    dir = (0, 1)

        if not within_bounds(x, y):
            game_close = True

        x = x + dir[0] * BLOCK_SIZE
        y = y + dir[1] * BLOCK_SIZE
        dis.fill(COLOR.BLUE)
        show_food(food_x, food_y)

        # snake_head = (x, y)

        snake_head = [x, y]
        snake.append(snake_head)

        if len(snake) > length_of_snake:
            del snake[0]

        for block in snake[:-1]:
            if block == snake_head:
                game_close = True

        show_snake(snake)
        show_score(length_of_snake - 1)

        pygame.display.update()
        if x == food_x and y == food_y:
            food_x, food_y = spawn_new_food()
            length_of_snake += 1

        clock.tick(GAME_SPEED)

    pygame.quit()
    quit()


if __name__ == "__main__":
    gameLoop()

"""
make snake an object
- append both sides of collection
- check for head collision (membership check)
- expect to grow size of screen (max)


test for bugs? write tests?
"""
