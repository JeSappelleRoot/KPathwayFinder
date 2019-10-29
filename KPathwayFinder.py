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
        # Parse result in a dictionnary format
        dictResult = pwSearch.parse(result)
        # Define a default value
        #defaultValue = 'NA'

        # If name exist as a key in dict 
        # KEGG parser give a list for the name
        # Assume that the first name is the good one
        if 'NAME' in dictResult.keys():
            name = dictResult['NAME'][0]
        else:
            # else name get defaultValue
            name = 'NONAME'

        # If class exist as a key in the dict    
        if 'CLASS' in dictResult.keys():
            pwClass = dictResult['CLASS']
        # Else class get the defaultValue
        else:
            pwClass = 'NOCLASS'

    # Finally format the pathway string
    pwFormat = f"{pathwayCode};{name};{pwClass}"

    return pwFormat


def getInfo(enzyme):
# Function to get info about specific enzyme

    print(f"[+] Searching for {enzyme} enzyme")

    # Initialize KEGG searcher
    keggSearch = KEGG()
    # List of ignored pathway if needed
    # Can be empty but don't remove it
    ignoredPathWay = ['ko01100']

    # Get result from search
    result = keggSearch.get(enzyme)
    # If Kegg return only an int, the code is incorrect or pathway does'nt exist (?)
    if type(result) is int:
        return False

    else:
        # Parse result in a dictionnary format
        dictResult = keggSearch.parse(result)
        # Define a defaultValue if a value is missing
        defaultValue = 'NA'
        # Initialize a list
        prefixList = ['']

        # Add enzyme name to prefix in a list
        
        prefixList.append(enzyme)
        
        # If name exist as a dict key
        # KEGG parser give a list for the name
        # Assume that the first name is the good one
        if 'NAME' in dictResult.keys():
            prefixList.append(dictResult['NAME'][0])
        # Else set name with the default value
        else:
            prefixList.append('NONAME')

        # If definition exist as a dict key
        if 'DEFINITION' in dictResult.keys():
            prefixList.append(dictResult['DEFINITION'])
        # Else set default value instead
        else:
            prefixList.append('NODEFINITION')
        
        # Finally build prefix as a string, separated by ,
        prefixStr = ';'.join(prefixList)
        
        # Get ko pathways from dict
        koReferences = list(dictResult['PATHWAY'].keys())
        finalList = []

#
# ------------------ Loop to add ko pathways
#
        # If pathways exist
        if koReferences:
            # Loop to get each pathway ko code
            for ko in koReferences:
                # Ignore 'Metabolic Pathway', don't make any sense !
                if ko not in ignoredPathWay:
                    print(f"  [-] Need information about {ko} pathway")
                    # Call formatPathway function
                    suffixStr = formatPathway(ko)
                    finalStr = f"{prefixStr} > {suffixStr}"
                    finalList.append(finalStr)
                else:
                    print(f"  [!] Ignored pathway : {ko}")

        # Else if pathways are missing           
        else:
            finalStr = f"{prefixStr} > NOPATHWAY"
            finalList.append(finalStr)


    return finalList




# -------------------- main --------------------

# List of gene from file, in a list
with open(r'/home/scratch/Downloads/source.txt', 'r') as inputFile:

    inputList = inputFile.read().splitlines()


# Define headers of CSV file
#header = ['Entry', 'Definition', 'Pathway']
# File where write result
outputFile = r'/home/scratch/Downloads/result.txt'
masterList = []

for enzyme in inputList:
    for entry in getInfo(enzyme):
        masterList.append(entry)
        print(f"-   {entry}")


#formatPathway('ko01100')



