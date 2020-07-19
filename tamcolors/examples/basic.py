import tamcolors


def run():
    tamcolors.printc("Hello", "World!", ("light blue", "white"), same_color=True)
    name = tamcolors.inputc("Whats Your Name? >>> ", (2, 7))
    tamcolors.clear()
    tamcolors.printc("Hello, ", ("white", "red"), name, ("light aqua", "gray"), "!", ("gray", "light aqua"), sep="")
