#########
tamcolors
#########

|Icon|
|TotalDownloads| |WeekDownloads| |Python3| |License| |Docs|

*********************
pip install tamcolors
*********************

********************
links
********************
* `github`_
* `pypi`_
* `read the docs`_
* `youtube`_

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
   from tamcolors.tam_io.tam_colors import *
   tamcolors.printc("Hello", "World!", ("light blue", "white"), same_color=True)
   name = tamcolors.inputc("Whats Your Name? >>> ", ("light aqua", "gray"))
   tamcolors.clear()
   tamcolors.printc("Hello, ", ("default", "default"), name, (GREEN, WHITE), "!", ("gray", "light aqua"), sep="")

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
                            foreground_color=tam_io.tam_colors.GREEN,
                            background_color=tam_io.tam_colors.BLACK,
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
* 3.9
* 3.8
* 3.7
* 3.6

*******************
platforms tested on
*******************
* Windows 10
* Ubuntu 20.04
* macOS 10.15.5

*****************
support tamcolors
*****************
* `paypal`_

***************
long term goals
***************
* build a community that builds fun terminal games
* text editor
* .ci testing
* make and change fonts at run time
* add .wav support

*****
goals
*****
* support Solaris
* support FreeBSD

***********
1.1.2 goals
***********
* add more io driver tests
* add TCP IO (dummy console)
* save/rest Windows buffer size on exit
* clean up c/c++
* supports Python 3.9
* supports Python 3.8
* supports Python 3.7
* supports Python 3.6

***********************
what defines a release?
***********************
* x.?.? - tamcolors has matured to a new level of capability.
* ?.x.? - Backwards compatibility was broken for most programs.
* ?.?.x - Most programs should still run in this release.
* All releases can have new features, bug fixes, depreciation and new tests.
* Any release older than 1.0.2 does not fallow this release pattern.

********
versions
********

*****
1.1.1
*****
* 10/10/2020
* added tam utils
* added compress utils module
* added encryption utils module
* added identifier utils module
* added log utils module
* added transport optimizer utils module
* added immutable cache utils module
* added slow tests
* added tcp utils utils module
* fixed macOS terminal cursor
* fixed windows missing dll
* added dependencies licences
* supports Python 3.9
* supports Python 3.8
* supports Python 3.7
* supports Python 3.6

*****
1.1.0
*****
* 9/7/2020
* fixed macOS!
* broke up IO into drivers
* added terminal identifier
* added 256 color mode
* added rgb color mode
* added RGBA
* added Color
* supports Python 3.8
* supports Python 3.7
* supports Python 3.6

*****
1.0.4
*****
* 8/13/2020
* added more examples
* bdist_wheel for Linux
* cleaned up win_tam, uni_tam and any_tam
* added alpha color for TAMBuffer
* set and get rgb value of color (fixed PowerShell colors)
* supports Python 3.8
* supports Python 3.7
* supports Python 3.6
* dropped support for Python 3.5

*****
1.0.3
*****
* 7/29/2020
* tamcolors
* bdist_wheel for macOS
* added more examples
* added documentation
* added tests for tam_basic
* added default console colors
* supports Python 3.8
* supports Python 3.7
* supports Python 3.6
* supports Python 3.5

*****
1.0.2
*****
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

*****
0.2.0
*****
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
.. |Docs| image:: https://readthedocs.org/projects/tamcolors/badge/?version=latest

.. _github: https://github.com/cmcmarrow/tamcolors
.. _pypi: https://pypi.org/project/tamcolors
.. _read the docs: https://tamcolors.readthedocs.io/en/latest/
.. _youtube: https://www.youtube.com/channel/UCgPjVibjJHFHuTZ0_xeq_HQ
.. _paypal: https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=DUKDNFSAWDKFE&source=url
