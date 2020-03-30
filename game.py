import pygame

import config
import objects
import players


class Game(object):
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()

        dimensions = [config.board['width'], config.board['height']]
        self.screen = pygame.display.set_mode(dimensions)
        self.running = False

        self.background = None
        self.player1 = self.player2 = None
        self.ball = None

        self._to_draw = None
        self._to_move = None
        self._to_react = None
        self.humans = None
        self.AIs = None

    def new_game(self):
        # Reset objects
        self.background = objects.Background()
        self.humans = []
        self.AIs = []
        self.scorecard = objects.ScoreCard()

        # Re-init containters
        self._to_draw = list()
        self._to_move = list()
        self._to_react = list()

        # Init and register game objects
        self.ball = objects.Ball(position='random', velocity='random')
        self._to_draw.append(self.ball)
        self._to_move.append(self.ball)

        self.player1 = players.HumanPlayer(side='left')
        self.player2 = players.AIPlayer(side='right')

        self._register_player(self.player1)
        self._register_player(self.player2)

        self._loop()

    def quit(self):
        pygame.quit()

    def _register_player(self, player):
        if players.is_human(player):
            self.humans.append(player)
            title = objects.PlayerTitle('Human', player.side)
        elif players.is_AI(player):
            self.AIs.append(player)
            title = objects.PlayerTitle('PongBot', player.side)

        self._to_react.append(player)
        self._to_move.append(player)
        self._to_draw.append(player)
        self._to_draw.append(title)

    def _loop(self):

        self.running = True
        while self.running:
            self._events()
            self._physics()
            self._move()
            self._draw()

            pygame.display.update()
            self.clock.tick(60)

    def _events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False
                break
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.running = pause()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_i:
                import pdb; pdb.set_trace()

            [human.react_to(event=event) for human in self.humans]
        [AI.react_to(ball=self.ball) for AI in self.AIs]

    def _physics(self):
        if self.player1.rect.colliderect(self.ball):
            self.ball.bounce_x()
            self.ball.rect.x = self.player1.rect.right

        if self.player2.rect.colliderect(self.ball):
            self.ball.bounce_x()
            self.ball.rect.right = self.player2.rect.x

        if self.ball.is_beyond_left():
            self.ball.bounce_x()
            self.scorecard.right_win()
        elif self.ball.is_beyond_right():
            self.ball.bounce_x()
            self.scorecard.left_win()

        if self.ball.is_beyond_top() or self.ball.is_beyond_bottom():
            self.ball.bounce_y()

    def _move(self):
        self.ball.move()
        self.player1.move()
        self.player2.move()

    def _draw(self):
        self.background.draw(self.screen)
        self.scorecard.draw(self.screen)

        [obj.draw(self.screen) for obj in self._to_draw]

        trajectory = self.ball.get_trajectory()
        trajectory.draw(self.screen)


def pause():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return True


def main():
    game = Game()
    pygame.display.set_caption('PyPong')
    game.new_game()

    play_again = False

    while play_again:
        game.new_game()

    game.quit()


if __name__ == "__main__":
    main()
