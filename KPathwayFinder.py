from bioservices.kegg import KEGG




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
            else:
                print(f"  [!] Ignored pathway : {pathway}")

            finalList.append(prefixList + suffixList)

        
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
# --------------------------------------------- Main ----------------------------------------------
# -------------------------------------------------------------------------------------------------





source = r'/home/scratch/Downloads/source.txt'
sourceList = ['K10','K00001', 'K0','K00002', 'K00003']
# List with ignored pathways, can be empty
ignoredPathway = ['ko01100']

# Seet verbosity of KEGG searcher
v = False
# Initialize the main list, wich contains other list about enzyme + pathways
enzymeList = []


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



print(enzymeList)

