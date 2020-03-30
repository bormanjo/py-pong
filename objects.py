import math
import pygame
import random

import config


class GameObject(object):
    def __init__(self, position, dimensions, color=config.black):
        self.pos = position
        self.dim = dimensions
        self.color = color

        self.rect = pygame.Rect(*self.pos, *self.dim)

        self.boundary = dict(
            top=0,
            left=0,
            right=config.board['width'],
            bottom=config.board['height']
        )

    def get_rect(self):
        return self.rect

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


class Background(GameObject):
    def __init__(self, color=config.white):
        super().__init__((0, 0), (config.board['width'], config.board['height']), color)


class Movable(GameObject):
    def __init__(self, position, dimensions, color=config.black):
        super().__init__(position, dimensions, color)

    def is_beyond_left(self, delta_x=0):
        return self.rect.x + delta_x < self.boundary['left']

    def is_beyond_right(self, delta_x=0):
        return (self.rect.x + self.dim[0]) + delta_x > self.boundary['right']

    def is_beyond_top(self, delta_y=0):
        return self.rect.y + delta_y < self.boundary['top']

    def is_beyond_bottom(self, delta_y=0):
        return (self.rect.y + self.dim[1]) + delta_y > self.boundary['bottom']

    def move(self, delta_x=0, delta_y=0):
        self.rect.move_ip(delta_x, delta_y)
        self.pos = self.rect.topleft


class Paddle(Movable):
    def __init__(self, position=(0, 0)):
        super().__init__(position, (10, 100))

        self.speed = 4

    def move(self, delta_x=0, delta_y=0):
        if self.is_beyond_left(delta_x) or self.is_beyond_right(delta_x):
            delta_x = 0
        if self.is_beyond_top(delta_y) or self.is_beyond_bottom(delta_y):
            delta_y = 0

        super().move(delta_x, delta_y)


class Ball(Movable):
    def __init__(self, position=(60, 60), velocity=[1, 0]):
        if position == 'random':
            position = self.get_random_start()
        if velocity == 'random':
            velocity = self.get_random_velocity()

        super().__init__(position, (15, 15))

        self.velocity = velocity

    def __repr__(self):
        return f'({self.pos}) moving ({self.velocity})'

    def __str__(self):
        return self.__repr__()

    def move(self):
        super().move(*self.velocity)

    def bounce_x(self):
        self.velocity[0] = -self.velocity[0]

    def bounce_y(self):
        self.velocity[1] = -self.velocity[1]

    def get_next_bounce(self):
        pass

    def get_trajectory(self):
        # Get the coordinates of the object center
        obj_center = self.rect.center

        # Calculate the path
        m = self.velocity[1] / self.velocity[0]
        b = (-m * obj_center[0]) + obj_center[1]
        path = Line(m, b)

        # Get the line segment of the path to be traveled
        x = 0 if self.velocity[0] < 0 else self.boundary['right']
        end_point = (x, path.solve_y(x=x))

        return LineSegment(obj_center, end_point)

    @staticmethod
    def get_random_start():
        x = round(config.board['width'] / 2, 0)
        y = random.randint(0, config.board['height'])
        return (x, y)

    @staticmethod
    def get_random_velocity(speed=5):
        quadrant = random.randint(1, 4)
        x_dir = -1 if quadrant in [2, 3] else 1
        y_dir = -1 if quadrant in [3, 4] else 1
        theta = random.randint(35, 55)

        v_x = round(x_dir * math.cos(theta) * speed, 0)
        v_y = round(y_dir * math.sin(theta) * speed, 0)
        return [v_x, v_y]


class Line(object):
    def __init__(self, m, b, color=(255, 0, 0)):
        self.m = m
        self.b = b
        self.color = color

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f'y = {self.m} * x + {self.b}'

    def solve_y(self, x):
        return (self.m * x) + self.b

    def solve_x(self, y):
        return (y - self.b) / self.m

    def draw(self, screen):
        x = screen.get_width()
        start = (0, self.b)
        end = (x, self.m * x + self.b)
        pygame.draw.line(screen, self.color, start, end)


class LineSegment(Line):
    def __init__(self, point_a, point_b, color=(255, 0, 0)):
        self.A = point_a
        self.B = point_b
        self.color = color

    def __repr__(self):
        return f'Segment {self.A} to {self.B}'

    def draw(self, screen):
        pygame.draw.line(screen, self.color, self.A, self.B)


class TextObject(object):
    def __init__(self, text, position, **kwargs):
        font_name = kwargs.get('font', 'freesansbold.ttf')
        font_size = kwargs.get('size', 32)
        self.font = pygame.font.Font(font_name, font_size)

        self.text = text
        self.position = position

        self.text_color = kwargs.get('text_color', config.blue)
        self.background = kwargs.get('background', config.white)

    def draw(self, screen):
        text_surface = \
            self.font.render(self.text, True, self.text_color, self.background)

        surface_rect = text_surface.get_rect()
        surface_rect.center = self.position

        screen.blit(text_surface, surface_rect)


class PlayerTitle(TextObject):
    def __init__(self, title, side, **kwargs):
        if side not in config.player_sides:
            raise ValueError(f'Side must be in: {config.player_sides}')
        elif side == 'left':
            x = round(config.board['width'] * 1.0 / 5.0, 0)
        elif side == 'right':
            x = round(config.board['width'] * 4.0 / 5.0, 0)

        super().__init__(title, (x, 20))


class ScoreCard(TextObject):
    def __init__(self, left_score=0, right_score=0, **kwargs):
        self.left_score = left_score
        self.right_score = right_score
        text = self.get_text()
        position = (config.board['width'] // 2, 20)

        super().__init__(text, position, **kwargs)

    def get_text(self):
        return f'{self.left_score} | {self.right_score}'

    def left_win(self):
        self.left_score += 1
        self.text = self.get_text()

    def right_win(self):
        self.right_score += 1
        self.text = self.get_text()