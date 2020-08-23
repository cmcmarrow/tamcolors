import tamcolors
from tamcolors.tam_io.tam_colors import *


def run():
    tamcolors.printc("Hello", "World!", ("light blue", "white"), same_color=True)
    name = tamcolors.inputc("Whats Your Name? >>> ", ("light aqua", "gray"))
    tamcolors.clear()
    tamcolors.printc("Hello, ", ("default", "default"), name, (GREEN, WHITE), "!", ("gray", "light aqua"), sep="")
