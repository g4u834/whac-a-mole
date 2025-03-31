import random


class GameModel:
    def __init__(self):
        # Constants
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.FPS = 60
        self.MOLE_WIDTH = 90
        self.MOLE_HEIGHT = 81
        self.FONT_SIZE = 31
        self.FONT_TOP_MARGIN = 26
        self.LEVEL_SCORE_GAP = 4
        self.LEFT_MOUSE_BUTTON = 1

        self.hole_positions = [
            (381, 295), (119, 366), (179, 169), (404, 479),
            (636, 366), (658, 232), (464, 119), (95, 43), (603, 11)
        ]

        # Game state
        self.score = 0
        self.misses = 0
        self.level = 1
        self.running = True

        # Animation state
        self.cycle_time = 0.0
        self.current_frame = -1
        self.is_down = False
        self.interval = 0.1
        self.initial_interval = 1.0
        self.current_hole_index = 0
        self.left_offset = 0

        self.player_name = "Player"  # שם ברירת מחדל

        self.max_misses = 10  # מספר הפיספוסים המקסימלי

    def calculate_level(self):
        new_level = 1 + int(self.score / self.LEVEL_SCORE_GAP)
        if new_level != self.level:
            self.level = new_level
            return True
        return False

    def get_interval_by_level(self):
        new_interval = self.initial_interval - self.level * 0.15
        return max(new_interval, 0.05)

    def check_hit(self, mouse_pos):
        if self.current_frame <= 0 or self.left_offset != 0:
            return False
        hole_x, hole_y = self.hole_positions[self.current_hole_index]
        mouse_x, mouse_y = mouse_pos
        return (hole_x <= mouse_x <= hole_x + self.MOLE_WIDTH and
                hole_y <= mouse_y <= hole_y + self.MOLE_HEIGHT)

    def start_new_mole(self):
        self.current_frame = 0
        self.is_down = False
        self.interval = 0.5
        self.current_hole_index = random.randint(0, 8)
        self.left_offset = 0
        return True

    def reset_mole(self):
        self.current_frame = -1
        self.left_offset = 0

    def advance_animation(self, delta_time):
        self.cycle_time += delta_time
        if self.cycle_time > self.interval:
            self.cycle_time = 0
            if self.current_frame > 5:
                self.reset_mole()
                return "reset"
            elif self.current_frame == -1:
                self.start_new_mole()
                return "new_mole"
            else:
                if not self.is_down:
                    self.current_frame += 1
                else:
                    self.current_frame -= 1

                if self.current_frame == 4:
                    self.interval = 0.3
                elif self.current_frame == 3:
                    self.current_frame -= 1
                    self.is_down = True
                    self.interval = self.get_interval_by_level()
                    return "pop"
                else:
                    self.interval = 0.1
            return "advance"
        return None

    def is_game_over(self):
        return self.misses >= self.max_misses

    def reset(self):
        self.score = 0
        self.misses = 0
        self.level = 1
        self.current_frame = -1
        self.left_offset = 0