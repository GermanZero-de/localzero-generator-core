
.. image:: https://github.com/GermanZero-de/localzero-generator-core/workflows/test/badge.svg
    :target: https://github.com/GermanZero-de/localzero-generator-core/actions?query=workflow%3Atest+branch%3Amain

Localzero Generator Core
=========================
This contains the calcuation. It should neither contain reference data
nor anything that is specific to the website.

Special cases
--------------
Here are some interesting special cases to note that were found when we tried to run
over all AGSes in Germany:

03255508
    https://de.wikipedia.org/wiki/Wenzen_(gemeindefreies_Gebiet). No population. But that is given
	in the population datasets as blank not as 0.

Install environment
=========================
- install Python 3.10.
- install Git
- install Poetry from https://python-poetry.org/docs/
    - on windows run this inside a power shell:
      :code:`(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python`

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
	- on windows: install Node.js (necessary for pyright)

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
    python devtool.py run -o output.json

Testing
-------

We use :code:`pytest` (the tests are in the directory `tests`).  We used to run a lot of
tests automatically in github actions, but sadly it turned out that they easily used more
than 2000 minutes every month (mostly because of the overhead involved in recreating
the local development environment inside github).

So now we rely on a little discipline enforced by peer pressure. When you make changes
you should run :code:`ready-to-rock.sh` before you push.  And you are only ready to push
if it outputs: :code:`I'm ready to rock and save the climate`. Please include the output
of the tool in your feature description like this:

.. code-block:: console

	(generatorcore-s105jb49-py3.10) --- localzero/localzero-generator-core ‹disable-github-actions› » ./ready-to-rock.sh
	============================================================== test session starts ==============================================================
	platform darwin -- Python 3.10.1, pytest-6.2.5, py-1.11.0, pluggy-1.0.0
	rootdir: /Users/benediktgrundmann/SynologyDrive/Programming/localzero/localzero-generator-core
	collected 7 items

	tests/test_end_to_end.py ......                                                                                                           [ 85%]
	tests/test_entries.py .                                                                                                                   [100%]

	=============================================================== 7 passed in 2.43s ===============================================================
	Trim Trailing Whitespace.................................................Passed
	Mixed line ending........................................................Passed
	Check for case conflicts.................................................Passed
	Check Yaml...............................................................Passed
	Check for added large files..............................................Passed
	Don't commit to branch...................................................Passed
	black....................................................................Passed
	I'm ready to rock and save the climate

