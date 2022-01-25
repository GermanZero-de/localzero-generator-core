Data folder
===========

The generator needs a bunch of data about residents, housing, energy, traffic... During
a run of the generator all the data is readonly and read from files that are all expected
to be in a subfolder of this folder.


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
