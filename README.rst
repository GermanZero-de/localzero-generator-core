
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
		- ensure that git is in your PATH variable (needed for devtool.py data checkout later)
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

- get the git repositories into your Data folder.

  This will clone the git data repositories in the subfolders ./data/public and ./data/proprietary

  **ISSUE:** You might not have access to the proprietary repository,
  but the data generator cannot run without it. We are working on that.

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
you should run :code:`python devtool.py ready-to-rock` before you push.  And you are only ready to push
if it outputs: :code:`I'm ready to rock and save the climate`. Please include the output
of the tool in your feature description like this:

.. code-block:: console

	================================ test session starts ================================
	platform win32 -- Python 3.10.3, pytest-6.2.5, py-1.11.0, pluggy-1.0.0
	rootdir: C:\GermanZero\GitHub\localzero-generator-core
	plugins: cov-3.0.0
	collected 16 items

	tests\test_end_to_end.py ...........                                           [ 68%]
	tests\test_entries.py .                                                        [ 75%]
	tests\test_refdata.py ....                                                     [100%]

	================================ 16 passed in 9.31s =================================
	Trim Trailing Whitespace.................................................Passed
	Mixed line ending........................................................Passed
	Check for case conflicts.................................................Passed
	Check Yaml...............................................................Passed
	Check for added large files..............................................Passed
	Don't commit to branch...................................................Passed
	black....................................................................Passed
	You are ready to rock and save the climate at 4985f650030c4ba94387b87da53c055772a342f8, but don't forget to copy paste the above into your pull request
