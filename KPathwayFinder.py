from bioservices.kegg import KEGG




def enzymeInfo(code):


    kSearch = KEGG()
    ignoredPathway = ['ko01100']

    result = kSearch.get(code)
    dictResult = kSearch.parse(result)
    
    pathwayList = list(dictResult['PATHWAY'].keys())
    

    # Create prefix list, info about enzyme herself
    prefixList = []
    prefixList.append(code)

    if 'NAME' in dictResult.keys():
        prefixList.append(dictResult['NAME'])
    else:
        prefixList.append('NONAME')

    if 'DEFINITION' in dictResult.keys():
        prefixList.append(dictResult['DEFINITION'])
    else:
        prefixList.append('NODEFINITION')


    # Create suffixList, tempList and finalList
    tempList = []
    finalList = []

    for pathway in pathwayList:
        if pathway not in ignoredPathway:
            suffixList = pathwayInfo(pathway)


        tempList = prefixList + suffixList
        finalList.append(tempList)

    
    return finalList


def pathwayInfo(code):

    kSearcher = KEGG()
    result = kSearcher.get(code)
    dictResult = kSearcher.parse(result)

    pathwayList = []

    pathwayList.append(code)
    if 'NAME' in dictResult.keys():
        pathwayList.append(dictResult['NAME'][0])
    else:
        pathwayList.append('NONAME')

    if 'CLASS' in dictResult.keys():
        pathwayList.append(dictResult['CLASS'])
    else:
        pathwayList.append('NOCLASS')


    return pathwayList












source = r'/home/scratch/Downloads/source.txt'


enzymeList = []
sourceList = ['K00001', 'K00002', 'K00003']
for enzyme in sourceList:
    enzymeList.append(enzymeInfo(enzyme))


