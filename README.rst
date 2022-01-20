Localzero Generator Core
=========================
This contains the calcuation. It should neither contain reference data
nor anything that is specific to the website.

How to get coding
=================

Poetry
------

If you want to develop the generator, it is recommended that you first
install poetry (https://python-poetry.org/docs/).  A good reasonably short
overview over poetry can be found here:
https://hackersandslackers.com/python-poetry-package-manager/

Then run :code:`poetry shell` in this directory (this creates a new virtualenv
containing the python 3.10 interpreter and activates it).  This step is
needed in any new terminal where you want to run python.

Then run :code:`poetry install` to (eh) install the dependencies. This step
is obviously a one time operation.

If you happen to use vscode (Visual Studio Code), then a good trick
is to start vscode for the first time with :code:`code .` in this terminal.
That way the editors builtin python support will pick up the virtualenv.
Alternatively use the :code:`Python: Select Interpreter` command.

Black
-----
We use black to automatically format the code and thereby avoid any spurious merge
conflicts, due to layout differences. This will happen in a pre-commit automatically,
but to for the best experience you should configure your editor to do the same.

How to run the generator
------------------------

.. code-block:: console
    python devtool.py run

But this will immediately fail, complaining that you don't have the necessary
data available.

Therefore you will have to checkout the proprietary and the public data
repositories into :code:`data/public` and :code:`data/proprietary` respectively.

Testing
-------

We use :code:`pytest` (the tests are in the directory `tests`). For now the
tests are also run inside a pre-commit hook, as that currently takes less
than 5seconds.  But if it will ever take longer we will change it to only run
when you try to push.