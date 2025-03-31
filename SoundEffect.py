from pygame import mixer

class SoundEffect:
    def __init__(self):
        mixer.music.load("sounds/themesong.wav")
        self.fire = mixer.Sound("sounds/fire.wav")
        self.pop = mixer.Sound("sounds/pop.wav")
        self.hurt = mixer.Sound("sounds/hurt.wav")
        self.level = mixer.Sound("sounds/point.wav")
        mixer.music.play(-1)

    def playFire(self): self.fire.play()
    def playPop(self): self.pop.play()
    def playHurt(self): self.hurt.play()
    def playLevelUp(self): self.level.play()