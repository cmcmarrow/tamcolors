import tamcolors


def run():
    tamcolors.printc("Hello", "World!", ("light blue", "white"), same_color=True)
    name = tamcolors.inputc("Whats Your Name? >>> ", ("light aqua", "gray"))
    tamcolors.clear()
    tamcolors.printc("Hello, ", ("default", "default"), name, (2, 7), "!", ("gray", "light aqua"), sep="")
