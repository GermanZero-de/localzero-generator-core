Localzero Generator Core
=========================
This contains the calcuation. It should neither contain reference data
nor anything that is specific to the website.

Install environment
=========================
- install Python 3.10.
- install Git
- install Poetry from https://python-poetry.org/docs/

  On windows run this inside a power shell:
    - :code:`(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python`

- configure Git
	- Token:
		- https://github.com/settings/tokens:
		- create personal access token (repo, workflow, admin:org:read, gist)
		- save your token
		- On Windows Token add the token Windows Anmeldeinformationen (similar tools exist on linux and mac)
			- Generische Anmeldeinformationen hinzufügen (Adresse: git:https://github.com, Benutzername: Git Nutzername, Passwort: Token)
- get this Git Repo (if you haven't done so already)
	- :code:`git clone https://github.com/GermanZero-de/localzero-generator-core`

- install poetry and pre-commit
	- :code:`install-environment.sh`

- get the code repositories into your Data folder.

.. code-block:: console

	poetry shell
	python devtool.py data checkout

Black
-----
We use black to automatically format the code and thereby avoid any spurious merge
conflicts, due to layout differences. This will happen in a pre-commit automatically,
but to for the best experience you should configure your editor to do the same.

How to run the generator
------------------------

.. code-block:: console

    poetry shell
    python devtool.py run > output.json

Testing
-------

We use :code:`pytest` (the tests are in the directory `tests`). We run tests automatically when a
pull request is created, but you should run them yourself. Remember to run them in a poetry shell
or use :code:`poetry run`.