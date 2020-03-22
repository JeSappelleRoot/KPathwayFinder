#!/bin/python3
import csv
import timeit
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








def enzymeInfo(code, ignored,stats, verbosity):
# Function to get info about an enzyme, from the code
# This function return a double list

    # Intialize KEGG searcher
    kSearch = KEGG(verbose=verbosity)

    # Get result and parse it in a dictionnary
    print(f"[+] Get info about enzyme {code}")
    result = kSearch.get(code)

    # If KEGG return an int, the enzyme code doesn't match in databases
    if type(result) is int:
        return False
    else:

        dictResult = kSearch.parse(result)

        # Create prefix list, info about enzyme herself
        prefixList = []

        # Add code at the begining of the list
        prefixList.append(code)

        # If name is present as key, else 'NA' insted
        if 'NAME' in dictResult.keys():
            #prefixList.append(dictResult['NAME'])
            # Convert names from list into a string
            # with strop '[]' part, and replace initial separator , by ;
            namesStr = str(dictResult['NAME']).strip("'[]'").replace(',',';')
            prefixList.append(namesStr)
        else:
            prefixList.append('NA')

        # If definition is present as key, else 'NA' insted
        if 'DEFINITION' in dictResult.keys():
            # If definition is a string comma separated, replace comma by semicolon
            # Fix to avoid wrong column formating at the end of the script
            definitionStr = str(dictResult['DEFINITION']).replace(',',';')
            prefixList.append(definitionStr)
        else:
            prefixList.append('NA')


        # If pathway exist as a key in result
        if 'PATHWAY' in dictResult.keys():

            # Get all pathways as keys in dictionnary
            pathwayList = list(dictResult['PATHWAY'].keys())



            # Create final list, which contain : 
            # - prefix (info about enzyme) 
            # - suffix list (info about each enzyme's pathways)
            finalList = []

            # Add suffix in final list
            finalList.append(prefixList)

            for pathway in pathwayList:
                # If pathway not in ignored list
                if pathway not in ignored:
                    print(f"  [-] Get info about {pathway} pathway")
                    suffixList = pathwayInfo(pathway)

                    # Add number of pathway for stats
                    stats['NB_PATHWAY'] = stats['NB_PATHWAY'] + 1

                    # Add suffix of pathway in final list
                    finalList.append(suffixList)

                # If enzyme have only 1 pathway and this pathway is in ignored list
                # Bad luck ! 
                elif len(pathwayList) == 1 and pathway in ignored:
                    print(f"  [!] Enzyme {code} have only 1 pathway : {pathway}")
                    print(f"  [!] and this pathway is ignored")
                    # Add entries for stats 
                    stats['ENZYME_ONLY_IGNORED_PATHWAY'] = stats['ENZYME_ONLY_IGNORED_PATHWAY'] + 1
                    stats['LIST_ENZYME_ONLY_IGNORED_PATHWAY'].append(code)
                    # Artificially create pathway entry, but empty 
                    suffixList = ['NA']
                    # Add suffix of pathway in final list
                    finalList.append(suffixList)

                else:
                    print(f"  [!] Ignored pathway : {pathway}")

        # Else, if pathway doesn't exist as a key in result
        elif 'PATHWAY' not in dictResult.keys():

            # Initialize an empty list
            finalList = []
            # Add suffix in final list
            finalList.append(prefixList)
            # Display a alert message
            print(f"[!] No pathway detected for enzyme {code}\n")
            # Increment number of failed pathway in stats and add enzyme in list
            stats['MISSING_PATHWAY_IN_KEGG'] = stats['MISSING_PATHWAY_IN_KEGG'] + 1
            stats['LIST_MISSING_PATHWAY_IN_KEGG'].append(code)
            # Artificially create pathway entry, but empty 
            suffixList = ['NA']
            # Add suffix of pathway in final list
            finalList.append(suffixList)


        return finalList


# -------------------------------------------------------------------------------------------------


def pathwayInfo(code):
# Function to get info about a pathway, from the code

    # Intialize searcher
    kSearcher = KEGG()
    # Get result and parse it in a dictionnary
    result = kSearcher.get(code)

    # Add code at the begining of the list
    dictResult = kSearcher.parse(result)


    # Initialize an empty list
    pathwayList = []

    # If name exist as a key in dictionnary, else 'NA' insted
    pathwayList.append(code)
    if 'NAME' in dictResult.keys():
        # If pathway name is a string comma separated, replace comma by semicolon
        # Fix to avoid wrong column formating at the end of the script
        nameStr = str(dictResult['NAME'][0].replace(',', ';'))
        pathwayList.append(nameStr)
    else:
        pathwayList.append('NA')

    # If class exist as a key in dictionnary, else 'NA' instead
    if 'CLASS' in dictResult.keys():
        # If pathway name is a string comma separated, replace comma by semicolon
        # Fix to avoid wrong column formating at the end of the script
        classStr = str(dictResult['CLASS']).replace(',',';')
        pathwayList.append(classStr)
    else:
        pathwayList.append('NA')


    return pathwayList


# -------------------------------------------------------------------------------------------------


def makeCSVHeader(n):
    
# Function to concantenate pathway to make a CSV header file
    print(f"\n[+] Prepare CSV header for maximum {n} pathways\n")
    # Define a prefix for the enzyme (code, name and definition)
    headerPrefix = 'enzyme_code,enzyme_name,enzyme_definition'
    # Empty header suffix
    headerSuffix = ''
    # Loop to concatenate header about N pathway (code, name and class)
    for i in range(n):
        headerSuffix = headerSuffix + (f"pathway{i + 1}_code,pathway{i + 1}_name,pathway{i + 1}_class,")

    # Format the final header
    csvHeader = f"{headerPrefix},{headerSuffix}"

    # [:-1] to remove last comma
    csvHeader = csvHeader[:-1]

    return csvHeader

# -------------------------------------------------------------------------------------------------

def formatCsv(inputFile, outputFile):
# Function to properly format CSV file, with :
# - CSV header
# - replace missings values (blank cells) by NA

    # Set maxLenght default value to 0
    maxLenght = 0

    # Read output file given in argument
    with open(inputFile, 'r') as fileStream:
        fileContent = fileStream.read().splitlines()

    # Get max number of line lenght
    for line in fileContent:
        lineLenght = len(str(line).split(','))
        if lineLenght > maxLenght:
            maxLenght = lineLenght

    # // 3 each pathway have 3 elements (code, name and class)
    # - 1 to exclude 1 empty loop in range() 
    nbColumns = (maxLenght // 3) - 1
    # Make CSV header
    fileHeader = makeCSVHeader(nbColumns)

    # Open output file in write mode and define a CSV writter
    with open(outputFile, 'w') as fileStream:
        writer = csv.writer(fileStream, delimiter=',')
        # Add CSV header (with split on comma, because writer want a list)
        writer.writerow(fileHeader.split(','))

        # Get the number of missings values in file per line
        for line in fileContent:
            # Get line lenght
            lineLenght = len(str(line).split(','))
            
            # If line is shorter than the max lenght
            if lineLenght < maxLenght:
                # Get the total number of missings values
                nbMissingValues = maxLenght - lineLenght
                # Concatenate NA for missings values
                neededValues = ',NA' * nbMissingValues
                newLine = line + neededValues
            else:
                newLine = line
            # Finally write new line with CSV writer
            writer.writerow(newLine.split(','))

    return 




# -------------------------------------------------------------------------------------------------
# --------------------------------------------- Main ----------------------------------------------
# -------------------------------------------------------------------------------------------------

# Initialize a parser for command line
parser = argparse.ArgumentParser(

formatter_class=argparse.RawDescriptionHelpFormatter,
# Add a brief description
description="""
KPathwayFinder is designed : \n
- from enzyme code (e.g K00001) get all pathways
- recover info about enzyme (code, name, definition)
- recover information about each pathway (code, name, class)
- concatenate each pathway for each enzyme (enzyme1 : pathway1, pathway2, pathway3...)
- format a previous CSV file, which contains informations about enzymes and pathways
"""
)

# Add arguments for command line
parser.add_argument('--mode', help='Specify which mode use', choices=['search', 'format-only'], required=True)
parser.add_argument('--input', help='The input file, which contain enzyme codes or CSV formated file', required=True)
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

# Set mode file argument
mode = args.mode

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
ignoredPathway = []                                         #
#                                                           #
#############################################################



# Initialize a dictionnary to report statistics at the end of the script
dictStat = {

    'IGNORED_PATHWAY':                      len(ignoredPathway),        # NB of ignored pathways (list above)
    'START_TIME':                           timeit.default_timer(),     # Time at start of script
    'END_TIME':                             0,                          # Time at end of script
    'NB_ENZYME':                            0,                          # NB of enzyme (in input file)
    'NB_PATHWAY':                           0,                          # NB pathways detected
    'FAILED_ENZYME':                        0,                          # NB of failed search with KEGG about an enzyme
    'ENZYME_ONLY_IGNORED_PATHWAY':          0,                          # NB of enzymes with only pathways in ignored list
    'MISSING_PATHWAY_IN_KEGG':              0,                          # NB of pathways missing in KEGG db
    'LIST_FAILED_ENZYME':                   [],                         # List of failed enzymes during search
    'LIST_ENZYME_ONLY_IGNORED_PATHWAY':     [],                         # List of enzymes without pathways (only ignored pathways)
    'LIST_MISSING_PATHWAY_IN_KEGG':         [],                         # List of enzymes without pathways in KEGG db

}

# If user choose format-only mode
if mode == 'format-only':

    formatCsv(inputFile, outputFile)
    print(f"[+] Result written in {outputFile}")
    

# Elif user choose search mode
elif mode == 'search':


    # Read input file with .read().splitlines to avoid \n at end of each lines
    with open(inputFile, 'r') as fileStream:
        sourceList = fileStream.read().splitlines()

    # Remove empty string in initial list
    # Can cause an issue when merging and writting pathway at the end of script
    # Post 1046 
    # https://stackoverflow.com/questions/3845423/remove-empty-strings-from-a-list-of-strings
    sourceList = list(filter(None, sourceList))

    # Add total number of enzymes in stats
    dictStat['NB_ENZYME'] = len(sourceList)


    # Main try to detect properly CTRL+C
    try:

    #
    # Main loop to get all required info about combo enzyme + pathway
    #

        # Open file in append mode and write row with CSV module
        with open(outputFile, 'w') as fileStream:
            # Define max lengh to 0 (used later to define CSV header lengh)
            nbRows = 0

            for enzyme in sourceList:

                # Check if file is not missing (in case of user suppression)
                if not path.isfile(outputFile):
                    print(f"\n[!] Output file is missing")
                    print(f"[!] Try to do not suppress it during script execution")
                    exit()


                # Get info about the enzyme
                aboutEnzyme = enzymeInfo(enzyme, ignoredPathway, dictStat, v)
                # If the function return False, the KEGG request is not valid and pass at the other enzyme
                if aboutEnzyme == False:
                    print(f"  [!] Something wrong happened with enzyme {enzyme} (skipped)")
                    # Add entry for stats (increment counter and add enzyme code in list)
                    dictStat['FAILED_ENZYME'] = dictStat['FAILED_ENZYME'] + 1
                    dictStat['LIST_FAILED_ENZYME'].append(enzyme)
                # Write row, comma separated to output file
                else:
                    # If lengh of list is greater than maxLengh (used later to make CSV header)
                    if len(sum(aboutEnzyme,[])) > nbRows:
                        nbRows = len(sum(aboutEnzyme,[]))

                    # sum aboutEnzyme list, and separate each item by comma
                    row = ','.join(sum(aboutEnzyme,[]))
                    # Define a writter (comma separated) and write row
                    writer = csv.writer(fileStream, delimiter=',')
                    writer.writerow(sum(aboutEnzyme, []))


    # In case of CTRL+C, exit the script without writting
    except KeyboardInterrupt:
        print("\n[-] KEGG research aborted")
        print(f"[-] Temporary results written in {outputFile}\n")
        print("bye.")
        exit()

    # Check if output file already exist, in case of deletion
    if not path.isfile(outputFile):
        print(f"\n[!] Output file is missing")
        print(f"[!] Try to do not suppress it during script execution")
        exit()

    else:
        # Finally call formatCSV function
        # Give input and output file in argument
        # In case of search mode, both files are sames to overwrite content
        # ... not very fancy method :(
        formatCsv(outputFile, outputFile)



    # Add current time in stats
    dictStat['END_TIME'] = timeit.default_timer()
    # Total time of execution, with 2 decimals
    totalTime = round(dictStat['END_TIME'] - dictStat['START_TIME'], 2)

    # Display statistics
    print('---------------------------------------------------\n')


    print(f"Total time of execution : {totalTime} second(s)\n")
    print(f"Total number of enzymes parsed : {dictStat['NB_ENZYME']}")
    print(f"Total number of founded pathways : {dictStat['NB_PATHWAY']}")
    print(f"Total number of failure in research about enzyme : {dictStat['FAILED_ENZYME']}")
    print(f"Total number of enzymes without pathway in KEGG db : {dictStat['MISSING_PATHWAY_IN_KEGG']}")
    print(f"Total number of enzymes having only ignored pathways : {dictStat['ENZYME_ONLY_IGNORED_PATHWAY']}")
    statFile = f"{path.abspath(path.dirname(outputFile))}/stats.txt"

    # Write stats in file, with list for details
    with open(statFile, 'w') as fileStream:
        fileStream.write(f"Total time of execution : {totalTime} second(s)\n")
        fileStream.write(f"Total number of enzymes parsed : {dictStat['NB_ENZYME']}\n")
        fileStream.write(f"Total number of found pathways : {dictStat['NB_PATHWAY']}\n")
        fileStream.write(f"Total number of failure in research about enzyme : {dictStat['FAILED_ENZYME']}\n")
        fileStream.write(f"Total number of enzymes without pathway in KEGG db : {dictStat['MISSING_PATHWAY_IN_KEGG']}\n")
        fileStream.write(f"Total number of enzymes having only ignored pathways : {dictStat['ENZYME_ONLY_IGNORED_PATHWAY']}\n")

        # If there are failed enzymes during search
        if dictStat['FAILED_ENZYME'] != 0:
            fileStream.write(f"List of failed enzymes during search : \n{dictStat['LIST_FAILED_ENZYME']}\n")

        # If there are enzyme with only ignored pathways (in ignoredList)
        if dictStat['ENZYME_ONLY_IGNORED_PATHWAY'] != 0:
            fileStream.write(f"List of enzymes only with ignored pathways :\n{dictStat['LIST_ENZYME_ONLY_IGNORED_PATHWAY']}\n")
        
        # If there are enzymes without pathways in KEGG db
        if dictStat['LIST_MISSING_PATHWAY_IN_KEGG']:
            fileStream.write(f"List of enzymes without pathways in KEGG db : \n{dictStat['LIST_MISSING_PATHWAY_IN_KEGG']}\n")



    print(f"[?] For more information, view {statFile} file")
