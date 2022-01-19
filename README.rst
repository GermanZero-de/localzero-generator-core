Localzero Generator Core
=========================
TODO: Write some text


How to get coding
-----------------

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
