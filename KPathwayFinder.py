from bioservices.kegg import KEGG
import csv
import requests



def getInfo(gene):

    keggSearch = KEGG()

    result = keggSearch.get(gene)
    if type(result) is int:
        return False

    else:

        dictResult = keggSearch.parse(result)
        defaultValue = 'EMPTY'
        resultList = []

        #print(dictResult['CLASS'])
        print(dictResult['PATHWAY'])

        resultList.append(gene)
        if dictResult['DEFINITION']:
            resultList.append(dictResult['DEFINITION'])
        else:
            print(f"[!] Missing definition for {gene}")
            resultList.append(defaultValue)

        if dictResult['PATHWAY']:
            resultList.append(dictResult['PATHWAY'])
        else:
            print(f"[!] Missing pathway for {gene}")
            resultList.append(emptyValue)

    return resultList




# -------------------- main --------------------

# List of gene from file, in a list
with open(r'/home/scratch/Downloads/source.txt', 'r') as inputFile:

    inputList = inputFile.read().splitlines()


# Define headers of CSV file
#header = ['Entry', 'Definition', 'Pathway']
# File where write result
outputFile = r'/home/scratch/Downloads/result.txt'

print(getInfo('K00010'))

"""
with open(outputFile,'w') as outputStream:
    fileWriter = csv.writer(outputStream, delimiter=',')

    for entry in inputList:
        
        print(f"[?] Searching about {entry}")
        result = getInfo(entry)

        if result is not False:
            print(f"[+] Write infos in {outputFile}\n")
            fileWriter.writerow(result)
        else:
            print(f"\n[!] Something wrong when trying to search {entry}")
            print(f"[!] This entry will be ignored\n")
            continue

    
"""


liste = ['toto']

