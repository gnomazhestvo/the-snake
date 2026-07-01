"""Змейка."""
from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT: tuple[int, int] = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject():
    """Класс для объектов игры."""

    def __init__(
            self,
            body_color: tuple[int, int, int] = BOARD_BACKGROUND_COLOR
            ) -> None:
        """Инициализация параметров."""
        self.body_color = body_color
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def draw(self):
        """Отрисовка объекта, будет определен в дочерних классах."""
        pass


class Apple(GameObject):
    """Класс для объекта яблока."""

    def __init__(
            self,
            body_color: tuple[int, int, int] = APPLE_COLOR
            ) -> None:
        super().__init__(body_color)
        self.position = self.randomize_position()

    def randomize_position(self) -> tuple[int, int]:
        """Перемещает яблоко из (0, 0) в случайную точку в сетке."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )
        return self.position

    def draw(self) -> None:
        """Отрисовывает яблоко на экране в позиции position."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для объекта змейки."""

    def __init__(
            self,
            body_color: tuple[int, int, int] = SNAKE_COLOR
            ) -> None:
        """Инициализация параметров змейки."""
        super().__init__(body_color)
        self.length = 1  # При иницилазиации длина змейки - 1.
        # Голова змейки в центре экрана:
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT  # Изначально движется вправо.
        self.next_direction = None  # Создается атрибут следующего шага.
        self.last = None  # Создается атрибут хвоста, который нужно стереть.

    def get_head_position(self) -> tuple[int, int]:
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Обновляет направление движения после нажатия на клавишу."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет координаты всех сегментов змейки."""
        dx = self.direction[0] * GRID_SIZE
        dy = self.direction[1] * GRID_SIZE
        # Вычисляет новые координаты головы в зависимости от направления:
        new_x = (self.positions[0][0] + dx) % SCREEN_WIDTH
        new_y = (self.positions[0][1] + dy) % SCREEN_HEIGHT
        self.new_position = (new_x, new_y)
        # Добавляет в список сегментов голову с новыми координатами...
        self.positions.insert(0, self.new_position)
        # ...и стирает хвост:
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self):
        """Отрисовка змейки."""
        for position in self.positions[1:]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
            self.last = None

    def reset(self):
        """Сбрасывает параметры змейки к изначальным."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = choice((LEFT, RIGHT, UP, DOWN))


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Функция управления игрой."""
    pygame.init()

    apple = Apple(APPLE_COLOR)
    snake = Snake(SNAKE_COLOR)

    while True:
        screen.fill(BOARD_BACKGROUND_COLOR)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        # проверка съедения яблока:
        if apple.position == snake.positions[0]:
            snake.length += 1
            apple.randomize_position()
        # проверка съедения себя:
        if snake.positions[0] in snake.positions[1:]:
            snake.reset()
            apple.randomize_position()
        snake.draw()
        apple.draw()
        pygame.display.update()
        clock.tick(SPEED)
        # проверка змейка съела яблоко


if __name__ == '__main__':
    main()
