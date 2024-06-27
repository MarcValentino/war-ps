import pygame


class Jukebox:
    _instance = None

    def __init__(self):
        self.current_index = 0

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            pygame.mixer.init()
            cls._instance.playlist = []
            cls._instance.current_index = -1
            cls._instance.volume = 0.5
            pygame.mixer.music.set_volume(cls._instance.volume)
        return cls._instance

    def add_song(self, song_path):
        self.playlist.append(song_path)

    def play(self):
        if self.playlist:
            self.current_index = (self.current_index + 1) % len(self.playlist)
            pygame.mixer.music.load(self.playlist[self.current_index])
            pygame.mixer.music.play()

    def is_playing(self):
        return pygame.mixer.music.get_busy()

    def check_event(self):
        if not self.is_playing():
            self.play()
    def run(self):
        self.add_song("classes/assets/Danger Loop.wav")
        self.play()
