import pygame


class GameView:
    def __init__(self, model):
        self.model = model
        self.screen = pygame.display.set_mode((model.SCREEN_WIDTH, model.SCREEN_HEIGHT))
        self.background = pygame.image.load("images/bg.png")
        self.font = pygame.font.Font('./fonts/GROBOLD.ttf', model.FONT_SIZE)

        sprite_sheet = pygame.image.load("images/mole.png")
        self.mole_frames = [
            sprite_sheet.subsurface(169, 0, 90, 81),
            sprite_sheet.subsurface(309, 0, 90, 81),
            sprite_sheet.subsurface(449, 0, 90, 81),
            sprite_sheet.subsurface(575, 0, 116, 81),
            sprite_sheet.subsurface(717, 0, 116, 81),
            sprite_sheet.subsurface(853, 0, 116, 81)
        ]
        for i in range(len(self.mole_frames)):
            self.mole_frames[i].set_colorkey((0, 0, 0))
            self.mole_frames[i] = self.mole_frames[i].convert_alpha()


    def render(self):
        self.screen.blit(self.background, (0, 0))
        if self.model.current_frame != -1 and self.model.current_frame < len(self.mole_frames):
            frame = self.mole_frames[self.model.current_frame]
            pos = self.model.hole_positions[self.model.current_hole_index]
            self.screen.blit(frame, (pos[0] - self.model.left_offset, pos[1]))

        texts = [
            (f"PLAYER: {getattr(self.model, 'player_name', 'Player')}",
             (self.model.SCREEN_WIDTH // 6, self.model.FONT_TOP_MARGIN)),
            (f"SCORE: {self.model.score}", (self.model.SCREEN_WIDTH // 1.7, self.model.FONT_TOP_MARGIN)),
            (f"MISSES: {self.model.misses}", (self.model.SCREEN_WIDTH // 5 * 4, self.model.FONT_TOP_MARGIN)),
            (f"LEVEL: {self.model.level}", (self.model.SCREEN_WIDTH // 5 * 2, self.model.FONT_TOP_MARGIN))
        ]
        for text, pos in texts:
            text_surface = self.font.render(text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=pos)
            self.screen.blit(text_surface, text_rect)

        pygame.display.flip()