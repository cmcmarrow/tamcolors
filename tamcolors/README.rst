#########
tamcolors
#########

|Icon|
|TotalDownloads| |WeekDownloads| |Python3| |License|

*********************
pip install tamcolors
*********************

********************
table tennis example
********************
.. code-block:: python

   import tamcolors
   tamcolors.examples.tabletennis.run()

*************
basic example
*************
.. code-block:: python

   import tamcolors
   tamcolors.examples.basic.run()

.. code-block:: python

   import tamcolors
   tamcolors.printc("Hello", "World!", ("light blue", "white"), same_color=True)
   name = tamcolors.inputc("Whats Your Name? >>> ", ("light aqua", "gray"))
   tamcolors.clear()
   tamcolors.printc("Hello, ", ("white", "red"), name, (2, 7), "!", ("gray", "light aqua"), sep="")

************
icon example
************
.. code-block:: python

   import tamcolors
   tamcolors.examples.icon.run()

.. code-block:: python

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

**************************************
versions of Python currently supported
**************************************
* 3.8
* 3.7
* 3.6
* 3.5

*******************
platforms tested on
*******************
* Windows 10
* Ubuntu 20.04
* macOS 10.15.5


***************
long term goals
***************
* build a community that builds fun terminal games
* support color modes larger than 16
* make windows run more efficient
* text editor
* .ci testing


*****
goals
*****
* support Solaris
* support FreeBSD

***********
1.0.3 goals
***********
* add documentation
* write more examples
* remove duplicate files
* bdist_wheel for macOS
* implement a better clear function for Linux
* add tests for tam_basic
* implement console default colors

********
versions
********

=====
1.0.2
=====
* 7/22/2020
* tamcolors is now very usable
* bdist_wheel for Windows
* added non interrupting keyboard input
* added TAMLoop
* added tam_tools
* added tests
* supports Python 3.8
* supports Python 3.7
* supports Python 3.6
* supports Python 3.5


=====
0.2.0
=====
* 2/1/2018
* tamcolors proof of concept
* added printc
* added inputc
* added textBuffer
* supports Python 3.6

.. |Icon| image:: https://raw.githubusercontent.com/cmcmarrow/tamcolors/master/icon.png
.. |TotalDownloads| image:: https://pepy.tech/badge/tamcolors
.. |WeekDownloads| image:: https://pepy.tech/badge/tamcolors/week
.. |Python3| image:: https://img.shields.io/badge/python-3-blue
.. |License| image:: https://img.shields.io/pypi/l/tamcolors
