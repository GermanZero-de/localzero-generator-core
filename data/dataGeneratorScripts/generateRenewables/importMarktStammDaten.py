from collections import defaultdict
import csv
from lxml import etree
import os
import re
import json


cutoffdate = "31.12.2018"

# this is only used in the handling of "not 2018"-ags keys
# this is not used in the xml parsing so far

exceptionDict = {
    "09478444": "Neuensorger Forst ist ein gemeindefreies gebiet",
    "01053105": "Sachsenwald ist ein gemeindefreies Gebiet",
    "06435200": "Gutsbezirk Spessart ist ist ein gemeindefreies Gebiet",
    "01060014": "BuchholzerForstist ist ein gemeindefreies Gebiet",
    "09572444": "Gdefr. Geb. (Lkr Erlangen-Höchstadt) ist ein gemeindefreies Gebiet",
    "03155501": "Solling (Landkreis Northeim) ist ein gemeindefreies Gebiet",
    "03153504": "Harz (Landkreis Goslar), gemfr. Gebiet ist ein gemeindefreies Gebiet",
}


def parse_elem(elem, tags: list[str]) -> list:
    returnList = [None] * len(tags)
    for subelem in elem:
        print(subelem.tag + "   " + subelem.text)
        for i, tag in enumerate(tags):
            if subelem.tag == tag:
                returnList[i] = subelem.text
    return returnList


def parse_xml(
    path: str,
    *,
    use_input_dict=False,
    input_dict=defaultdict(float),
    print_info: bool = False,
    print_exit: bool = False,
) -> defaultdict:
    """This parses the XML file under path and returns a dict formated list {key: power | ags keys in xml}
    Right now we also filter out some entries due to some specifications like the installation date.
    There are just a few entries (<10) in the xml that do not ags keys. ATM we disregard those.
    """
    return_dict = defaultdict(float)
    if use_input_dict:
        return_dict = input_dict
    with open(path, "r", encoding="utf-16") as file:

        tree = etree.parse(file, parser=etree.XMLParser())
        root = tree.getroot()

        no_ags_count = 0
        no_power_count = 0
        no_date = 0
        for elem in root:
            [ags, netpower, date, enddate, status] = parse_elem(
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
                no_date += 1
            elif (
                int(date[:4]) > 2018
            ):  # filter out "in Betrieb gegangen nach ende 2018"
                continue

            if ags is None:
                no_ags_count += 1
            elif netpower is None:
                no_power_count += 1
            else:
                return_dict[ags] += float(netpower)

        if print_info:
            print(
                "In "
                + path
                + ": No AGS Count: "
                + str(no_power_count)
                + ", No power Count: "
                + str(no_power_count)
                + ", No Date: "
                + str(no_date)
            )
        if print_exit:
            print("parsed " + path)

    return return_dict


def parse_multi_xml(base_path, number_of_files, *, print_exit=False, print_info=False):
    """We need this as the data for one Energieträger (Pv) is stored in multiple XML files."""
    pv_dict = defaultdict(float)
    for i in range(1, number_of_files + 1):
        pv_dict = parse_xml(
            base_path + "_" + str(i) + ".xml",
            use_input_dict=True,
            input_dict=pv_dict,
            print_info=print_info,
            print_exit=print_exit,
        )

    return pv_dict


def load_master(path) -> list:
    """This loads the master.csv file and returns a list of all ags keys."""
    master_list = []
    with open(path, "r") as file:
        master_reader = csv.reader(file, delimiter=",")
        _ = next(master_reader)  # remove header
        for entry in master_reader:
            master_list.append(entry[0])
    return master_list


def load_population(path) -> dict:
    """This loads the 2018.csv population file that contains a list of all ags keys with their population."""
    population_dict = dict()
    with open(path, "r") as file:
        population_reader = csv.reader(file, delimiter=",")

        _ = next(population_reader)  # remove header
        for entry in population_reader:
            population_dict[entry[0]] = entry[1]
    return population_dict


def calc_sum(input_dict: defaultdict) -> float:
    """This calculates sums over all values of the input dict"""
    sum = 0
    for value in input_dict.values():
        sum += value
    return sum


def handle_not_in_master(
    input_dict: defaultdict,
    master: list,
    dataList,
    lookUpDict,
    populationData: dict,
    *,
    printDetails: bool = False,
):
    """
    This deals with all ags entries in input_dict that are not contained in the master list. It adds the power values of the missing ags keys to their
     successors or predecessors.

     So far the powers are distributes over sevreal ags keys proportional to their population.
     The EE-unit is disregarded/deleted if the ags corresponds to a gemeindefreie Gebiet.
    """
    notInMaster = set()
    for key in input_dict.keys():
        if key not in master:
            notInMaster.add(key)

    for ags in notInMaster:
        newAGSnotinMaster = False
        if printDetails:
            print("handling ags " + ags)

        changedAgsList = lookUpAGSinRepo(
            ags, lookUpDict=lookUpDict, repo=dataList, printDetails=printDetails
        )

        if (
            changedAgsList == []
        ):  # this happens if the ags key is a gemeindefreies Gebiet and the ags key occurs in the exception list
            if printDetails:
                print(str(ags) + "ags key not in master")
                print(str(input_dict[ags]) + "power lost")
            del input_dict[ags]
            continue

        if printDetails:
            print("ags in changed AGS List" + str(changedAgsList))

        for agsKey in changedAgsList:
            if (
                agsKey not in master
            ):  # this happens if the new ags key is a gemeindefreies Gebiet and the ags key occurs in the exception list
                if printDetails:
                    print(str(agsKey) + " new Ags not in master")
                if agsKey in exceptionDict:
                    if printDetails:
                        print(exceptionDict[agsKey])
                        print(str(input_dict[ags]) + " power lost")
                    newAGSnotinMaster = True
                else:
                    exit(1)

        if newAGSnotinMaster:
            continue

        populationSum = sum(float(populationData[agsKey]) for agsKey in changedAgsList)
        power = float(input_dict[ags])

        for agsKey in changedAgsList:
            populationinchangedAGS = float(populationData[agsKey])
            input_dict[agsKey] += power * (populationinchangedAGS / populationSum)

    return input_dict


def loadAGSRepo(repoPath):
    """This loads the json from https://www.xrepository.de/api/xrepository/urn:xoev-de:bund:destatis:bevoelkerungsstatistik:codeliste:ags.historie_2021-12-31/download/Destatis.AGS.Historie_2021-12-31.json
    to a dict "agsList" and creates a lookup dict "agslookUpDict" that saves all contained ags keys with the indices, where they appear in agsList
    [code,predecessorAGS,name,validFrom,changeType,validUntil,successorAGS,successorName,successorAGSValidFrom,descritpion] with
    the following description
    - code - Code
    - predecessorAGS - AGS
    - name - Gemeindenamen mit Zusatz
    - validFrom - gueltig ab
    - changeType - Aenderungsart
    - validUntil - gueltig bis
    - successorAGS - AGS des Nachfolgers
    - successorName - Name des Nachfolgers
    - successorAGSValidFrom - Nachfolger gueltig ab
    - descritpion - Hinweis
    nützliche info aus der xrepository json
    In dieser Codeliste sind alle Gebietsänderungen seit dem 01.01.2007 abgebildet. Sie enthält alle AGS,
    die zu irgendeinem Zeitpunkt seit dem 31.12.2006 existiert haben. Jeweils mit Gültigkeitszeitraum,
    Gemeindebezeichnung und (falls die Gemeinde inzwischen aufgelöst wurde) dem Rechtsnachfolger.

    with the change types:
    - 1 = Auflösung (AGS wird ungültig)
    - 2 = Teilausgliederung (Gemeinde gibt einen Teil ab, AGS bleibt weiterhin gültig)
    - 3 = Schlüsseländerung (AGS wird ungültig, Gemeinde bekommt einen neuen AGS, z.B. bei Kreiszugehörigkeitsänderungen)
    - 4 = Namensänderung (AGS bleibt bestehen, Gemeinde bekommt einen neuen Namen oder eine Zusatzbezeichnung wie z.B. "Stadt")
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


def lookUpAGSinRepo(
    ags: str, lookUpDict, repo, *, printDetails: bool = False
) -> list[str]:
    """
    This looks up an ags and returns a list of all ags keys that are either predecessors or successors of the key.
    """
    # TODO: Check if this deals with all cases correctly.

    agsReturnList = []
    dataList = repo["daten"]
    vorkommnisse = lookUpDict[ags]

    agsAsPredecessor = []
    agsAsSuccessor = []

    for elem in vorkommnisse:
        if elem[1] == 1:  # the ags key is at the predecessor position in the data
            agsAsPredecessor.append(dataList[elem[0]])

        elif elem[1] == 6:  # the ags key is at the successor position in the data
            agsAsSuccessor.append(dataList[elem[0]])
        else:
            print(
                "This should not happen. Check if the repository is prvoded in the following form:\n [code,predecessorAGS,name,validFrom,changeType,validUntil,successorAGS,successorName,successorAGSValidFrom,descritpion]"
            )
            exit(1)

    if len(agsAsPredecessor) > 0:

        for elem in agsAsPredecessor:

            [
                code,
                predecessorAGS,
                name,
                validFrom,
                changeType,
                validUntil,
                successorAGS,
                successorName,
                successorAGSValidFrom,
                descritpion,
            ] = elem
            if successorAGS != None:
                if printDetails:
                    print(
                        successorAGS
                        + " ags as predeccessor date "
                        + successorAGSValidFrom
                    )
                if int(successorAGSValidFrom[-4:]) <= int(cutoffdate[-4:]):
                    if successorAGS != ags:
                        agsReturnList.append(successorAGS)

    if len(agsAsSuccessor) > 0:
        for elem in agsAsSuccessor:
            [
                code,
                predecessorAGS,
                name,
                validFrom,
                changeType,
                validUntil,
                successorAGS,
                successorName,
                successorAGSValidFrom,
                descritpion,
            ] = elem
            if printDetails:
                print(
                    predecessorAGS + " ags as successor date " + successorAGSValidFrom
                )
            if int(successorAGSValidFrom[-4:]) > int(cutoffdate[-4:]):
                if predecessorAGS != ags:
                    agsReturnList.append(predecessorAGS)

    if len(agsReturnList) == 0:
        if ags in exceptionDict:
            if printDetails:
                print(exceptionDict[ags])
        else:
            print("apperatently you did not handle all cases for " + ags)
            exit(1)

    return agsReturnList


def saveDict(input_dict: dict, name: str):
    if not os.path.exists("xmlZwischenspeicher"):
        os.makedirs("xmlZwischenspeicher")

    with open("xmlZwischenspeicher/" + name + ".json", "w") as file:
        json.dump(input_dict, file)


def loadDictFromJson(name: str):
    return_dict = defaultdict(float)
    with open("xmlZwischenspeicher/" + name + ".json", "r") as file:
        return_dict = defaultdict(float, json.loads(file.read()))
    return return_dict


def fuseDicts(input_dictList: list[defaultdict], masterList) -> dict:
    return_dict = {}
    for ags in masterList:
        return_dict[ags] = [input_dict[ags] for input_dict in input_dictList]
    return return_dict


def aggregateDict(input_dict: dict):
    """aggregates the input dict and creates sums for all state and district ags keys."""

    def addLists(list1: list[float], list2: list[float]) -> list[float]:
        if list1 == []:
            return list2
        if list2 == []:
            return list1
        return [list1[i] + list2[i] for i, _ in enumerate(list2)]

    sumoverDistr = defaultdict(list[float])
    sumoverState = defaultdict(list[float])
    for ags, powerList in input_dict.items():
        ags_sta = ags[:2] + "000000"
        ags_dis = ags[:5] + "000"
        sumoverDistr[ags_dis] = addLists(sumoverDistr[ags_dis], powerList)
        sumoverState[ags_sta] = addLists(sumoverState[ags_sta], powerList)

    for key, val in sumoverDistr.items():
        input_dict[key] = val

    for key, val in sumoverState.items():
        input_dict[key] = val


def dictToSortedList(input_dict: dict) -> list:
    returnList = []
    for ags, powers in input_dict.items():
        returnList.append([ags, *powers])

    returnList.sort(key=lambda x: int(x[0]))  # sort by ags keys

    return returnList


def main():

    reloadfromXML: bool = False

    pv_dict = defaultdict(float)
    BiomassDict = defaultdict(float)
    WasserDict = defaultdict(float)
    WindDict = defaultdict(float)

    if reloadfromXML:
        pv_dict = parse_multi_xml("Xml/EinheitenSolar", 24, print_exit=True, print_info=True)
        BiomassDict = parse_xml(
            "Xml/EinheitenBiomasse.xml", print_exit=True, print_info=True
        )
        WasserDict = parse_xml("Xml/EinheitenWasser.xml", print_exit=True, print_info=True)
        WindDict = parse_xml("Xml/EinheitenWind.xml", print_exit=True, print_info=True)

        saveDict(pv_dict, "pv_dict")
        saveDict(BiomassDict, "biomassDict")
        saveDict(WindDict, "windDict")
        saveDict(WasserDict, "wasserDict")
    else:
        pv_dict = loadDictFromJson("pv_dict")
        BiomassDict = loadDictFromJson("biomassDict")
        WasserDict = loadDictFromJson("wasserDict")
        WindDict = loadDictFromJson("windDict")

    masterAGS = load_master("Master2018/master.csv")
    population = load_population("population/2018.csv")

    [agsList, lookUpDict] = loadAGSRepo("Xrepo/xrepo.json")

    BiomassDict = handle_not_in_master(
        BiomassDict,
        master=masterAGS,
        dataList=agsList,
        lookUpDict=lookUpDict,
        populationData=population,
    )
    pv_dict = handle_not_in_master(
        pv_dict,
        master=masterAGS,
        dataList=agsList,
        lookUpDict=lookUpDict,
        populationData=population,
    )
    WasserDict = handle_not_in_master(
        WasserDict,
        master=masterAGS,
        dataList=agsList,
        lookUpDict=lookUpDict,
        populationData=population,
    )
    WindDict = handle_not_in_master(
        WindDict,
        master=masterAGS,
        dataList=agsList,
        lookUpDict=lookUpDict,
        populationData=population,
    )

    BiomassTotal = calc_sum(BiomassDict)
    WasserTotal = calc_sum(WasserDict)
    WindTotal = calc_sum(WindDict)
    PvTotal = calc_sum(pv_dict)

    totalDict = fuseDicts(
        [pv_dict, WindDict, BiomassDict, WasserDict], masterList=masterAGS
    )

    aggregateDict(totalDict)

    sortedAgsList = dictToSortedList(totalDict)

    with open("2018.csv", "w", newline="") as renewable_energy:
        renewable_energy.write("ags,pv,wind_on,biomass,water\n")
        writer = csv.writer(renewable_energy)

        writer.writerow(["DG000000", PvTotal, WindTotal, BiomassTotal, WasserTotal])

        for agsAndPowerValueRow in sortedAgsList:
            writer.writerow(agsAndPowerValueRow)


main()
