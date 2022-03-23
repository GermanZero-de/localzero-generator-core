from collections import defaultdict
import csv
from lxml import etree
import os
import re
import json


def parseElem(elem, tags: list[str]) -> list:
    returnList = [None] * len(tags)
    for subelem in elem:
        # print(subelem.tag+"   "+subelem.text)
        for i, tag in enumerate(tags):
            if subelem.tag == tag:
                returnList[i] = subelem.text
    return returnList


def parseXML(
    path: str,
    *,
    useinputDict=False,
    inputDict=defaultdict(float),
    printInfo: bool = False,
    printExit: bool = False,
) -> defaultdict:
    """This parses the XML file under path and returns a dict formated list {key: power | ags keys in xml}
    Right now we also filter out some entries due to some specifications like the installation date.
    There are just a few entries (<10) in the xml that do not ags keys. ATM we disregard those.
    """
    returnDict = defaultdict(float)
    if useinputDict:
        returnDict = inputDict
    with open(path, "r", encoding="utf-16") as file:

        tree = etree.parse(file, parser=etree.XMLParser())
        root = tree.getroot()

        noAgsCount = 0
        noPowerCount = 0
        noDate = 0
        for elem in root:
            [ags, netpower, date, enddate, status] = parseElem(
                elem,
                [
                    "Gemeindeschluessel",
                    "Nettonennleistung",
                    "Inbetriebnahmedatum",
                    "DatumEndgueltigeStilllegung",
                    "EinheitBetriebsstatus",
                ],
            )

            # Betriebsstatus
            # 35 -> In Betrieb, 31 -> In Planung, 37 -> Vorübergehend stillgelegt, 38 -> Endgültig stillgelegt
            if status == "31":  # filter out "in Planung"
                continue

            if (
                enddate is not None and int(enddate[:4]) < 2019
            ):  # filter out "stillgelegt vor 2019"
                continue

            if date is None:
                noDate += 1
            elif (
                int(date[:4]) > 2018
            ):  # filter out "in Betrieb gegangen nach ende 2018"
                continue

            if ags is None:
                noAgsCount += 1
            elif netpower is None:
                noPowerCount += 1
            else:
                returnDict[ags] += float(netpower)

        if printInfo:
            print(
                "In "
                + path
                + ": No AGS Count: "
                + str(noPowerCount)
                + ", No power Count: "
                + str(noPowerCount)
                + ", No Date: "
                + str(noDate)
            )
        if printExit:
            print("parsed " + path)

    return returnDict


def parsemultiXML(basepath, numberOfFiles, *, printExit=False, printInfo=False):
    """We need this as the data for one Energieträger (Pv) is stored in multiple XML files."""
    pvDict = defaultdict(float)
    for i in range(1, numberOfFiles + 1):
        pvDict = parseXML(
            basepath + "_" + str(i) + ".xml",
            useinputDict=True,
            inputDict=pvDict,
            printInfo=printInfo,
            printExit=printExit,
        )

    return pvDict


def loadMaster(path) -> list:
    """This loads the master.csv file and returns a list of all ags keys."""
    masterAGS = []
    with open(path, "r") as master:
        masterR = csv.reader(master, delimiter=",")
        masterAGS = []
        _ = next(masterR)  # remove header
        for entry in masterR:
            masterAGS.append(entry[0])
    return masterAGS


def calcSum(inDict: defaultdict) -> float:
    """This calculates sums over all values of the input dict"""
    sum = 0
    for value in inDict.values():
        sum += value
    return sum


def handleNotInMaster(indict: defaultdict, master: list, dataList, lookUpDict):
    """This deals with all ags entries in indict that are not contained in the master list. It updates the ags to its successor or devides an ags key into its predecessors."""
    notInMaster = set()
    for key in indict.keys():
        if key not in master:
            notInMaster.add(key)

    for ags in notInMaster:
        changedAgsList = lookUpAGSinRepo(ags, lookUpDict=lookUpDict, repo=dataList)

        if len(changedAgsList) == 1:
            # wenn der ags nur einmal in der json vorkommt aber nicht in der masterliste ist,
            # ist der ags veraltet und muss durch den neuen ersetzt werden.
            indict[changedAgsList[0]] += indict[ags]
        else:
            for changedAgs in changedAgsList:
                # die Leistung wir auf alle vorgänger ags gleichmäßig aufgeteilt
                indict[changedAgs] += indict[ags] / len(changedAgsList)
    return indict


def loadAGSRepo(repoPath):
    """This loads the json from https://www.xrepository.de/api/xrepository/urn:xoev-de:bund:destatis:bevoelkerungsstatistik:codeliste:ags.historie_2021-12-31/download/Destatis.AGS.Historie_2021-12-31.json
    to a dict "agsList" and creates a lookup dict "agslookUpDict" that saves all contained ags keys with the indices, where they appear in agsList
    """
    # TODO: Check if this handles all cases correctly or if we could do better easily.
    with open(repoPath, "r", encoding="utf-8") as repo:
        agsList = json.loads(repo.read())
    dataList = agsList["daten"]
    agsLookUpDict = defaultdict(list)
    for (i, data) in enumerate(dataList):
        for ii, elem in enumerate(data):
            # print(elem)
            if elem == None:
                continue
            if re.match(r"[0-9]{8}", elem):
                agsLookUpDict[elem].append([i, ii])
    return agsList, agsLookUpDict


def lookUpAGSinRepo(ags: str, lookUpDict, repo) -> list[str]:
    """This looks up an ags and returns a list of ags keys. If the ags only appears once, we assume it has a single predecessor and return the predecessor.
    If the ags key appears multiple times, we return all predecessor."""
    # TODO: Check if this deals with all cases correctly.

    agsReturnList = []
    dataList = repo["daten"]
    vorkommnisse = lookUpDict[ags]
    if len(vorkommnisse) == 1:
        [
            _,
            _,
            name,
            validFrom,
            changeType,
            validUntil,
            successorAGS,
            successorName,
            successorAGSValidFrom,
            descritpion,
        ] = dataList[vorkommnisse[0][0]]
        # if changeType is not None:
        #    print("change type "+changeType+" valid until " +validUntil)
        agsReturnList.append(successorAGS)

    if len(vorkommnisse) > 1:
        # print("Ags: "+ags)
        for [i, _] in vorkommnisse:
            ersterAgsInData = dataList[i][1]
            if ersterAgsInData is not ags:
                agsReturnList.append(ersterAgsInData)
        # print("mehere Vorkomnisse")
    return agsReturnList


def saveDict(indict: dict, name: str):
    if not os.path.exists("xmlZwischenspeicher"):
        os.makedirs("xmlZwischenspeicher")

    with open("xmlZwischenspeicher/" + name + ".json", "w") as file:
        json.dump(indict, file)


def loadDictFromJson(name: str):
    returnDict = defaultdict(float)
    with open("xmlZwischenspeicher/" + name + ".json", "r") as file:
        returnDict = defaultdict(float, json.loads(file.read()))
    return returnDict


def fuseDicts(indictList: list[defaultdict], masterList) -> dict:
    returnDict = {}
    for ags in masterList:
        returnDict[ags] = [indict[ags] for indict in indictList]
    return returnDict


def aggregateDict(indict: dict):
    """aggregates the input dict and creates sums for all state and district ags keys."""

    def addLists(list1: list[float], list2: list[float]) -> list[float]:
        if list1 == []:
            return list2
        if list2 == []:
            return list1
        return [list1[i] + list2[i] for i, _ in enumerate(list2)]

    sumoverDistr = defaultdict(list[float])
    sumoverState = defaultdict(list[float])
    for ags, powerList in indict.items():
        ags_sta = ags[:2] + "000000"
        ags_dis = ags[:5] + "000"
        sumoverDistr[ags_dis] = addLists(sumoverDistr[ags_dis], powerList)
        sumoverState[ags_sta] = addLists(sumoverState[ags_sta], powerList)

    for key, val in sumoverDistr.items():
        indict[key] = val

    for key, val in sumoverState.items():
        indict[key] = val


def main():

    reloadfromXML: bool = False

    PvDict = defaultdict(float)
    BiomassDict = defaultdict(float)
    WasserDict = defaultdict(float)
    WindDict = defaultdict(float)

    if reloadfromXML:
        PvDict = parsemultiXML("Xml/EinheitenSolar", 24, printExit=True, printInfo=True)
        BiomassDict = parseXML(
            "Xml/EinheitenBiomasse.xml", printExit=True, printInfo=True
        )
        WasserDict = parseXML("Xml/EinheitenWasser.xml", printExit=True, printInfo=True)
        WindDict = parseXML("Xml/EinheitenWind.xml", printExit=True, printInfo=True)

        saveDict(PvDict, "pvDict")
        saveDict(BiomassDict, "biomassDict")
        saveDict(WindDict, "windDict")
        saveDict(WasserDict, "wasserDict")
    else:
        PvDict = loadDictFromJson("pvDict")
        BiomassDict = loadDictFromJson("biomassDict")
        WasserDict = loadDictFromJson("wasserDict")
        WindDict = loadDictFromJson("windDict")

    BiomassTotal = calcSum(BiomassDict)
    WasserTotal = calcSum(WasserDict)
    WindTotal = calcSum(WindDict)
    PvTotal = calcSum(PvDict)

    masterAGS = loadMaster("Master2018/master.csv")

    [agsList, lookUpDict] = loadAGSRepo("Xrepo/xrepo.json")

    BiomassDict = handleNotInMaster(
        BiomassDict, master=masterAGS, dataList=agsList, lookUpDict=lookUpDict
    )
    PvDict = handleNotInMaster(
        PvDict, master=masterAGS, dataList=agsList, lookUpDict=lookUpDict
    )
    WasserDict = handleNotInMaster(
        WasserDict, master=masterAGS, dataList=agsList, lookUpDict=lookUpDict
    )
    WindDict = handleNotInMaster(
        WindDict, master=masterAGS, dataList=agsList, lookUpDict=lookUpDict
    )

    totalDict = fuseDicts(
        [PvDict, WindDict, BiomassDict, WasserDict], masterList=masterAGS
    )

    aggregateDict(totalDict)

    # TODO: Sort ags keys

    with open("2018.csv", "w", newline="") as renewable_energy:
        renewable_energy.write("ags,pv,wind_on,biomass,water\n")
        writer = csv.writer(renewable_energy)

        writer.writerow(["DG000000", PvTotal, WindTotal, BiomassTotal, WasserTotal])

        for ags, powerList in totalDict.items():
            writer.writerow([ags, *powerList])


main()

# nützliche info aus der xrepository json
# "In dieser Codeliste sind alle Gebietsänderungen seit dem 01.01.2007 abgebildet. Sie enthält alle AGS,"
# " die zu irgendeinem Zeitpunkt seit dem 31.12.2006 existiert haben. Jeweils mit Gültigkeitszeitraum,"
# " Gemeindebezeichnung und (falls die Gemeinde inzwischen aufgelöst wurde) dem Rechtsnachfolger. "
# "Enthalten ist ebenfalls - für alle Gemeinden, bei denen sich Änderungen ergeben haben - "
# "die entsprechende Änderungsart:
# 1=Auflösung (AGS wird ungültig);
# 2=Teilausgliederung (Gemeinde gibt einen Teil ab, AGS bleibt weiterhin gültig);
# 3=Schlüsseländerung (AGS wird ungültig, Gemeinde bekommt einen neuen AGS, z.B. bei Kreiszugehörigkeitsänderungen);
# 4=Namensänderung (AGS bleibt bestehen, Gemeinde bekommt einen neuen Namen oder eine Zusatzbezeichnung wie z.B. \", Stadt\").","lang":null}]


# [{"spaltennameLang":"Code","spaltennameTechnisch":"Code","datentyp":"string","codeSpalte":true,"verwendung":{"code":"REQUIRED"},"empfohleneCodeSpalte":true,"sprache":null},
# {"spaltennameLang":"AGS","spaltennameTechnisch":"AGS","datentyp":"string","codeSpalte":false,"verwendung":{"code":"REQUIRED"},"empfohleneCodeSpalte":false,"sprache":null},
# {"spaltennameLang":"Gemeindenamen mit Zusatz","spaltennameTechnisch":"GemeindenamenMitZusatz","datentyp":"string","codeSpalte":false,"verwendung":{"code":"REQUIRED"},"empfohleneCodeSpalte":false,"sprache":null},
# {"spaltennameLang":"gueltig ab","spaltennameTechnisch":"gueltigAb","datentyp":"string","codeSpalte":false,"verwendung":{"code":"REQUIRED"},"empfohleneCodeSpalte":false,"sprache":null},
# {"spaltennameLang":"Aenderungsart","spaltennameTechnisch":"Aenderungsart","datentyp":"string","codeSpalte":false,"verwendung":{"code":"OPTIONAL"},"empfohleneCodeSpalte":false,"sprache":null},
# {"spaltennameLang":"gueltig bis","spaltennameTechnisch":"gueltigBis","datentyp":"string","codeSpalte":false,"verwendung":{"code":"OPTIONAL"},"empfohleneCodeSpalte":false,"sprache":null},
# {"spaltennameLang":"AGS des Nachfolgers","spaltennameTechnisch":"NachfolgerAGS","datentyp":"string","codeSpalte":false,"verwendung":{"code":"OPTIONAL"},"empfohleneCodeSpalte":false,"sprache":null},
# {"spaltennameLang":"Name des Nachfolgers","spaltennameTechnisch":"NachfolgerName","datentyp":"string","codeSpalte":false,"verwendung":{"code":"OPTIONAL"},"empfohleneCodeSpalte":false,"sprache":null},
# {"spaltennameLang":"Nachfolger gueltig ab","spaltennameTechnisch":"NachfolgerGueltigAb","datentyp":"string","codeSpalte":false,"verwendung":{"code":"OPTIONAL"},"empfohleneCodeSpalte":false,"sprache":null},
# {"spaltennameLang":"Hinweis","spaltennameTechnisch":"Hinweis","datentyp":"string","codeSpalte":false,"verwendung":{"code":"OPTIONAL"},"empfohleneCodeSpalte":false,"sprache":null}]
