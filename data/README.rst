Data folder
===========

The generator needs a bunch of data about residents, housing, energy, traffic... During
a run of the generator all the data is readonly and read from files that are all expected
to be in a subfolder of this folder.

How to change the data
----------------------

When you make changes to the data in the public or private repository they will
only be used by the generator once we switch the generator to the corresponding
revision (this is what the production.json file the generator core and KNUD are for).

However you should test your changes anyway before we merge them into the data
repositories.  For that you can use the usual `ready to rock` test in the
generator core repository.

If you use windows be advised that some windows tools might write files in
an encoding that is not `utf-8` but for example `latin-1`.  That would cause
trouble, so make sure you set the corresponding options.

Furthermore it is a good idea to run `python devtool.py data normalize FILE`
on every data file you have changed, so minor encoding differences (such as
wether or not to put `"` around fields in a CSV) do not result in spurious
merge conflicts later on.

We also added the *dataGeneratorScripts* folder, that includes some python scripts
which generate data files for the data repositories from various sources.

Where to get the data: Public Domain
------------------------------------

*tl;dr* Run `python devtool.py checkout` if you are a member of the localzero team.

The majority of the relevant data was curated by German Zero from various sources that
are in the public domain. You can checkout a copy of that data from the repository
located here: publicRepository_.

Please put that checkout into ``data/public/``

Where to get the data: Proprietary Data
----------------------------------------

There is a small amount of data that German Zero could only get by paying a vendor.
The website edition of the Generator uses this data. However we would violate the
license if we would make the data available for free. If you are part of the German
Zero team you can put a copy of that data into ``data/proprietary`` and use it to
work on the website edition of the Generator, but remember that the data should not
be put on a public github or otherwise be given away to people outside of GermanZero.

.. _publicRepository: https://github.com/GermanZero-de/localzero-data-public.git
