.. tamcolors documentation master file, created by
   sphinx-quickstart on Fri Jul 24 22:58:31 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to tamcolors's documentation!
=====================================

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
   tamcolors.printc("Hello", "World!", ("light blue", "white"), same_color=True)
   name = tamcolors.inputc("Whats Your Name? >>> ", ("light aqua", "gray"))
   tamcolors.clear()
   tamcolors.printc("Hello, ", ("default", "default"), name, (2, 7), "!", ("gray", "light aqua"), sep="")

************
icon example
************
.. code-block:: python

   import tamcolors
   tamcolors.examples.icon.run()

.. toctree::
   :maxdepth: -1
   :caption: Contents:

   modules


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


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
