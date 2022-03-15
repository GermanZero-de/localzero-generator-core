4. Strom
========
| **Autor: Manfred Schüssler**
| **Stand: 15.12.21** 

 
Dieses Dokument gibt einen Überblick über die wesentlichen Prinzipien, die den Berechnungen für Strom in LocalZero zugrunde liegen. Generell ist mit Strom hier nur die Bereitstellung (nicht die Nutzung) des Endenergieträgers Strom gemeint. Grundsätzliches Vorgehen ist: Erhebung der Bedarfe, Bereitstellung/Stromgestehung aus unterschiedlichen Primärenergieträgern, THG-Emissionen abgeleitet mit Emissionsfaktoren aus dem spezifischen Stromgestehungsprozess. Bei der Bilanz 2018 erfolgt die Bereitstellung mit dem deutschen Bundesmix 2018, getrennt nach fossiler (fossil) und erneuerbarer (renew) Stromgestehung. Bei der Bilanz im Zieljahr der Klimaneutralität wird ausgehend vom Bedarf zuerst das lokale Potential (local) ausgeschöpft und nur wenn dieses nicht ausreicht mit erneuerbarem Strom aus einem Deutschlandmix (renew) die Lücke geschlossen. 

4.1 Eingabedaten 
----------------
Wir gehen vom Endenergieverbrauch (EEV) für 2018 aus, der von der AG Energiebilanzen in Spalte AD für die verschiedenen Bereiche (Private Haushalte, GHD: Gewerbe/Handel/Dienstleistungen, Industrie, Verkehr und Landwirtschaft) für Deutschland gesamt angegeben wird [AGE2020, AGE2021]. Diese Werte werden dann gemäß Einwohnerzahl (Haushalte, GHD und Verkehr), industriell genutzte Fläche (Industrie) und landwirtschaftlich genutzte Fläche (Landwirtschaft) auf die betrachtete Kommune heruntergebrochen. Diese Standardwerte können in der Eingabe überschrieben werden, wenn genaue Werte für die Kommune vorliegen sollten. 

Die im Juni 2021 in der betrachteten Kommune/Gebietskörperschaft installierte elektrische Leistung von Anlagen für nicht-fossile Stromerzeugung (Photovoltaik, Windkraft onshore, Biomasse und Laufwasser) wurde automatisch dem Marktstammdatenregister der Bundesnetzagentur [MaStR2021] entnommen. Für die Ausschöpfung des gesamten Potentials sind derzeit (Stand Februar 2022) Standard-Annahmen hinterlegt. In einem zukünftigen Update von LocalZero könnte zu jeder Erzeugungskategorie von den Benutzer:innen angegeben werden, zu welchem Prozentsatz das entsprechende Gesamtpotential genutzt werden soll, um die lokale Stromerzeugung individuell auszubauen und so einen möglichst hohen Anteil an Eigenversorgung zu erreichen. Dabei bleiben bestehende Anlagen aber auf jeden Fall erhalten, d.h. 0% Ausbau bedeutet Erhaltung des Status quo. 
 

4.2 Bilanzierung 2018
---------------------
4.2.1 Nachfrage und Bereitstellung 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Die (eventuell überschriebenen) Strom-EEV der Sektoren werden im Sektor Strom Sektor-summiert unter Nachfrage aufgelistet. Die Bereitstellung des gesamten Strombedarfs wird gemäß den prozentualen Anteilen des deutschen Strommix 2018 der verschiedenen fossilen Primärenergieträger (Steinkohle, Braunkohle, Erdgas, sonstige konventionelle, Kernenergie) und der erneuerbaren Energien aus Photovoltaik (PV), Windkraft, Biomasse, Laufwasser, und Geothermie an der Gesamtstromerzeugung laut Statistischem Bundesamt [DESTATIS2018] auf die Energieträger verteilt.  

Außerdem wird die lokale Stromerzeugung aus erneuerbaren Energien durch bereits jetzt (2021) in der betrachteten Kommune vorhandene lokale Anlagen berechnet. Dazu werden die Erzeugungskapazitäten (MWp) für die verschiedenen Erzeugungsformen aus dem Marktstammdatenregister mit mittleren Volllaststunden multipliziert. Für die PV sind diese spezifisch für jedes Bundesland angegeben (www.foederal-erneuerbar.de), für die anderen Stromerzeuger werden sie gemäß dem jeweiligen Anteil an der Bruttostromerzeugung für Deutschland insgesamt aus [DESTATIS2018] berechnet. 
Auf diese Weise kann der jetzige Anteil der lokalen Erzeugung aus EE-Quellen am lokalen Stromverbrauch geschätzt werden, welcher aber erst bei den Ausbauzielen zur Klimaneutralität genutzt wird. 

4.2.2 Treibhausgas-Emissionen 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Für die Berechnung der THG-Emissionen aus der Stromproduktion werden folgende Annahmen gemacht: 

1) Für Photovoltaik, Windkraft, Geothermie, Laufwasser und Kernenergie werden keine Emissionen aus der Vorkette (Herstellung und Installation der Anlagen) bei der Stromerzeugung berücksichtigt. Diese Emissionen sind ggf. in den Bereichen Industrie und GHD im jeweiligen Herstellungsjahr zu bilanzieren. Beim Betrieb der Anlagen sind in der jährlichen Bilanz dann keine Emissionen zu berücksichtigen. Elektrische Hilfsenergie ist in der allgemeinen Strombilanz bereits enthalten und wird nicht getrennt bilanziert. 

2) Bei der Biomasse werden (im Einklang mit den allgemein verwendeten Bilanzierungsregeln z.B. des Umweltbundesamtes oder im Nationalen Inventarbericht) keine verbrennungsbedingten CO2-Emissionen bilanziert, da die entsprechenden Mengen CO2 vorher beim Wachsen der Biomasse aus der Atmosphäre sequestriert wurden. Bei einjährigen Pflanzen ist diese CO2-Neutralität evident; bei Holzverbrennung findet die vorherige Sequestrierung allerdings über einen langen Zeitraum statt und es gibt keinen Ausgleich innerhalb eines Jahres. Dies wird berücksichtigt, indem die jährlichen CO2-Emissionen aus der Holzverbrennung in der Bilanzierung des Bereichs LULUCF (Land use, land use change, forestry) von der jährlichen Sequestrierung von CO2 in der Forstwirtschaft abgezogen werden. 

3) Verbrennungsbedingte Emissionen von CH4 (Methan) und N2O (Lachgas) bei der Biomasse werden in CO2-Äquivalenten berücksichtigt, weil ihnen keine entsprechenden Sequestrierungen gegenüberstehen. Die entsprechenden direkten Emissionsfaktoren sind der Studie "Emissionsbilanz erneuerbarer Energieträger" des Umweltbundesamtes entnommen [UBA2019a] und gemäß den Anteilen der verschiedenen Energieträger (Holz, Biogas, biogener Müll usw.) an der Stromproduktion aus Biomasse in strombezogene Emissionsfaktoren (Tonnen CO2-Äquivalent pro MWh erzeugter Strom) umgerechnet. Die Emissionen aus der Vorkette (z.B. bei der Biogas-Herstellung) werden im Bereich Landwirtschaft bilanziert. 

4) Die verbrennungsbedingten Emissionen der fossilen Energieträger (Kohle, Erdgas, nicht-biogener Müll etc.) für die Stromerzeugung werden berechnet, indem zunächst der jeweilige Primärenergieeinsatz (in TJ) der Kraftwerke der allgemeinen Versorgung, der Industriekraftwerke und der anderen Stromproduzenten (Zeilen 11,12 und 14) in [AGE2021] summiert werden. Mit den primärenergiebezogenen Emissionsfaktoren (Tonnen CO2 pro TJ Primärenergie) aus Tabelle 563 in [NIR2020] ergeben sich daraus die jeweiligen Gesamtemissionen der einzelnen Energieträger. Daraus wiederum werden die strombezogenen Emissionsfaktoren (Tonnen CO2 pro MWh Bruttostromerzeugung) aus den Anteilen der jeweiligen Energieträger an der gesamten Bruttostromerzeugung in [DESTATIS2018] berechnet. Da in der Berechnung von LocalZero der Strom-EEV betrachtet wird (ca. 513 TWh gegenüber ca. 643 TWh Bruttostromerzeugung, BSE), werden für EEV-bezogene Emissionsfaktoren die oben bestimmten Emissionsfaktoren jeweils noch mit dem Faktor BSE/EEV = 1,25 multipliziert. Das Ergebnis dieser Berechnungen für Deutschland gesamt weicht nur um ca. 0,6% vom Wert in [NIR2020] für den Bereich 1.A.1.a ab.  

Allerdings wurden in LocalZero zwei Emissions-Verschiebungen vorgenommen: Wie im Erklärtext Wärme geschildert werden die Emissionen aus der Erzeugung von Fernwärme i.H.v. 29,8 Mt CO2e dem Sektor Wärme zugerechnet. Dafür werden aber die Emissionen aus der Stromerzeugung in Industriekraftwerken i.H.v 39,2 Mt CO2e aus der Industrie in den Sektor Strom verlagert, um dort die gesamten Emissionen aus der berichteten Bruttostromerzeugung in Kraftwerken der öffentlichen und industriellen Versorgung abzubilden. 

Energiebedingte Emissionen der „Industriekraftwerke (nur für Strom)“ (AG EB Zeile 12 bzw. 24) verstecken sich im NIR unter „Verarbeitendes Gewerbe - Weitere Energieerzeugung (CRF 1.A.2.g, Sonstige, stationär) und darin in der Subkategorie 1.A.2.g viii „Sonstige“. Die 77,7 Mt CO2e in CRF 1.A.2.g (9% der deutschen Emissionen) werden in LocalZero erstmal dem Subsektor Sonstige Industrie zugeordnet. Davon werden aber die Emissionen der Eigenstromerzeugung mit eigener Berechnung abgezogen: Alle Energieträger in AG EB Zeile 12 „Industriekraftwerke (nur für Strom)“ wurden mit den verbrennungsbedingten Emissionsfaktoren des UBA multipliziert und aufsummiert (Biomasse mit 0,028 t/ MWh für non-CO2-THG). Diese Emissionen i.H.v. 39,2 Mt CO2e werden dem Bereich Strom zugeschlagen, da dort der gesamte EEV von Strom bilanziert wird und die Industriekraftwerke etwa 9% zur Bruttostromerzeugung beitragen, von der der EEV abgeleitet wird. 

4.2.3 Kosten 
^^^^^^^^^^^^
Stromkosten für die Verbraucher werden gemäß den Preisen für Haushalte, GHD und Industrie, die im Monitoringbericht 2018 der Bundesnetzagentur [BNA2018] angegeben sind, angesetzt. Für den Verkehrsbereich wird der Strompreis für Haushaltsstrom angenommen.  

Bei den Stromgestehungskosten für die verschiedenen Energieträger werden Brennstoffkosten (für konventionelle und Biomasse-Anlagen), CO2-Zertifikatskosten (für Stromerzeugung aus fossilen Brennstoffen) sowie Betriebskosten (M&O) für alle Anlagen betrachtet. Für die Kern-, Kohle- und Erdgaskraftwerke werden die mittleren Brennstoffkosten pro MWhth aus [VGB2015] betrachtet und durch den elektrischen Wirkungsgrad der jeweiligen Kraftwerke dividiert, um Kosten pro MWhel zu ermitteln. Für M&O-Kosten werden die Kosten pro MW installierter Leistung und Jahr aus der gleichen Quelle durch die mittleren Volllaststunden pro Jahr dividiert, um die M&O-Kosten pro MWhel zu berechnen. Für die Biomasse werden die entsprechenden Daten aus [ISE2018] betrachtet und die aus der Stromerzeugung aus Biomasse berechneten mittleren Volllaststunden der Anlagen verwendet. 

Bei den übrigen Anlagen (Photovoltaik, Windkraft, Laufwasser, Geothermie) fallen keine Brennstoffkosten, sondern nur M&O-Kosten an. Diese ergeben sich aus dem jeweiligen Prozentsatz der Investitionskosten pro MW installierter Leistung und Jahr, dividiert durch die mittleren Volllaststunden, woraus sich wiederum Kosten pro MWhel ergeben. Die entsprechenden Zahlenwerte entstammen aus [ISE2020b]. 

Die Kosten pro MWhel werden dann jeweils mit den Anteilen der jeweiligen Energieträger an der Bruttostromerzeugung multipliziert, um die Kosten pro Jahr zu berechnen. 

Aktuell (Stand Februar 2022) sind die Energiepreise, Brennstoff-, Zertifikats und Betriebskosten aber nicht für alle Sektoren und Energieträger hinterlegt, weswegen sie in der Klimavision auch nicht für Strom ausgewiesen werden. 

4.3 Maßnahmen 
-------------

Im Zieljahr soll der Strombedarf komplett aus erneuerbaren Energien gedeckt werden. Dazu werden die Photovoltaik (auf Dächern, Fassaden, Freiflächen und Agrarflächen) und Windkraft (an Land) auf lokaler Ebene (Kommunen, Landkreise) ausgebaut. Das Potential für Elektrizitätserzeugung aus Laufwasser gilt als bereits weitgehend ausgeschöpft, so dass hier kein weiterer Ausbau vorgesehen ist. Für die Nutzung von Biomasse ist ebenfalls standardmäßig kein Ausbau angesetzt, da die Holzverbrennung grundsätzlich problematisch ist und es bei Biopflanzen eine Flächenkonkurrenz zum Anbau von Nahrungspflanzen gibt. Außerdem ist pro Flächeneinheit die energetische Effizienz der Nutzung von Biopflanzen der von Photovoltaik und Windkraft weit unterlegen. Standardmäßig wird eine hohe Nutzung der Potentiale von Windkraft onshore (90%) sowie Photovoltaik auf Dächern (90%) und Freiflächen (80%) angenommen. Für die Nutzung des Potentials für Photovoltaik an Gebäudefassaden wird standardmäßig nur ein Anteil von 10% angenommen, da die Installation im Vergleich zu PV Dach/Freifläche erheblich teurer und die Stromausbeute pro Flächeneinheit kleiner ist. Der angenommene Standardwert für die Nutzung des Potentials für Agri-PV (kombinierte Nutzung von Agrarflächen für den Nahrungsmittelanbau und PV mittels aufgeständerter Anlagen in Höhe von ca. 14% ergibt sich aus der Forderung, dass der Strombedarf für Deutschland gesamt (AGS=DG000000) komplett klimaneutral gedeckt werden soll. Mit den angenommenen Ausbauzielen für die anderen Erzeuger ergibt sich dann das Ausbauziel für Agri-PV, die grundsätzlich ein sehr hohes Potential hat. 

Nur wenn dieses lokal weitgehend ausgeschöpfte Potential nicht ausreicht, um den Strombedarf zu decken, wird Strom aus der allgemeinen Versorgung ergänzt. Dieser im Deutschland-Szenario ermittelter Strommix enthält die gleichen Kategorien wie die lokale Bereitstellung plus drei weitere Kategorien: 

Windkraft offshore und Tiefengeothermie werden ohne konkreten Bezug auf die lokale Ebene für das allgemeine Netz ausgebaut. Als nationale Reserve müssen ebenso für die Rückverstromung von Wasserstoff in Zeiten ungenügenden Angebots an EE-Strom müssen zusätzliche GuD-Gaskraftwerke (GuD: Gas und Dampf) errichtet werden, die nicht spezifisch für eine Kommune zur Verfügung stehen. Bestehende Gaskraftwerke müssen ggf. für den Betrieb mit Wasserstoff umgerüstet werden. 

Für die Potentiale der verschiedenen EE-Stromerzeuger gilt: 

| **PV Dach:** Das Potential wird in [BMVI2015] differenziert nach Ein-, Zwei- und Mehrfamilienhäusern sowie pauschal für Nichtwohngebäude angegeben. Die entsprechenden Gebäudezahlen werden aus dem Wohnungszensus gemeindespezifisch übernommen. 
| **PV Fassade:** In [EGGERS2020] wird ein Wert von 2200 qkm Fläche für PV-Module an geeigneten Fassaden in Deutschland berechnet. Für die Kommune wird dieser Wert mit der Zahl der Gebäude in der Gemeinde durch Gesamtzahl in Deutschland skaliert. Der geringere Ertrag der Fassaden-PV pro Modulfläche, z.B. aufgrund von Verschattung wird bei der Berechnung berücksichtigt.   
| **PV Freifläche:** In [ISE2021] (S. 40) wird ein Anteil von 3164 qkm (ca. 0,9% der Gesamtfläche) in Deutschland als restriktionsfrei nutzbare Fläche in Deutschland angegeben. Dieser Prozentsatz wird entsprechend auf die Gesamtfläche der Kommune angewendet. Eine geringere Flächenverfügbarkeit in Städten kann in der Eingabe durch einen entsprechend herabgesetztes Ausbauziel (Standardwert 80%) berücksichtigt werden. 
| **Agri-PV:** In [ISE2021] (S.38) wird ein Potential von mindestens 1700 GWp für Deutschland angesetzt, was ca. 15,6% der landwirtschaftlichen Fläche entspricht. Zur Deckung des Strombedarfs im Zieljahr müssen davon ca. 230 GW genutzt werden, entsprechend etwa 2% der landwirtschaftlichen Fläche. Für die Kommune wird der entsprechende Anteil der kommunalen landwirtschaftlichen Fläche betrachtet. 
| **Biomasse:** Laut [ISE2021] werden bereits heute etwa 14% der landwirtschaftlichen Fläche Deutschlands zum Anbau von Energiepflanzen genutzt. Das Potential für die installierbare Leistung zur Stromerzeugung aus Biomasse insgesamt wird Bundesland-spezifisch gemäß dem in [AEE2013] angegebenen energetischen Potential von Biomasse, dem elektrischen Wirkungsgrad und den jährlichen Volllaststunden von Anlagen zur Stromerzeugung aus Biomasse berechnet. Für die Kommune wird das Potential durch Skalierung mit dem Anteil der kommunalen landwirtschaftlichen Fläche an der des jeweiligen Bundeslandes bestimmt.  
| **Windkraft an Land:** Für das Flächenpotential wird gemäß [BWE2011] ein Anteil von 2% an der Gesamtfläche angenommen. Eine geringere Flächenverfügbarkeit in Städten kann in der Eingabe durch einen entsprechend herabgesetztes Ausbauziel (Standardwert 90%) berücksichtigt werden. Die sich daraus ergebende installierbare Leistung für Anlagen mit 3,5 MWp Leistung wird gemäß dem Bundesland-spezifischen Wert für den spezifischen Flächenbedarf (ha/MWp) aus [UBA2019b] (Tabelle 8) berechnet. 
| **Windkraft auf See (offshore):** Es wird vom maximal nutzbaren Szenario in der Studie [AGORA2020] (S.41) mit ca. 145 GW Potential und einem Ausbaugrad im Zieljahr von 90% ausgegangen.  
| **Tiefengeothermie:** Es wird das in [AEE2021] angegebene technische Potential von ca. 26 TWh für Stromerzeugung aus Tiefengeothermie angenommen, das bis zum Zieljahr zu 100% ausgeschöpft wird.  

Durch den Ausbau der EE-Quellen wird auch ein Ausbau der Stromnetze notwendig. Dieser teilt sich auf in  
a) HGÜ (Hochspannungs-Gleichstrom-Übertragung) von Nord nach Süd, Ausbau vor allem für den Transport von Offshore-Windstrom,  
b) das Mittelspannungsnetz, Ausbau vor allem zum Transport von Onshore-Windstrom, 
c) das lokale Verteilnetz, Ausbau vor allem zum Transport von PV-Strom. 
Die Ausbauziele gemäß Offshore/Onshore-Wind und PV sind etwas willkürlich, aber die Kostenannahmen gemäß der verwendeten Quelle [ISE2020b] gehen von einer solchen Verteilung aus.   

Im Bereich Stromspeicher werden in der jetzigen Version keine Ausbaumaßnahmen betrachtet, da die Entwicklung der Konzepte dafür noch zu sehr im Fluss ist. Zur Netzstabilisierung wird der Ausbau von Batteriespeichern diskutiert. Ob es sich dabei aber um zentrale Großspeicher mit Kapazitäten im GWh-Bereich (evtl. aufgebaut aus “ausgedienten” Batterien von E-Kfz) handeln soll oder um verteilte Speicher (in Kombination mit PV-Anlagen oder Batterien von E-Kfz), die in einem “Smart Grid” flexibel genutzt werden können, ist gegenwärtig unklar. Auch “Demand Side Management” mit flexibler Zu- und Abschaltung großer Lasten kann eine große Rolle für die Dimensionierung solcher Speicher spielen.  

Für den Bereich der Rückverstromung werden Wasserstoff-Speicher benötigt. Die erste Wahl dafür sind existierende Kavernenspeicher, die gegenwärtig für Erdgas genutzt werden. Dafür fallen nur vergleichbar geringe Investitionskosten an. Gegebenenfalls müssen aber Erdgaspipelines zur GuD-Kraftwerken für Wasserstoff ertüchtigt werden 
oder Wasserstoffpipelines neu gebaut werden. Das Ausmaß solcher Maßnahmen hängt aber von der regionalen Verteilung der Kraftwerke und der Elektrolyseure ab, über die gegenwärtig keine fundierten Aussagen gemacht werden können. 

  

4.4 Bilanz Zieljahr
-------------------
4.4.1 Nachfrage 
^^^^^^^^^^^^^^^

Für die Privathaushalte und GHD ergibt sich der Strombedarf im Zieljahr aus  
einem reduzierten Strombedarf bei elektrischen Verbrauchern (-23,8%) durch Suffizienz/Effizienz gemäß RESCUE GreenSupreme und einen zusätzlicher Strombedarf durch Wärmepumpen für Raumwärme und Warmwasser. Bei der Industrie erhöht sich der Bedarf durch den stärkeren Stromeinsatz für Prozesswärme und die Erzeugung von Wasserstoff und Methan. In den Bereichen Verkehr und auch Landwirtschaft ergibt sich ein erheblicher Bedarf an E-Fuels (E-Benzin, E-Diesel, E-Kerosin). Abhängig vom Zieljahr macht der Bedarf für Wasserstoff und E-Fuels etwa die Hälfte des Gesamtstrombedarfs für Deutschland aus.  

Darin enthalten ist auch der Strombedarf für die Wasserstoffherstellung zur Rückverstromung in Zeiten, in denen eine positive Residuallast (aktueller Strombedarf minus aktuelle Erzeugung aus EE) nicht durch andere Speicher (Batterien etc.) oder Nachfrageflexibilität gedeckt werden kann. Wasserstoff als saisonaler Speicher muss vor allem die verbleibende Residuallast während Zeiten von „kalter Dunkelflaute“ decken. Der Strombedarf für die Herstellung von H2 zu diesem Zweck wird gemäß einer Studie des FZ Jülich bestimmt [FZJ2020]. In der Studie wird bei einer bei 100% EE ein Anteil von 4,8% der gesamten Strombereitstellung aus der Rückverstromung von Wasserstoff erzeugt. In leichter Abwandlung dieses Ansatzes wenden wir den Prozentsatz von 4,8% nur auf die Strombereitstellung abzüglich des Strombedarfs für die H2-Erzeugung zur Rückverstromung selbst an. Dies ist sinnvoll, weil während Zeiten negativer Residuallast mit Rückverstromung sicher kein Wasserstoff für die Rückverstromungs-Reserve hergestellt wird.  

4.4.2 Bereitstellung
^^^^^^^^^^^^^^^^^^^^
Im Zieljahr wird der gesamte Strombedarf durch EE gedeckt. Dazu wird zunächst der bundesweite Strombedarf bestimmt und der Ausbau der jeweiligen Potentiale der verschiedenen Erzeuger (PV, Windkraft, Biomasse, Geothermie) in dem Maß angenommen, dass der Strombedarf gedeckt wird. Dabei werden von der Bruttostromerzeugung 4,1% abgezogen, um die Leitungsverluste zu berücksichtigen (entsprechend ihrem prozentualen Anteil in der Bilanz 2018 gemäß [AGE2021]). Wird der formale AGS “DG000000” eingegeben, so wird so die Gesamtbereitstellung unter Einschluss der Erzeuger, die nicht lokal der Kommune zugerechnet werden (Windkraft offshore, Tiefengeothermie und Rückverstromung von Wasserstoff) berechnet. Die entsprechenden prozentualen Anteile für PV, Windkraft onshore und Biomasse werden als Standardwerte dann auch für den regenerativen Strommix der allgemeinen Bereitstellung übernommen.  

Für die jeweilige Kommune wird der Bedarf bilanziell durch zwei Quellen gespeist: 
a) durch lokal installierte Anlagen und  
b) (für den ggf. verbleibenden Bedarf) aus dem allgemeinen Stromnetz. 
Für die lokalen Anlagen zur EE-Stromerzeugung werden Ausbauziele als prozentuale Anteile an den lokal zur Verfügung stehenden Potentialen der verschiedenen Erzeuger festgelegt (Standardwerte gemäß angenommenem Ausbau für Deutschland gesamt, siehe oben). Die erzeugte Strommenge aus den lokalen Anlagen (Bestand + Ausbau) wird berechnet und mit dem lokalen Bedarf verglichen. Ergibt sich ein Defizit, so wird der verbleibende Bedarf durch Bezug aus dem allgemeinen Netz gedeckt, ergibt sich ein Überschuss, so wird (bilanziell) kein Strom aus dem allgemeinen Netz bezogen. Die ausgewiesenen Anteile der verschiedenen Erzeuger am Strombezug aus dem allgemeinen Netz entsprechen den Anteilen für Deutschland gesamt. 

4.4.3 THG-Emissionen
^^^^^^^^^^^^^^^^^^^^
Da keine fossilen Brennstoffe mehr eingesetzt werden und die CO2-Emissionen bei der Verbrennung von Biomasse nicht in die Bilanz eingehen (entweder wegen der CO2-Bindung im gleichen Jahr bei einjährigen Pflanzen oder durch die Verrechnung mit der Sequestrierung in der Forstwirtschaft), fallen nur noch Emissionen von Methan (CH4) und Lachgas (N2O) bei der Stromgestehung aus Biomasse an. Diese werden wie in Abschnitt 4.2.2 beschrieben bilanziert. 

4.4.4 Kosten 
^^^^^^^^^^^^
Für den Ausbau der EE-Anlagen fallen Investitionskosten an. Für Windkraft (offshore und onshore), PV Dach und Freifläche werden dabei die Kosten pro MW zu installierender Leistung aus [ISE2020b] angenommen, wobei (da das Zieljahr nicht fest vorgegeben ist) Mittelwerte der dort angegebenen Zahlen für 2030, 2035 und 2040 angesetzt werden. Für Fassaden-Photovoltaik gibt es wenig belastbare Informationen, insbesondere auch zur zukünftigen Kostenentwicklung. Es wird deshalb hier ein heutiger Wert angesetzt, der aus den Informationen in [ENEX2021] berechnet werden kann (aus Stromertrag von 80 kWh pro qm und Jahr, 600 Volllaststunden im Jahr sowie Modul- und Installationskosten von 400€ pro qm). Für Agri-PV sind die Investitionskosten aus [SCHINDELE2020] entnommen, während für Biomasse-Anlagen der Mittelwert für 2018 aus [ISE2018] angesetzt wird. Für Tiefengeothermie wird der Wert aus [FRIEDRICH2015] angenommen.  

Für den Bau zusätzlicher GuD-Gaskraftwerke zur Rückverstromung von Wasserstoff werden die Investitionskosten pro MW gemäß [ISE2020b] angesetzt. 

Die Investitionskosten für den lokalen Ausbau von PV, Windkraft onshore und ggf. Biomasse werden zu 100% den Akteuren in der Kommune zugeschrieben, während die Kosten für den Ausbau von Windkraft offshore, Tiefengeothermie und GuD-Kraftwerken entsprechend dem Anteil der Kommune am Gesamtstromverbrauch als “extraterritoriale” Kosten getrennt ausgewiesen werden. In diese Kategorie werden eventuell in späteren Updates auch die Kosten für Wasserstoffpipelines und –speicherung fallen. 

Die laufenden M&O-Kosten werden für die einzelnen Erzeugertypen nach dem Muster der Bilanz 2018 berechnet und ausgewiesen. Brennstoffkosten fallen nur noch für Biomasse an – hier wird der Wert für 2018 weiterverwendet. 

Für den Netzausbau auf den verschiedenen Spannungsebenen werden die Kosten gemäß [ISE2020b] angenommen. Analog zu den oben beschriebenen überregionalen Quellen (Wind offshore, Tiefengeothermie usw.) werden die Kosten für den HGÜ-Ausbau (für Offshore-Windstrom) nur anteilig der Kommune bei den “extraterritorialen Kosten” zugeschrieben. Dagegen werden die Kosten für Mittelspannungs- und Verteilnetz der Kommune entsprechend dem lokalen Ausbau von Onshore-Wind und PV zugeschlagen. 
 

4.4.5 Stellen
^^^^^^^^^^^^^
Um die Zahl der für die Maßnahmen erforderlichen Personalstellen (Vollzeitäquivalente) abzuschätzen, wird zunächst der prozentuale Personalkostenanteil am Umsatz der jeweiligen Branche (Anlagenbaubau, Elektro- und Heizungshandwerk usw.) ermittelt und mit der Gesamtinvestition multipliziert. Das Ergebnis wird dann durch die Personalkosten pro Kopf geteilt, die in den meisten Fällen der Quelle [DESTATIS2017] entnommen wurden. Das Ergebnis wird dann mit der Zahl der Beschäftigten in der jeweiligen Branche verglichen und so die Zahl der erforderlichen neuen Stellen bestimmt, falls die vorhandenen Stellen nicht ausreichen. Für die Kommune werden jeweils die bundesweiten Personalzahlen mit dem Verhältnis der Einwohnerzahl Kommune zur Einwohnerzahl Deutschland skaliert.  

In einigen Fällen greifen verschiedene Maßnahmen auf den gleichen Pool von Arbeitskräften zu (z.B. Photovoltaik Dach, Fassade, Freifläche und Agri-PV). Es werden dann die vorhandenen Stellen formal anteilig nach dem jeweiligen Bedarf der Maßnahme verteilt, so dass in der Summe nicht mehr vorhandene Stellen ausgewiesen werden als tatsächlich existieren. 

Die 2018 vorhandenen Stellen für Windkraft (onshore und offshore) wurden der Quelle [BWE2018] entnommen, für den Anlagenbau in den Bereichen Geothermie und GuD-Kraftwerke (Rückverstromung) der Studie [HBS2015], für Elektro- und Heizungsinstallation der Datenbank GENESIS des Statistischen Bundesamtes  [DESTATIS2019] und für Biomasse aus [BBE2016]. 

Für den Netzausbau wurde wie in Wärme und Kraftstoffe der Anteil der Personalkosten (25,5%) an den Investitionskosten im Bauhauptgewerbe (WZ 41.2, 42, 43.1, 43.9) und der durchschnittliche Jahreslohn (47.195 €/a) angesetzt.   

 
Mögliche Punkte für Erweiterungen/Updates: 
  * Ausbaupotential für Laufwasser von ca. 1,1 GW gemäß [BMVI2015] (S.98) berücksichtigen 
  * Kostenentwicklung für Fassaden-PV recherchieren und Werte ggf. korrigieren 
  * Wasserstoff-Speicherung, Wasserstoff-Pipelines in die Berechnung der (extraterritorialen) Kosten aufnehmen 
  * Batteriespeicher (lokal in den Häusern mit PV, kleinere Anlagen auf lokaler Ebene, große Anlagen überregional) 
  * Smart Grid  

 

Quellen
-------
| [AEE2013]: “Potenzialatlas Bioenergie in den Bundesländern”, Agentur für Erneuerbare Energien, 2013 
| https://www.unendlich-viel-energie.de/medi/file/239.AEE_Potenzialatlas_Bioenergie_Daten+Quellen_feb13.pdf 

| [AEE2021], https://www.foederal-erneuerbar.de/landesinfo/bundesland/D/kategorie/erdw%E7%A3%B4rme/auswahl/815-technisches_potenzia/#goto_815 

| [AGE2020]: https://ag-energiebilanzen.de/10-0-Auswertungstabellen.html 

| [AGE2021]: https://ag-energiebilanzen.de/7-0-Bilanzen-1990-2019.html 

| [AGORA2020]: “Making the most of offshore Wind”, AGORA Energiewende, 2020 
| https://static.agora-energiewende.de/fileadmin/Projekte/2019/Offshore_Potentials/176_A-EW_A-VW_Offshore-Potentials_Publication_WEB.pdf 

| [BBE2016]: Website Bundesverband Bioenergie,   
| https://www.bioenergie.de/themen/wirtschaft 

| [BMVI2015]: “Räumlich differenzierte Flächenpotentiale für erneuerbare Energien in Deutschland”, Bundesministerium für Verkehr und digitale Infrastruktur”, Online-Publikation, Nr. 08/2015, S. 94ff 

| [BNA2018]: „Monitoring-Bericht 2018“, Bundesnetzagentur/Bundeskartellamt 

| [BWE2011]: “Potential der Windenergienutzung an Land”, Bundesverband Windenergie, 2011 https://www.wind-energie.de/fileadmin/redaktion/dokumente/publikationen-oeffentlich/themen/01-mensch-und-umwelt/03-naturschutz/bwe_potenzialstudie_kurzfassung_2012-03.pdf 

| [BWE2018]: https://www.wind-energie.de/themen/zahlen-und-fakten/deutschland/ 

| [DESTATIS2017]: “Produzierendes Gewerbe - Kostenstruktur der Unternehmen im Baugewerbe”, https://www.destatis.de/DE/Themen/Branchen-Unternehmen/Bauen/Publikationen/Downloads-Baugewerbe-Struktur/kostenstruktur-baugewerbe-2040530177004.pdf?__blob=publicationFile 

| [DESTATIS2018]: https://www.destatis.de/DE/Themen/Branchen-Unternehmen/Energie/Erzeugung/Tabellen/bruttostromerzeugung.html  

| [DESTATIS2021]: Datenbank Genesis, https://www-genesis.destatis.de 

| [EGGERS2020]: “PV-Ausbauerfordernisse versus Gebäudepotenzial: Ergebnis einer gebäudescharfen Analyse für ganz Deutschland”, 35. PV-Symposium, Bad Staffelstein, pp. 837-856, 2020 (https://www.pv-symposium.de/pv-symposium/tagungsunterlagen) 

| [ENEX2021]: https://www.energie-experten.org/erneuerbare-energien/solarenergie/solaranlage/photovoltaik-fassade 

| [FRIEDRICH2015]: “Analyse der Kostenstruktur verschiedener Erneuerbare-Energien-Technologien", Bachelor-Arbeit, Univ. St. Gallen, 2015, p. 43 
| https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwid2OGZvYHzAhXCg_0HHQDBD2EQFnoECAMQAQ&url=https%3A%2F%2Fiorcf.unisg.ch%2F-%2Fmedia%2Fdateien%2Finstituteundcenters%2Fiorcf%2Fabschlussarbeiten%2Ffriedrich-2015-ba--analyse-der-kostenstruktur-verschiedener-erneuerbareenergientechnologien.pdf%3Fla%3Dde%26hash%3D1D12750F929F19307F7915D9609E644585B00EC3&usg=AOvVaw3xujeDI_nJ40RP2T9s2jRK 

| [FZJ2020]: "Kosteneffiziente und klimagerechte Transformationsstrategien für das deutsche Energiesystem bis zum Jahr 2050" (FZ Jülich 2020) 

| [HBS2015]: “Für einen modernen und effizienten Energieanlagenbau in Deutschland”, 
| Hans Böckler Stiftung (2015), https://www.boeckler.de/pdf_fof/98809.pdf 

| [ISE2018]: „Stromgestehungskosten Erneuerbare Energien“, Fraunhofer ISE, 2018 

| [ISE2020a]: „Wege zu einem klimaneutralen Energiesystem“, Fraunhofer ISE, 2020 
 
| [ISE2020b]: Anhang zu [ISE2020a], Fraunhofer ISE, 2020,  
| https://www.ise.fraunhofer.de/content/dam/ise/de/documents/publications/studies/Anhang-Studie-Wege-zu-einem-klimaneutralen-Energiesystem.pdf 

| [UBA2019a]: "Emissionsbilanz erneuerbarer Energieträger", Climate Change 37/2019, 
| Umweltbundesamt, Dessau-Roßlau 

| [UBA2019b]: “Analyse der kurz- und mittelfristigen Verfügbarkeit von Flächen für die Windenergienutzung an Land”, Climate Change 38/2019, Umweltbundesamt, Dessau-Roßlau 

| [NIR 2020] Nationaler Inventarbericht (Zitat steht woanders) Tabelle 563 

| [MaStR2021] https://www.marktstammdatenregister.de/MaStR 

| [RESCUE 2019] 

| [SCHINDELE2020]: "Implementation of agrophotovoltaics: Techno-economic analysis of the price-performance ratio and its policy implications”, Applied Energy, 265, 114737, 2020  
| https://www.sciencedirect.com/science/article/pii/S030626192030249X?via%3Dihub 

| [VGB2015]: "Levelised Cost of Electricity" (Issue 2015), VGB Powertech 
| https://web.archive.org/web/20200408085821/https://www.vgb.org/en/lcoe2015.html?dfid=74042 