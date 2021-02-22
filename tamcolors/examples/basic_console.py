from tamcolors.tam_basic import console
from tamcolors.tam_io.tam_colors import *


def run():
    console.printc("Hello", "World!", ("light blue", "white"), same_color=True)
    name = console.inputc("Whats Your Name? >>> ", ("light aqua", "gray"))
    console.clear()
    console.printc("Hello, ", ("default", "default"), name, (GREEN, WHITE), "!", ("gray", "light aqua"), sep="")
