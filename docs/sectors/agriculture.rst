8. Landwirtschaft
=================
| **Autor:innen: Vera Middendorf, Hauke Schmülling**
| **Stand: 25.02.22**

Dieses Dokument gibt einen Überblick über die wesentlichen Prinzipien, die den Berechnungen für Landwirtschaft in der Klimavision zugrunde liegen. Die Landwirtschaft ist in zwei strukturell verschiedene Bereiche geteilt: Pb Emissionen entstehen in den Subsektoren Tierhaltung (CRF 3.A), Düngerwirtschaft (CRF 3.B), Landwirtschaftlichen Böden (CRF 3.D) und Sonstige Landwirtschaft (CRF 3.G-J). Diese werden anhand von Tier- und Flächenzahlen abgeschätzt und die Maßnahmen beziehen sich auch primär auf diese Parameter. Cb Emissionen entstehen im Subsektor Betriebe und Maschinen (BuM; CRF 1.A.4.c), sodass sich die ganze Bereitstellung von Endenergieträgern auch nur auf diesen Subsektor bezieht. Hier wird ähnlich wie in GHD verfahren, sprich energetische Sanierung und Heizungsaustausch sowie Umstellung der landwirtschaftlichen Maschinen auf E-Fuels.

8.1 Eingabedaten
----------------
Ähnlich wie GHD werden die EEV in BuM von der nationalen Ebene mit der landwirtschaftlichen Fläche runtergerechnet. Diese Default-Werte können online in der Eingabe getrennt nach Endenergieträgern überschrieben werden, wenn kommunenfeine Daten vorliegen. Grundlage ist das Blatt 6.5 “Landwirtschaft/Fischerei/Bauwirtschaft" in den Auswertungstabellen [AGE2020] der AG Energiebilanzen: Die hier aufgeführten nationalen EEV werden vom Oberbereich GHD exkludiert. Da die landwirtschaftlich genutzten Flächen bereits kommunenfein vorliegen, ist hier keine Benutzer:inneneingabe notwendig. Lediglich die Anzahl der Nutztiere kann überschrieben werden. Die Default-Werte werden hier von bundeslandfeinen Daten wiederum mit der landwirtschaftlichen Fläche runtergerechnet.

8.2 Bilanzierung 2018
---------------------
8.2.1 Energiebedingte Emissionen: Nachfrage und Bereitstellung von Endenergieträgern
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Wie einleitend erwähnt ist die Landwirtschaft als einziger Sektor stark geteilt in einen nicht-energetischen Produktionsbereich und den energetischen Subsektor Betriebe und Maschinen (BuM; CRF 1.A.4.c), der Bereich Bereitstellung von Endenergieträgern bezieht sich also auch nur auf BuM. Im Jahr 2018 wird die Nutzung von Heizöl, LPG, Erdgas und Biomasse komplett der Kategorie „Betriebe Heizung“ zugeschrieben, Benzin und Diesel der Kategorie „Fahrzeuge“ und Strom der Kategorie „Elektrische Verbraucher“. Analog zu GHD werden die energiebedingten THG-Emissionen (cb Emissionen) auf der Bereitstellungs-Seite bilanziert, indem den Endenergieträgern Emissionsfaktoren zugeordnet werden.

8.2.2 Prozessbedingte Emissionen: Landwirtschaftliche Produktion
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Grundlage für die Berechnungen der prozessbedingten Treibhausgas-Emissionen (pb Emissionen) im Sektor Landwirtschaft ist der Nationale Inventar-Bericht [NIR 2020]. Dort wird in Emissionen aus der Fermentation bei der Verdauung (Subsektor Tierhaltung; CRF 3.A), aus der Behandlung von Wirtschaftsdüngern (Subsektor Düngerwirtschaft; CRF 3.B), aus der Nutzung landwirtschaftlicher Böden (Subsektor Landwirtschaftliche Böden; CRF 3.D), aus der im Zusammenhang mit Energiepflanzen-Vergärung entstehenden Emissionen, aus Kalkung, aus der Anwendung von Harnstoff sowie der Anwendung anderer kalkhaltiger Dünger (Subsektor Sonstige Landwirtschaft; CRF 3.G-J) unterschieden. Die Daten wurden dort mit dem Inventarmodell GAS-EM berechnet. Der NIR basiert auf Daten des Thünen-Instituts (Thünen Report 77), dessen Berechnungsgrundlagen (Anhänge) für die kommunenspezifischen Berechnungen in LocalZero genutzt wurde [Haenel 2020].

Die Fermentation bei der Verdauung wurde auf Grundlage von Tierzahlen unterschiedlicher Tierkategorien gebildet. Hier unterscheiden wir zwischen Milchkühen, anderen Rindern, Schweinen, Geflügel und anderen Tieren (Schafe, Ziegen, Equiden (hauptsächlich Pferde)). Emissionen treten hier als Methan (CH4) auf. Dieses entsteht durch die Aktivität von methanogenen Bakterien bei der Zersetzung organischer Substanz in anaerober Umgebung bzw. wird bei Wiederkäuern nach der Verdauung freigesetzt, weshalb in der Kategorie Geflügel z.B. keine Emissionen entstehen. Für den Bereich 3.A wurden keine gesonderten Annahmen, welche über die Annahmen aus dem NIR hinausgehen, getroffen. Die bundeslandfeinen Tierplatzzahlen aus dem Thünen-Report für das Jahr 2018 sind mit der jeweiligen landwirtschaftlich genutzten Fläche auf die einzelnen Kommunen eines Bundeslandes heruntergerechnet worden. Die Emissionsfaktoren eines Tierplatzes pro Jahr wurden mit den nationalen Gesamtemissionen und Tierplatzzahlen ermittelt.

Im Wirtschaftsdünger-Management wird über Methan- (CH4), Lachgas- (N2O) Stickstoffmonoxid- (NO) und NMVOC-Emissionen berichtet. Gülle- und strohbasierte Systeme werden mit ihren typischen Lagerformen berücksichtigt. Direkte N2O-Emissionen entstehen bei Nitrifikations- und Denitrifikationsprozessen während der Lagerung von Wirtschaftsdünger und Gärresten. NO entsteht durch Nitrifikation in den Oberflächenschichten im Lager. NMVOC-Emissionen werden aus Silage-Futter und Wirtschaftsdüngerlager freigesetzt. In der Berichterstattung werden dem Wirtschaftsdünger-Management auch indirekte N2O-Emissionen zugeordnet. Diese können bei Umsetzungsprozessen in Böden aus reaktivem Stickstoff, der aus der Deposition von NH3 und NO aus dem Wirtschaftsdünger- und Gärrestemanagement stammt, auftauchen. Die anaerobe Vergärung von Wirtschaftsdünger und Energiepflanzen in Biogasanlagen wird in die Berechnungen einbezogen [NIR 2020: 478]. Da das Wirtschaftsdüngeraufkommen von der Tierzahl abhängt, werden die pb Emissionen von den Tierplatzzahlen im Subsektor „Tierhaltung“ abgeleitet. Die Emissionsfaktoren der Düngerwirtschaft (CO2e pro Jahr und Tierplatz) werden gemäß Thünen Report 77 bundeslandfein ermittelt und mit den Tierplatzzahlen multipliziert. Auch für das Wirtschaftsdünger-Management im Bereich 3.B wurden keine gesonderten Annahmen, welche über die Annahmen aus dem NIR hinausgehen, getroffen.

Emissionen aus der Nutzung landwirtschaftlicher Böden sind in weitere Unterkategorien aufgeteilt. Diese beschreiben das Material, welches Emissionen aus dem Boden verursacht und aufgetragen wurde (Wirtschaftsdünger, Mineraldünger, Energiepflanzen-Gärreste, Klärschlamm, Weidegang, Ernterückstände) oder durch Abbauprozesse entsteht (Mineralisierung, organische Böden). Auch indirekte Emissionen durch Deposition oder Auswaschung werden betrachtet. In diesem Bereich werden Lachgas-Emissionen (N2O) bilanziert. Zur Umrechnung der N2O-N-Emissionen werden Default-Werte des IPCC (2006)-Werte genutzt [NIR 2020: 518]. Die flächenbezogenen Emissionsfaktoren der landwirtschaftlichen Böden werden gemäß dem Thünen Report 77 bundeslandfein ermittelt und mit den Flächen für Ackerland und/oder Grünland multipliziert, teilweise noch spezifiziert nach organischem Boden.

Im Subsektor „Sonstige Landwirtschaft“ werden kleinere Posten von CRF 3 gesammelt.

Die Kalkdüngung (die Zuführung von Carbonaten) verringert den Säuregehalt des Bodens und verbessert das Pflanzenwachstum, wobei CO2 freigesetzt wird. Die Kalkung geschieht mit Calcit, Dolomit (CRF 3.G) oder Kalkammonsalpeter (KAS; CRF 3.I). Bei der Stickstoffdüngung mit Harnstoff entsteht unter Einwirkung von Urease und Wasser CO2, das bei der industriellen Herstellung von Harnstoffdünger gebunden wurde [NIR 2020: 524]. Für all diese Düngerausbringungen wird die genutzte Menge über die landwirtschaftliche Fläche abgeschätzt, abgeleitet von bundeslandfeinen Daten, die im Thünen Report 77 zur Verfügung stehen. Dort sind ebenfalls bundeslandfein Zahlen zur Nutzung von Energiepflanzen-Trockenmasse hinterlegt. Die Vergärung von Energiepflanzen in Fermentern dient der Gewinnung von Biokraftstoffen (siehe Biogas, Bioethanol und Biogas im Sektor Kraftstoffe). Dabei entstehen vor allem Methan-Emissionen durch Leckagen, ebenso bei der anschließenden Gärreste-Lagerung. Die pb Emissionen aus der Ausbringung von Gärresten auf Feldern werden wie beschrieben in CRF 3.D bilanziert.

8.3 Maßnahmen
-------------
Der Bereich Landwirtschaft wird weiterhin THG-Emissionen haben. Eine Reduktion der Emissionen ist hier aber trotzdem mit verschiedenen Maßnahmen möglich. Grundlage für die Auswahl an Maßnahmen ist hier die Studie des Umweltbundesamts „Wege in eine ressourcenschonende Klimaneutralität“ [RESCUE 2019].

Bei der Umstellung auf Öko-Landwirtschaft werden 20% der landwirtschaftlichen Flächen angestrebt. Hierbei sorgt vor allem der Verzicht auf mineralische Stickstoffdüngung und Pestizide für erhebliche Einsparungen von Energie und Treibhausgasemissionen [UBA 2014]. Zudem wird eine Beratung zur Umstellung der landwirtschaftlichen Betriebe angeboten: Diese Maßnahme wirken sich auf alle betrachteten Subsektoren aus. Daher werden bei der landwirtschaftlichen Produktion keine weiteren Kosten angesetzt, lediglich die energetische Sanierung der Betriebe und Heizungsaustausch werden analog zu GHD als notwendige Investitionen angesetzt.

Nachgelagert zu Beratung und Umstellung der landwirtschaftlichen Betriebe (und damit einhergehend des Konsums) ergeben sich jedoch subsektorspezifische Folgen:

Die RESCUE-Studie vom UBA, „Klimaneutrales Deutschland 2045“ von Agora und "Quantifizierung von Maßnahmenvorschlägen" vom Ökoinstitut sehen die Reduktion der Tierplatzzahlen für das variable Zieljahr vor und flossen in die Bestimmung der Reduktionsmengen von CH4 ein. Die Tierbestände werden je nach Tiergruppe um etwa die Hälfte reduziert, insbesondere durch weniger Kühe können erheblich THG-Emissionen gespart werden.

Die THG-Emissionen bei der Düngerwirtschaft reduzieren sich stark infolge des gesunkenen Wirtschaftsdüngeraufkommens und die Annahme, dass alle Gärrestelager luftdicht abgedeckt werden.

Bei den landwirtschaftlichen Böden wird eine Reduktion der N-Überschüsse durch Bestimmung des Düngebedarfs von Pflanzen, verbesserte Berücksichtigung der N-Nachlieferung aus der organischen Substanz des Bodens während der Vegetationsperiode und die Analyse der Nährstoffgehalte der organischen Dünger beabsichtigt [UBA 2014]. Damit werden sowohl die direkten als auch die indirekten Emissionen reduziert. Des Weiteren wird angenommen, dass weder Klärschlamm noch Energiepflanzen-Gärreste ausgebracht werden (Ausnahme: als Karbonisate). Durch den Rückgang der organischen Böden als landwirtschaftliche Nutzfläche (siehe LULUCF) sinken die Emissionen, die durch den Abbau organischer Substanz entstanden sind [RESCUE 2020].

8.4 Bilanz Zieljahr
-------------------

8.4.1 Energiebedingte Emissionen: Nachfrage und Bereitstellung von Endenergieträgern
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Ein Nachfragerückgang von -37,7% bei den Fahrzeugen und -15,4% bei den elektrischen Verbrauchern wurde analog zu GHD basierend auf dem GreenSupreme-Szenario angenommen. Ebenso erfolgt die energetische Sanierung der landwirtschaftlichen Gebäude und ein Heizungsaustausch zugunsten von Wärmepumpen.

8.4.2 Prozessbedingte Emissionen: Landwirtschaftliche Produktion
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Der Sektor Landwirtschaft ist auch im Zieljahr nicht treibhausgasneutral.

Zur Berechnung der Wirksamkeiten den Maßnahmen wurde die Studie “Treibhausgasneutrales Deutschland im Jahr 2050” des Umweltbundesamtes sowie die Studie “Quantifizierung von Maßnahmenvorschlägen der deutschen Zivilgesellschaft zu THG-Minderungspotenzialen in der Landwirtschaft bis 2030” des Öko-Institut e.V. zurate gezogen.

Die Reduktion der pb Emissionen in der Quellgruppe Landwirtschaft werden folgendermaßen mathematisch abgebildet:

* Fermentation: Reduktion der Tierplatzzahlen, Emissionsfaktoren bleiben gleich

* Düngerwirtschaft: Reduktion der Tierplatzzahlen, Emissionsfaktoren sinken gemäß RESCUE um 60% durch bessere Abdeckung

* Landwirtschaftliche Böden: Bewirtschaftete Flächen ändern sich gemäß LULUCF, alle stickstoffbasierten Emissionsfaktoren halbieren sich durch die Halbierung des Stickstoffüberschusses

* Sonstige Landwirtschaft: Die Menge des ausgebrachten Kalks bleibt konstant da weiter benötigt, nur der Emissionsfaktor der Harnstoffdüngung halbiert sich durch die Halbierung des Stickstoffüberschusses, Vergärung von Energiepflanzen wird eingestellt


8.4.3 Kosten
^^^^^^^^^^^^
Als Kosten für die Umstellung der Landwirtschaft sind hauptsächlich Beratungskosten für die Umstellung auf treibhausgasarme Düngung sowie auf Ökolandwirtschaft angenommen worden. Investitionen sind hierbei nur für die Umstellung auf Ökolandwirtschaft berücksichtigt worden [Fraunhofer/UBA 2015].

Für die Umrechnung auf Öko-Landwirtschaft ist angenommen worden, dass alle Kommunen auf mind. 20% Öko-Landwirtschaft kommen müssen. Dafür wurden die Anteile der Öko-Betriebe auf Bundeslandebene auf die Kommunen heruntergerechnet und der fehlende Anteil berechnet [Destatis]. Die Daten beziehen sich auf das Jahr 2016, anstatt auf das sonst angenommene Jahr 2018.

Die Investitionen und Arbeitsplätze für die energetische Sanierung und Wärmepumpen-Einbau wurde analog zu GHD ermittelt.


Quellen
-------
| NIR 2020

| RESCUE 2020

| Haenel 2020: Haenel et al. 2020: Thünen Report 77. Berechnung von gas- und partikelförmigen Emissionen aus der deutschen Landwirtschaft 1990-2018. Report zu Methoden und Daten (RMD) Berichterstattung 2020.

| UBA 2014: Umweltbundesamt 2014: Treibhausgasneutrales Deutschland im Jahr 2050

| Öko 2019: Öko-Institut e.V. 2019: Quantifizierung von Maßnahmenvorschlägen der deutschen Zivilgesellschaft zu THG-Minderungspotenzialen in der Landwirtschaft bis 2030

| Destatis: Landwirtschaftliche Betriebe und deren landwirtschaftlich genutzte Fläche (LF) nach Art der Bewirtschaftung - Jahr - regionale Tiefe: Kreise und krfr. Städte. Jahr unbekannt

| Fraunhofer/UBA 2015: Green Finance. Strategien und Instrumente zur Finanzierung des ökologischen Modernisierungsprozesses.













