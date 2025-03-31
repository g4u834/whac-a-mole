import pygame


class TextInput:
    def __init__(self, x, y, width, height, font_size=32):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = pygame.Color('lightskyblue3')
        self.active_color = pygame.Color('dodgerblue2')
        self.text = ''
        self.font = pygame.font.Font(None, font_size)
        self.active = False
        self.done = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
            self.color = self.active_color if self.active else pygame.Color('lightskyblue3')

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.done = True
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 2)
        text_surface = self.font.render(self.text, True, pygame.Color('white'))
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))

        label_font = pygame.font.Font(None, 36)
        label = label_font.render("Enter your name:", True, pygame.Color('white'))
        screen.blit(label, (self.rect.x, self.rect.y - 40))