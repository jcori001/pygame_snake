import random

import pygame

from snake import Direction, Snake, SnakeCollisionError

BLACK = (0, 0, 0)
BLUE = (50, 153, 213)
GREEN = (0, 255, 0)
RED = (213, 50, 80)
YELLOW = (255, 255, 102)
WHITE = (255, 255, 255)


class App:

    TITLE = "Snake"
    ANTIALIASING = True
    BLOCK_SIZE = 10
    HEIGHT = 400
    WIDTH = 600
    SPEED = 15

    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption(App.TITLE)
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((App.WIDTH, App.HEIGHT))

    def run(self):
        running = True
        score = 0

        while running:
            self.display.fill(BLUE)
            self._show_menu()
            self._show_score(score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
                    elif event.key == pygame.K_c:
                        score = self.snake_game()

        self._quit()

    def snake_game(self):
        game_over = False
        snake = Snake(
            starting_position=self._center_coordinates(),
            block_size=App.BLOCK_SIZE,
        )
        food = self._random_coordinates()

        while not game_over:
            self.display.fill(BLUE)
            self._show_food(food)
            self._show_snake(snake)
            self._show_score(snake.food_eaten())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        snake.set_direction(Direction.LEFT)
                    elif event.key == pygame.K_RIGHT:
                        snake.set_direction(Direction.RIGHT)
                    elif event.key == pygame.K_UP:
                        snake.set_direction(Direction.UP)
                    elif event.key == pygame.K_DOWN:
                        snake.set_direction(Direction.DOWN)

            try:
                snake.move()
            except SnakeCollisionError:
                game_over = True

            if not self._within_bounds(*snake.head()):
                game_over = True

            pygame.display.update()

            if snake.head() == food:
                snake.eat()
                food = self._random_coordinates()

            self.clock.tick(App.SPEED)

        return snake.food_eaten()

    def _block_interval(self, num: int) -> int:
        """Converts integer into multiple of BLOCK_SIZE"""
        return num // App.BLOCK_SIZE * App.BLOCK_SIZE

    def _center_coordinates(self) -> tuple[int, int]:
        return (
            self._block_interval(App.WIDTH // 2),
            self._block_interval(App.HEIGHT // 2),
        )

    def _random_coordinates(self) -> tuple[int, int]:
        return (
            self._block_interval(random.randrange(0, App.WIDTH - App.BLOCK_SIZE)),
            self._block_interval(random.randrange(0, App.HEIGHT - App.BLOCK_SIZE)),
        )

    def _show_food(self, food: tuple[int, int]):
        rectangle = [*food, App.BLOCK_SIZE, App.BLOCK_SIZE]
        pygame.draw.rect(self.display, GREEN, rectangle)

    def _show_menu(self):
        text = "Press C to start new game or Q to quit"
        font = pygame.font.SysFont("bahnschrift", 25)
        text_image = font.render(text, App.ANTIALIASING, YELLOW)
        position = text_image.get_rect(center=(App.WIDTH // 2, App.HEIGHT // 2))
        self.display.blit(text_image, position)

    def _show_score(self, score):
        text = f"Score: {score}"
        font = pygame.font.SysFont("comicsansms", 25)
        position = [0, 0]
        text_image = font.render(text, App.ANTIALIASING, YELLOW)
        self.display.blit(text_image, position)

    def _show_snake(self, snake: Snake):
        for block in snake:
            rectangle = [*block, App.BLOCK_SIZE, App.BLOCK_SIZE]
            pygame.draw.rect(self.display, BLACK, rectangle)

    def _within_bounds(self, x, y) -> bool:
        return all(
            [
                0 < x < self._block_interval(App.WIDTH),
                0 < y < self._block_interval(App.HEIGHT),
            ]
        )

    def _quit(self):
        pygame.quit()
        quit()


if __name__ == "__main__":
    App().run()
