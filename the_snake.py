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

KEYBOARD = {
    pg.K_UP: {
        'direction': UP,
        'ignore': DOWN},
    pg.K_DOWN: {
        'direction': DOWN,
        'ignore': UP},
    pg.K_RIGHT: {
        'direction': RIGHT,
        'ignore': LEFT},
    pg.K_LEFT: {
        'direction': LEFT,
        'ignore': RIGHT},
}

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
        """Любой игровой объект."""
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        # Добавляет позицию в занятые позиции
        self.occupied_positions.append(self.position)
        self.body_color = body_color

    def draw_rect(self, position: tuple[int, int]) -> None:
        """Отрисовывает ячейку по заднным координатам."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):
        """Отрисовывает объект в окне."""
        raise NotImplementedError(f'В классе {self.__class__.__name__} не '
                                  'определён метод draw')


class SingleCellGameObject(GameObject):
    """Представляет абстрактный класс для создания одиночных объетов."""

    def __init__(self, body_color=None):
        """Представляет абстрактный класс для создания одиночных объетов."""
        super().__init__(body_color=body_color)
        self.randomize_position()

    def draw(self):
        """Отрисовывает объект «яблоко» в игровом окне."""
        self.draw_rect(self.position)

    def randomize_position(self):
        """Устанавливает случайное положение яблока на игровом поле.

        Задаёт атрибуту position новое значение. Координаты выбираются так,
        чтобы яблоко оказалось в пределах игрового поля.
        """
        def position():
            """Возвращает новый кортеж случайных координат."""
            return (
                randint(0, SCREEN_WIDTH // GRID_SIZE - 1) * GRID_SIZE,
                randint(0, SCREEN_HEIGHT // GRID_SIZE - 1) * GRID_SIZE)

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
    """Представляет игровой объект «Камень»."""

    def __init__(self, body_color=STONE_COLOR):
        """Представляет игровой объект «Камень»."""
        super().__init__(body_color=body_color)


class Apple(SingleCellGameObject):
    """Представляет игровой объект «Яблоко».

    Оно добавляет объекту «Змейка» одну часть.
    """

    def __init__(self, body_color=APPLE_COLOR):
        """Представляет игровой объект «Яблоко».

        Оно добавляет объекту «Змейка» одну часть.
        """
        super().__init__(body_color=body_color)


class GreenApple(Apple):
    """Представляет игровой объект «Зелёное яблоко».

    Оно отнимает объекту «Змейка» одну часть.
    """

    def __init__(self, body_color=GREEN_APPLE_COLOR):
        """Представляет игровой объект «Зелёное яблоко».

        Оно отнимает объекту «Змейка» одну часть.
        """
        super().__init__(body_color=body_color)


class Snake(GameObject):
    """Объкт класса представляет «змейку».

    Атрибуты и методы класса обеспечивают логику движения, отрисовку и
    поведение «змейки» в игре.
    """

    def __init__(self, body_color=SNAKE_COLOR):
        """Объкт класса представляет «змейку».

        Атрибуты и методы класса обеспечивают логику движения, отрисовку и
        поведение «змейки» в игре.
        """
        super().__init__(body_color=body_color)
        self.reset()

    @property
    def head_position(self):
        """Возвращает позицию головы."""
        return self.get_head_position()

    def reset(self):
        """Сбрасывает параметры объекта «змейки» в начальное состояние."""
        self.lenght = 1
        self.positions = [self.position]
        self.direction = choice([RIGHT, LEFT, UP, DOWN])
        self.last = None

        # Удаляю все позиции змейки с занятых ячеек и добавляю новые.
        for position in self.positions:
            self.occupied_positions.remove(position)
        self.occupied_positions.append(self.head_position)

    def update_direction(self, next_direction):
        """Обновляет направление объекта «змейки»."""
        self.direction = next_direction

    def move(self):
        """Обновляет позицию объекта «змейки» (координаты каждой секции).

        Добавляет новую голову в начало списка positions и удаляет последний
        элемент, если длина змейки не увеличилась.
        """
        x_direction, y_direction = self.direction
        x_head_position, y_head_position = self.head_position

        # Формирование новой позиции по формуле
        new_position = (
            ((x_head_position + x_direction * GRID_SIZE)
             % SCREEN_WIDTH),
            ((y_head_position + y_direction * GRID_SIZE)
             % SCREEN_HEIGHT))

        # Добавляет новую позицию в список занятых позиций
        self.occupied_positions.append(new_position)
        self.positions.insert(0, new_position)
        # Удаляю все лишние элементы с конца
        while len(self.positions) > self.lenght + 1:
            # Удаляю позицию в списке занятых позиций
            self.occupied_positions.remove(self.positions[-1])
            self.positions.pop(-1)

    def get_head_position(self):
        """Возвращает позицию головы «змейки»."""
        return self.positions[0]

    def draw(self):
        """Отрисовывает змейку на экране, затирая след."""
        for position in self.positions[:-1]:
            self.draw_rect(position)


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш, для изменения движения змейки."""
    for event in pg.event.get():
        if event.type not in [pg.QUIT, pg.KEYDOWN]:
            continue

        if event.type == pg.QUIT or (event.type == pg.KEYDOWN
                                     and event.key == pg.K_q):
            pg.quit()
            raise SystemExit

        if event.type == pg.KEYDOWN:
            # # Словарь направлений для клавиш
            # Допустимые направления для выбранного пользователем
            if event.key not in KEYBOARD:
                continue

            if game_object.direction != KEYBOARD[event.key]['ignore']:
                game_object.update_direction(KEYBOARD[event.key]['direction'])


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
