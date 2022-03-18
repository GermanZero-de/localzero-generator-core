9. LULUCF (inkl. Pyrolyse)
==========================
| **Autor:innen: Jule Schwartz**
| **Stand: 25.02.22**

Dieses Dokument gibt einen Überblick über die wesentlichen Prinzipien, die den Berechnungen für LULUCF (Land use, land use change and forestry) in Local Zero zugrunde liegen. Die Emissionen entstehen alle bei natürlichen Prozessen auf den Flächen der Kommune und sind damit prozessbedingt. Da die Emissionen nur mithilfe von modellierten Emissionsfaktoren ermittelt werden können, unterliegen sie einer großen Unsicherheit und Schwankung. Die nationale THG-Bilanz wird darum einmal mit und einmal ohne LULUCF ausgewiesen. Da diese pb Emissionen aber auch international unter CRF 4 bilanziert werden und aufgrund ihres Senkenpotentials essentieller Teil der Klimaneutralität sind, wird LULUCF in LocalZero mitbilanziert. Dabei wird eine Aufteilung in folgende Subsektoren gemacht: Wald, Ackerland, Grünland im engeren Sinne, Grünland (Gehölze), Feuchtgebiete (terrestrisch), Feuchtgebiete (Gewässer), Siedlungen, Sonstiges und Holzprodukte. Reicht auch diese Senkenleistung im Zieljahr der Klimaneutralität nicht aus, werden als Backup Pyrolyseanlagen aufgebaut, um Kohlenstoff dauerhaft in Pflanzenkohle zu speichern.

9.1 Eingabedaten
-----------------
Grundlage für den Sektor LULUCF sind Flächenangaben. Da diese kommunenfein vorliegen, müssen keine Werte in der Eingabe überschrieben werden.

9.2 Bilanzierung 2018
---------------------
Wichtigste Quelle für die Berechnung der Bilanzen 2018 und im Zieljahr für den LULUCF Sektor war der National Inventory Report der Bundesregierung aus dem Jahr 2020 [NIR 2020]. Er wurde für Angaben zu bundesweiten Emissionen aus dem LULUCF Sektor 2018 genutzt. Diese waren aufgeteilt nach Landnutzungsarten[1] auf Mineral- bzw. organischem Boden[2]. Die Regionalstatistik [Regionalstatistik 2018] lieferte die Flächenangaben für die einzelnen Landnutzungsarten pro Kommune und auf Bundesebene, d.h. wie viel Wald, Acker, Moor etc. in den einzelnen Kommunen vorhanden ist. Bundesweite Flächenangaben aus dem NIR wurden verwendet, um sie mit den Regionalstatistikdaten abzugleichen und die dort angegebenen Flächenangaben zu kontrollieren. Außerdem wurde bei Flächennutzung auf organischem Boden zwischen Niedermoor- und Hochmoorflächen unterschieden. Hierzu wurden Daten von der Universität Greifswald zur Niedermoor- und Hochmoorfläche in Deutschland verwendet [Uni Greifswald 2012].

Um die CO2 Bilanz des LULUCF Sektors für 2018 aufzustellen, wurden zunächst die bundesweiten Emissionsangaben aus dem National Inventory Report [NIR 2020] verwendet. Sie waren pro Landnutzungsart jeweils für Emissionen aus der Landnutzung auf Mineralboden, auf organischem Boden, für Biomasse und Totholz/Streu/tote organische Substanz aufgegliedert angegeben. Unter der Landnutzungsart Wald wurden zudem Emissionen aus Waldbränden aufgeführt. Mit diesen Angaben und den Flächenangaben pro Landnutzungsart aus der Regionalstatistik wurden spezifische Emissionsfaktoren berechnet; so zum Beispiel die Emissionen in Tonnen CO2eq/ha Ackerland auf mineralischem Boden. Für die Berechnung der Emissionen aus organischem Boden war ein weiterer Rechnungsschritt nötig. Mit Hilfe der Daten der Uni Greifswald, dass 76% des deutschen organischen Bodens Niedermoorboden ist und 23% Hochmoorboden, wurden die spezifischen Emissionsfaktoren für Hoch- und Niedermoorboden berechnet.

Um die Emissionen der Kommunen aus dem LULUCF-Sektor zu berechnen, wurde jeder Emissionsfaktor mit den kommunenspezifischen Flächenangaben der entsprechenden Landnutzungsart [Regionalstatistik, 2018] multipliziert und die einzelnen Emissionen addiert, um die Gesamtemission (oder Sequestierung, je nachdem ob die Bilanz positiv oder negativ ist) der Kommune aus diesem Sektor zu ermitteln.


9.3 Maßnahmen
-------------
* Erhöhung der ungenutzten Waldfläche (=Naturwald) auf 6,9% [RESCUE 2019]. Diese lag 2018 nur bei 2,7% [Deutsches Jagdportal 2019].

* Aufforstung aller Waldschadflächen 2018.

* Anwendung von humusaufbauenden Maßnahmen (Zwischenfruchtanbau, verbesserte Fruchtfolge, Ökolandbau, Umwandlung von Acker zu Grünland, Agroforstwirtschaft, Obstwiesen, mehr Festmist und Kompost-Verwendung) auf 25% des Ackerlandes auf Mineralboden [Scheffler & Wiegmann 2019].

* Wiedervernässung von 80% aller organischen Böden unter Grünland (i.e.S.), Grünland (Gehölze) und Ackerland. Erhöhung des Wasserspiegels zum ursprünglichen Zustand in terrestrischen Feuchtgebieten/Mooren [RESCUE 2019].

* Praktizierung von Paludikultur auf 65% aller wiedervernässten organischen Böden [Uni Greifswald 2012].

* Flächenversiegelungsrate von 0 Hektar pro Tag im Zieljahr [RESCUE 2019].

* Speicherung von Kohlenstoff aus Biomasse über die Produktion von Pflanzenkohle zur Kompensation von Restemissionen im Zieljahr.


9.4 Bilanz Zieljahr
--------------------


Um angepasste Emissionsfaktoren für die Zieljahresbilanz zu finden, die in Folge von Klimaschutzmaßnahmen greifen, wurden vier Studien verwendet: Das Greensupreme Szenarion aus der Rescue-Studie des Umweltbundesamtes 2019 [RESCUE 2019], die Ökoinstitut Studie 2019 (Maßnahmenvorschlägen für die Transformation der Landwirtschaft) [Scheffler & Wiegmann 2019], eine Greenpeace Studie zu zukunftsfähigem Wald [Böttcher 2018] und eine Studie aus „Nature“ zur Kohlenstoffspeicherung alter Wälder [Luyssaert 2008].

Für die Zieljahresbilanz wurden die Flächenangaben von 2018 aus der Regionalstatistik wieder verwendet. Dann wurden, je nach angewandter Maßnahme, Flächen in einigen Landnutzungskategorien verkleinert und in anderen vergrößert (s. Maßnahmen). Diese neuen Flächenangaben wurden dann mit den alten und je nach Maßnahme einigen neuen Emissionsfaktoren multipliziert. Die resultierenden Emissionen pro Landnutzungsart wurden addiert und bildeten die Gesamtemission (oder -sequestierung) aus LULUCF der Kommune im Zieljahr.

Sofern in der Kommune trotz aller Klimaschutzmaßnahmen in den verschiedenen Sektoren im Zieljahr noch Emissionen bestehen, können diese durch die Produktion von Pflanzenkohle (Pyrolse) aus Biomasse und deren langfristiger Speichermöglichkeiten von Kohlenstoff z.B. im Boden kompensiert werden. Die Gesamtemissionen der Kommune im Zieljahr über sämtliche Sektoren hinweg bildete die Grundlage für die Berechnung der zu produzierenden Pflanzenkohle. Hierzu wurde die Menge der restlichen Emissionen in CO2-Äquvalenten in die Menge zu kompensierenden Kohlenstoffs umgerechnet. Unter der Annahme, dass Pflanzenkohle zu durchschnittlich etwa 65% aus Kohlenstoff besteht [UBA 2016], wurde die Menge zu produzierender Pflanzenkohle berechnet. Die Kosten für die Pyrolyseanlage wurde für eine Kapazität von 2000 t Pflanzenkohle pro Jahr auf 721.000 Euro angenommen [Teichmann 2015].


Quellen
-------
| [NIR 2020]: Umweltbundesamt (April 2020). Submission under the United Nations Framework Convention on Climate Change and the Kyoto Protocol 2020. National Inventory Report for the German Greenhouse Gas Inventory 1990 – 2018. Federal Environment Agency. Retrieved from https://unfccc.int/ghg-inventories-annex-i-parties/2020

| [Regionalstatistik 2018]: Regionalstatistik 2018 Bodenfläche nach Art der tatsächlichen Nutzung. Retrieved from https://www.regionalstatistik.de/genesis//online?operation=table&code=33111-01-02-5&bypass=true&levelindex=0&levelid=1630590227869#abreadcrumb

| [Uni Greifswald 2012]: Universität Greifswald (August 2012). Moore in Deutschland: Nutzung und Klimawirkung. BMBF Projekt VIP – Vorpommern Initiative Paludikultur. Retrieved from https://www.moorwissen.de/doc/infothek/Factsheet%20-%20Moore%20in%20Deutschland%20-%20Nutzung%20und%20Klimawirkung.pdf, https://infoportal-kirchenland.de/oekologische-aspekte/landbewirtschaftung-&-moore/paludikultur/

| [RESCUE 2019]: UBA 2019_RESCUE_Wege in eine ressourcenschonende Treibhausgasneutralität (Climate Change 2019)

| [Scheffler & Wiegmann 2019]: Scheffler, M. & Wiegmann, K. (2019). Quantifizierung von Maßnahmenvorschlägen der deutschen Zivilgesellschaft zu THG-Minderungspotenzialen in der Landwirtschaft bis 2030. Berlin: Ökoinstitut e.V. Retrieved from https://www.oeko.de/fileadmin/oekodoc/Quantifizierung-von-Massnahmenvorschlaegen-der_Klima-Allianz_Landwirtschaft.pdf

| [Böttcher 2018]: Böttcher, H., Hennenberg, K. & Winger, C. (2018). Waldvision Deutschland. Berlin: Ökoinstitut e.V., S.7. Retrieved from https://www.greenpeace.de/sites/www.greenpeace.de/files/publications/20180228-greenpeace-oekoinstitut-waldvision-methoden-ergebnisse.pdf

| [Luyssaert 2008]: Luyssaert, S.; Schulze, E.-D.; Börner, A.; Knohl, A.; Hessenmöller, D.; Law, B. E. et al. (2008): Old-growth forests as global carbon sinks. In: Nature 455 (7210), S. 213–215. DOI: 10.1038/nature07276.

| [Deutsches Jagdportal 2019]: Deutsches Jagdportal, 17. April 2019. Retrieved from https://www.deutsches-jagdportal.de/portal/index.php/aktuelles/8708-deutschland-hat-zu-wenig-flaeche-fuer-naturwaelder#!/ccomment

| [UBA 2016]: Umweltbundesamt 2016._Chancen und Risiken des Einsatzes von Biokohle und anderer "veränderter" Biomasse als Bodenhilfsstoffe oder für die C-Sequestrierung in Böden, S. 36.

| [Teichmann 2015]: Teichmann 2015. Data Documentation An Economic Assessment of Soil

| Carbon Sequestration with Biochar in Germany: Data Documentation, S. 11 (or 1). Retrieved from: https://www.diw.de/documents/publikationen/73/diw_01.c.502939.de/diw_datadoc_2015-078.pdf.







[1] Die Landnutzungsarten umfassen: Wald, Acker, Grünland, Feuchtgebiete, Siedlungen und sonstiges Land. Zusätzlich werden im LULUCF-Sektor die Emissionen aus Holzprodukten erfasst.

[2] Organischer Boden besteht i.d.R. auf Flächen, auf denen ehemals bzw. noch aktuell Moor lag. Entsprechend sind Treibhausgas-Emissionen von Flächen auf organischem Boden i.d.R. deutlich höher als auf mineralischen Boden.




