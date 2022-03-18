7. Verkehr
==========
| **Autor:innen: Sebastian Lüttig, Silvan Ostheimer, Leon Schomburg, Anne Schwob**
| **Stand: 25.02.22**


Dieses Dokument gibt einen Überblick über die wesentlichen Prinzipien, die den Berechnungen für Verkehr in LocalZero zugrunde liegen. Im Gegensatz zu den anderen Sektoren gibt es hier kommunenfeine Primärdaten der Verkehrsleistung, die vom ifeu für das Projekt LocalZero zur Verfügung gestellt worden sind. Darauf basierend findet die EEV- und THG-Bilanzierung getrennt nach Verkehrsträgern statt. Die verwendeten Emissionsfaktoren der Endenergieträger sind aber identisch mit den anderen Sektoren.

7.1 Eingabedaten
----------------
Berechnungen in LocalZero für den Bereich Verkehr basieren auf kommunenfeinen Daten, die vom ifeu für das Projekt LocalZero bereitgestellt wurden. Daher ist hier keine individuelle Anpassung der Eingabe nötig und möglich.

7.2 Bilanzierung 2018
---------------------

7.2.1 Nachfrage und Bereitstellung
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Die Nachfrage aus dem Sektor Verkehr setzt sich aus der Nutzung verschiedener Verkehrsträger zum Transport von Gütern oder der Beförderung von Personen zusammen. Die Bereitstellung der erforderlichen Energie in Form verschiedener Kraftstoffe oder Strom ist den Verkehrsträgern zugeordnet.

| **Straßenverkehr**

Zur Bestimmung der Fahrleistung in Fahrzeugkilometern des motorisierten Individualverkehrs (MIV) sowie der leichten und schweren Nutzfahrzeuge (LNF und SNF) werden gemeindefeine Daten des Instituts für Energie- und Umweltforschung (ifeu) herangezogen.  Dabei wird zwischen der Nutzung von Straßen des Typs “Innerorts und Außerorts” sowie “Autobahn” unterschieden.

Für den Busverkehr im Liniennahverkehr wird auf kreisfeine Daten vom Statistischen Bundesamt zurückgegriffen (Destatis 2020). Die entsprechenden Verkehrsleistungen auf Gemeindeebene werden anhand der Einwohner in der jeweiligen Kommune im Verhältnis zu den Einwohnern des Landkreises abgeschätzt. Verkehrsleistungen des Linienfernbus- und Gelegenheitsbusverkehrs werden nicht separat ausgegeben.

Die Umrechnung der Verkehrsleistungen in Beförderungs- bzw. Transportleistung in Personen- und Tonnenkilometern erfolgt anhand eigens berechneter Faktoren basierend auf den Angaben zu den Beförderungsleistungen im Jahr 2018 in UBA 2020a.

Die Berechnung des kommunalen Endenergieverbrauches (=EEV) für den Straßenverkehr erfolgt über die Fahrleistung und den spezifischer EEV (MWh/km) je nach Antriebsart und Straßenkategorie. Dabei werden – neben Strom für Elektrofahrzeuge - folgende Kraftstoffe separat betrachtet: Benzin, Diesel, LPG, CNG (Erdgas), Biogas, Bioethanol und Biodiesel. Die spezifischen Endenergieverbräuche wurden ebenfalls durch das ifeu bereitgestellt.

| **Schienenverkehr**

Für die Ermittlung der Fahrleistung von Straßen-, Stadt- und U-Bahn (SSU) im ÖPNV wird - wie beim Linienbusnahverkehr – auf kreisfeine Daten des statistischen Bundesamtes zurückgegriffen (Destatis 2020).

Für den Eisenbahnverkehr für Güter und Personen bilden gemeindefeine Endenergieverbrauchsdaten des ifeu die Grundlage für weitere Berechnungen. Hier kommt es zu bekannten aber ungeklärten Abweichungen zu den von der AG Energiebilanzen (AGEB) ausgegebenen Werten, welche regelmäßig unter denen des ifeu und des TREMOD-Berichtes (UBA 2020 S. 74) liegen. LocalZero bedient sich in diesem Fall der höheren Werte, um das Risiko zu gering eingeschätzter Verbrauchsdaten zu minimieren.

Auf Basis der gesamten in Deutschland erbrachten Beförderungs- bzw. Transportleistungen im Schienenverkehr in Deutschland aus UBA (2020a) wird das Verhältnis von EEV zur Verkehrsleistung bestimmt. Aus diesem Faktor wird die Verkehrsleistung in Personenkilometern bzw. Tonnenkilometern in der jeweiligen Kommune bestimmt.

| **Luftverkehr**

Die  Beförderungs- und Transportleistung im Luftverkehr entspricht den Daten nach BMVI “Verkehr in Zahlen” (BMVI 2020).

Grundlage für den EEV ist der bundesweite EEV nach den AG Energiebilanzen von Kerosin und Flugbenzin in MWh. Dieser umfasst alle in Deutschland betankten Flugzeuge und bildet den nationalen und internationalen Luftverkehr für Güter und Personen ab.

Flughäfen erfüllen in der Regel überregionale Funktionen bei der Bereitstellung von Verkehrsinfrastruktur. Daher wird der mit einem Flughafen verbundene EEV nicht allein der Kommune zugerechnet auf dessen Gebiet sich ein Flughafen befindet. Stattdessen wird der EEV einer Kommune im Luftverkehr anhand der Einwohner der Kommune im Verhältnis zur gesamten Einwohnerzahl in Deutschland pauschal berechnet. Die Berechnungen in LocalZero weichen hier daher von der Einflussbilanz ab. Diese Zuordnung über die Endverbraucher – und damit tatsächlichen Nutzer – wird meist als „gerechter“ erachtet. Wesentliche regulatorische Maßnahmen zur THG-Reduktion sind in dem Bereich zudem auf nationaler oder gar internationaler Ebene umzusetzen. Für eine mögliche zukünftige Anpassung an die Einflussbilanz müssten Verkehrsaufkommen und Kerosinbedarf aller deutschen Flughäfen spezifisch ermittelt und den jeweiligen Kommunen zugewiesen werden.

| **Schifffahrt**

Die Transportleistung in Tonnenkilometern für die Seeschifffahrt ist BMVI (2020) entnommen. Für die Küsten- und Binnenschifffahrt dient UBA (2020a) als Quelle.

Die Berechnung des kommunalen EEV erfolgt, wie im Luftverkehr, auf Basis der Einwohnerzahl und weicht damit von der Einflussbilanz ab. Grundlage ist der bundesweite EEV nach den AG Energiebilanzen (Verbrauch von Diesel und Heizöl in MWh in der Schifffahrt).

Damit folgt die Berechnungslogik der des Luftverkehrs, da die Schifffahrt im Wesentlichen analog eine überregionale Funktion des Gütertransportes erfüllt und die kommunale Einflussnahme gering ist. Für eine mögliche zukünftige Anpassung an die Einflussbilanz müssten Verkehrsaufkommen und EEV auf allen deutschen Wasserstraßen spezifisch ermittelt und den jeweiligen Kommunen zugewiesen werden.

| **Fuß- und Radverkehr**

Grundlage für die Ermittlung der Verkehrsleistung im Fuß- und Radverkehr ist der raumtypenspezifische Modal Split der Verkehrsleistung nach BMVI (2018). Es wird nach den sieben Typen des zusammengefassten regionalstatistischen Raumtypen (RegioStaR 7) differenziert. Die Verkehrsleistung im Fuß- und Radverkehr wird anhand der durchschnittlichen Tagesstrecke eines Einwohners des jeweiligen Raumtyps und der Einwohnerzahl der Kommune berechnet.


7.2.2 Treibhausgas-Emissionen
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Die Berechnung der THG-Emissionen erfolgt im Sektor Verkehr “Tank-to-Wheel" - also für während der Fahrzeugnutzung durch Verbrennung freigesetzte Emissionen. Der berechnete EEV je nach Verkehrsträger wird mit den direkten spezifischen CO2-Emissionsfaktoren (t/MWh) für alle verwendeten Kraftstoffe multipliziert. Datenbasis für die Emissionsfaktoren sowie die Anteile der Kraftstoffarten bildet die UBA Publikation „Aktualisierung TREMOD für die Berichterstattung 2020“ (UBA 2020a).

Die “Well-to-Tank“ THG-Emissionen (Vorkettenemissionen, die bei der Herstellung der Kraftstoffe anfallen) werden im Bereich Kraftstoffe von LocalZero bilanziert.


7.4 Bilanz Zieljahr
-------------------

Das Zieljahr stellt die Erreichung der Klimaneutralität dar. Verschiedene Veröffentlichungen bzw. Szenarien beschreiben mögliche Pfade zur THG-Reduktion durch Vermeidung und Verlagerung von Verkehr sowie durch Verbesserung der genutzten Technologien.

Als Leitszenario für LocalZero wird das GreenSupreme Szenario aus der RESCUE-Studie des UBA (2019) gewählt.  Es stellt ein ambitioniertes Klimaschutzszenario, insbesondere auch in Bezug auf die Vermeidung von Verkehr dar. Weitere Orientierungspunkte gibt zudem die von AGORA in Auftrag gegebene und von Prognos, Öko-Institut und Wuppertal-Institut durchgeführte Studie “Klimaneutrales Deutschland - In drei Schritten zu null Treibhausgasen bis 2050” sowie die Aktualisierung dieser Studie „Klimaneutrales Deutschland 2045“.

7.2.1 Nachfrage und Bereitstellung
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
| **Straßenverkehr**

Die Beförderungsleistung in Personenkilometern im Zieljahr richtet sich nach der Einwohnerzahl sowie dem Raumtyp (Stadt, Halbstadt, Land). Je nach Raumtyp wird ein Modalsplit zwischen den verschiedenen Verkehrsträgern im Zieljahr angenommen (Prognos et al. 2020). Die Berechnung der Fahrleistung in Fahrzeugkilometern erfolgt bei Linienbussen anhand der Fahrzeugauslastung im Jahr 2018 und beim MIV anhand der Annahmen aus dem GreenSupreme Szenario.

Die Energiebereitstellung im MIV und im Linienbusbereich erfolgt zum überwiegenden Teil direkt durch Strom aufgrund der weiten Durchdringung von reinen Elektrofahrzeugen (Prognos et al. 2020). Nur ein kleiner Teil der Bestandsfahrzeuge wird noch mit Verbrennungsmotor betrieben. Dort werden strombasierte Kraftstoffe (E-Fuels) zum Einsatz kommen. Brennstoffzellenantriebe hingegen sollen in diesen Fahrzeugkategorien keine merkliche Rolle spielen.

Im Güterverkehr (LNF und SNF) wird die bundesweite Transportleistung in Tonnenkilometern aus dem UBA GreenSupreme Szenario als Basis genommen. Diese wird anhand der Anteile der Kommunen an der bundesweiten Transportleistung im Jahr 2018 auf die einzelnen Gemeinden umgerechnet. Die Verteilung nach den Straßenkategorien “Innerorts und Außerorts” und “Autobahn” erfolgt nach dem Verhältnis im Basisjahr 2018.

Im Güterverkehr - bei LNF und insbesondere bei SNF - wird neben reinen batterieelektrischen Fahrzeugen ein nennenswerter Anteil mit Wasserstoff betrieben, wobei auch E-Fuels zum Einsatz kommen. Grundlage ist das Szenario aus der AGORA Studie, welches eine Verteilung der Fahrleistung von 80% batterieelektrisch und 20% Wasserstoff bzw. regenerative Kraftstoffe annimmt (Prognos et al. 2020).


| **Schienenverkehr**

Die Beförderungsleistung in Personenkilometern für Straßen-, Stadt- und U-Bahn (SSU) und den Personen-Eisenbahnverkehr errechnet sich aus dem ModalSplit zum ÖPNV aus GreenSupreme bei gleicher Verteilung der öffentlichen Verkehrsträger SSU, Eisenbahn und Linienbussen wie im Basisjahr 2018.

Für SSU-Bahnen erfolgt eine Umrechnung auf Fahrzeugkilometer anhand der Fahrzeugauslastung im Jahr 2018.

Im Schienengüterverkehr wird die Transportleistung über GreenSupreme bezogen und auf die Einwohnerzahl umgelegt.

Im Zieljahr-Szenario von GreenSupreme ist der Schienenverkehr komplett elektrifiziert, d.h. der EEV wird ausschließlich über Strom abgedeckt. Eine mögliche Nutzung von Brennstoffzellenantrieben anstatt heutiger Dieselaggregate wird dabei nicht explizit genannt. Dies wird in der Praxis im Rahmen der Elektrifizierung auch eine gewisse Rolle spielen und sei hier zumindest angemerkt.


**Schifffahrt**

Für die Seeschifffahrt sowie für die Küsten- und Binnenschifffahrt wird der EEV nach GreenSupreme dargestellt und anhand der Einwohnerzahl auf die Kommunen bezogen.

Als Kraftstoffe kommen hier fast ausschließlich strombasierte Kraftstoffe zum Einsatz.


**Luftverkehr**

Auch der EEV für internationale Flüge wird nach GreenSupreme dargestellt und auf die Einwohnerzahl umgelegt. Innerdeutsche Flüge existieren in diesem Szenario nicht mehr.

Der Antrieb der Flugzeuge erfolgt ausschließlich mit E-Kerosin bzw. strombasierten Kraftstoffen.

**Fuß- und Radverkehr**

Der Fuß- und Radverkehr im Zieljahr ergibt sich aus der Prognose zum Modalsplit nach Einwohnerzahl und Raumtyp der Kommune nach Prognos et al. (2020).


7.2.2 Wirkungsgrade und Treibhausgas-Emissionen
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Wie in der Ausgangsbilanz wird der berechnete EEV je nach Verkehrsträger mit den direkten spezifischen CO2-Emissionsfaktoren (t/MWh) für die verwendeten Kraftstoffe multipliziert.

Die CO2-Emissionsfaktoren für Kraftstoffe entsprechen dabei denen im Ausgangsjahr, da nicht davon auszugehen ist, dass sich in der Nutzung die fossilen von den regenerativen Kraftstoffen hinsichtlich ihrer direkten THG-Wirkung unterscheiden. Wesentlicher Grund liegt in dem Erfordernis regenerative Kraftstoffe für bestehende Fahrzeugflotten einsetzen zu können, so dass kaum Spielraum für „CO2-optimierte“ Kraftstoffe bestehen dürfte. Die „CO2-Neutralität“ von regenerativen Kraftstoffen entsteht sozusagen durch die Bindung von CO2 bei der Kraftstoffherstellung und wird dort entsprechend ausgewiesen.

Jedoch werden bei der Berechnung des spezifischen EEV im Zieljahr - je nach Verkehrsträger und Antriebsart - Verbesserungen des Wirkungsgrades durch technischen Fortschritt bei der Antriebstechnologie selbst angenommen.

Dabei werden für den Straßenverkehr aktuelle Endenergieverbrauchswerte des ifeu um prozentuale Effizienzsteigerungswerte für das Zieljahr reduziert. Dies betrifft batterieelektrisch (12-16%) und verbrennungsmotorisch (12-22%) angetriebene Fahrzeuge. Grundlage ist die Fraunhofer Studie „Klimabilanz, Kosten und Potenziale verschiedener Kraftstoffarten und Antriebssysteme für Pkw und Lkw“.

Im elektrisch angetriebenen Schienenverkehr wurden aufgrund der hohen Technologiereife keine wesentlichen Effizienzsteigerungen angenommen.

Die Entwicklung im Flug- und Schiffsverkehr lässt sich hinsichtlich Wirkungsgradverbesserungen schwer quantifizieren und wird deswegen zunächst vernachlässigt.

7.3 Maßnahmen, Investitionen und Beschäftigungseffekte
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Es existiert eine Reihe an Quellen und Studien, welche vielerlei Maßnahmen zur Erreichung der regionalen und überregionalen Klimaziele mehr oder weniger detailliert beschreiben. Neben Veröffentlichungen des UBA (vor allem RESCUE) oder von AGORA (Prognos et al. 2020) gehören dazu auch Studien wie “Klimaschutz in Kommunen” des difu, das “Handbuch Klimaschutz” von Mehr Demokratie oder “CO2 neutral bis 2035” des Wuppertal Instituts, welche auch einen stärker lokalen Bezug darstellen.

Die von jeder Kommune individuell zu ergreifenden Maßnahmen hängen von der jeweiligen Ausgangslage - also bereits erfolgter Umbau zu einem klimafreundlichen Verkehrssystem - und den vorliegenden Rahmenbedingungen hinsichtlich der existierenden bzw. erforderlichen Verkehrsinfrastruktur ab.

Dennoch will LocalZero Kommunen zumindest grobe Richtwerte zu Maßnahmenfeldern, damit verbundenen Investitionserfordernissen sowie daraus entstehenden Beschäftigungseffekten geben.

Als Leitstudie wurde hierzu die Studie Gesamtwirtschaftliche Wirkungen durch die
Transformation zu nachhaltiger Mobilität von “M-FIVE” und  Fraunhofer ISI genutzt, da das hier beschriebene MM35 Szenario dem GreenSupreme Szenario des UBA hinsichtlich zukünftigem Modalsplit und Fahrleistungen sehr ähnlich ist. Die Studie ist zudem eine der wenigen, welche nachvollziehbare Aussagen zu erforderlichen Investitionen und möglichen Beschäftigungseffekten für den Personenverkehr trifft. Die Studienergebnisse werden daher auch für LocalZero übernommen.

Um den Güterverkehr ebenfalls zu adressieren, werden zusätzlich Angaben zu Mehrinvestitionen aus der BCG Studie "Klimapfade für Deutschland” herangezogen.

Investitionen zum Erhalt der Verkehrsinfrastruktur sind dem Bundesverkehrswegeplan entnommen.

Die Investitionen werden wesentlichen Maßnahmen zugordnet. Im Wesentlichen sind dies:

* Zusätzlicher Personalbedarf im Bereich "Verkehrsplanung"

* Investitionen in den ÖPNV: Kauf von E-Bussen, Ausbau der Businfrastruktur und Auf/Ausbau von Straßen- und Stadtbahnen

* Antriebswechsel bei schweren und leichten Nutzfahrzeuge inklusive Aufbau der erforderlichen Infrastruktur z.B. für Oberleitungs-Lkw

* Antriebswechsel bei PkW – also den Kauf elektrisch angetriebener Fahrzeuge

* Ausbau der Ladesäuleninfrastruktur für PKW, LKW und Bus

* Erhalt von Straßeninfrastruktur

* Erhalt, Auf- und Ausbau der Schieneninfrastruktur sowie Investitionen in Züge und Bahnhöfe

* Erhalt und Ausbau der Küsten- und Binnenschifffahrt

* Auf- und Ausbau von Fuß- und Radverkehrsinfrastruktur

Nicht adressiert werden Investitionen in den internationalen Flugverkehr (also im Wesentlichen die Umstellung auf E-Kerosin sowie die Effizienzsteigerung beim Flugzeugantrieben) sowie in die internationale Seeschifffahrt. Die Kosten der Produktion von E-Fuels selbst wird im Sektor Kraftstoffe bilanziert.

Die bundesweiten Investitionssummen aus M-FIVE und der BCG-Studie werden je nach Maßnahme bestmöglich auf die jeweilige Gemeinde umgelegt - Basis ist entweder die Einwohnerzahl oder die Verkehrsleistung des jeweiligen Verkehrsträgers in der Kommune.

Der Anteil der Investitionen, die aus öffentlicher Hand stammen sollten, sind grobe eigene Einschätzungen von GermanZero. So wird beispielsweise der Ausbau der Schieneninfrastruktur und Bahnhöfen der öffentlichen Hand zugerechnet, Investitionen in neue Züge hingegen nicht, da diese von überwiegend privaten Unternehmen beschafft werden. Beim Aufbau der öffentlichen Ladeinfrastruktur wird basierend auf Förderprogrammen des BMVI ein öffentlicher Investitionsanteil von 21% angenommen, beim Ausbau der Businfrastruktur sind es 100%. Generell ist zu betonen, dass mit öffentlicher Hand hier verschiedene Verwaltungsebenen gemeint sein können und diese Zuordnung lokal interpretiert werden muss je nach vorhandener Beteiligungsstruktur.

Der jährliche Investitionsbedarf ergibt sich aus der Gesamtsumme und den verbleibenden Jahren bis zum Zieljahr.

Um zudem Hinweise auf kommunale Beschäftigungseffekte zu geben, dient ebenfalls die M-FIVE Studie als Grundlage. Die dort beschriebenen bundesweiten Beschäftigungseffekte für die Segmente „Landverkehr“ und „Ausbau der Verkehrsinfrastruktur“ reflektieren im Wesentlichen auch den Verkehrsbereich in LocalZero. Die zusätzlich erforderlichen Stellen laut M-FIVE in diesen Bereichen werden über die Einwohnerzahl überschlägig auf die Kommunen umgelegt.

Zudem wird ein Näherungswert für die benötigten Beschäftigten in der Verkehrsplanung angegeben. Als Eckdaten dienen hier ein Anteil von 5% an Planungskosten der Investitionssumme bei Infrastrukturmaßnahmen sowie Personaldurchschnittskosten von 112.000 EUR pro Jahr basierend auf öffentlichen Tarifverträgen.



Quellen
-------
| BMVI (2018): Mobilität in Deutschland − MiD – Ergebnisbericht. Verfügbar unter https://www.bmvi.de/SharedDocs/DE/Anlage/G/mid-ergebnisbericht.pdf?__blob=publicationFile [22.08.2021].

| BMVI (2020): Verkehr in Zahlen 2020/2021. Verfügbar unter https://www.bmvi.de/SharedDocs/DE/Publikationen/G/verkehr-in-zahlen-2020-pdf.pdf?__blob=publicationFile [22.08.2021].

| Destatis (2020): Verkehr: Personenverkehr mit Bussen und Bahnen 2018. Verfügbar unter https://www.destatis.de/DE/Themen/Branchen-Unternehmen/Transport-Verkehr/Personenverkehr/_inhalt.html;jsessionid=B2DC81DA4AC703849259871697F99071.live711 [20.08.2021].

| Fraunhofer ISI (2020): M-FIVE Synthese und Handlungsempfehlungen zu Beschäftigungseffekten nachhaltiger Mobilität. Verfügbar unter: https://m-five.de/wp-content/uploads/M-Five_AP5_Gesamtwirtschaftliche_Analyse_Nachhaltige_Mobilit%C3%A4t_200131_FINAL.pdf [26.08.2021].

| Fraunhofer ISI (2020): M-FIVE Gesamtwirtschaftliche Wirkungen durch die Transformation zu nachhaltiger Mobilität. Verfügbar unter: https://m-five.de/wp-content/uploads/M-Five_AP5_Gesamtwirtschaftliche_Analyse_Nachhaltige_Mobilit%C3%A4t_200131_FINAL.pdf [26.08.2021].

| Ifeu (2019): BISKO Bilanzierungs-Systematik Kommunal, Empfehlungen zur Methodik der kommunalen Treibhausgasbilanzierung  für den Energie- und Verkehrssektor in Deutschland. Verfügbar unter: https://www.ifeu.de/fileadmin/uploads/BISKO_Methodenpapier_kurz_ifeu_Nov19.pdf [26.08.2021].

| ifeu (2021):  Gemeindefein abgeleitete Verkehrsdaten zur kommunalen THG-Bilanzierung für den Bereich Verkehr. Im April 2021 durch das ifeu für das Projekt “LocalZero” zur Verfügung gestellt.

| Nationale Leitstelle Ladeinfrastruktur (2020): Ladeinfrastruktur nach
| 2025/2030: Szenarien für den Markthochlauf. Verfügbar unter https://www.now-gmbh.de/wp-content/uploads/2020/11/Studie_Ladeinfrastruktur-nach-2025-2.pdf [22.08.2021].

| Prognos, Öko-Institut, Wuppertal-Institut (2020): Klimaneutrales Deutschland. Studie im Auftrag von Agora Energiewende, Agora Verkehrswende und Stiftung Klimaneutralität. Verfügbar unter https://www.agora-energiewende.de/veroeffentlichungen/klimaneutrales-deutschland/ [11.08.2021].

| Prognos, Öko-Institut, Wuppertal-Institut (2021): Klimaneutrales Deutschland 2045 - Wie Deutschland seine Klimaziele schon vor 2050 erreichen kann. Verfügbar unter https://www.agora-verkehrswende.de/fileadmin/Projekte 2021/KNDE_2045_Langfassung/KNDE2045_Langfassung.pdf [22.08.2021]

| UBA (2020a): Aktualisierung der Modelle TREMOD/TREMOD-MM für die Emissionsberichterstattung 2020 (Berichtsperiode 1990- 2018). Verfügbar unter https://www.umweltbundesamt.de/publikationen/aktualisierung-tremod-2019 [11.08.2021].

| UBA (2019): RESCUE – Studie, Wege in eine ressourcenschonende Treibhausgasneutralität. Verfügbar unter: https://www.umweltbundesamt.de/rescue [11.08.2021].

| UBA (2020b): Transformationsprozess zum treibhausgasneutralen und ressourcenschonenden Deutschland – GreenSupreme. Verfügbar unter: https://www.umweltbundesamt.de/publikationen/transformationsprozess-treibhausgasneutrales-ressourcenschonendes-deutschland-greensupreme [11.08.2021].

