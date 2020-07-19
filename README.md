# tamcolors

![icon](https://github.com/cmcmarrow/tamcolors/blob/master/icon.png?raw=true)

## Installation
`pip install tamcolors`

## Hello World!
```python
import tamcolors
tamcolors.printc("Hello", "World!", ("light blue", "white"), same_color=True)
name = tamcolors.inputc("Whats Your Name? >>> ", (2, 7))
tamcolors.clear()
tamcolors.printc("Hello, ", ("white", "red"), name, ("light aqua", "gray"), "!", ("gray", "light aqua"), sep="")
```
