renewable_energy import script
==============================

The importMarktStammDaten.py script imports data from the Marktstammdaten Register and saves them into the
renewable_energy data file (2018.csv). If one wants to work with the original data from the Marktstammdaten Register,
one should download the original Xml files (see Xml folder) from their website and change the *reloadfromXML* boolean in the python
script to *True*. Otherwise you can also use our json files, that contain the information we extracted from the xml files and used
to generate the renewable_energy data. 

Note that if you want the reload the xml data you need to install the third party lxml python package (Download and install https://lxml.de/). 