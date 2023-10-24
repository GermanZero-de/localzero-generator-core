What is this?
================

When we did the reference data update 2018 -> 2022. We needed to have a way to update the traffic reference data.  Concretely given that
no new reference data was available from IFEU AND that the reference data if it would be available would probably be distorted by the
COVID-19 pandemic, we decided to use the 2018 reference data and scale it to 2022.

The problem was that the 2018 reference data is keyed by the 2018 AGS and the 2022 reference data is keyed by the 2022 AGS.  Concretely
some AGSs will be renamed, others will be split and others will be merged.  This means that we need to map the 2018 AGS to the 2022 AGS.

In particular partial spin offs mean that we need to do some best guess of how much of the existing traffic happens
in the new vs the old commune.  For that we need to either use the population or the area of the commune.

Luckily destatis provides a area change history (https://www.destatis.de/DE/Themen/Laender-Regionen/Regionales/Gemeindeverzeichnis/Namens-Grenz-Aenderung/namens-grenz-aenderung.html)

So the script here loads those excel sheets into a python native representation, for further processing.


