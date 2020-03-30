import pygame

white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
black = (0, 0, 0)


board = {
    'width': 600,
    'height': 600,
    'background': 'black'
}

player_sides = ('left', 'right')

control_sets = dict(
    left=dict(
        up=pygame.K_w,
        down=pygame.K_s,
        left=pygame.K_a,
        right=pygame.K_d
    ),
    right=dict(
        up=pygame.K_UP,
        down=pygame.K_DOWN,
        left=pygame.K_LEFT,
        right=pygame.K_RIGHT
    )
)
