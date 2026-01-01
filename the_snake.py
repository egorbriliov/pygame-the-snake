from datetime import datetime
from random import choice, randint

import pygame as pg

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)
GREEN_APPLE_COLOR = (170, 255, 0)

STONE_COLOR = (128, 128, 128)

# Цвет змейки
SNAKE_COLOR = (218, 165, 32)

# Скорость движения змейки:
SPEED = 5

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Любой игровой объект."""

    # Параметр содержит все занятые ячейки объектами игрыы
    occupied_positions: list[tuple[int, int]] = []

    def __init__(self, body_color=None) -> None:
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        # Добавляет позицию в занятые позиции
        self.occupied_positions.append(self.position)
        self.body_color = body_color

    def draw(self):
        """Отрисовывает объект в окне."""
        raise NotImplementedError(f'В классе {self.__class__.__name__} не '
                                  'определён метод draw')


class SingleCellGameObject(GameObject):
    """Представляет абстрактный класс для создания одиночных объетов."""

    def __init__(self, body_color=None):
        super().__init__(body_color=body_color)
        self.randomize_position()

    def draw(self):
        """Отрисовывает объект «яблоко» в игровом окне."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self):
        """Устанавливает случайное положение яблока на игровом поле.

        Задаёт атрибуту position новое значение. Координаты выбираются так,
        чтобы яблоко оказалось в пределах игрового поля.
        """
        def position():
            """Возвращает новый кортеж случайных координат."""
            new_position = (
                randint(0, SCREEN_WIDTH // GRID_SIZE - 1) * GRID_SIZE,
                randint(0, SCREEN_HEIGHT // GRID_SIZE - 1) * GRID_SIZE)
            return new_position

        new_position = position()
        # Пока новая позия входит в состав занятых позиций
        while new_position in self.occupied_positions:
            # Генерируется новая позиция
            new_position = position()
            # Позиция отправляется на новую проверку
            continue

        # Если предыдущя позиция существует (она была,
        # по умолчанию - это центр)
        if self.position:
            # Удаляет предыдущую позицию из занятых
            self.occupied_positions.remove(self.position)
        # Переназначает старой позицию новую
        self.position = new_position
        # Добавляю позицию в список новых
        self.occupied_positions.append(new_position)


class Stone(SingleCellGameObject):
    """Представляет игровой объект «Камень».
    Он перезапускает игру.
    """

    def __init__(self, body_color=STONE_COLOR):
        super().__init__(body_color=body_color)


class Apple(SingleCellGameObject):
    """Представляет игровой объект «Яблоко».
    Оно добавляет объекту «Змейка» одну часть.
    """

    def __init__(self, body_color=APPLE_COLOR):
        super().__init__(body_color=body_color)


class GreenApple(Apple):
    """Представляет игровой объект «Зелёное яблоко».
    Оно отнимает объекту «Змейка» одну часть.
    """

    def __init__(self, body_color=GREEN_APPLE_COLOR):
        super().__init__(body_color=body_color)


class Snake(GameObject):
    """Объкт класса представляет «змейку».
    Атрибуты и методы класса обеспечивают логику движения, отрисовку и
    поведение «змейки» в игре.
    """

    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(body_color=body_color)
        self.lenght = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.last = None

    @property
    def head_position(self):
        """Возвращает позицию головы."""
        return self.get_head_position()

    def update_direction(self, next_direction):
        """Обновляет направление объекта «змейки»"""
        self.direction = next_direction

    def move(self):
        """Обновляет позицию объекта «змейки» (координаты каждой секции).

        Добавляет новую голову в начало списка positions и удаляет последний
        элемент, если длина змейки не увеличилась.
        """
        new_position = tuple(
            [self.head_position[index] + self.direction[index] * GRID_SIZE
             for index in range(len(self.head_position))])

        x, y = new_position
        if x < 0:
            x = SCREEN_WIDTH - GRID_SIZE
        if y < 0:
            y = SCREEN_HEIGHT - GRID_SIZE
        if x > SCREEN_WIDTH - GRID_SIZE:
            x = 0
        if y > SCREEN_HEIGHT - GRID_SIZE:
            y = 0
        new_position = (x, y)

        # Добавлюя новую позицию в список занятых позиций
        self.occupied_positions.append(new_position)
        self.positions.insert(0, new_position)

        while len(self.positions) > self.lenght + 1:
            # Удаляю позицию в списке занятых позиций
            self.occupied_positions.remove(self.positions[-1])
            self.positions.pop(-1)

    def get_head_position(self):
        """Возвращает позицию головы «змейки»."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает параметры объекта «змейки» в начальное состояние.
        Изменяет параметры змейки.
        """
        # Удаляю все позиции змейки с поля.
        for position in self.position:
            self.occupied_positions.remove(position)

        self.lenght = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = choice([RIGHT, LEFT, UP, DOWN])

    def draw(self):
        """Отрисовывает змейку на экране, затирая след."""
        for position in self.positions[:-1]:
            rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pg.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш, чтобы изменить направление движения
    змейки.
    """
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.update_direction(UP)
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.update_direction(DOWN)
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.update_direction(LEFT)
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.update_direction(RIGHT)
            elif event.key == pg.K_q:
                pg.quit()
                raise SystemExit


def main():
    """Запускает основную логику игры."""
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

        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)

        handle_keys(snake)

        snake.move()
        if snake.head_position == apple.position:
            snake.lenght += 1
            apple.randomize_position()
        if snake.head_position == green_apple.position:
            if snake.lenght > 1:
                snake.lenght -= 1
            green_apple.randomize_position()
        for stone in stones:
            if snake.head_position == stone.position:
                snake.reset()
        if snake.head_position in snake.positions[1:]:
            snake.reset()

        green_apple.draw()
        snake.draw()
        apple.draw()
        for stone in stones:
            stone.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
