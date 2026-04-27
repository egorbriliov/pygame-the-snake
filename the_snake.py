"""Game the snake."""

from datetime import datetime
from random import choice, randint

import pygame as pg

import constants


screen = pg.display.set_mode((constants.SCREEN_WIDTH,
                              constants.SCREEN_HEIGHT), 0, 32)

pg.display.set_caption('The snake')

clock = pg.time.Clock()


class GameObject:
    """Any game object."""

    occupied_positions: list[tuple[int, int]] = []

    def __init__(self, body_color=(0, 0, 0)) -> None:
        """Any game object."""
        self.position = ((constants.SCREEN_WIDTH // 2),
                         (constants.SCREEN_HEIGHT // 2))
        self.occupied_positions.append(self.position)
        self.body_color = body_color

    def draw_rect(self, position: tuple[int, int]) -> None:
        """Draws a cell at the given coordinates.."""
        rect = pg.Rect(position, (
            constants.GRID_SIZE, constants.GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, constants.BORDER_COLOR, rect, 1)

    def draw(self):
        """Draws an object in a window."""
        raise NotImplementedError(f'The class {self.__class__.__name__} does \
                                  not define the draw method')


class SingleCellGameObject(GameObject):
    """Represents an abstract class for creating singleton objects.."""

    def __init__(self, body_color=None):
        """Represent an abstract class for creating singleton objects."""
        super().__init__(body_color=body_color)
        self.randomize_position()

    def draw(self):
        """Draws an apple object into the game window.."""
        self.draw_rect(self.position)

    def randomize_position(self):
        """Set a random position for the apple on the game board.

        Sets the position attribute to a new value. The coordinates are chosen
        so that the apple is within the game board..
        """
        def position():
            """Set the position attribute to a new value.

            The coordinates are chosen.
            """
            return (
                randint(0, constants.SCREEN_WIDTH //
                        constants.GRID_SIZE - 1) * constants.GRID_SIZE,
                randint(0, constants.SCREEN_HEIGHT //
                        constants.GRID_SIZE - 1) * constants.GRID_SIZE)

        new_position = position()
        while new_position in self.occupied_positions:
            new_position = position()
            continue

        if self.position:
            self.occupied_positions.remove(self.position)
        self.position = new_position
        self.occupied_positions.append(new_position)


class Stone(SingleCellGameObject):
    """Represents the game object "Stone"."""

    def __init__(self, body_color=constants.STONE_COLOR):
        """Represent a Stone."""
        super().__init__(body_color=body_color)


class Apple(SingleCellGameObject):
    """Represents the Apple game object.

    It adds one part to the Snake object.
    """

    def __init__(self, body_color=constants.APPLE_COLOR):
        """Represent an Apple..

        It adds one part to the Snake object.
        """
        super().__init__(body_color=body_color)


class GreenApple(Apple):
    """Represents the Green Apple game object.

    It subtracts one part from the Snake object.
    """

    def __init__(self, body_color=constants.GREEN_APPLE_COLOR):
        """Represent the Green Apple.

        It subtracts one part from the Snake object.
        """
        super().__init__(body_color=body_color)


class Snake(GameObject):
    """Represent a Snake.

    The class's attributes and methods provide the movement logic, rendering,
    and the snake's behavior in the game.
    """

    def __init__(self, body_color=constants.SNAKE_COLOR):
        """Represent a snake.

        The class's attributes and methods provide the movement logic,
        rendering, and the snake's behavior in the game.
        """
        super().__init__(body_color=body_color)
        self.reset()

    @property
    def head_position(self):
        """Returns the head position."""
        return self.get_head_position()

    def reset(self):
        """Reset the snake object's parameters to their initial state."""
        self.lenght = 1
        self.positions = [self.position]
        self.direction = choice([constants.RIGHT,
                                 constants.LEFT,
                                 constants.UP,
                                 constants.DOWN])
        self.last = None

        for position in self.positions:
            self.occupied_positions.remove(position)
        self.occupied_positions.append(self.head_position)

    def update_direction(self, next_direction):
        """Update the direction of the snake object."""
        self.direction = next_direction

    def move(self):
        """Update the position of the snake object.

        Adds a new head to the beginning of the positions list and removes
        the last element if the snake's length has not increased.
        """
        x_direction, y_direction = self.direction
        x_head_position, y_head_position = self.head_position

        new_position: tuple[int, int] = (
            ((x_head_position + x_direction * constants.GRID_SIZE)
             % constants.SCREEN_WIDTH),
            ((y_head_position + y_direction * constants.GRID_SIZE)
             % constants.SCREEN_HEIGHT))

        self.occupied_positions.append(new_position)
        self.positions.insert(0, new_position)  # type: ignore
        while len(self.positions) > self.lenght + 1:
            self.occupied_positions.remove(self.positions[-1])
            self.positions.pop(-1)

    def get_head_position(self):
        """Return the position of the snake's head."""
        return self.positions[0]

    def draw(self):
        """Draws a snake on the screen, erasing the trace."""
        for position in self.positions[:-1]:
            self.draw_rect(position)


def handle_keys(game_object):
    """Process keystroke to change the snake's movement."""
    for event in pg.event.get():
        if event.type not in [pg.QUIT, pg.KEYDOWN]:
            continue

        if event.type == pg.QUIT or (event.type == pg.KEYDOWN
                                     and event.key == pg.K_q):
            pg.quit()
            raise SystemExit

        if event.type == pg.KEYDOWN:
            if event.key not in constants.KEYBOARD:
                continue

            if game_object.direction != constants.KEYBOARD[event.key
                                                           ]['ignore']:
                game_object.update_direction(constants.KEYBOARD[event.key
                                                                ]['direction'])


def main():
    """Run the main logic of the game."""
    pg.init()

    snake = Snake()
    apple = Apple()
    green_apple = GreenApple()
    stones = [Stone()]

    last_time = datetime.now()

    while True:
        if (datetime.now() - last_time).seconds > 60:
            last_time = datetime.now()
            stones.append(Stone())

        clock.tick(constants.SPEED)
        screen.fill(constants.BOARD_BACKGROUND_COLOR)

        handle_keys(snake)

        snake.move()
        if snake.head_position == apple.position:
            snake.lenght += 1
            apple.randomize_position()
        elif snake.head_position == green_apple.position:
            if snake.lenght > 1:
                snake.lenght -= 1
            green_apple.randomize_position()
        elif snake.head_position in snake.positions[1:]:
            snake.reset()
        elif snake.head_position in [stone.position for stone in stones]:
            snake.reset()

        green_apple.draw()
        snake.draw()
        apple.draw()
        for stone in stones:
            stone.draw()

        pg.display.update()


if __name__ == '__main__':
    main()
