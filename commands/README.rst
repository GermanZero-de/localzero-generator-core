
Devtools
=========================
# TODO list useful devtools

Regarding Data
------------------------
**Checks out the production version of the reference data and if necessary clones them first**

.. code-block:: console

	poetry shell
	python devtool.py data checkout



Regarding Generator
------------------------
**Run the generator and save the results in a file called output.json**

.. code-block:: console

    poetry shell
    python devtool.py run -o output.json