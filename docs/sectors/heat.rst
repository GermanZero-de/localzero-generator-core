2. Wärme
========
| **Autor: Hauke Schmülling**
| **Stand: 23.02.22**



Dieses Dokument gibt einen Überblick über die wesentlichen Prinzipien, die den Berechnungen für Wärme in der Klimavision zugrunde liegen. Generell ist mit Wärme hier nur die Bereitstellung (nicht die Nutzung) von den Endenergieträgern gemeint, die hauptsächlich zur Wärmebereitstellung genutzt werden, also Heizöl, sonstige Mineralölprodukte, Kohle, LPG (Flüssiggas), Erdgas, sonstige fossile Energieträger, Fernwärme und Biomasse. Sonstige Erneuerbare Energieträger (Geothermie, Umweltwärme (heißt in der Klimavision Wärmepumpe), Solarthermie laut Vorwort zu den Energiebilanzen 2015 [AGE15]) werden physikalisch in PH etc. erzeugt, aber in Wärme aggregiert ausgewiesen. E-Methan, das in Zukunft Erdgas ersetzt, wird in Kraftstoffe aufgeführt, da dessen Produktionsprozess dem der E-Fuels ähnelt. Grundsätzliches Vorgehen ist: Erhebung der Bedarfe, Bereitstellung mit unterschiedlichen Endenergieträgern, THG-Emissionen abgeleitet mit Emissionsfaktoren aus der Produktion der Endenergieträger.

2.1 Eingabedaten
----------------

Grundlage der THG-Bilanzierung 2018 ist der Endenergieverbrauch (EEV) 2018 der Wärmeträger in Megawattstunden (MWh) in den Sektoren PH, GHD, Verkehr, Industrie und Landwirtschaft. Als User:in kann man dort jeweils Defaultwerte der EEV überschreiben, wenn diese für die Kommune bekannt sind. Diese Default-Werte werden basierend auf der Bilanz 2018 der AG Energiebilanzen ermittelt (siehe jeweils die Sektoren-Texte).


| **Heizöl:** AG EB 2018 Spalte P, aggregiert in Zeile 45
| **Sonstige Mineralölprodukte:** AG EB 2018 Spalte Q, R, T, U; aggregiert in Zeile 45
| **Kohle:** AG EB 2018 Spalte C-J; aggregiert in Zeile 45
| **LPG:** AG EB 2018 Spalte S; aggregiert in Zeile 45
| **Erdgas:** AG EB 2018 Spalte X; aggregiert in Zeile 45
| **Sonstige fossile Energieträger:** AG EB 2018 Spalte AC; aggregiert in Zeile 45
| **Fernwärme:** AG EB 2018 Spalte AF; aggregiert in Zeile 45
| **Biomasse:** AG EB 2018 Spalte AA; aggregiert in Zeile 45

Die (eventuell überschriebenen) Wärmeträger der Sektoren werden im Sektor Wärme dann Sektor-summiert unter Nachfrage und Wärmeträger-summiert unter Produktion aufgelistet.


2.2 Bilanzierung 2018
---------------------

Ausgehend von der produzierten Endenergieträger-Menge werden nur die THG-Emissionen aus der Vorkette ermittelt, nicht aus dem Verbrauch. Die THG-Emissionen aus der Verbrennung der Endenergieträger werden gemäß der Einflussbilanz bei der Nutzung in den Sektoren PH, GHD, Verkehr, Industrie und Landwirtschaft bilanziert. Die Vorkette wiederum enthält nur die Emissionen, die bei der eigentlichen Bereitstellung der Wärmeträger anfallen, also durch Exploration, Förderung, Transport, Raffinierung, Lagerung, Verteilung, Leitungsverluste, Ausblasen, Abfackeln. Da der NIR die Grundlage ist, sind dies nur die in Deutschland anfallenden Vorkettenemissionen. Die vollständige Zuordnung der im NIR (Zitate und Seitenzahlen beziehen sich immer darauf) enthaltenen Emissionen zu bestimmten Wärmeträgern gestaltete sich jedoch schwierig, weshalb an manchen Stellen Annahmen getroffen werden mussten. Wenn einem Wärmeträger keine cb und/oder pb Emissionen zugeordnet werden konnten, wurde für diesen auch kein entsprechender Emissionsfaktor hinterlegt. Mit den nationalen THG und EEV eines Wärmeträgers kann jeweils dessen Emissionsfaktor der Bereitstellung ermittelt werden.

| **Heizöl:**
| Cb Emissionen = 2.885.355  t/a (Anteil von CRF 1.A.1.b)
| Da in CRF 1.A die "Verbrennung von Brennstoffen" gemeldet wird, handelt es sich bei CRF 1.A.1.b Mineralölraffinerien um verbrennungsbedingte Emissionen zur Produktion von Mineralölprodukten. Diese cb Emissionen entspringen im NIR auf S. 177 einer Produktion von 101 Mt Mineralölprodukte (was mit dem MWV Jahresbericht 2019 passt), aber aufgeteilt auf 53 Mt Kraftstoffe, 19,9 Mt Heizöl, 6 Mt Naphtha verbleiben uns ca. 22 Mt auf andere Produkte (was im MVW gar nicht auftaucht und mit Quellenangaben des NIR nicht nachvollziehbar ist, weswegen zur Emissionsverteilung die Produktionsmengen des MWV Jahresbericht 2019 herangezogen werden). [Min19]

| **Sonstige Mineralölprodukte:**
| Cb Emissionen = 4.446.146  t/a (Anteil von CRF 1.A.1.b)
| anteilig nach Produktionsmenge laut MWV Jahresbericht 2019 (Erklärung siehe Heizöl)

| Pb Emissionen =398100+76320+260 (CRF 1.B.2.a) +341690+760+590 (CRF 1.B.2.c)
| Exploration, Förderung, Transport, Lagerung, Verteilung von (Roh)Öl und anderen Mineralölprodukten, daher der Kategorie "Sonstige Mineralölprodukte" zugeschlagen (S. 265)
| Ausblasen und Abfackeln von (Roh)Öl und Gas, aber überwiegend Öl laut NIR DEU inventory Table1.B.2 (S. 289)

| **Kohle:**
| Cb Emissionen = 9700880+150930+161360 CO2e (komplett CRF 1.A.1.c auf S. 181)
| "Der Kategorie 1.A.1.c werden der Steinkohlen- und Braunkohlenbergbau sowie die Kokereien und Brikettfabriken zugerechnet, außerdem die Gewinnung von Rohöl und Erdgas." Auf S. 182 wird allerdings deutlich, dass die Emissionen etwa 50/50 auf Braunkohle und Kokereigase (4.809 t S. 184) entfallen, nur minimal Erdgas. Da im Generator unter Kohle alle Kohleprodukte fallen, wird diese Kategorie komplett der Kohleproduktion zugeschlagen. Im NIR wird nicht ganz deutlich, was 2018 noch zu 1.A.1.c gehört, da z.B. viele Steinkohleanlagen umgemeldet wurden. Die verbrennungsbedingten Emissionen stammen aus dem "Einsatz zur Wärmeerzeugung, insbesondere zur Braunkohlentrocknung zur Herstellung von Braukohlenprodukten" (S. 183), "CO2-Emissionen aus der Gichtgasverbrennung in Kokereien" (S. 184) etc.

| Pb Emissionen =1618410+665070 (komplett CRF 1.B.1 auf S. 255)
| Diffuse Emissionen (besonders CH4) in CRF 1.B.1 (S. 255f):
| "Die Kategorie Kohlenbergbau und -umwandlung ist für CH4-Emissionen eine Hauptkategorie nach der Emissionshöhe und dem Trend. Im Bergbau wird zwischen Tagebau, Gewinnung des Rohstoffs in offenen Gruben und Tiefbau, Abbau der Lagerstätte in untertägigen Abbauräumen unterschieden. In Deutschland wird Steinkohle ausschließlich im Tiefbau, Braunkohle seit 2003 ausschließlich im Tagebau gewonnen."

| **LPG:**
| Cb Emissionen = 606.849  t/a (Anteil von CRF 1.A.1.b)
| anteilig nach Produktionsmenge laut MWV Jahresbericht 2019 (Erklärung siehe Heizöl)

| **Erdgas:**
| Cb Emissionen =1323230+11750+6490 (komplett CRF 1.A.3.e auf S. 233)
| "In der Kategorie 1.A.3.e – Übriger Verkehr werden nur die Emissionen von Gasturbinen in Erdgasverdichterstationen des Transportnetzes berichtet. Die Emissionen aus Gasturbinen der Förderstationen werden in der Kategorie 1.A.1.c berichtet. Die diffusen Emissionen aus den Verdichtern werden unter 1.B.2.b.iii & iv berichtet. "

| Pb Emissionen =4822590+601890 (komplett CRF 1.B.2.b auf S. 277)
| Gas: Förderung, Verarbeitung, Transport, Verteilung, Sonstiges.
| S. 277: "Die Kategorie 1.B.2.b „Erdgas“ ist für CH4-Emissionen aus Erdgas eine Hauptkategorie nach der Emissionshöhe."
| S. 288: "Aus der Tiefe kommendes Erdgas wird über Tage zunächst in Trocknungs- und Aufbereitungsanlagen behandelt. Diese Vorbehandlung des Erdgases findet in der Regel in Anlagen auf der Förderstation statt."

| **Sonstige fossile Energieträger:**
| Die AG-EB-Energieträger-Klasse Sonstige Energieträger (Nicht-erneuerbare Abfälle, Abwärme) hat keine Entsprechung in NIR CRF 1. Wir gehen jedoch davon aus, dass die Emissionen der Erzeugung und Lagerung bereits in der ursprünglichen Produktion des Abfalls bzw. der Abwärme erfasst sind, daher schreiben wir der Produktion/Bereitstellung dieses abfallenden Energieträgers keine zusätzlichen Emissionen zu.

| **Fernwärme:**
| Fernwärme wird laut AG Energiebilanzen auf 2 Arten bereitgestellt: Entweder in Heizkraftwerken der allgemeinen Versorgung (das bedeutet mittels Kraft-Wärme-Kopplung, also als Beiprodukt der Stromproduktion; Kraft ist ein anderes Wort für Strom) oder in Fernheizwerken (das bedeutet reine Wärmeproduktion).

| Cb Emissionen der KWK-Fernwärme aus Heizkraftwerken der allgemeinen Versorgung 2018 = 22.431.929 t/a (Teil aus 1.A.1.a):
| Emissionen der KWK-Fernwärmeerzeugung mit eigener Berechnung: Alle Energieträger in AG EB Zeile 15 Heizkraftwerke der allgemeinen Versorgung wurden mit den verbrennungsbedingten Emissionsfaktoren des UBA multipliziert und aufsummiert (Biomasse mit 0,028 t/ MWh für non-CO2-THG). Diese Emissionen werden dem CRF 1.A.1.a (Öffentliche Elektrizitäts- und Wärmeversorgung) entnommen und der Wärme zugeschlagen, auch wenn die Produktion der KWK-Wärme im Bereich Strom ausgewiesen wird.
| Cb Emissionen der Fernwärme aus Fernheizwerken 2018 = 7.405.993 t/a (Teil aus CRF 1.A.1.a):
| Emissionen der Fernwärmeerzeugung in Fernheizwerken mit eigener Berechnung: Alle Energieträger in AG EB Zeile 16 Fernheizwerke wurden mit den verbrennungsbedingten Emissionsfaktoren des UBA multipliziert und aufsummiert (Biomasse mit 0,028 t/ MWh für non-CO2-THG). Diese Emissionen werden dem CRF 1.A.1.a (Öffentliche Elektrizitäts- und Wärmeversorgung) entnommen und der Wärme zugeschlagen.

| **Biomasse:**
| Die AG-EB-Energieträger-Klasse Biomasse und erneuerbare Abfälle hat keine Entsprechung in NIR CRF 1. Wir gehen jedoch davon aus, dass die Emissionen der Erzeugung und Lagerung bereits in der ursprünglichen Produktion der Biomasse erfasst sind (also CRF 3), daher schreiben wir der Produktion/Bereitstellung dieses Energieträgers keine zusätzlichen Emissionen zu. Zudem weist der NIR selbst die verbrennungsbedingten Emissionen der Biomasse nur nachrichtlich aus (NIR S. 877 Fußnote 3), was wir jedoch in LULUCF korrigieren.

| **Sonstige EE:**
| Geothermie, Solarthermie, Umweltwärme (laut Vorwort zu den Energiebilanzen 2015) werden eigentlich direkt in PH erzeugt und deren mögliche Emissionen gemäß der Einflussbilanz auch dort bilanziert. Einzig bei der Geothermie (die laut RWI-Endbericht 2020 „Erstellung der Anwendungsbilanzen 2018 für den Sektor der Privaten Haushalte und den Verkehrssektor in Deutschland“ S. 17 [RWI20]) nicht gesondert ausgewiesen werden kann, aber thematisch eher zu Umweltwärme (heißt in der Klimavision Wärmepumpe) gehört) könnten pb Emissionen außerhalb des Einflussbereichs der PH etc. auftreten. Doch laut NIR S. 292 hat CRF 1.B.2.d Geothermie keine Emissionen: "Beim Betrieb der Geothermiekraftwerke und Geothermieheizwerke in Deutschland treten keine Emissionen von klimawirksamen Gasen auf. Der Thermalwasserkreislauf ist geschlossen und wird untertägig und obertägig unter Luftabschluss betrieben, so dass während des Betriebs keine Emissionen auftreten." Daher werden sowohl Solarthermie als auch Wärmepumpe keine pb Emissionen zugeschrieben.



2.3 Maßnahmen
-------------
Nach der komplexen Bilanzierung 2018 sind die Maßnahmen relativ einfach. Es wird angenommen und angestrebt, dass im Zieljahr der Klimaneutralität keine fossilen Energieträger (also Heizöl, sonstige Mineralölprodukte, Kohle, LPG, Erdgas, sonstige fossile Energieträger) mehr genutzt werden, dementsprechend fallen diese einfach weg. Die Biomasse-Nutzung bleibt etwa konstant, weswegen keine Maßnahme vonnöten ist. Wärme aus Sonstigen EE (also Solarthermie und Wärmepumpe) wird in den Sektoren PH etc. selbst produziert, weswegen die Maßnahmen bzw. Investitionen dort anfallen. Somit beschränkt sich das Handlungsspektrum auf die Bereitstellung klimaneutraler Fernwärme: Ein Teil kommt immer noch aus der KWK (Heizkraftwerke der allgemeinen Versorgung), doch da auch die Strombereitstellung erneuerbar geworden ist, lediglich aus Stromgestehung mittels Biomasse. Während diese Fernwärme-Menge fix vom Sektor Strom bereitgestellt wird, wird die verbleibende Lücke des Fernwärme-Bedarfs aus 3 Quellen gedeckt: Fernheizwerke/Solarthermiefelder (10,4%), Großwärmepumpen (57,1%) und Geothermie (32,5%). Die Anteile beruhen auf dem GreenSupreme-Szenario 2050 der RESCUE-Studie auf S.89: Neben Fernwärme aus Biomasse-KWK gibt es dort vier Kategorien der Wärmenetzversorgung, wovon Großwärmepumpen und Quartiers-WP zu einer Kategorie Großwärmepumpen zusammengefasst werden.

Von dem Fernwärmebedarf wird dann der Leistungsbedarf und die Investitionen abgeleitet: Statt klassischer Fernheizwerke werden Solarthermiefelder aufgebaut, dazu Großwärmepumpen und Geothermie-Anlagen. Die pauschalisierten Investitionskosten stammen aus dem Anhang der Fraunhofer-Studie „Wege zu einem klimaneutralen Energiesystem“ [Fra20]

Für die Transformation werden also Stellen im Anlagenbau benötigt: Dafür wurde der Anteil der Personalkosten (25,5%) an den Investitionskosten im Bauhauptgewerbe (WZ 41.2, 42, 43.1, 43.9) und der durchschnittliche Jahreslohn (47.195 €/a) ermittelt.

Neben der eigentlichen Wärmeproduktion werden noch zwei allgemeine Maßnahmen durchgeführt: Der Aufbau von Wärmespeichern (Kapazität abhängig von der benötigten Wärmemenge) geschieht strukturell ähnlich wie die Fernwärmekapazitäten.

Außerdem ist eine einjährige Wärmeleitplanung vorgesehen, deren Kosten sich an der „Pflicht zur kommunalen Wärmeleitplanung“ in Baden-Württemberg orientieren. [Min21]


2.4 Bilanz Zieljahr
-------------------
Die Endenergiebilanz 2018 umfasst Biomasse, die zu Informationszwecken ausgewiesenen Sonstigen EE und fokussiert sich v.a. auf den Fernwärmebedarf der Sektoren. Nur in diesem Bereich werden überhaupt noch Emissionen ausgewiesen, nämlich die verbrennungsbedingten non-CO2-THG aus der Biomasse-KWK (0,045 t/MWh). Alle Wärmeträger weisen keine pb Emissionen bei der Bereitstellung auf. Damit kann die Wärme im Zieljahr nahezu klimaneutral zur Verfügung gestellt werden. Eine Sektorkopplung ergibt sich durch den Einsatz von Großwärmepumpen: Der dafür notwendige Strombedarf wird an den Sektor Strom übergeben, sodass hier eine Umwandlung eines Endenergieträgers (Strom) in einen anderen (Fernwärme) erfolgt.



Quellen
--------

| [AGE15]
| AG Energiebilanzen: „Vorwort zu den Energiebilanzen für die Bundesrepublik Deutschland“ [online nicht mehr verfügbar, auf Anfrage bei LocalZero oder AG Energiebilanzen] (2015)

| [Min19]
| Mineralölwirtschaftsverband: „Jahresbericht 2019“ [online nicht mehr verfügbar, auf Anfrage bei LocalZero oder en2x] (2019)
| https://www.mwv.de/wp-content/uploads/2021/01/MWV-Jahresbericht_2019_Webversion_MineraloelwirtschaftsverbandEV.pdf

| [Min21]
| Ministeriums für Umwelt, Klima und Energiewirtschaft Baden-Württemberg: „Verwaltungsvorschrift zur Förderung der kommunalen Wärmeplanung in Landkreisen und Gemeinden (VwV freiwillige kommunale Wärmeplanung)“ (2021)
| https://um.baden-wuerttemberg.de/fileadmin/redaktion/m-um/intern/Dateien/Dokumente/5_Energie/Beratung_und_Information/210915-VwV-Forrderrichtlinie-kommunale-Waermeplanung.pdf

| [RWI20]
| RWI – Leibniz-Institut für Wirtschaftsforschung: „Erstellung der Anwendungsbilanzen 2018 für den Sektor der Privaten Haushalte und den Verkehrssektor in Deutschland“ (2020)
| https://www.rwi-essen.de/media/content/pages/publikationen/rwi-projektberichte/ageb_anwendungsbilanz_2018_(priv._hh_und_verkehr).pdf

| [Fra20]
| Fraunhofer-Institut für Solare Energiesysteme ISE „Wege zu einem klimaneutralen Energiesystem - Anhang zur Studie“ (2020)
| https://www.ise.fraunhofer.de/content/dam/ise/de/documents/publications/studies/Anhang-Studie-Wege-zu-einem-klimaneutralen-Energiesystem.pdf

