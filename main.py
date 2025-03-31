import pygame
from GameModel import GameModel
from GameView import GameView
from GameController import GameController
from SoundEffect import SoundEffect
from TextInput import TextInput


def show_name_input_screen(screen):
    input_box = TextInput(250, 300, 300, 50)
    clock = pygame.time.Clock()

    while not input_box.done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            input_box.handle_event(event)

        screen.fill((30, 30, 30))
        input_box.draw(screen)
        pygame.display.flip()
        clock.tick(30)

    return input_box.text if input_box.text.strip() != "" else "Player"


if __name__ == "__main__":
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
    pygame.init()

    # Create temporary screen for name input
    temp_screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Whack A Mole - Enter Your Name")
    player_name = show_name_input_screen(temp_screen)

    if player_name is None:
        pygame.quit()
        exit()

    # Initialize main game
    model = GameModel()
    model.player_name = player_name

    view = GameView(model)
    sound = SoundEffect()
    controller = GameController(model, view, sound)

    # Set game window title
    pygame.display.set_caption(f"Whack A Mole - Player: {player_name}")

    controller.run()
    pygame.quit()