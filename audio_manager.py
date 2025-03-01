import pygame

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.music = None

    def load_sound(self, name, filepath):
        self.sounds[name] = pygame.mixer.Sound(filepath)

    def play_sound(self, name, loops=0):
        if name in self.sounds:
            self.sounds[name].play(loops=loops)

    def stop_sound(self, name):
        if name in self.sounds:
            self.sounds[name].stop()

    def load_music(self, filepath):
        self.music = filepath

    def play_music(self, loops=-1):
        if self.music:
            pygame.mixer.music.load(self.music)
            pygame.mixer.music.play(loops=loops)

    def stop_music(self):
        pygame.mixer.music.stop()

    def set_music_volume(self, volume):
        pygame.mixer.music.set_volume(volume)

    def set_sound_volume(self, name, volume):
        if name in self.sounds:
            self.sounds[name].set_volume(volume)