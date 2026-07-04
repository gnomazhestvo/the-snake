"""
Игра Змейка.

В центре игрового пространства, разделенного на клетки 20х20 px, появляется
змейка, состоящая из одного сегмента, движущаяся в одном из четырех направлений
(при старте игры - вправо).

В случайной точке появляется яблоко, при съедении которого длина змейки
увеличивается, а яблоко появляется снова, в другой случайной точке.

При столкновении головы змейки с любым из ее сегментов - "поражение", игра
начинается заново.
"""

from random import choice, randint

import pygame

# Константы размеров игрового пространства:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
ZERO_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Константы объектов игры:
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
SPEED = 20

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


# Создание игрового пространства.
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject():
    """Родительский класс для различных объектов игры."""

    def __init__(
            self,
            body_color: tuple[int, int, int] = BOARD_BACKGROUND_COLOR
    ) -> None:
        """Инициализирует объект игры.

        Параметры:
        - body_color - цвет объекта, коржеж RGB. По умолчанию - цвет игрового
        поля.

        Артибуты:
        - position - стандартная, "нулевая" позиция объекта.
        """
        self.body_color = body_color
        self.position = ZERO_POSITION

    def draw(self):
        """Отрисовывает объект, определяется в дочерних классах."""

    def draw_cell(self, coordinates, cell_color):
        """Отрисовывает клетку с границей вокруг.

        Каждый объект состоит из одинаковых клеток разных цветов. Яблоко -
        одна клетка. Змейка - несколько соединенных клеток.

        Параметры:
        - coordinates - координаты отрисовки клетки;
        - cell_color - цвет клетки.
        """
        cell_rect = pygame.Rect(coordinates, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, cell_color, cell_rect)
        pygame.draw.rect(screen, BORDER_COLOR, cell_rect, 1)


class Apple(GameObject):
    """Описывает яблоко, которое съедает змейка."""

    def __init__(
            self,
            body_color: tuple[int, int, int] = APPLE_COLOR
    ) -> None:
        """Инициализирует яблоко.

        Яблоко - объект, состоящий из одной клетки. В начале игры появляется
        в случайной позиции. Затем появляется в случайной позиции после
        каждого съедения.

        Параметры:
        - body_color - цвет яблока. По умолчанию - константа цвет яблока.

        Атрибуты:
        - position - координаты яблока. Определены методом randomize_position.
        """
        super().__init__(body_color)
        self.position = self.randomize_position(ZERO_POSITION)

    def randomize_position(self, snake_positions) -> tuple[int, int]:
        """Возвращает случайные координаты яблока в сетке игры.

        Проверяет, что позиция, в которой создается яблоко, свободно.

        Параметры:
        - snake_positions - текущие координаты ячеек, в которых есть змейка.
        """
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if self.position not in snake_positions:
                return self.position

    def draw(self) -> None:
        """Отрисовывает яблоко на экране в позиции position."""
        self.draw_cell(self.position, self.body_color)


class Snake(GameObject):
    """Описывает змейку.

    Змейка представлена списком сегментов.
    """

    def __init__(
            self,
            body_color: tuple[int, int, int] = SNAKE_COLOR
    ) -> None:
        """Инициализирует змейку.

        Параметры:
        - body_color - цвет объекта. По умолчанию - константа цвет змейки.

        Атрибуты:
        - reset - метод, передающий начальные, "нулевые" атрибуты змейки -
        длина = 1, координаты - середина экрана.
        - direction - начальное направление движение змейки. Вправо.
        - next_direction - атрибут, отвечающий за следующее направление
        змейки. В начале игры = None.
        - last - атрибут, отвечающий за координаты последнего сегмента змейки.
        """
        super().__init__(body_color)
        self.reset()
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    @property
    def get_head_position(self) -> tuple[int, int]:
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def update_direction(self) -> None:
        """Обновляет направление движения змейки после нажатия на клавишу."""
        if self.next_direction:
            self.direction = self.next_direction

    def move(self):
        """Отвечает за движение змейки.

        Метод обновляет координаты головы змейки в рамках игрового пространства
        в зависимости от направления движения direction.
        """
        # Приращение координат в зависимости от направления:
        dx, dy = self.direction
        dx *= GRID_SIZE
        dy *= GRID_SIZE
        # Новые координаты головы:
        head_x, head_y = self.get_head_position
        new_head_x = (head_x + dx) % SCREEN_WIDTH
        new_head_y = (head_y + dy) % SCREEN_HEIGHT
        self.new_get_head_position = (new_head_x, new_head_y)
        # Добавление головы с новыми координатами и исключение последнего
        # сегмента тела змейки:
        self.positions.insert(0, self.new_get_head_position)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self) -> None:
        """Отрисовка змейки."""
        # Цикл, рисующий единичную клетку для каждого элемента списка сегментов
        # змейки, кроме головы змейки:
        for position in self.positions[1:]:
            self.draw_cell(position, self.body_color)

        # Отрисовка головы змейки:
        self.draw_cell(self.get_head_position, self.body_color)

        # Затирание последнего сегмента:
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
            self.last = None

    def reset(self):
        """Задает начальные параметры змейки."""
        self.length = 1
        self.positions = [(ZERO_POSITION)]
        self.direction = choice((LEFT, RIGHT, UP, DOWN))
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(game_object):
    """Обрабатывает действия пользователя."""
    # Словарь для кнопок, отвечающих за направление движения. В значениях
    # словаря кортеж следующего и "запрещенного" направления - в которое змейка
    # не может передвинуться из текущего направления.
    direct_keys = {
        pygame.K_UP: (UP, DOWN),
        pygame.K_DOWN: (DOWN, UP),
        pygame.K_LEFT: (LEFT, RIGHT),
        pygame.K_RIGHT: (RIGHT, LEFT)
    }

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

        if event.type == pygame.KEYDOWN:
            if event.key in direct_keys:
                next_direction, prohibited_direction = direct_keys[event.key]
                if game_object.direction != prohibited_direction:
                    game_object.next_direction = next_direction


def main():
    """Функция управления игрой."""
    pygame.init()

    apple = Apple(APPLE_COLOR)
    snake = Snake(SNAKE_COLOR)

    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Проверка съедения яблока:
        if apple.position == snake.get_head_position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        # Проверка съедения себя:
        if snake.get_head_position in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake.positions)

        # Отрисовка объектов:
        snake.draw()
        apple.draw()
        pygame.display.update()
        clock.tick(SPEED)


if __name__ == '__main__':
    main()
