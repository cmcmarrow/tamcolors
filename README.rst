# tamcolors	

![icon](https://github.com/cmcmarrow/tamcolors/blob/master/icon.png?raw=true)	

## Installation	
`pip install tamcolors`	

## Basic Example	
```python	
import tamcolors	
tamcolors.examples.basic.run()	
```	
```python	
import tamcolors	
tamcolors.printc("Hello", "World!", ("light blue", "white"), same_color=True)	
name = tamcolors.inputc("Whats Your Name? >>> ", ("light aqua", "gray"))	
tamcolors.clear()	
tamcolors.printc("Hello, ", ("white", "red"), name, (2, 7), "!", ("gray", "light aqua"), sep="")	
```	

## Icon Example	
```python	
import tamcolors	
tamcolors.examples.icon.run()	
```	
```python	
from tamcolors import tam, tam_tools, tam_io	
class BootLogo(tam.tam_loop.TAMFrame):	
    def __init__(self):	
        super().__init__(fps=10,	
                         char=" ",	
                         foreground_color=2,	
                         background_color=0,	
                         min_width=70, max_width=70, min_height=40, max_height=40)	
        self.icon = tam_tools.tam_fade.tam_fade_in(buffer=tam_tools.tam_icon.get_icon(),	
                                                   char=" ",	
                                                   foreground_color=tam_io.tam_colors.BLACK,	
                                                   background_color=tam_io.tam_colors.BLACK)	
        self.wait = 10	
    def update(self, tam_loop, keys, loop_data):	
        if not self.icon.done():	
            self.icon.slide()	
        else:	
            self.wait -= 1	
        if self.wait == 0:	
            tam_loop.done()	
    def draw(self, tam_buffer, loop_data):	
        tam_buffer.clear()	
        tam_buffer.draw_onto(self.icon.peak(),	
                             *tam_tools.tam_placing.center(x=35, y=15, buffer=self.icon.peak()))	
        tam_tools.tam_print.tam_print(tam_buffer, *tam_tools.tam_placing.center(x=35,	
                                                                                y=28,	
                                                                                width=len("tamcolors"),	
                                                                                height=1),	
                                      text="tamcolors",	
                                      foreground_color=tam_io.tam_colors.LIGHT_WHITE,	
                                      background_color=tam_io.tam_colors.BLACK)	
tam.tam_loop.TAMLoop(BootLogo()).run()	
```