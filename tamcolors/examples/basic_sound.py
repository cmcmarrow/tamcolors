from time import sleep
from tamcolors.utils.path import abspath
from tamcolors.tam_basic.sound import Sound


def run():
    with Sound(abspath("typing.wav")) as s:
        s.play()
        s2 = Sound(abspath("tally.wav"))
        s2.play()
        sleep(5)
        s.play()
        s2.play()
        sleep(5)
        s2.close()
