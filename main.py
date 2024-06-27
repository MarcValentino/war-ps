import asyncio

import pygame

from classes.Jukebox import Jukebox
from classes.MainMenu import MainMenu


def main():
    pygame.init()
    pygame.display.set_caption('War')
    jukebox = Jukebox()
    jukebox.add_song("classes/assets/Danger Loop.wav")
    jukebox.play()

    menu = MainMenu()
    menu.run()


if __name__ == '__main__':
    import cProfile

    cProfile.run('main()', 'output.dat')

    import pstats
    from pstats import SortKey

    with open('output_time.txt', 'w') as f:
        p = pstats.Stats('output.dat', stream=f)
        p.sort_stats('time').print_stats()

    with open('output_calls.txt', 'w') as f:
        p = pstats.Stats('output.dat', stream=f)
        p.sort_stats('calls').print_stats()
