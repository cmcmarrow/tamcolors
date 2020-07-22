tamcolors
=========

.. image:: icon.png
   :target: https://raw.githubusercontent.com/cmcmarrow/tamcolors/master/icon.png

pip install tamcolors
---------------------

.. code-block:: python
   import tamcolors
   tamcolors.examples.basic.run()

.. code-block:: python
   tamcolors.printc("Hello", "World!", ("light blue", "white"), same_color=True)
   name = tamcolors.inputc("Whats Your Name? >>> ", ("light aqua", "gray"))
   tamcolors.clear()
   tamcolors.printc("Hello, ", ("white", "red"), name, (2, 7), "!", ("gray", "light aqua"), sep="")
