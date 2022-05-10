renewable_energy import script
==============================

The importMarktStammDaten.py script imports data from the Marktstammdaten Register and saves them into the
renewable_energy data file (2018.csv). The Marktstammdaten Register lists all local energy sources (alle Strom- und Gaserzeugungsanlagen)
in germany including wind turbines, solar cells etc. but also fossil fuel dependent energy producers
like small "Blockheizkraftwerke" (more than 2.8 million entries). (almost) All units come with ags keys,
which is why we use this source to generate our renewable_energy data.

This script performs an SQL request and downloads the marktstammdatenregister directly to an .gz file using gunzip. Feel free to use any other zip tool that runs on your maschine.
```
curl https://s3.eu-central-1.wasabisys.com/mastr-backup/Marktstammdatenregister.db.gz | gunzip -> Marktstammdatenregister.db
```

The json file that is used to update all ags keys to 2018 is downloaded from https://www.xrepository.de/api/xrepository/urn:xoev-de:bund:destatis:bevoelkerungsstatistik:codeliste:ags.historie_2021-12-31/download/Destatis.AGS.Historie_2021-12-31.json
and holds data on all ags keys and changes that happend after 2006. Download and provide the json file via:
```
curl -o ags_historie.json https://www.xrepository.de/api/xrepository/urn:xoev-de:bund:destatis:bevoelkerungsstatistik:codeliste:ags.historie_2021-12-31/download/Destatis.AGS.Historie_2021-12-31.json
```

To run the code you also need to add the disjoint-set library to poetry via:
```
poetry add disjoint-set
```

Finally you can run the script via:
```
python importMarktStammDaten.py data/public/population/2018.csv ags_historie.json Marktstammdatenregister.db
```
Make sure that you use the correct paths to the required files. This includes the local zeros population file (data/public/population/2018.csv) that is used
to distribute the installed unit powers over several ags keys if the power can not be linked to a specific ags key.

Unfortunatly not all AGS Keys in the Marktstammdatenregister are valid keys, that are used by local zero. This is due to the fact that the ags keys change over time. To update
the keys we use the following algorithms: We create sets of ags keys {ags keys| ags keys linked via ags history} that are linked via a entries in the ags history and accumulate
all powers of the renewable units in this set. Afterwards we distribute the accumulated power over subsets of these sets
{{ags keys| ags keys linked via ags history & used by local zero}} by the using their respective share in population. With the assumption that 
most ags keys do not change over the years and the {ags keys| ags keys linked via ags history} sets do not get too big, the resulting error is acceptable.