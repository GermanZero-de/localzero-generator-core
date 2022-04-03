from collections import defaultdict
import csv
from dataclasses import dataclass
from tkinter.ttk import Separator
from lxml import etree
import os
import re
import json

class Date():

    @dataclass
    class Year():
        year:int
        def __gt__(self,other) -> bool:
            returnBool:bool = False
            if self.year > other.year:
                returnBool = True
            return returnBool
        
        def __lt__(self,other) -> bool:
            returnBool:bool = False
            if self.year < other.year:
                returnBool = True

            return returnBool
        
        def __eq__(self,other) -> bool:
            returnBool:bool = False
            if self.year == other.year:
                returnBool = True
            return returnBool

        def __ge__(self,other) -> bool:
            return self > other or self == other

        def __le__(self,other) -> bool:
            return self < other or self == other


    @dataclass
    class Month():
        month:int
        def __gt__(self,other) -> bool:
            returnBool:bool = False
            if self.month > other.month:
                returnBool = True
            return returnBool
        
        def __lt__(self,other) -> bool:
            returnBool:bool = False
            if self.month < other.month:
                returnBool = True

            return returnBool
        
        def __eq__(self,other) -> bool:
            returnBool:bool = False
            if self.month == other.month:
                returnBool = True
            return returnBool

        def __ge__(self,other) -> bool:
            return self > other or self == other

        def __le__(self,other) -> bool:
            return self < other or self == other

    @dataclass
    class Day():
        day:int
        def __gt__(self,other) -> bool:
            returnBool:bool = False
            if self.day > other.day:
                returnBool = True
            return returnBool
        
        def __lt__(self,other) -> bool:
            returnBool:bool = False
            if self.day < other.day:
                returnBool = True

            return returnBool
        
        def __eq__(self,other) -> bool:
            returnBool:bool = False
            if self.day == other.day:
                returnBool = True
            return returnBool
        
        def __ge__(self,other) -> bool:
            return self > other or self == other

        def __le__(self,other) -> bool:
            return self < other or self == other

    year:Year
    month:Month
    day:Day

    def __init__(self,year,month,day):
        self.year = self.Year(year=year)
        self.month = self.Month(month=month)
        self.day = self.Day(day=day)

    @classmethod
    def parse_day_month_year(cls,inputdate:str,separator:str="."):
        [day,month,year] = inputdate.split(separator)
        return cls(int(year),int(month),int(day))

    @classmethod
    def parse_year_month_day(cls,inputdate:str,separator:str="-"):
        [year,month,day] = inputdate.split(separator)
        return cls(int(year),int(month),int(day))

    def __gt__(self,other) -> bool:
        returnBool:bool = False

        if self.year > other.year:
            returnBool = True

        elif self.year == other.year:
            if self.month > other.month:
                returnBool = True
            elif self.month == other.month:
                if self.day > other.day:
                    returnBool = True

        return returnBool
    
    def __lt__(self,other) -> bool:
        returnBool:bool = False

        if self.year < other.year:
            returnBool = True

        elif self.year == other.year:
            if self.month < other.month:
                returnBool = True
            elif self.month == other.month:
                if self.day < other.day:
                    returnBool = True

        return returnBool
    
    def __eq__(self,other) -> bool:
        returnBool:bool = False
        if self.year == other.year and self.month == other.month and self.day == other.day:
            returnBool = True
        return returnBool
    
    def __ge__(self,other) -> bool:
        return self > other or self == other

    def __le__(self,other) -> bool:
        return self < other or self == other
    
    

CUTOFFDATE = "31.12.2018"
cut_off_date:Date = Date.parse_day_month_year(CUTOFFDATE)


EXCEPTION_DICT = {
    "09478444": "Neuensorger Forst ist ein gemeindefreies gebiet",
    "01053105": "Sachsenwald ist ein gemeindefreies Gebiet",
    "06435200": "Gutsbezirk Spessart ist ist ein gemeindefreies Gebiet",
    "01060014": "BuchholzerForstist ist ein gemeindefreies Gebiet",
    "09572444": "Gdefr. Geb. (Lkr Erlangen-Höchstadt) ist ein gemeindefreies Gebiet",
    "03155501": "Solling (Landkreis Northeim) ist ein gemeindefreies Gebiet",
    "03153504": "Harz (Landkreis Goslar), gemfr. Gebiet ist ein gemeindefreies Gebiet",
}


def parse_elem(elem, tags: list[str]) -> list:
    return_list = [None] * len(tags)
    for subelem in elem:
        print(subelem.tag + "   " + subelem.text)
        for i, tag in enumerate(tags):
            if subelem.tag == tag:
                return_list[i] = subelem.text
    return return_list


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
            [ags, netpower, start_date_string, end_date_string, status,temp_shut_down_date_string,reactivation_date_string] = parse_elem(
                elem,
                [
                    "Gemeindeschluessel",
                    "Nettonennleistung",
                    "Inbetriebnahmedatum",
                    "DatumEndgueltigeStilllegung",
                    "EinheitBetriebsstatus",
                    "DatumBeginnVoruebergehendeStilllegung",
                    "DatumWiederaufnahmeBetrieb"
                ],
            )

            # Betriebsstatus
            # 35 -> In Betrieb, 31 -> In Planung, 37 -> Vorübergehend stillgelegt, 38 -> Endgültig stillgelegt
            if status == "31":  # filter out "in Planung"
                continue

            if end_date_string != None:
                end_date = Date.parse_year_month_day(end_date_string)
                if end_date < cut_off_date: # die Einheit wurde vor unserem Cutt-Off Datum stillgelegt
                    continue

            if start_date_string != None:
                start_date = Date.parse_year_month_day(start_date_string)
                if start_date > cut_off_date:  # filter out "in Betrieb gegangen nach ende 2018"
                    continue
            else: 
                no_date += 1
            
            if temp_shut_down_date_string != None:
                temp_shut_down_date = Date.parse_year_month_day(temp_shut_down_date_string)
                if temp_shut_down_date < cut_off_date:
                    # die Einheit wurde vor dem Cut-Off Datum temporär stillgelegt
                    if reactivation_date_string != None:
                        reactivation_date = Date.parse_year_month_day(reactivation_date_string)
                        if reactivation_date > cut_off_date:
                            # Die Einheit wurde nach dem Cut-Off Datum reaktiviert -> rausfiltern
                            continue
                    else:
                        # Die Einheit wurde bisher nicht reaktiviert (es gibt kein Wiederaufnahme Datum) -> rausfiltern
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
    data_list,
    look_up_dict,
    population_dict: dict,
    *,
    print_details: bool = False,
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
        if print_details:
            print("handling ags " + ags)

        changedAgsList = lookUpAGSinRepo(
            ags, look_up_dict=look_up_dict, repo=data_list, print_details=print_details
        )

        if (
            changedAgsList == []
        ):  # this happens if the ags key is a gemeindefreies Gebiet and the ags key occurs in the exception list
            if print_details:
                print(str(ags) + "ags key not in master")
                print(str(input_dict[ags]) + "power lost")
            del input_dict[ags]
            continue

        if print_details:
            print("ags in changed AGS List" + str(changedAgsList))

        for agsKey in changedAgsList:
            if (
                agsKey not in master
            ):  # this happens if the new ags key is a gemeindefreies Gebiet and the ags key occurs in the exception list
                if print_details:
                    print(str(agsKey) + " new Ags not in master")
                if agsKey in EXCEPTION_DICT:
                    if print_details:
                        print(EXCEPTION_DICT[agsKey])
                        print(str(input_dict[ags]) + " power lost")
                    newAGSnotinMaster = True
                else:
                    exit(1)

        if newAGSnotinMaster:
            continue

        populationSum = sum(float(population_dict[agsKey]) for agsKey in changedAgsList)
        power = float(input_dict[ags])

        for agsKey in changedAgsList:
            populationinchangedAGS = float(population_dict[agsKey])
            input_dict[agsKey] += power * (populationinchangedAGS / populationSum)

    return input_dict


def load_ags_repo(repoPath):
    """This loads the json from https://www.xrepository.de/api/xrepository/urn:xoev-de:bund:destatis:bevoelkerungsstatistik:codeliste:ags.historie_2021-12-31/download/Destatis.AGS.Historie_2021-12-31.json
    to a dict "agsList" and creates a lookup dict "look_up_dict" that saves all contained ags keys with the indices, where they appear in agsList
    [code,predecessor_ags,name,valid_from,change_type,valid_until,successor_ags,successor_name,successor_ags_valid_from,descritpion] with
    the following description
    - code - Code
    - predecessor_ags - AGS
    - name - Gemeindenamen mit Zusatz
    - valid_from - gueltig ab
    - change_type - Aenderungsart
    - valid_until - gueltig bis
    - successor_ags - AGS des Nachfolgers
    - successor_name - Name des Nachfolgers
    - successor_ags_valid_from - Nachfolger gueltig ab
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
    data_list = agsList["daten"]
    agsLookUpDict = defaultdict(list)
    for (i, data) in enumerate(data_list):
        for ii, elem in enumerate(data):
            # print(elem)
            if elem == None:
                continue
            if re.match(r"[0-9]{8}", elem):
                agsLookUpDict[elem].append([i, ii])
    return agsList, agsLookUpDict


def lookUpAGSinRepo(
    ags: str, look_up_dict, repo, *, print_details: bool = False
) -> list[str]:
    """
    This looks up an ags and returns a list of all ags keys that are either predecessors or successors of the key.
    """
    # TODO: Check if this deals with all cases correctly.

    ags_return_list = []
    data_list = repo["daten"]
    vorkommnisse = look_up_dict[ags]

    ags_as_predecessor = []
    ags_as_successor = []

    for elem in vorkommnisse:
        if elem[1] == 1:  # the ags key is at the predecessor position in the data
            ags_as_predecessor.append(data_list[elem[0]])

        elif elem[1] == 6:  # the ags key is at the successor position in the data
            ags_as_successor.append(data_list[elem[0]])
        else:
            print(
                "This should not happen. Check if the repository is prvoded in the following form:\n [code,predecessor_ags,name,valid_from,change_type,valid_until,successor_ags,successor_name,successor_ags_valid_from,descritpion]"
            )
            exit(1)

    if len(ags_as_predecessor) > 0:

        for elem in ags_as_predecessor:

            [
                code,
                predecessor_ags,
                name,
                valid_from,
                change_type,
                valid_until,
                successor_ags,
                successor_name,
                successor_ags_valid_from,
                descritpion,
            ] = elem
            if successor_ags != None:
                if print_details:
                    print(
                        successor_ags
                        + " ags as predeccessor date "
                        + successor_ags_valid_from
                    )
                successor_ags_valid_from_date = Date.parse_day_month_year(successor_ags_valid_from)     
                if successor_ags_valid_from_date <= cut_off_date:
                    if successor_ags != ags:
                        ags_return_list.append(successor_ags)

    if len(ags_as_successor) > 0:
        for elem in ags_as_successor:
            [
                code,
                predecessor_ags,
                name,
                valid_from,
                change_type,
                valid_until,
                successor_ags,
                successor_name,
                successor_ags_valid_from,
                descritpion,
            ] = elem
            if print_details:
                print(
                    predecessor_ags + " ags as successor date " + successor_ags_valid_from
                )
            successor_ags_valid_from_date =  Date.parse_day_month_year(successor_ags_valid_from)   
            if successor_ags_valid_from_date > cut_off_date:
                if predecessor_ags != ags:
                    ags_return_list.append(predecessor_ags)

    if len(ags_return_list) == 0:
        if ags in EXCEPTION_DICT:
            if print_details:
                print(EXCEPTION_DICT[ags])
        else:
            print("apperatently you did not handle all cases for " + ags)
            exit(1)

    return ags_return_list


def save_dict(input_dict: dict, name: str):
    if not os.path.exists("xmlZwischenspeicher"):
        os.makedirs("xmlZwischenspeicher")

    with open("xmlZwischenspeicher/" + name + ".json", "w") as file:
        json.dump(input_dict, file)


def load_dict_from_json(name: str):
    return_dict = defaultdict(float)
    with open("xmlZwischenspeicher/" + name + ".json", "r") as file:
        return_dict = defaultdict(float, json.loads(file.read()))
    return return_dict


def fuse_dicts(input_dict_list: list[defaultdict], master_ags_list) -> dict:
    return_dict = {}
    for ags in master_ags_list:
        return_dict[ags] = [input_dict[ags] for input_dict in input_dict_list]
    return return_dict


def aggregate_dict(input_dict: dict):
    """aggregates the input dict and creates sums for all state and district ags keys."""

    def addLists(list1: list[float], list2: list[float]) -> list[float]:
        if list1 == []:
            return list2
        if list2 == []:
            return list1
        return [list1[i] + list2[i] for i, _ in enumerate(list2)]

    sum_over_districts = defaultdict(list[float])
    sum_over_states = defaultdict(list[float])
    for ags, powers_list in input_dict.items():
        ags_sta = ags[:2] + "000000"
        ags_dis = ags[:5] + "000"
        sum_over_districts[ags_dis] = addLists(sum_over_districts[ags_dis], powers_list)
        sum_over_states[ags_sta] = addLists(sum_over_states[ags_sta], powers_list)

    for key, val in sum_over_districts.items():
        input_dict[key] = val

    for key, val in sum_over_states.items():
        input_dict[key] = val


def dict_to_sorted_list(input_dict: dict) -> list:
    return_list = []
    for ags, powers in input_dict.items():
        return_list.append([ags, *powers])

    return_list.sort(key=lambda x: int(x[0]))  # sort by ags keys

    return return_list


def main():

    reloadfromXML: bool = False

    pv_dict = defaultdict(float)
    biomass_dict = defaultdict(float)
    wasser_dict = defaultdict(float)
    wind_dict = defaultdict(float)

    if reloadfromXML:
        pv_dict = parse_multi_xml("Xml/EinheitenSolar", 24, print_exit=True, print_info=True)
        biomass_dict = parse_xml(
            "Xml/EinheitenBiomasse.xml", print_exit=True, print_info=True
        )
        wasser_dict = parse_xml("Xml/EinheitenWasser.xml", print_exit=True, print_info=True)
        wind_dict = parse_xml("Xml/EinheitenWind.xml", print_exit=True, print_info=True)

        save_dict(pv_dict, "pv_dict")
        save_dict(biomass_dict, "biomass_dict")
        save_dict(wind_dict, "wind_dict")
        save_dict(wasser_dict, "wasser_dict")
    else:
        pv_dict = load_dict_from_json("pv_dict")
        biomass_dict = load_dict_from_json("biomass_dict")
        wasser_dict = load_dict_from_json("wasser_dict")
        wind_dict = load_dict_from_json("wind_dict")

    master_ags_list = load_master("Master2018/master.csv")
    population_dict = load_population("population/2018.csv")

    [agsList, look_up_dict] = load_ags_repo("Xrepo/xrepo.json")

    biomass_dict = handle_not_in_master(
        biomass_dict,
        master=master_ags_list,
        data_list=agsList,
        look_up_dict=look_up_dict,
        population_dict=population_dict,
    )
    pv_dict = handle_not_in_master(
        pv_dict,
        master=master_ags_list,
        data_list=agsList,
        look_up_dict=look_up_dict,
        population_dict=population_dict,
    )
    wasser_dict = handle_not_in_master(
        wasser_dict,
        master=master_ags_list,
        data_list=agsList,
        look_up_dict=look_up_dict,
        population_dict=population_dict,
    )
    wind_dict = handle_not_in_master(
        wind_dict,
        master=master_ags_list,
        data_list=agsList,
        look_up_dict=look_up_dict,
        population_dict=population_dict,
    )

    biomass_total = calc_sum(biomass_dict)
    wasser_total = calc_sum(wasser_dict)
    wind_total = calc_sum(wind_dict)
    pv_total = calc_sum(pv_dict)

    renewables_dict = fuse_dicts(
        [pv_dict, wind_dict, biomass_dict, wasser_dict], master_ags_list=master_ags_list
    )

    aggregate_dict(renewables_dict)

    sorted_ags_list = dict_to_sorted_list(renewables_dict)

    with open("2018.csv", "w", newline="") as renewable_energy:
        renewable_energy.write("ags,pv,wind_on,biomass,water\n")
        writer = csv.writer(renewable_energy)

        writer.writerow(["DG000000", pv_total, wind_total, biomass_total, wasser_total])

        for ags_and_power_value_row in sorted_ags_list:
            writer.writerow(ags_and_power_value_row)


main()
