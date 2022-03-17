3. Kraftstoffe
==============
| **Autor: Leon Schomburg, Hauke Schmülling**
| **Stand: 23.02.22**


Dieses Dokument gibt einen Überblick über die wesentlichen Prinzipien, die den Berechnungen für Kraftstoffe in LocalZero zugrunde liegen. Generell ist mit Kraftstoffen hier nur die Bereitstellung (nicht die Nutzung) von den Endenergieträgern gemeint, die hauptsächlich zur Fortbewegung genutzt werden, also Benzin, Diesel, Kerosin (sowie die entsprechenden synthetischen Kraftstoffe (E-Fuels)), Bioethanol, Biodiesel, Biogas, E-Methan und Wasserstoff. Damit ist dies grob die analoge Auslagerung der Endenergieträgerproduktion aus dem Sektor Verkehr wie dies bereits mit Strom und Wärme aus PH, GHD, Industrie und Landwirtschaft erfolgt ist. Grundsätzliches Vorgehen ist: Erhebung der Bedarfe, Bereitstellung mit unterschiedlichen Endenergieträgern, THG-Emissionen abgeleitet mit Emissionsfaktoren aus der Produktion der Endenergieträger.

3.1 Eingabedaten
----------------
Grundlage der THG-Bilanzierung 2018 ist der Endenergieverbrauch (EEV) 2018 der Kraftstoffe in Megawattstunden (MWh) in den Sektoren PH, GHD, Verkehr, Industrie und Landwirtschaft. Als User:in kann man dort jeweils Defaultwerte der EEV überschreiben, wenn diese für die Kommune bekannt sind. Diese Default-Werte werden i.d.R. basierend auf der Bilanz 2018 der AG Energiebilanzen ermittelt (siehe jeweils die Sektoren-Texte). Nur im Bereich Verkehr liegen bereits kommunenfeine Fahrleistungen und EEV vor, weswegen auf diese zurückgegriffen wird, auch wenn diese in Summe leicht von AG Energiebilanzen abweichen.

| **Benzin:** AG EB 2018 Spalte L, aggregiert in Zeile 45
| **Diesel:** AG EB 2018 Spalte O, aggregiert in Zeile 45
| **Kerosin:** AG EB 2018 Spalte N, aggregiert in Zeile 45
| **Bioethanol, Biodiesel, Biogas:** entspricht grob AG EB 2018 Spalte AA, aggregiert in Zeile 72


Die (eventuell überschriebenen) Kraftstoffverbräuche der Sektoren werden im Sektor Kraftstoffe dann Sektor-summiert unter Nachfrage und Kraftstofftyp-summiert unter Produktion aufgelistet.

3.2 Bilanzierung 2018
---------------------
Für das Bilanzjahr 2018 wurden die Treibhausgasemissionen, die bei der Herstellung, Verarbeitung, Transport und Lagerung der fossilen Kraftstoffe anfallen, nicht über Vorketten-Emissions-Faktoren aus dem TREMOD-Modell (vgl. [Umw20a] S. 122) abgebildet, sondern analog zum Wärme-Sektor von CRF 1.A.1.b abgeleitet, um nur die in Deutschland anfallenden Vorketten-Emissionen zu betrachten und mit dem NIR kongruent zu sein. Diese cb Emissionen werden durch die Zeilensummen der AG EB geteilt, um Emissionsfaktoren pro MWh EEV zu enthalten.


| **Benzin:**
| Cb Emissionen = 4.126.534 (Anteil von CRF 1.A.1.b)
| Da in CRF 1.A die "Verbrennung von Brennstoffen" gemeldet wird, handelt es sich bei CRF 1.A.1.b Mineralölraffinerien um verbrennungsbedingte Emissionen zur Produktion von Mineralölprodukten. Diese cb Emissionen entspringen im NIR auf S. 177 einer Produktion von 101 Mt Mineralölprodukte (was mit dem MWV Jahresbericht 2019 passt), aber aufgeteilt auf 53 Mt Kraftstoffe, 19,9 Mt Heizöl, 6 Mt Naphtha verbleiben uns ca. 22 Mt auf andere Produkte (was im MVW gar nicht auftaucht und mit Quellenangaben des NIR nicht nachvollziehbar ist, weswegen zur Emissionsverteilung die Produktionsmengen des MWV Jahresbericht 2019 herangezogen werden). [Min19]

| **Diesel:**
| Cb Emissionen = 5.928.633 (Anteil von CRF 1.A.1.b)
| anteilig nach Produktionsmenge laut MWV Jahresbericht 2019 (Erklärung siehe Benzin)

| **Kerosin:**
| Cb Emissionen = 960.154 (Anteil von CRF 1.A.1.b)
| anteilig nach Produktionsmenge laut MWV Jahresbericht 2019 (Erklärung siehe Benzin)

| **Bioethanol, Biodiesel, Biogas (Biomasse):**
| Die AG-EB-Energieträger-Klasse Biomasse und erneuerbare Abfälle hat keine Entsprechung in NIR CRF 1. Wir gehen jedoch davon aus, dass die Emissionen der Erzeugung und Lagerung bereits in der ursprünglichen Produktion der Biomasse erfasst sind (also CRF 3), daher schreiben wir der Produktion/Bereitstellung dieses Energieträgers keine zusätzlichen Emissionen zu. Zudem weist der NIR selbst die verbrennungsbedingten Emissionen der Biomasse nur nachrichtlich aus (NIR S. 877 Fußnote 3), was wir jedoch in LULUCF korrigieren.



3.3 Maßnahmen
-------------
Im Zieljahr werden keine fossilen Kraftstoffe mehr eingesetzt. Für den Flug- und Schiffverkehr sowie Restbestände von mit Verbrennungsmotoren betriebenen Fahrzeugen im Straßenverkehr werden synthetisch aus Strom, Wasser und Kohlenstoffdioxid hergestellte Kraftstoffe (E-Fuels in Form von E-Benzin, E-Kerosin und E-Diesel) benötigt (vgl. [Pro20] S. 95). Auch wenn Studien davon ausgehen, dass die über Power to Gas (PtG) / Power to Liquid (PtL) hergestellten Kraftstoffe im Zieljahr zu gut drei Vierteln importiert (vgl. [Umw20b], S. 94) werden, nehmen wir in LocalZero an, dass die entsprechenden Produktionskapazitäten in der Kommune selbst aufgebaut werden. Entsprechend werden Stromerzeugung und Investitionen in die Anlagen angepasst. Je zeitnäher das Zieljahr ist, um so weniger realistisch ist das zwar - aber das gilt natürlich auch für die Importmöglichkeiten. Auf jeden Fall gilt, den Bedarf für synthetische Kraftstoffe möglichst zu minimieren und alle Möglichkeiten zu nutzen, Elektrizität direkt zu nutzen.

Neben dem Aufbau von Anlagen für E-Fuels werden E-Methan-Anlagen benötigt: In der Industrie, aber auch in nicht-sanierten (oder ohne Heizungsaustausch) Gebäuden wird E-Methan das fossile Erdgas ersetzen müssen. Nur dann wird durch die CO2-Bindung bei dieser synthetischen Kraftstoffproduktion auf dem kommunalen Gebiet die entsprechenden Positivemissionen bei deren Verbrennung ausgeglichen und Klimaneutralität ist rechnerisch möglich.

Außerdem muss mit Elektrolyseuren Wasserstoff für den Verkehr und die Industrie produziert werden. Aus der immensen Stromabhängigkeit unserer klimaneutralen Kommune ergibt sich aber noch ein zusätzlicher Bedarf: Etwa alle 2 Jahre tritt eine sogenannte kalter Dunkelflaute, in der etwa 2 Wochen lang zu wenig Wind weht und zu wenig Sonne scheint, um unseren Strombedarf zu decken [Ene17]. Für diesen Fall müssen immense Mengen Wasserstoff zurückgehalten werden, die in diesem Notfall mit GuD-Kraftwerken rückverstromt werden können. Energetisch ist das problematisch, weil bei der doppelten Umwandlung von Strom in Wasserstoff und zurück etwa die Hälfte der Energie „verloren“ geht. Außerdem erforderte dieser Umstand eine gewisse Entkopplung der LocalZero-Berechnungen von Strom und Wasserstoff, um einen Zirkelschluss zu vermeiden. Mehr Details finden sich im Erklärtext Strom.

Das Zwischenprodukt Wasserstoff bei der Herstellung der anderen synthetischen Kraftstoffe wird nicht gesondert ausgewiesen, sondern ist in den Wirkungsgraden als Zwischenschritt jeweils schon inkludiert. Bei allen Kraftstoffen im Zieljahr wird die benötigte Strommenge über entsprechende Wirkungsgrade bei der Herstellung ermittelt (vgl. [Öko20] S. 12; [FVV18] S. 30) und an den Sektor Strom übergeben.

Von den Endenergiebedarfen lassen sich die benötigten Leistungskapazitäten der Erzeugungsanlagen jeweils über Jahresarbeitszahlen ableiten. Wie im Sektor Wärme werden Arbeitskräfte in der Umsetzungsphase für den Aufbau der Anlagen aus dem Bauhauptgewerbe (WZ 41.2, 42, 43.1, 43.9) benötigt: Der Anteil der Personalkosten beträgt 25,5% an den Investitionskosten und der durchschnittliche Jahreslohn 47.195 €/a.


3.4 Bilanz Zieljahr
-------------------
Die Produktion von Wasserstoff benötigt nur Strom und Wasser und ist damit klimaneutral. Während die Vorkette der fossilen Energieträger positive Emissionen nach sich zog, kehrt sich das bei den E-Fuels und E-Methan um. Für deren Produktion sind komplexe chemische Prozesse vonnöten, als Ausgangsstoffe aber lediglich Wasserstoff und Kohlenstoffdioxid. Der Wasserstoff selbst wird klimaneutral produziert und reines CO2 wird mittels CO2-Abscheidung (Carbon Capture) oder Direct Air Capture gewonnen. Bei beiden Verfahren wird CO2, das sich bereits in der Luft befindet, gebunden und damit negative Emissionen erzeugt. LocalZero setzt die Emissionsfaktoren aus der Verbrennung der Kraftstoffe in Verkehr etc. als negative Emissionsfaktoren in deren Produktion an, der Sektor Kraftstoffe fungiert also als eine technische Kohlenstoffsenke. Damit kommt die Produktion von synthetischen Kraftstoffen der THG-Bilanz stark zugute, allerdings ist fraglich, ob die im Klimaneutralitäts-Szenario benötigten Kapazitäten so schnell und in diesem Umfang aufgebaut werden können. Denn während bei der CO2-Abscheidung Abgase aus Industrieanlagen mit einem hohen CO2-Gehalt relativ effizient genutzt werden können, ist deren Verfügbarkeit mit zunehmender Dekarbonisierung der Industrie begrenzt. Bei Direct Air Capture wird CO2 direkt aus normaler Luft mit einem niedrigen CO2-Gehalt extrahiert, weswegen sich die Verfügbarkeit und Wirtschaftlichkeit dieser Technologie noch entwickeln muss.



Quellen
-------
| [Ene17]
| Energy Brainpool: „Kalte Dunkelflaute – Robustheit des Stromsystems bei Extremwetter“ (2017)
| https://www.energybrainpool.com/fileadmin/download/Studien/Studie_2017-06-26_GPE_Studie_Kalte-Dunkelflaute_Energy-Brainpool.pdf

| [FVV18]
| FVV (2018): Defossilisierung des Transportsektors. Verfügbar unter https://www.fvv-net.de/fileadmin/user_upload/medien/materialien/FVV__Kraftstoffe__Studie_Defossilisierung__R586_final_v.3_2019-06-14__DE.pdf [11.08.2021].

| [Min19]
| Mineralölwirtschaftsverband: „Jahresbericht 2019“ [online nicht mehr verfügbar, auf Anfrage bei LocalZero oder en2x] (2019)
| https://www.mwv.de/wp-content/uploads/2021/01/MWV-Jahresbericht_2019_Webversion_MineraloelwirtschaftsverbandEV.pdf

| [Öko20]
| Öko-Institut: „E-Fuels im Verkehrssektor“ (2020)
| https://www.oeko.de/fileadmin/oekodoc/E-Fuels-im-Verkehrssektor-Hintergrundbericht.pdf [11.08.2021].

| [Pro20]
| Prognos, Öko-Institut, Wuppertal-Institut: „Klimaneutrales Deutschland. Studie im Auftrag von Agora Energiewende, Agora Verkehrswende und Stiftung Klimaneutralität.“ (2020) https://www.agora-energiewende.de/veroeffentlichungen/klimaneutrales-deutschland/ [11.08.2021].

| [Umw20a]
| Umweltbundesamt: „Aktualisierung der Modelle TREMOD/TREMOD-MM für die Emissionsberichterstattung 2020 (Berichtsperiode 1990- 2018)“ (2020) https://www.umweltbundesamt.de/publikationen/aktualisierung-tremod-2019 [11.08.2021].

| [Umw20b]
| Umweltbundesamt: „Transformationsprozess zum treibhausgasneutralen und ressourcenschonenden Deutschland – GreenSupreme“
| https://www.umweltbundesamt.de/publikationen/transformationsprozess-treibhausgasneutrales-ressourcenschonendes-deutschland-greensupreme [11.08.2021].













