import pygame
from GameOverView import GameOverView


class GameController:
    def __init__(self, model, view, sound):
        self.model = model
        self.view = view
        self.sound = sound

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.model.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == self.model.LEFT_MOUSE_BUTTON:
                self.sound.playFire()
                if self.model.check_hit(pygame.mouse.get_pos()):
                    self.model.score += 1
                    if self.model.calculate_level():
                        self.sound.playLevelUp()
                    self.sound.playHurt()
                    self.model.current_frame = 3
                    self.model.left_offset = 14
                    self.model.is_down = False
                    self.model.interval = 0
                else:
                    self.model.misses += 1

    def run(self):
        clock = pygame.time.Clock()
        game_over_view = GameOverView(self.model.SCREEN_WIDTH, self.model.SCREEN_HEIGHT)

        while True:
            if not self.model.is_game_over():
                self.handle_events()
                delta_time = clock.tick(self.model.FPS) / 1000.0
                result = self.model.advance_animation(delta_time)

                if result == "new_mole":
                    self.sound.playPop()
                elif result == "pop":
                    self.sound.playPop()

                self.view.render()
            else:
                # מצב game over
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.model.running = False
                        return
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.model.reset()
                        elif event.key == pygame.K_ESCAPE:
                            self.model.running = False
                            return

                # הצגת מסך הסיום
                game_over_view.draw(self.view.screen, self.model.score, getattr(self.model, 'player_name', 'Player'))
                pygame.display.flip()