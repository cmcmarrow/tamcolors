#########
tamcolors
#########

|Icon|

|TotalDownloads| |WeekDownloads| |Python3| |License| |Docs| |Tests|

*****
about
*****
tamcolors is a terminal game library which supports multiplayer and audio.
tamcolors gives a buffer which lets the user set the character, foreground color and background color which can draw at a stable FPS of 25 on all supported console.

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
* `patreon`_
* `facebook`_

********************
table tennis example
********************
|TableTennis|

.. code-block:: python

   import tamcolors
   tamcolors.examples.tabletennis.run()

*************
basic example
*************
|BasicExample|

.. code-block:: python

   import tamcolors
   tamcolors.examples.basic_console.run()

.. code-block:: python

   from tamcolors.tam_basic import console
   from tamcolors.tam_io.tam_colors import *
   console.printc("Hello", "World!", ("light blue", "white"), same_color=True)
   name = console.inputc("Whats Your Name? >>> ", ("light aqua", "gray"))
   console.clear()
   console.printc("Hello, ", ("default", "default"), name, (GREEN, WHITE), "!", ("gray", "light aqua"), sep="")

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
                             min_width=57, max_width=57, min_height=20, max_height=20)

            self.icon = tam_tools.tam_fade.tam_fade_in(surface=tam_tools.tam_icon.get_icon(),
                                                       char=" ",
                                                       foreground_color=tam_io.tam_colors.BLACK,
                                                       background_color=tam_io.tam_colors.BLACK)
            self.wait = 10

        def update(self, tam_loop, keys, loop_data, *args):

            if not self.icon.done():
                self.icon.slide()
            else:
                self.wait -= 1

            if self.wait == 0:
                tam_loop.done()

        def draw(self, tam_surface, loop_data, *args):
            tam_surface.clear()

            tam_surface.draw_onto(self.icon.peak(), 0, 0)


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

***********
2.0.0 goals
***********
* add .wav support - Working on Windows!
* add .wav tests - In Progress
* add basic sound - Done
* add basic sound tests - Done
* update tamloop - In Progress
* update tamframe - In Progress
* add IO event bus - In Progress
* supports Python 3.9
* supports Python 3.8
* supports Python 3.7
* supports Python 3.6

***********
2.1.0 goals
***********
* add full keys state support for linux and MacOS
* add SPA, LAT, GER and FRE keyboard maps
* make and change fonts at run time
* add SHIFT KEY and other keys
* supports Python 3.9
* supports Python 3.8
* supports Python 3.7
* supports Python 3.6

***********
2.2.2 goals
***********
* update tamtools
* supports Python 3.9
* supports Python 3.8
* supports Python 3.7
* supports Python 3.6


***********
3.0.0 goals
***********
* clean up code
* mass changing of function names
* add more tests
* make docs user friendly
* add docs to wiki
* drop read the docs
* find new CI
* drop travis CI

.. |Icon| image:: https://raw.githubusercontent.com/cmcmarrow/tamcolors/master/photos/small_icon.png
.. |TableTennis| image:: https://raw.githubusercontent.com/cmcmarrow/tamcolors/master/photos/table_tennis.png
.. |BasicExample| image:: https://raw.githubusercontent.com/cmcmarrow/tamcolors/master/photos/basic_example.png
.. |TotalDownloads| image:: https://pepy.tech/badge/tamcolors
.. |WeekDownloads| image:: https://pepy.tech/badge/tamcolors/week
.. |Python3| image:: https://img.shields.io/badge/python-3-blue
.. |License| image:: https://img.shields.io/pypi/l/tamcolors
.. |Docs| image:: https://readthedocs.org/projects/tamcolors/badge/?version=latest
.. |Tests| image:: https://travis-ci.com/cmcmarrow/tamcolors.svg?branch=master

.. _github: https://github.com/cmcmarrow/tamcolors
.. _pypi: https://pypi.org/project/tamcolors
.. _read the docs: https://tamcolors.readthedocs.io/en/latest/
.. _youtube: https://www.youtube.com/channel/UCgPjVibjJHFHuTZ0_xeq_HQ
.. _patreon: https://www.patreon.com/tamcolors
.. _facebook: https://www.facebook.com/C4tamcolors
