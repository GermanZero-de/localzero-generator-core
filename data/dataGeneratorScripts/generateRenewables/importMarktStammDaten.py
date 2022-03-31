from collections import defaultdict
import csv
from lxml import etree
import os
import re
import json


cutoffdate="31.12.2018"

# this is only used in the handling of "not 2018"-ags keys 
# this is not used in the xml parsing so far

exceptionDict={
"09478444":"Neuensorger Forst ist ein gemeindefreies gebiet",
"01053105":"Sachsenwald ist ein gemeindefreies Gebiet",
"06435200":"Gutsbezirk Spessart ist ist ein gemeindefreies Gebiet",
"01060014":"BuchholzerForstist ist ein gemeindefreies Gebiet",
"09572444":"Gdefr. Geb. (Lkr Erlangen-Höchstadt) ist ein gemeindefreies Gebiet",
"03155501":"Solling (Landkreis Northeim) ist ein gemeindefreies Gebiet",
"03153504":"Harz (Landkreis Goslar), gemfr. Gebiet ist ein gemeindefreies Gebiet"}



def parseElem(elem,tags:list[str]) -> list:
    returnList = [None]*len(tags)
    for subelem in elem:
        print(subelem.tag+"   "+subelem.text)
        for i,tag in enumerate(tags):
            if subelem.tag == tag:
                returnList[i] = subelem.text           
    return returnList
        
def parseXML(path:str,*, useinputDict = False, inputDict = defaultdict(float) ,printInfo:bool=False, printExit:bool=False) -> defaultdict:
    """This parses the XML file under path and returns a dict formated list {key: power | ags keys in xml}
    Right now we also filter out some entries due to some specifications like the installation date.
    There are just a few entries (<10) in the xml that do not ags keys. ATM we disregard those.  
    """
    returnDict = defaultdict(float)
    if useinputDict:
        returnDict=inputDict
    with open(path,"r", encoding='utf-16') as file: 

        tree = etree.parse(file, parser = etree.XMLParser())
        root = tree.getroot()

        noAgsCount = 0
        noPowerCount = 0
        noDate = 0 
        for elem in root:           
            [ags,netpower,date,enddate,status] = parseElem(elem,["Gemeindeschluessel","Nettonennleistung","Inbetriebnahmedatum","DatumEndgueltigeStilllegung","EinheitBetriebsstatus"])
            
            #Betriebsstatus
            # 35 -> In Betrieb, 31 -> In Planung, 37 -> Vorübergehend stillgelegt, 38 -> Endgültig stillgelegt
            if status == "31": #filter out "in Planung"
                continue

            if enddate is not None and int(enddate[:4]) < 2019:    #filter out "stillgelegt vor 2019"
                continue                

            if date is None:
                noDate += 1 
            elif int(date[:4])>2018: #filter out "in Betrieb gegangen nach ende 2018"
                continue

            if ags is None:
                noAgsCount += 1
            elif netpower is None:
                noPowerCount +=1
            else:   
                returnDict[ags] += float(netpower)   
        
        if printInfo:
            print("In "+path+": No AGS Count: "+str(noPowerCount)+", No power Count: "+str(noPowerCount)+", No Date: "+str(noDate))
        if printExit:
            print("parsed "+path)
       
    return returnDict

def parsemultiXML(basepath,numberOfFiles,*,printExit=False,printInfo=False):
    """We need this as the data for one Energieträger (Pv) is stored in multiple XML files."""
    pvDict = defaultdict(float)
    for i in range(1,numberOfFiles+1):
        pvDict = parseXML(basepath+"_"+str(i)+".xml",useinputDict=True,inputDict=pvDict,printInfo=printInfo,printExit=printExit)

    return pvDict

def loadMaster(path) -> list:
    """This loads the master.csv file and returns a list of all ags keys."""
    masterAGS = []
    with open(path,"r") as master:
        masterR = csv.reader(master,delimiter=',')
        _= next(masterR) # remove header
        for entry in masterR:
            masterAGS.append(entry[0]) 
    return masterAGS


def loadPopulation(path) -> dict:
    """This loads the 2018.csv population file that contains a list of all ags keys with their population."""
    population = dict()
    with open(path,"r") as populationFile:
        populationFileR = csv.reader(populationFile,delimiter=',')

        _= next(populationFileR) # remove header
        for entry in populationFileR:
            population[entry[0]]= entry[1] 
    return population


def calcSum(inDict:defaultdict) -> float:
    """This calculates sums over all values of the input dict"""
    sum = 0 
    for value in inDict.values():
        sum+=value
    return sum

def handleNotInMaster(indict:defaultdict,master:list,dataList,lookUpDict,populationData:dict,*,printDetails:bool=False):
    """
    This deals with all ags entries in indict that are not contained in the master list. It adds the power values of the missing ags keys to their 
     successors or predecessors.

     So far the powers are distributes over sevreal ags keys proportional to their population. 
     The EE-unit is disregarded/deleted if the ags corresponds to a gemeindefreie Gebiet.
     """
    notInMaster = set()
    for key in indict.keys():
        if key not in master:
            notInMaster.add(key)

    for ags in notInMaster:
        newAGSnotinMaster = False
        if printDetails : print("handling ags "+ags)
        
        changedAgsList = lookUpAGSinRepo(ags,lookUpDict=lookUpDict,repo=dataList,printDetails=printDetails)

        if changedAgsList == []: # this happens if the ags key is a gemeindefreies Gebiet and the ags key occurs in the exception list
            if printDetails:
                print(str(ags) + "ags key not in master")
                print(str(indict[ags]) + "power lost")
            del indict[ags] 
            continue

        if printDetails : print("ags in changed AGS List"+str(changedAgsList))

        for agsKey in changedAgsList: 
            if agsKey not in master: # this happens if the new ags key is a gemeindefreies Gebiet and the ags key occurs in the exception list
                 if printDetails: print(str(agsKey) + " new Ags not in master")
                 if agsKey in exceptionDict:
                    if printDetails: 
                        print(exceptionDict[agsKey])
                        print(str(indict[ags]) + " power lost")
                    newAGSnotinMaster = True
                 else:
                    exit(1)

        if newAGSnotinMaster:
            continue

        populationSum = sum(float(populationData[agsKey]) for agsKey in changedAgsList)
        power = float(indict[ags])

        for agsKey in changedAgsList:
            populationinchangedAGS = float(populationData[agsKey])
            indict[agsKey] += power * (populationinchangedAGS/populationSum)
            
    return indict

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
    #TODO: Check if this handles all cases correctly or if we could do better easily.
    with open(repoPath,"r",encoding="utf-8") as repo:
        agsList = json.loads(repo.read())
    dataList = agsList["daten"]
    agsLookUpDict = defaultdict(list)
    for (i,data) in enumerate(dataList):
        for ii,elem in enumerate(data):
            #print(elem)
            if elem == None: continue
            if re.match(r"[0-9]{8}",elem):
                agsLookUpDict[elem].append([i,ii])
    return agsList,agsLookUpDict

def lookUpAGSinRepo(ags:str,lookUpDict,repo,*,printDetails:bool=False) -> list[str]:
    """
    This looks up an ags and returns a list of all ags keys that are either predecessors or successors of the key. 
    """
    #TODO: Check if this deals with all cases correctly.

    agsReturnList = []
    dataList = repo["daten"]    
    vorkommnisse = lookUpDict[ags]

    agsAsPredecessor = []
    agsAsSuccessor = []


    for elem in vorkommnisse:
        if elem[1] == 1: # the ags key is at the predecessor position in the data
            agsAsPredecessor.append(dataList[elem[0]])

        elif elem[1] == 6: # the ags key is at the successor position in the data
            agsAsSuccessor.append(dataList[elem[0]])
        else:
            print("This should not happen. Check if the repository is prvoded in the following form:\n [code,predecessorAGS,name,validFrom,changeType,validUntil,successorAGS,successorName,successorAGSValidFrom,descritpion]")
            exit(1)
    
    if len(agsAsPredecessor) > 0:
        
        for elem in agsAsPredecessor:

            [code,predecessorAGS,name,validFrom,changeType,validUntil,successorAGS,successorName,successorAGSValidFrom,descritpion] = elem
            if successorAGS != None:
                if printDetails: print(successorAGS +" ags as predeccessor date " + successorAGSValidFrom)
                if(int(successorAGSValidFrom[-4:]) <= int(cutoffdate[-4:])):
                    if successorAGS != ags:
                        agsReturnList.append(successorAGS)

    if len(agsAsSuccessor) > 0:
        for elem in agsAsSuccessor:
            [code,predecessorAGS,name,validFrom,changeType,validUntil,successorAGS,successorName,successorAGSValidFrom,descritpion] = elem
            if printDetails: print(predecessorAGS+" ags as successor date " + successorAGSValidFrom)
            if(int(successorAGSValidFrom[-4:]) > int(cutoffdate[-4:])):
                if predecessorAGS != ags:
                    agsReturnList.append(predecessorAGS)
            
    if len(agsReturnList) == 0:
        if ags in exceptionDict:
            if printDetails: print(exceptionDict[ags])
        else:
            print("apperatently you did not handle all cases for " + ags)
            exit(1)

    return agsReturnList

def saveDict(indict:dict,name:str):
    if not os.path.exists("xmlZwischenspeicher"):
        os.makedirs("xmlZwischenspeicher")

    with open("xmlZwischenspeicher/"+name+".json","w") as file:
        json.dump(indict,file)

def loadDictFromJson(name:str):
    returnDict = defaultdict(float)
    with open("xmlZwischenspeicher/"+name+".json","r") as file:
        returnDict = defaultdict(float,json.loads(file.read()))
    return returnDict

def fuseDicts(indictList:list[defaultdict],masterList) -> dict:
    returnDict = {}
    for ags in masterList:
        returnDict[ags]= [indict[ags] for indict in indictList]
    return returnDict

def aggregateDict(indict:dict):
    """aggregates the input dict and creates sums for all state and district ags keys."""
    def addLists(list1:list[float],list2:list[float]) -> list[float]:
        if list1 == []:
            return list2
        if list2 == []:
            return list1
        return [list1[i]+list2[i] for i,_ in enumerate(list2)]

    sumoverDistr = defaultdict(list[float])
    sumoverState = defaultdict(list[float])
    for ags,powerList in indict.items():
        ags_sta = ags[:2] + "000000"
        ags_dis = ags[:5] + "000"
        sumoverDistr[ags_dis] = addLists(sumoverDistr[ags_dis],powerList) 
        sumoverState[ags_sta] = addLists(sumoverState[ags_sta],powerList) 

    for key,val in sumoverDistr.items():
        indict[key] = val

    for key,val in sumoverState.items():
        indict[key] = val

def dictToSortedList(indict:dict)->list:
    returnList = []
    for ags, powers in indict.items():
        returnList.append([ags,*powers])

    returnList.sort(key = lambda x: int(x[0])) # sort by ags keys

    return returnList


def main ():

    reloadfromXML:bool = False

    PvDict = defaultdict(float)
    BiomassDict = defaultdict(float)
    WasserDict = defaultdict(float)
    WindDict = defaultdict(float)

    if reloadfromXML:
        PvDict = parsemultiXML("Xml/EinheitenSolar",24,printExit=True,printInfo=True)
        BiomassDict = parseXML("Xml/EinheitenBiomasse.xml",printExit=True,printInfo=True)
        WasserDict = parseXML("Xml/EinheitenWasser.xml",printExit=True,printInfo=True)
        WindDict = parseXML("Xml/EinheitenWind.xml",printExit=True,printInfo=True)

        saveDict(PvDict,"pvDict")
        saveDict(BiomassDict,"biomassDict")
        saveDict(WindDict,"windDict")
        saveDict(WasserDict,"wasserDict")
    else:
        PvDict = loadDictFromJson("pvDict")
        BiomassDict = loadDictFromJson("biomassDict")
        WasserDict = loadDictFromJson("wasserDict")
        WindDict = loadDictFromJson("windDict")  
    
    masterAGS = loadMaster("Master2018/master.csv")
    population = loadPopulation("population/2018.csv")

    [agsList,lookUpDict] = loadAGSRepo("Xrepo/xrepo.json") 

    BiomassDict = handleNotInMaster(BiomassDict,master=masterAGS,dataList=agsList,lookUpDict=lookUpDict,populationData = population)
    PvDict = handleNotInMaster(PvDict,master=masterAGS,dataList=agsList,lookUpDict=lookUpDict,populationData = population)
    WasserDict = handleNotInMaster(WasserDict,master=masterAGS,dataList=agsList,lookUpDict=lookUpDict,populationData = population)
    WindDict =  handleNotInMaster(WindDict,master=masterAGS,dataList=agsList,lookUpDict=lookUpDict,populationData = population)

    BiomassTotal = calcSum(BiomassDict)
    WasserTotal = calcSum(WasserDict)
    WindTotal = calcSum(WindDict)
    PvTotal = calcSum(PvDict)

    totalDict = fuseDicts([PvDict,WindDict,BiomassDict,WasserDict],masterList=masterAGS)

    aggregateDict(totalDict)

    sortedAgsList = dictToSortedList(totalDict)

    with open("2018.csv","w",newline="") as renewable_energy:
        renewable_energy.write("ags,pv,wind_on,biomass,water\n")
        writer = csv.writer(renewable_energy)

        writer.writerow(['DG000000',PvTotal,WindTotal,BiomassTotal,WasserTotal]) 
        
        for agsAndPowerValueRow in sortedAgsList:
            writer.writerow(agsAndPowerValueRow)

main()





