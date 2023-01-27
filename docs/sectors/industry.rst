6. Industrie
============
| **Autor: Hauke Schmülling**
| **Stand: 24.02.22**

Dieses Dokument gibt einen Überblick über die wesentlichen Prinzipien, die den Berechnungen für den Sektor Industrie in der Klimavision zugrunde liegen.

6.1 Eingabedaten
----------------
Im Gegensatz zu den anderen Sektoren, die in allen Kommunen eine Rolle spielen, sind die industriellen Betriebe sehr ungleichmäßig über Deutschland verteilt. Da eine automatische ortsspezifische Zuordnung aller Industriebetriebe (bisher) nicht möglich ist, werden der Endenergieverbrauch und die Emissionen basierend auf dem deutschen Durchschnitt und der kommunalen Industrie- und Gewerbefläche abgeschätzt. Falls die industrielle Zusammensetzung vor Ort bekannt ist, können die deutschen Standardwerte des Endenergieverbrauchs der vier Subsektoren Mineralische Industrie (11,0%), Chemische Industrie (23,7%), Metallherstellende Industrie (26,4%), Sonstige Industrie (38,9%) online anders umverteilt werden.

6.2 Bilanzierung 2018
---------------------
Die vier Subsektoren Mineralische Industrie (CRF 2.A + 1.A.2.f, AG EB 52+53, WZ 23), Chemische Industrie (CRF 2.B + Teil von 1.A.2.g, AG 49+50, WZ 20+21), Metallherstellende Industrie (CRF 2.C + 1.A.2.a-b, AG EB 54+55, WZ 24.1+4-5), Sonstige Industrie (CRF 2.D-H + 1.A.2.d-e und Teil von 1.A.2.g, AG EB 46-48+51+56-59, WZ alle anderen ohne 5.1, 5.2, 6, 9, 19.1, 19.2) orientieren sich am CRF (common reporting format) im NIR (National Inventory Report) 2018 von 2020 (https://www.umweltbundesamt.de/sites/default/files/medien/1410/publikationen/2020-04-15-climate-change_22-2020_nir_2020_de.pdf), den Zeilen in der deutschen Energiebilanz 2018 der AG Energiebilanzen (AG EB) von 2021 (https://ag-energiebilanzen.de/7-0-Bilanzen-1990-2019.html) und der dazugehörigen Klassifikation der Wirtschaftszweigen (WZ) von 2008 des Statistischen Bundesamtes (https://www.destatis.de/static/DE/dokumente/klassifikation-wz-2008-3100100089004.pdf). Eine ähnliche Einteilung mit Fokus auf die ersten drei Subsektoren nimmt auch die Agora-Studie „Klimaneutrale Industrie“ (https://static.agora-energiewende.de/fileadmin/Projekte/2018/Dekarbonisierung_Industrie/164_A-EW_Klimaneutrale-Industrie_Studie_WEB.pdf) vor.

Die größte Schwierigkeit bestand darin, die Daten kongruent mit den drei Klassifizierungssysteme zu verbinden. Die Endenergiebedarfe (EEV) stammen von AG EB, die prozessbedingten (process-based = pb) CO2e-Emissionen aus CRF 2 des NIR, die Produktionsmengen aus unterschiedlichen Quellen, meist den Branchen selbst, die jedoch nicht immer ausdrücklich nach WZ klassifizieren.



Die energiebedingten (combustion-based = cb) CO2e-Emissionen (CRF 1) mussten aus NIR, Daten der Branchensteckbriefe Industrie des BMWI 2019 (https://www.bmwi.de/Redaktion/DE/Artikel/Energie/energiewende-in-der-industrie.html) und eigenen Berechnungen basierend auf AG EB zurechtgepuzzelt werden. Von den 77,7 Mt CO2e in CRF 1.A.2.g (Zitat NIR S.199: "Diese Subkategorie ist wegen ihrer Eigenschaft als Auffangposition für nicht branchenscharf disaggregierbare Brennstoffeinsätze besonders bedeutsam und trägt substanziell zu den CO2-Emissionen des gesamten Energiesektors bei.") werden die Emissionen der Industriekraftwerke im Sektor Strom ausgewiesen, da diese Teil der deutschen Bruttostromerzeugung sind, deren Emissionen wir gesammelt unter Strom ausweisen. Dafür wurden alle Energieträger in AG EB Zeile 12 Industriekraftwerke (nur für Strom) mit den verbrennungsbedingten Emissionsfaktoren des UBA multipliziert und zu 39,2 Mt CO2e aufsummiert (Biomasse mit 0,028 t/ MWh für non-CO2-THG).

Wird Strom mithilfe von EEV (also in AG EB Zeile 46-59) auf Industriegelände erzeugt und gleich wieder verbraucht, taucht diese Eigenstromerzeugung nicht in der deutschen Bruttostromerzeugung auf, sodass der EEV und die cb CO2e der Industrie zugeschrieben werden.

Die Bilanzierung der Emissionen erfolgt in der Industrie über einen Sonderweg, nämlich die jährlichen Produktionsmengen in t/a. Diese werden zunächst mit einem festen Faktor vom EEV in MWh abgeleitet. Da sich bei der Umstellung der industriellen Produktion insbesondere der Energieeinsatz und die cb CO2e reduzieren lassen, die pb CO2e aber teilweise prozessimmanent sind, ist es sinnvoll, die Emissionen getrennt nach cb und pb von den Produktionsmengen abzuleiten. Auch hier wurden für die festen Emissionsfaktoren die deutschlandweiten Emissionen durch die deutschlandweiten Produktionsmengen geteilt.

EEV in MWh/a à Produktionsmenge in t/a à cb und pb CO2e in t/a

Die Subsektoren wurden vor allem basierend auf den Kategorien in CRF 2 noch mal unterteilt in Subsubsektoren:

| **Mineralische Industrie (CRF 2.A + 1.A.2.f, AG EB 52+53, WZ 23)**

#. Zement (CRF 2.A.1 + 1.A.2.f Zement, AG EB 53, WZ 23.51)

#. Kalk (CRF 2.A.2 + 1.A.2.f Kalk, AG EB 53, WZ 23.52)

#. Glas (CRF 2.A.3 + 1.A.2.f Glas, AG EB 52, WZ 23.1)

#. Keramik (CRF 2.A.4 + 1.A.2.f Keramik, AG EB 52, WZ 23.2+23.31+23.4)

| **Chemische Industrie (CRF 2.B + Teil von 1.A.2.g, AG EB 49+50, WZ 20+21)**

#. Grundstoffchemie ohne Ammoniak (CRF 2.B.2-8 + Teil von 1.A.2.g, AG EB 49, WZ 20.1)

#. Ammoniak Produktion (CRF 2.B.1 + Teil von 1.A.2.g, AG EB 49, WZ 20.15)

#. Sonstige Chemieindustrie (Teil von CRF 1.A.2.g, AG EB 50, WZ 20, 21 ohne 20.1)

| **Metallherstellende Industrie (CRF 2.C + 1.A.2.a-b, AG EB 54+55, WZ 24.1+4-5)**

#. Eisen+Stahl (CRF 2.C.1 + 1.A.2.a, AG EB 54, WZ 24.1)
    #. Davon Primärroute
    #. Davon Sekundärroute
#. Nichteisenmetalle (hauptsächlich Al, Cu) + Gießereien (CRF 2.C.2-7 + 1.A.2.b, AG EB  55, WZ 24.4+5)

| **Sonstige Industrie (CRF 2.D-H + 1.A.2.d-e und Teil von 1.A.2.g, AG EB 46-48+51+56-59, WZ alle anderen ohne 5.1, 5.2, 6, 9, 19.1, 19.2)**

#. Papierindustrie (CRF 1.A.2.d, AG EB 48, WZ17)
#. Ernährungsindustrie (CRF 1.A.2.e + Teil von 1.A.2g, AG EB 47, WZ 10-12)
#. Weitere Branchen (Textil, Möbel, Pharma, Automobil…) (CRF 2.D + Teil von 1.A.2.g, AG EB 46+51+56-59, WZ alle anderen ohne 5.1, 5.2, 6, 9, 19.1, 19.2)
    #. …dazu pb F-Gas-Emissionen (CRF 2.E-H, über alle AG EB und WZ hinweg)



6.3 Maßnahmen
-------------
Die meisten Subsektoren enthalten noch mal zahlreiche verschiedene Produktionskategorien, beispielsweise die Grundstoffchemie. Daher müssen zur Erreichung der Klimaneutralität eigentlich zahlreiche verschiedene Anpassungen innerhalb eines Subsektors erfolgen. In der Klimavision wurde aber versucht, die wichtigste (übergreifende) Maßnahme pro Subsektor zu identifizieren und diese mathematisch für den gesamten Subsektor anzusetzen. So lautet die Maßnahme für die Grundstoffchemie „Umstellung auf erneuerbare Energieträger“, was insbesondere in den Industriezweigen das Mittel der Wahl ist, wo vor allem cb Emissionen auftreten. Nur bei den Subsektoren, die bereits als Einzelprozess einen hohen Energiebedarf und Emissionen aufweisen, wurden spezifische Maßnahmen angesetzt, also beispielsweise bei der Zement- oder Ammoniakproduktion. Größter industrieller Emittent ist aber die Stahlerzeugung, weshalb diese dezidiert in Primär- und Sekundärproduktion aufgespalten wurde: In der Primärstahlerzeugung über die klassische Hochofen-Konverter-Route ist die CO2-Emission ein essenzieller Teil des Prozesses, da dem Eisenerz mittels Koks als Reduktionsmittel der Sauerstoff entzogen wird. Wird stattdessen Wasserstoff eingesetzt (DRI), entsteht Wasser statt CO2. Mit dem Einsatz von Elektroöfen und einer höheren Recyclingquote in der Sekundärstahlerzeugung wird die Stahlproduktion praktisch klimaneutral. Eine Besonderheit stellt der Posten „…dazu pb F-Gas-Emissionen“ unter „Weitere Branchen“ in „Sonstige Industrie dar: Diese kategoriale Stellung macht schon deutlich, dass es sich hierbei um einen Sammelposten über alle Wirtschaftsbereiche handelt (CRF 2.E-H). Diese fluorierten THG treten u.a. bei der Kühlung auf und müssten daher eigentlich sowohl in GHD als auch bestimmten Industriezweigen bilanziert werden, wo sie genutzt werden. Da aber der NIR selbst diese Zuordnung nicht vornimmt, ist dies auch in der Klimavision nicht möglich. Als Gesamtmaßnahme wird hier die Umstellung auf natürliche Kühlgase angesetzt.
Allen Maßnahmen nachgelagert sind die Investitionskosten: Grundsätzlich wurde versucht, Investitionskosten pro produzierte t pro Jahr zu ermitteln. Also was kostet z.B. ein DRI-Stahlwerk mit einer jährlichen Produktionsmenge von 100.000 t Stahl?

Hier gibt es so gut wie keine Standardwerte, sodass versucht wurde, Berichte über beispielhafte Investitionen zu finden.

So heißt es beispielsweise in einer Pressemitteilung zu Deutschlands bisher einziger DRI-Anlage, dass die Projektkosten für den Demonstrationsmaßstab mit einer Jahresproduktion von 100.000 t Stahl 65 Mio. € betragen. Also wurden durchschnittliche Investitionskosten i.H.v. 650€ pro t/a angesetzt.

https://hamburg.arcelormittal.com/icc/arcelor-hamburg-de/med/1f6/1f640c6c-f454-b961-d4e1-e3050736c0f2,11111111-1111-1111-1111-111111111111.pdf



6.4 Bilanz Zieljahr
-------------------
Die Bilanzierung im Zieljahr erfolgt grundsätzlich identisch wie 2018. Als Ausgangsgröße wird dieses Mal jedoch die Produktionsmenge verwendet. In Greensupreme-Szenario sind Produktionsmengen der Sektoren für 2050 hinterlegt. Im Vergleich zu den Produktionsmengen 2018 wird somit eine prozentuale Veränderung ermittelt und in den meisten Sektoren gibt es deutliche Produktionsrückgänge, die mit einem reduzierten Konsum auf Verbraucherseite einhergehen. Greensupreme gibt zumeist auch an, ob es noch cb und pb Emissionen gibt. Die cb Emissionen werden dort durchgängig mit 0 angesetzt, da synthetischen Energieträgern keine Emissionen zugeschrieben werden. In der Klimavision haben aber zumindest E-Methan und Biomasse noch positive Emissionen, sodass aus deren Bedarf bei der Produktion individuelle cb Emissionsfaktoren für den Subsektor ermittelt werden. Damit ergibt sich als Rechenschema folgendes Vorgehen:

Produktionsmenge in t/a à (EEV in MWh/a à cb und) pb CO2e in t/a

Quellen
-------












