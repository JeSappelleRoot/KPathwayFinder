from bioservices.kegg import KEGG
import csv
import requests


def formatPathway(pathwayCode):
# Function to format properly pathways from KEGG
# Get ko code, name and class

    # Initialize KEGG searcher
    pwSearch = KEGG()

    # Get answer
    result = pwSearch.get(pathwayCode)

    # If Kegg return only an int, the code is incorrect or pathway does'nt exist (?)
    if type(result) is int:
        pwFormat = False
    else:
        # Parse result in a dictionnary
        dictResult = pwSearch.parse(result)
        # Define a default value
        defaultValue = 'NA'

        # If name exist as a key in dict 
        # KEGG parser give a list for the name
        # Assume that the first name is the good one
        if 'NAME' in dictResult.keys():
            name = dictResult['NAME'][0]
        else:
            # else name get defaultValue
            name = defaultValue

        # If class exist as a key in the dict    
        if 'CLASS' in dictResult.keys():
            pwClass = dictResult['CLASS']
        # Else class get the defaultValue
        else:
            pwClass = defaultValue

    # Finally format the pathway string
    pwFormat = f"{pathwayCode};{name};{pwClass}"
    print(pwFormat)

    return pwFormat


def getInfo(gene):

    keggSearch = KEGG()
    ignoredPathWay = ['ko01100']


    result = keggSearch.get(gene)
    if type(result) is int:
        return False

    else:

        dictResult = keggSearch.parse(result)
        defaultValue = 'NA'
        resultList = []

        koReferences = list(dictResult['PATHWAY'].keys())
        for ko in koReferences:
            # Ignore 'Metabolic Pathway', don't make any sense !
            if ko not in ignoredPathWay:
                formatPathway(ko)



    return resultList




# -------------------- main --------------------

# List of gene from file, in a list
#with open(r'/home/scratch/Downloads/source.txt', 'r') as inputFile:

    #inputList = inputFile.read().splitlines()


# Define headers of CSV file
#header = ['Entry', 'Definition', 'Pathway']
# File where write result
outputFile = r'/home/scratch/Downloads/result.txt'

getInfo('K00010')

#formatPathway('ko01100')

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


