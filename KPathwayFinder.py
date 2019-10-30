import csv
import argparse
from os import path, sys
from bioservices.kegg import KEGG

def displayBanner():
# Function to add a simple banner in your boring dull terminal


    print(r"""


  _  _______      _   _                        ______ _           _           
 | |/ /  __ \    | | | |                      |  ____(_)         | |          
 | ' /| |__) |_ _| |_| |____      ____ _ _   _| |__   _ _ __   __| | ___ _ __ 
 |  < |  ___/ _` | __| '_ \ \ /\ / / _` | | | |  __| | | '_ \ / _` |/ _ \ '__|
 | . \| |  | (_| | |_| | | \ V  V / (_| | |_| | |    | | | | | (_| |  __/ |   
 |_|\_\_|   \__,_|\__|_| |_|\_/\_/ \__,_|\__, |_|    |_|_| |_|\__,_|\___|_|   
                                          __/ |                               
                                         |___/                                
                              
    """)


    return







def enzymeInfo(code, ignored,verbosity):
# Function to get info about an enzyme, from the code
# This function return a double list

    # Intialize KEGG searcher
    kSearch = KEGG(verbose=verbosity)



    # Get result and parse it in a dictionnary
    print(f"[+] Get info about enzyme {code}")


    
    result = kSearch.get(code)

    if type(result) is int:
        return False
    else:

        dictResult = kSearch.parse(result)
        
        # Get all pathways as keys in dictionnary
        pathwayList = list(dictResult['PATHWAY'].keys())
        

        # Create prefix list, info about enzyme herself
        prefixList = []

        # Add code at the begining of the list
        prefixList.append(code)

        # If name is present as key, else 'NONAME' insted
        if 'NAME' in dictResult.keys():
            prefixList.append(dictResult['NAME'])
        else:
            prefixList.append('NONAME')

        # If definition is present as key, else 'NODEFINITION' insted
        if 'DEFINITION' in dictResult.keys():
            prefixList.append(dictResult['DEFINITION'])
        else:
            prefixList.append('NODEFINITION')


        # Create final list, which contain : 
        # - prefix (info about enzyme) 
        # - suffix list (info about each enzyme's pathways)
        finalList = []

        for pathway in pathwayList:
            if pathway not in ignored:
                print(f"  [-] Get info about {pathway} pathway")
                suffixList = pathwayInfo(pathway)

                finalList.append(prefixList + suffixList)
                
            else:
                print(f"  [!] Ignored pathway : {pathway}")


            

        
        return finalList


# -------------------------------------------------------------------------------------------------


def pathwayInfo(code):
# Function to get info about a pathway, from the code

    # Symbol to separate enzyme properties (code, name, definition) to the pathway part
    # Used at the end, when formatting enzyme_properties, pathway1, pathway2, pathway3...pathwayN
    pathwaySeparator = '>'


    # Intialize searcher
    kSearcher = KEGG()
    # Get result and parse it in a dictionnary
    result = kSearcher.get(code)

    # Add code at the begining of the list
    dictResult = kSearcher.parse(result)


    # Initialize an empty list
    pathwayList = []

    # Add separator
    pathwayList.append(pathwaySeparator)

    # If name exist as a key in dictionnary, else 'NONAME' insted
    pathwayList.append(code)
    if 'NAME' in dictResult.keys():
        pathwayList.append(dictResult['NAME'][0])
    else:
        pathwayList.append('NONAME')

    # If class exist as a key in dictionnary, else 'NOCLASS' instead
    if 'CLASS' in dictResult.keys():
        pathwayList.append(dictResult['CLASS'])
    else:
        pathwayList.append('NOCLASS')


    return pathwayList


# -------------------------------------------------------------------------------------------------


def makeCSVHeader(n):
# Function to concantenate pathway to make a CSV header file
    print(f"\n[+] Prepare CSV header for maximum {n} pathway\n")
    # Define a prefix for the enzyme (code, name and definition)
    headerPrefix = 'enzyme_code,enzyme_name,enzyme_definition'
    # Empty header suffix
    headerSuffix = ''
    # Loop to concatenate header about N pathway (code, name and class)
    for i in range(n):
        headerSuffix = headerSuffix + (f"pathway{i + 1}_code,pathway{i + 1}_name,pathway{i + 1}_class,")

    # Format the final header
    csvHeader = f"{headerPrefix},{headerSuffix}"

    return csvHeader



# -------------------------------------------------------------------------------------------------
# --------------------------------------------- Main ----------------------------------------------
# -------------------------------------------------------------------------------------------------

# Initialize a parser for command line
parser = argparse.ArgumentParser(

formatter_class=argparse.RawDescriptionHelpFormatter,
# Add a brief description
description="""
KPathwayFinder is designed : \n
-from enzyme code (e.g K00001) get all pathways
-recover info about enzyme (code, name, definition)
-recover information about each pathway (code, name, class)
-concatenate each pathway for each enzyme (enzyme1 : pathway1, pathway2, pathway3...)
"""
)

# Add arguments for command lin
parser.add_argument('--input', help='The input file, which contain enzyme codes', required=True)
parser.add_argument('--output', help='The output file, in CSV style (comma separated)', required=True)
parser.add_argument('-v', help='Increase verbosity', action='store_true', default=False)

# With a banner, it's always better ! 
displayBanner()

# If number of arguments = 1, print help and exit
if len(sys.argv) == 1:
    parser.print_help()
    sys.exit()

# Parse arguments
args = parser.parse_args()

# Set input/output file argument
inputFile = args.input
outputFile = args.output
# Set verbosity argument, used by KEGG() object
v = args.v

# Check if input file exist
if not path.isfile(inputFile):
    print(f"[!] Input file doesn't exist, check your path : ")
    print(f"{inputFile}")
    exit()

# Check if output file is not a existant directory
elif path.isdir(outputFile):
    print(f"[!] Output file is not valid, it refer to an existant directory : ")
    print(f"{outputFile}")
    exit()   


#
# Begining of the script
#


#############################################################
#MODIFY THIS VALUE TO IGNORE SPECIFIC PATHWAY (CAN BE EMPTY)#
# List with ignored pathways                                #
ignoredPathway = ['ko01100']                                #
#                                                           #
#############################################################



# Read input file with .read().splitlines to avoid \n at end of each lines
with open(inputFile, 'r') as fileStream:
    sourceList = fileStream.read().splitlines()

# Initialize the main list, wich contains other list about enzyme + pathways
enzymeList = []

#
# Main loop to get all required info about combo enzyme + pathway N
#
for enzyme in sourceList:
    # Get info about the enzyme
    aboutEnzyme = enzymeInfo(enzyme, ignoredPathway, v)
    # If the function return False, the KEGG request is not valid and pass at the other enzyme
    if aboutEnzyme == False:
        print(f"[!] Something wrong happened with enzyme {enzyme} (skipped)\n")
        pass
    else:
        # Else, for each list return by the function, add these in the main list
        for liste in aboutEnzyme:
            enzymeList.append(liste)


#
# Formating the main list enzymeList (double list)
#

# Initialize an empty list for each combo enzyme1 + pathwayN
# Which contains only the enzyme code
codeList = []
for individualList in enzymeList:
    codeList.append(individualList[0])

# Get the maximum code occurence
codeMax = max(codeList,key=codeList.count)

# Get the number of the code in the codeList
nbMaxOccurence = codeList.count(codeMax)

# Create the header of the CSV file, with dedicated function
# - 1 because codeMax include the enzyme code itsel (enzyme + pathwayN)
# Need only the number of pathway (represented by a line in the list)
csvHeader = makeCSVHeader(nbMaxOccurence)
# Remove last comma
csvHeader = csvHeader[:-1]

#
# Concatenate each pathway with the relative enzyme
#

# Define the last list, which contain [[enzyme], [pathway1], [pathway2], [pathwayN]] 
masterList = []
# Loop on the code gived by the input file
for code in sourceList:
    print(f"[+] Merging pathways from {code} enzyme")
    # Initialize a list with a empty value on index 0
    tmpList = ['']
    # Loop on list in the double list enzymeList
    for liste in enzymeList:
        # If enzyme code from file and enzyme code from double list match
        if liste[0] == code:
            # Get the index of the separator symbol
            sepPosition = liste.index('>')
            # First position of list always take from the begining to the separator symbol 
            tmpList[0] = liste[0:sepPosition]
            # And always add successively from the separator symbol to the end of the line
            tmpList.append(liste[sepPosition + 1:])
    # Add the temp list to the final master list
    masterList.append(tmpList)


#
# Write in file in CSV style (comma separated)
#

# With open statement to write into output file
with open(output, 'w') as fileStream:
    # Specify CSV delimiter file
    writer = csv.writer(fileStream, delimiter=',')
    # Write CSV header (with a split)
    writer.writerow(csvHeader.split(','))
    # For each list in masterList, remove sub lists with sum
    # and write the entire line in CSV file
    for liste in masterList:
        writer.writerow(sum(liste,[]))

