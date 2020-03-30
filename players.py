import pygame

import config
import objects


starting_positions = dict(
    left=(10, config.board['height'] / 2),
    right=(config.board['width'] - 20, config.board['height'] / 2)
)


def is_AI(player):
    return isinstance(player, AIPlayer)


def is_human(player):
    return isinstance(player, HumanPlayer)


class Player(objects.Paddle):
    def __init__(self, side):
        if side not in config.player_sides:
            raise ValueError(f'Side must be in: {config.player_sides}')

        super().__init__(starting_positions[side])

        self.side = side
        self.controls = config.control_sets[side]
        self.last_key = None

    def move(self):
        if self.last_key is None:
            pass
        elif self.last_key == self.controls['down']:
            super().move(delta_y=1 * self.speed)
        elif self.last_key == self.controls['up']:
            super().move(delta_y=-1 * self.speed)
        elif self.last_key == self.controls['left'] and False:
            super().move(delta_x=-1 * self.speed)
        elif self.last_key == self.controls['right'] and False:
            super().move(delta_x=1 * self.speed)


class HumanPlayer(Player):
    def react_to(self, **kwargs):
        event = kwargs.get('event', None)

        if event is None:
            return

        is_key_pressed = event.type == pygame.KEYDOWN
        is_key_released = event.type == pygame.KEYUP

        if is_key_pressed and event.key in self.controls.values():
            self.last_key = event.key
        elif is_key_released and event.key in self.controls.values():
            self.last_key = None


class AIPlayer(Player):
    def react_to(self, **kwargs):
        ball = kwargs.get('ball', None)

        if ball is None:
            return

        vert_dist = self.get_vertical_distance(ball)

        if vert_dist > 0:
            self.last_key = self.controls['down']
        elif vert_dist < 0:
            self.last_key = self.controls['up']
        elif round(vert_dist, 0) == 0:
            self.last_key = None

    def get_vertical_distance(self, ball):
        ball_pos = ball.rect.center
        my_pos = self.rect.center

        return ball_pos[1] - my_pos[1]
