
.. image:: https://github.com/GermanZero-de/localzero-generator-core/workflows/test/badge.svg
    :target: https://github.com/GermanZero-de/localzero-generator-core/actions?query=workflow%3Atest+branch%3Amain

Localzero Generator Core
=========================
LocalZero is a community project providing a tool that determines

 - greenhouse gas balances for the reference year 2018 and the planned target year
 - final energy consumptions for the reference year 2018 and the planned target year
 - and the most important measures and costs required to become carbon neutral.
 
This tool can be used at city, district or state level using their respective unique 8-digit AGS-key (Amtlicher Gemeindeschlüssel).
More information on the methodology can be found in our documentation on readthedocs: https://localzero-generator.readthedocs.io/de/latest/.

- 19.03.2018 Important Note!
    - The LocalZero Generator is not yet usable by people outside of GermanZero, as some required data is proprietary. However, the tool can be tested on our website: germanzero.de/loesungen/localzero. Future work will include the development of a REST API Service.


Setup
=========================
- Install Python
    - Version 3.10.
- Install Git
		- ensure that git is in your PATH variable (needed for devtool.py data checkout later)
- Install Poetry from https://python-poetry.org/docs/
    - **On Windows:** run this inside a power shell:

      :code:`(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python`

- Configure Git
	- Token:
		- https://github.com/settings/tokens:
		- create personal access token (repo, workflow, admin:org:read, gist)
		- save your token
		- On Windows Token add the token Windows Anmeldeinformationen (similar tools exist on linux and mac)
			- Generische Anmeldeinformationen hinzufügen (Adresse: git:https://github.com, Benutzername: Git Nutzername, Passwort: Token)
    - get this Git Repo (if you haven't done so already)
	- :code:`git clone https://github.com/GermanZero-de/localzero-generator-core`

- Install poetry and pre-commit
	- :code:`install-environment.sh`
	- **On Windows:** install Node.js (necessary for pyright)

- Get the required Data Repos
    - Clone https://github.com/GermanZero-de/localzero-data-public into ./data/public
    - Clone https://github.com/GermanZero-de/localzero-data-proprietary into ./data/proprietary

      **ISSUE:** You might not have access to the proprietary repository. We are providing a REST API Service soon.

Contributing to this project
=========================

Development
-----
This repository contains the calculations of the LocalZero Generator Core only. It should neither contain reference data
nor anything that is specific to the website.

For local development, checkout our helpful commands in devtool.py please.

Some notes on the code structure / history of the project
----------------------------------------------------------

The prototype was written as an excel spreadsheet, that contained both the data and the calculations.
To translate the spreadsheet into python a semi-automatic process (read some scripts + a lot of work)
was used and the structure dictated by the spreadsheet was kept. This allowed us to gain confidence in
the new implementation as the results including all intermediate results could be compared directly.

However it also sadly meant that the new code uses very little of the expressive power of python
and was sometimes even less easy to understand than the spreadsheet.

So we added an end to end testing framework, again so that we can make changes to the code without
accidentally changing the numbers that are computed.  But this time independently of excel.

We are using this new found freedom to clarify the code structure, but this is an ongoing project.
Our current plan is to finish a first pass over all sectors clarifying each sector individually.
When that is done, we will do another pass to factor out common functionality across sectors.

So some sectors are currently more readable than others, but we didn't want this fact to delay
the release.  If you have questions on any individual sector feel free to contact us.

Formatting
-----
We use **black** to automatically format the code and thereby avoid any spurious merge
conflicts, due to layout differences. This will happen in a pre-commit automatically,
but to for the best experience you should configure your editor to do the same.


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


