5. Haushalte (HH) und Gewerbe/Handel/Dienstleistung (GHD)
=========================================================
| **Autor: Manfred Schüssler, Hauke Schmülling**
| **Stand: 25.02.22**

Dieses Dokument gibt einen Überblick über die wesentlichen Prinzipien, die den Berechnungen für Haushalte und GHD in der Klimavision zugrunde liegen. Das Vorgehen ist in beiden Sektoren ähnlich: Ausgehend vom Gebäudebestand 2018 werden zunächst die energetisch schlechtesten Gebäude saniert und deren Heizung durch Wärmepumpen oder Solarthermie ersetzt. Vereinfacht wird dieses Vorgehen auch in Betriebe und Maschinen (BuM) im Sektor Landwirtschaft angewandt, deren Gebäude aus den Nichtwohngebäuden von GHD exkludiert wurden.

5.1 Eingabedaten
----------------
Der Energiebedarf und die daraus resultierenden THG-Emissionen setzen sich in diesen beiden Bereichen aus den Bedarfen für Strom und für Wärme zusammen. Im Bereich GHD wird für 2018 in [AGE2021] auch noch ein Anteil an Kraftstoffen (Benzin, Diesel, Kerosin) ausgewiesen, die offensichtlich nicht dem Bereich Verkehr zugerechnet werden (ebenso ein Anteil Benzin bei den Haushalten). Allerdings werden in den Auswertungstabellen [AGE2020] diese Energieträger nicht in den Bereichen HH und GHD aufgeführt, dafür aber in Blatt 6.5 im Bereich “Landwirtschaft/Fischerei/Bauwirtschaft". Daher wurden diese Werte der Landwirtschaft von den Gesamtzahlen für GHD in [AGE2021] abgezogen. Für den Strombedarf 2018 werden die Daten ebenfalls den Tabellen in [AGE2020] entnommen.

Bei den Berechnungen in den Bereichen HH und GHD geht es im hauptsächlich um den Bedarf und die Bereitstellung von Wärme für Gebäudeheizung, Warmwasserversorgung und Kochen. Dazu werden für die Haushalte Daten über die Gebäude mit Wohnraum und Wohnungen gemeindespezifisch auf der Basis des Gebäudezensus von 2011 [ZENSUS2011] verwendet, insbesondere auch nach Baujahresklassen unterteilt. Dazu kommen Informationen über den Anteil von Wohnungen mit Fernwärmeanschluss und den Anteil der Wohnfläche im kommunalen Eigentum. Die Zahl der neu gebauten Wohngebäude in Deutschland nach 2011 wurde der Quelle [DESTATIS2020] entnommen und nach der Einwohnerzahl auf die jeweilige Kommune umgerechnet. Dieser Wert kann beim Vorliegen genauerer kommunaler Daten von den Benutzer:innen in der Eingabe korrigiert werden.

Für die Gebäude im Bereich GHD (Nichtwohngebäude) liegen leider keine gemeindespezifischen Daten vor. Der bundesdeutsche Gesamtwert gemäß [DENA2016] wird deshalb gemäß Einwohnerzahl auf die Kommune umgerechnet.

| Weitere möglicherweise später überschreibbare Eingabemöglichkeiten betreffen
| a) die Sanierungsrate (energetische Sanierung und Heizungserneuerung) des Gebäudebestands pro Jahr. Standardmäßig ist ein Wert von 4% gemäß [GZ2021] voreingestellt (der heutige Wert liegt um die 1% pro Jahr).
| b) den gewünschten Anteil der mit Fernwärme geheizten Wohnungen im Zieljahr.
| Standardmäßig ist der jetzige Stand voreingestellt.

5.2 Bilanzierung 2018
---------------------
5.2.1 Nachfrage und Bereitstellung
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Zunächst wird die Bereitstellung der für Heizung/Warmwasser/Kochen relevanten Energieträger (Kohle, Heizöl, Erdgas, Flüssiggas, Biomasse, Fernwärme, Solarthermie, Luft- und Erdwärme (Wärmepumpe) und Elektro-Direktheizung aus [AGE2020] bestimmt.

Für den Bereich Haushalte wird der Energiebedarf für die verschiedenen Baualtersklassen in einem ersten Schritt gemäß der jeweiligen Wohnfläche und dem spezifischen Wärmebedarf pro qm gemäß [BMWI2014] verteilt. Die resultierende Summe des Heizenergiebedarfs über alle Gebäude ist (für Deutschland gesamt) etwa 15% höher als der aus der Bereitstellung der Energieträger berechnete Wert. Dies dürfte auf Wirkungsgradeffekte und auch darauf zurückzuführen sein, dass wir auch indirekte Heizeffekte, z.B. aus der Abwärme von Elektrogeräten und anderen Quellen. haben. Um dies zu berücksichtigen, wird die Verteilung der Energiebereitstellung auf die Gebäudealtersklassen gemäß dem prozentualen Anteil des gemäß [BMWI2014] berechneten Energiebedarfs vorgenommen. Dadurch ergeben sich effektive Werte für die spezifische Wärmebereitstellung pro qm für die verschiedenen Gebäudealtersklassen.

Da wir im Bereich GHD keine Information über Gebäudealtersklassen haben, wird eine solche Prozedur dort nicht vorgenommen und die Bereitstellung pro qm aus der gesamten Bereitstellung für Heizwärme und Warmwasser dividiert durch die Gesamtfläche der Nichtwohngebäude (abzüglich des Anteils der Betriebsgebäude im Bereich Landwirtschaft, die dort separat betrachtet werden) berechnet.

5.2.2 Treibhausgas-Emissionen
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Die aus der Bereitstellung von Energie resultierenden THG-Emissionen werden unter Verwendung der jeweiligen Emissionsfaktoren aus [NIR2020] (Tabelle 563) getrennt für HH und GHD berechnet. Für Strom werden die Emissionen gemäß Einflussbilanz nur im Sektor “Strom” ausgewiesen. Für die Fernwärme werden die Emissionen entsprechend nur im Bereich “Wärme” ausgewiesen.

5.2.3 Kosten
^^^^^^^^^^^^
Kosten für die verschiedenen Energieträger für die Endverbraucher in HH und GHD werden gemäß mittleren Preisen in 2018 berechnet, werden derzeit (Stand 2021) aber nicht in der Klimavision ausgewiesen, da diese Berechnungen in den anderen Sektoren nicht vorliegen.


5.3 Maßnahmen
-------------
Die Maßnahmen betreffen zwei Bereiche: auf der Nachfrageseite führt die energetische Sanierung der Gebäude (Dämmung, Fensteraustausch usw.) zu einem verringerten spezifischen Wärmebedarf. Dies gestattet auf der Seite der Bereitstellung die Umrüstung der Heizungssysteme in den sanierten Gebäuden auf Wärmepumpen mit unterstützender Solarthermie. Zusätzlich wird die Fernwärmeversorgung mindestens konstant gehalten, wobei diese auf klimaneutrale Erzeugung (Großwärmepumpen, Solarthermiefelder mit Großspeichern) umgestellt wird (ist im Bereich “Wärme” näher ausgeführt). Bei den bis zum Zieljahr noch nicht sanierten Gebäude werden die Heizungen auf synthetisches e-Methan umgestellt.

Das Vorgehen der Bereitstellung im Detail: Gebäude, die derzeit bereits mit Biomasse, Fernwärme, Direktheizung, Solarthermie oder Wärmepumpe beheizt werden, werden zunächst nicht saniert, da diese Energiequellen (fast) klimaneutral bereitstellbar sind. Daher werden zunächst all die Häuser saniert, die derzeit eine fossile Heizungsanlage haben: Dabei wird angenommen, dass Kohle und Heizöl komplett verdrängt wird und je nach Zieljahr der Klimaneutralität als einziger quasi-fossiler Energieträger E-Methan (als Ersatz für Erdgas) übergangsweise genutzt wird. Verdrängt werden diese durch Wärmepumpen (plus Solarthermie), die bei der energetischen Sanierung eingesetzt werden. Erst wenn alle fossil geheizten Gebäude saniert und mit Wärmepumpen ausgestattet sind, werden Gebäude saniert, die heute schon mit Biomasse, Fernwärme oder Direktheizung versorgt werden, sodass deren Energiebedarf sukzessive sinkt. Bei diesen drei Wärmetypen wird als standardmäßig kein Zuwachs der beheizten Gebäudezahl angenommen, auch wenn in einer späteren Version insbesondere ein gewisser Ausbau der Fernwärme je nach kommunaler Situation möglich wäre.

Bei der energetischen Sanierung gehen wir nicht davon aus, dass alle Gebäude bis zum Zieljahr (das ja typischerweise 2030 oder 2035 sein wird), saniert werden können. Bei einer gegenwärtigen Rate von etwa 1% der Gebäude pro Jahr, würde dies z.B. für Zieljahr 2030 eine Verzehnfachung der Sanierungsrate erfordern, was unrealistisch ist. Stattdessen geben wir eine ambitionierte mittlere Sanierungsrate von 4% vor (die in einer späteren Version ggf. von den Benutzenden geändert werden kann) und priorisieren die Sanierung der besonders ineffizienten älteren Gebäudealtersklassen mit höheren Sanierungsraten.
Dazu verteilen wir die gesamte zu sanierende Fläche bis zum Zieljahr (d.h. Summe der Flächen für alle Baujahre bis 2004 x Sanierungsrate x Jahre bis zum Zieljahr) gemäß dem prozentualen Anteil der entsprechenden Baujahresklassen am Energiebedarf aller zu sanierenden Baualtersklassen gemäß [BMWI2014]. Baujahre ab 2005 werden nicht saniert, da sie gemäß den Energieeinsparungsverordnungen (EnEV) ab 2004 bereits einen Endenergiebedarf von unter 70 kWh pro qm und Jahr (mit der EnEV 2009 unter 45 kWh pro qm und Jahr, KfW-Effizienzhaus 70) aufweisen. Damit liegt dieser Gebäudebestand nahe am oder unter dem hier angenommenen Wert von 45 kWh pro qm und Jahr nach energetischer Sanierung.

Bemerkung: Beim jetzt realisierten Konzept der priorisierten energetischen Sanierung mit vorgegebener Sanierungsrate kann es vorkommen (allerdings nur bei Zieljahren ab 2041), dass Gebäudealterklassen eine Sanierungsrate von 100% erreichen. Die dadurch freiwerdende Sanierungskapazität sollte dann eigentlich auf die anderen Altersklassen verteilt werden (iterativ). Solch eine Prozedur ist gegenwärtig nicht realisiert und sollte für spätere Updates überlegt werden. Der Unterschied in den Resultaten ist nicht sehr groß - und vermutlich erheblich kleiner als die Unsicherheiten in den Annahmen allgemein, insbesondere was die Sanierungsrate angeht.

Eine weitere wesentliche Maßnahme ist eine erhebliche Intensivierung der Energieberatung (kombiniert für Strom und Wärme) im Sinne einer aufsuchenden Beratung, durch die bis zum Zieljahr jedes Gebäude mindestens einmal erfasst wird.


5.4 Bilanz Zieljahr
-------------------
5.4.1 Nachfrage
^^^^^^^^^^^^^^^

Durch die energetische Sanierung ergibt sich ein insgesamt geringerer Energiebedarf der Gebäude. Dabei wird angenommen, dass der Gebäudebestand insgesamt konstant bleibt. Das kann im Einzelfall jeder Kommune natürlich anders sein (wachsende Städte, schrumpfende Landgemeinden). Auch die Wirkungen des demographischen Wandels und mögliche Suffizienzeffekte (mögliche Verringerung der mittleren Wohnfläche pro Person) können nicht belastbar prognostiziert werden. Insoweit Neubauten Gebäude aus älteren Baujahresklassen ersetzen, würde sich der Energiebedarf insgesamt gegenüber den hier berechneten Werten weiter reduzieren.

5.4.2 Bereitstellung
^^^^^^^^^^^^^^^^^^^^
Im Zieljahr werden keine fossilen Energieträger mehr verwendet (Kohle, Heizöl, Erdgas, Flüssiggas), sondern ausschließlich erneuerbare Energien eingesetzt. Dabei wird angenommen, dass alle sanierten Gebäude mit Wärmepumpen beheizt werden und die nicht durch Photovoltaik belegten Dachflächen für Solarthermie genutzt werden. Dabei werden die verfügbaren Dachflächen gemäß dem Wohn/Nutzflächenanteil von HH und GHD verteilt und die mittlere spezifische Leistung (Wärmeertrag pro qm Kollektorfläche und Jahr) nach [SOLTHERM2015] angenommen. Bestehende Fernwärmeanschlüsse bleiben erhalten. Der Beitrag der Biomasse (im wesentlichen Holzfeuerung) wird als konstant angenommen; tendenziell sollte er wie die Elektro-Direktheizung (da ineffizient im Vergleich mit Wärmepumpen) im weiteren Verlauf sinken. Der nicht durch diese Quellen abgedeckte Restbedarf wird durch E-Methan gedeckt, wobei angenommen wird, dass es sich dabei um verbleibende Gasheizungen handelt. Da die Herstellung des E-Methans aus Strom mit erheblichen Verlusten behaftet ist und dafür erhebliche Produktions-Kapazitäten aufgebaut werden müssen, ist diese „Brückentechnologie“ nicht optimal, aber die einzige Alternative zu einer noch höheren Sanierungsrate, um die Klimaneutralität zu erreichen.

5.4.3 THG-Emissionen
^^^^^^^^^^^^^^^^^^^^
Da keine fossilen Brennstoffe mehr eingesetzt werden und die CO2-Emissionen bei der Holzverbrennung nicht in die Bilanz eingehen (durch die Verrechnung mit der Sequestrierung in der Forstwirtschaft), fallen nur noch Emissionen von Methan (CH4) und Lachgas (N2O) durch Biomasse an. Diese werden wie in Abschnitt 4.2.2 (im Bereich “Strom”) beschrieben bilanziert.

5.4.4 Kosten
^^^^^^^^^^^^
Kostenfaktoren sind die Investitionen für die energetische Sanierung der Gebäude, die Umrüstung der Heizungsanlagen (Wärmepumpen und Solarthermie) und die aufsuchende Energieberatung.

Für die energetische Sanierung werden Kosten pro qm für verschiedene Gebäudearten (Ein-, Zwei-, Mehrfamilienhäuser) und Gebäudealtersklassen aus [NMYOEN2020] angenommen und gemäß den entsprechenden Anteilen an der Gesamtwohnfläche in der Kommune berechnet. Multipliziert mit der sanierten Fläche in den jeweiligen Gebäudealtersklassen ergibt sich dann die Investitionssumme. Für die Wohnungen im kommunalen Eigentum werden die Kosten für Großsiedlungen angenommen, da die meisten kommunalen Wohnungen in solchen  zu finden sind, bzw. bei solchen Sanierungen typischerweise Skaleneffekte zu geringeren spezifischen Investionskosten führen.

Bei der Umrüstung der Heizsysteme wird angenommen, dass alle sanierten Gebäude mit Luft- oder Erdwärmepumpen ausgestattet werden und ein Teil der Wärme für Heizung und Warmwasser auch durch den Ausbau von Solarthermie gewonnen wird.
Die resultierenden Investitionskosten (Kollektoren, Speicher, Leitungen, Installation  usw.) werden für Solarthermie gemäß einem typischen Preis pro qm Kollektorfläche nach [EEXP2021] berechnet.  Für Wärmepumpen werden mittlere Kosten pro kWh thermischer Leistung für Luft- und Erdwärmepumpen nach [UBA2016] gemäß der Anteile des jeweiligen Typs an den Neuanlagen gemäß [BWP2021] berechnet. Der Anteil der öffentlichen Hand (Kommune) an den Investitionskosten ergibt sich aus dem prozentualen Anteil der kommunalen Wohnfläche (für HH), bzw. dem kommunalen Anteil an der Fläche der Nichtwohngebäude.

Bei der aufsuchenden Energieberatung wird angenommen, dass für jedes Gebäude bis zum Zieljahr eine ausführliche Beratung durchgeführt wird. Die Kosten pro Gebäude sind separat für Ein- und Zweifamilienhäuser sowie Mehrfamilienhäuser in [KLEIN2021] angegeben. Für Nichtwohngebäude (GHD) wird der mittlere Wert für Mehrfamilienhäuser angenommen.

5.4.5 Stellen
^^^^^^^^^^^^^
Um die Zahl der für die Maßnahmen erforderlichen Personalstellen (Vollzeitäquivalente) abzuschätzen, wird zunächst der prozentuale Personalkostenanteil am Umsatz der jeweiligen Branche (Ausbau- und Heizungshandwerk usw.) ermittelt und mit der Gesamtinvestition multipliziert. Das Ergebnis wird dann durch die Personalkosten pro Kopf geteilt, die in den meisten Fällen der Quelle [DESTATIS2017] entnommen wurden. Das Ergebnis wird dann mit der Zahl der Beschäftigten in der jeweiligen Branche verglichen und so die Zahl der erforderlichen neuen Stellen bestimmt, falls die vorhandenen Stellen nicht ausreichen. Für die Kommune werden jeweils die bundesweiten Personalzahlen mit dem Verhältnis der Einwohnerzahl Kommune zur Einwohnerzahl Deutschland skaliert.

Die vorhandenen Stellen für das Ausbaugewerbe wurden [DESTATIS2017] entnommen, die Beschäftigtenzahl im Heizungsinstallationsgewerbe einer Abfrage bei der Datenbank GENESIS des Statistischen Bundesamtes  [DESTATIS2019].

Bei der Energieberatung nehmen wir der Einfachheit halber an, dass die Kosten nur Personalkosten sind. Die Zahl der erforderlichen Stellen ergibt sich dann durch Division der jährlichen Kosten durch das mittlere Gehalt von Energieberater:innen aus [AEB2021]. Die gegenwärtig (2019) vorhandene Zahl von Stellen in diesem Bereich ist in  [BFEE2020] ausgewiesen.

In einigen Fällen greifen verschiedene Maßnahmen auf den gleichen Pool von Arbeitskräften zu (z.B. Installation von Wärmpumpen und Solarthermie). Es werden dann die vorhandenen Stellen formal anteilig nach dem jeweiligen Bedarf der Maßnahme verteilt, so dass in der Summe nicht mehr vorhandene Stellen ausgewiesen werden als tatsächlich existieren. Entsprechend werden die vorhandenen Stellen zwischen HH, GHD und BuM gemäß den jeweiligen Anteilen am Bedarf verteilt.


Quellen
-------

Hier nicht aufgeführte Quellen: siehe Erklärungsdokument “Strom”

| [AEB2021]: https://www.ausbildung-energieberater.de/energieberater-gehalt/

| [BFEE2020]: Bundesstelle für Energieeffizienz (BfEE) (Hrsg.), „Empirische Untersuchung des Marktes für Energiedienstleistungen, Energieaudits und andere Energieeffizienzmaßnahmen im Jahr 2019“, Endbericht 2019 - BfEE 17/2017, S.28
| https://www.bfee-online.de/SharedDocs/Downloads/BfEE/DE/Energiedienstleistungen/markterhebung2020.pdf?__blob=publicationFile&v=3

| [BMWI2014]: Sanierungsbedarf im Gebäudebestand, BMWI, S. 7
| https://www.bmwi.de/Redaktion/DE/Publikationen/Energie/sanierungsbedarf-im-gebaeudebestand.pdf?__blob=publicationFile&v=3

| [BWP2021]: https://www.waermepumpe.de/presse/pressemitteilungen/details/positives-signal-fuer-den-klimaschutz-40-prozent-wachstum-bei-waermepumpen/#content

| [DENA2021]: Gebäudereport 2016, Deutsche Energie-Agentur, S. 156
| https://www.dena.de/fileadmin/user_upload/8162_dena-Gebaeudereport.pdf

| [EEXP2021]: https://www.energie-experten.org/heizung/solarthermie/wirtschaftlichkeit/kosten

| [GZ2021]: „Maßnahmen für ein 1,5-Grad-Gesetzespaket", GermanZero  (2021), S. 313
| https://germanzero.de/media/pages/assets/fcd6e7bfe9-1635502123/GermanZero_Massnahmenkatalog_210907.pdf

| [KLEIN2021:] https://www.drklein.de/energieberater.html#c236239

| [NMYOEN2020]: "Kosten der klimaneutralen Sanierung des Berliner Wohngebäudebestands", nymoen 2020, S. 6
| https://www.energietage.de/fileadmin/user_upload/2020/Vortraege/2.08_Nymoen_Ergebnisse_Kosten_Klimaneutralitaet.pdf

| [SOLTHERM2015]: http://solarthermie-info.de/fakten-kennzahlen/kollektorertag-kollektorleistung/#ertraege

| [UBA2016]: “Klimaneutraler Gebäudebestand 2050”, Umweltbundesamt (2016),  S. 248
| https://www.umweltbundesamt.de/sites/default/files/medien/378/publikationen/climate_change_06_2016_klimaneutraler_gebaeudebestand_2050.pdf

| [ZENSUS2011]: https://www.zensus2011.de/SharedDocs/Downloads/DE/Pressemitteilung/DemografischeGrunddaten/xlsx_GebaudeWohnungen.xlsx;jsessionid=A8A9D39FD3A2B9D9C28301C0FB3DF61E.live932?__blob=publicationFile&v=2













