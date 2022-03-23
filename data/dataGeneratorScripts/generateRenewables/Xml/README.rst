XML data
========

This folder should contain XML files if the "importMarktStammDaten.py" is used. 
The Marktstammdaten Register lists all local energy sources (alle Strom- und Gaserzeugungsanlagen)
in germany including wind turbines, solar cells etc. but also fossil fuel dependent energy producers
like small "Blockheizkraftwerke" (more than 2.8 million entries). (almost) All units come with ags keys,
which is why we use this source to generate our renewable_energy data. The Marktstammdaten Register
provides a full data download under https://www.marktstammdatenregister.de/MaStR/Datendownload.
However the zip-file is ~900 MByte and the unziped XML-files are more than 19 GB. This is why we dont
provide them here directly but feel free to download them on your own and play around with the python script.
 