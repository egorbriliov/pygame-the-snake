"""All constants for project."""


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


BOARD_BACKGROUND_COLOR = (0, 0, 0)


BORDER_COLOR = (93, 216, 228)


APPLE_COLOR = (255, 0, 0)
GREEN_APPLE_COLOR = (170, 255, 0)

STONE_COLOR = (128, 128, 128)


SNAKE_COLOR = (218, 165, 32)


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
