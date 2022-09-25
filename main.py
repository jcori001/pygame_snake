import random

import pygame

from snake import Direction, Snake, SnakeCollisionError

TITLE = "Snake"
BLOCK_SIZE = 10
DISPLAY_HEIGHT = 400
DISPLAY_WIDTH = 600
GAME_SPEED = 15

BLACK = (0, 0, 0)
BLUE = (50, 153, 213)
GREEN = (0, 255, 0)
RED = (213, 50, 80)
YELLOW = (255, 255, 102)
WHITE = (255, 255, 255)


def block_interval(num: int) -> int:
    """Converts integer into multiple of BLOCK_SIZE"""
    return num // BLOCK_SIZE * BLOCK_SIZE


def center_coordinates() -> tuple[int, int]:
    return (
        block_interval(DISPLAY_WIDTH // 2),
        block_interval(DISPLAY_HEIGHT // 2),
    )


def random_coordinates() -> tuple[int, int]:
    return (
        block_interval(random.randrange(0, DISPLAY_WIDTH - BLOCK_SIZE)),
        block_interval(random.randrange(0, DISPLAY_HEIGHT - BLOCK_SIZE)),
    )


def within_bounds(x, y) -> bool:
    return all(
        [0 < x < block_interval(DISPLAY_WIDTH), 0 < y < block_interval(DISPLAY_HEIGHT)]
    )


pygame.init()

clock = pygame.time.Clock()
dis = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption(TITLE)


def draw_text(text, font, color, position, antialiasing=True):
    text_image = font.render(text, antialiasing, color)
    dis.blit(text_image, position)


def show_food(food: tuple[int, int]):
    rectangle = [*food, BLOCK_SIZE, BLOCK_SIZE]
    pygame.draw.rect(dis, GREEN, rectangle)


def show_menu():
    font = pygame.font.SysFont("bahnschrift", 25)
    position = [DISPLAY_WIDTH / 6, DISPLAY_HEIGHT / 3]
    text = "Press: C-Play or Q-Quit"
    draw_text(text, font, RED, position)


def show_score(score):
    font = pygame.font.SysFont("comicsansms", 25)
    position = [0, 0]
    text = f"Score: {score}"
    draw_text(text, font, YELLOW, position)


def show_snake(snake: Snake):
    for block in snake:
        rectangle = [*block, BLOCK_SIZE, BLOCK_SIZE]
        pygame.draw.rect(dis, BLACK, rectangle)


def run_game():
    game_over = False
    snake = Snake(
        starting_position=center_coordinates(),
        block_size=BLOCK_SIZE,
    )
    food = random_coordinates()

    while not game_over:
        dis.fill(BLUE)
        show_food(food)
        show_snake(snake)
        show_score(snake.food_eaten())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
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

        if not within_bounds(*snake.head()):
            game_over = True

        pygame.display.update()

        if snake.head() == food:
            snake.eat()
            food = random_coordinates()

        clock.tick(GAME_SPEED)

    return snake.food_eaten()


def game_app():
    running = True
    score = 0

    while running:
        dis.fill(BLUE)
        show_menu()
        show_score(score)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_c:
                    score = run_game()

    pygame.quit()
    quit()


if __name__ == "__main__":
    game_app()
