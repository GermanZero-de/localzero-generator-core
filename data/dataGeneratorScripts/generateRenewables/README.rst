renewable_energy import script
==============================

The importMarktStammDaten.py script imports data from the Marktstammdaten Register and saves them into the
renewable_energy data file (2018.csv). If one wants to work with the original data from the Marktstammdaten Register,
one should download the original Xml files and save them into a folder and adapt the path in the script. Also make sure to have the *reloadfromXML* boolean set as *True*.
Once you parsed the xml files once, you can also use the json files that are created during the xml parsing.
In order to use the json files set *reloadfromXML* boolean set as *False*.

Note that if you want the parse the xml data you need to install the third party lxml python package (Download and install https://lxml.de/).

The json file that is used to update all ags keys to 2018 is downloaded from https://www.xrepository.de/api/xrepository/urn:xoev-de:bund:destatis:bevoelkerungsstatistik:codeliste:ags.historie_2021-12-31/download/Destatis.AGS.Historie_2021-12-31.json
and holds data on all ags keys and changes that happend after 2006. 

More info on the Marktstammdaten register:
The Marktstammdaten Register lists all local energy sources (alle Strom- und Gaserzeugungsanlagen)
in germany including wind turbines, solar cells etc. but also fossil fuel dependent energy producers
like small "Blockheizkraftwerke" (more than 2.8 million entries). (almost) All units come with ags keys,
which is why we use this source to generate our renewable_energy data. The Marktstammdaten Register
provides a full data download under https://www.marktstammdatenregister.de/MaStR/Datendownload.
However the zip-file is ~900 MByte and the unziped XML-files are more than 19 GB. This is why we dont
provide them here directly but feel free to download them on your own and play around with the python script.
