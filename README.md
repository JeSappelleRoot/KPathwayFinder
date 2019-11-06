# KPathwayFinder

- [KPathwayFinder](#kpathwayfinder)
- [How to use it](#how-to-use-it)
- [Before use it](#before-use-it)
- [About output file](#about-output-file)
- [Exclude manually some pathways](#exclude-manually-some-pathways)
- [Example](#example)
  - [Command line](#command-line)
  - [Statistics reporting in file](#statistics-reporting-in-file)



# How to use it

KPathwayFinder is a very simple tool. You need to specify : 
- `--input` argument which indicate source file, wich contains enzyme list  
- `--output` argument which indicate output file (**.txt or .csv extension**), which will contains the result of the search about pathways  
  
> You can also use `-v` argument to increase verbosity of KEGG library

# Before use it

KPathwayFinder can be very slow due to KEGG library. For example, with a source which contains 20 000 enzymes codes, **the total process of the script will take approximately 7h** (depends of your internet connection).  

It's recommanded, if you have a large file of enzymes codes, to split your source file in several small files. 

To detect the maximum number of pathways, KPathwayFinder have to parse all enzymes codes first, that explain what : 

>- **KPathwayFinder will write final file only at the end of the search**  
>- **If an error occurs during the search, the script will not write the final file**

# About output file

KPathwayFinder will automatically detect the maximum number of pathways, and create an output file as a CSV formatted file. 

This file will contains 1 line by enzyme code, with fields : 
- enzyme code
- enzyme name
- enzyme definition
  
Then, the script will create fields about pathways with the maximum number of pathways. Final header of CSV file will looks like : 

| Enzyme code | Enzyme name | Enzyme definition | code of pw1 | name of pw1 | class of pw1 | code of pw2 | name of pw2 | class of pw2 | name of pw n | ... |   |
|-------------|-------------|-------------------|-------------|-------------|--------------|-------------|-------------|--------------|--------------|-----|---|
|             |             |                   |             |             |              |             |             |              |              |     |   |

# Exclude manually some pathways

If you want exclude some pathways, you need to modify the script, line 263. 

```
#############################################################
#MODIFY THIS VALUE TO IGNORE SPECIFIC PATHWAY (CAN BE EMPTY)#
# List with ignored pathways                                #
ignoredPathway = []                                         #
#                                                           #
#############################################################
```

You can specify some pathways, with the following syntax :  
`ignoredPathway = ['k0001', 'k0002', 'k0003']`  

KPathwayFinder will automatically skip these pathways (view example below)


# Example 

With a source file which contains the following lines : 
```
K00012
K00013
K error
K01
```
> `K error` and `K01` are deliberate errors for demonstration  

## Command line  
`python3 KPathwayFinder.py --input ~/Downloads/source.txt --output ~/Downloads/output.csv`

```


  _  _______      _   _                        ______ _           _           
 | |/ /  __ \    | | | |                      |  ____(_)         | |          
 | ' /| |__) |_ _| |_| |____      ____ _ _   _| |__   _ _ __   __| | ___ _ __ 
 |  < |  ___/ _` | __| '_ \ \ /\ / / _` | | | |  __| | | '_ \ / _` |/ _ \ '__|
 | . \| |  | (_| | |_| | | \ V  V / (_| | |_| | |    | | | | | (_| |  __/ |   
 |_|\_\_|   \__,_|\__|_| |_|\_/\_/ \__,_|\__, |_|    |_|_| |_|\__,_|\___|_|   
                                          __/ |                               
                                         |___/                                
                              
    
[+] Get info about enzyme K00012
  [-] Get info about ko00040 pathway
  [-] Get info about ko00053 pathway
  [-] Get info about ko00520 pathway
  [!] Ignored pathway : ko01100
[+] Get info about enzyme K00013
  [-] Get info about ko00340 pathway
  [!] Ignored pathway : ko01100
  [-] Get info about ko01110 pathway
  [-] Get info about ko01230 pathway
[+] Get info about enzyme K error
  [!] Something wrong happened with enzyme K error (skipped)
[+] Get info about enzyme K01
  [!] Something wrong happened with enzyme K01 (skipped)


[+] Prepare CSV header for maximum 3 pathway

[+] Merging pathways from K00012 enzyme
[+] Merging pathways from K00013 enzyme


[+] Writing informations about enzyme K00012
[+] Writing informations about enzyme K00013
---------------------------------------------------

Total time of execution : 60.82 second(s)

Total number of enzymes parsed : 4
Total number of founded pathways : 6
Total number of failure in research about enzyme : 2
Total number of enzymes without pathway in KEGG db : 0
Total number of enzymes having only ignored pathways : 0
[?] For more information, view ~/Downloads/stats.txt file
```

## Statistics reporting in file
```
Total time of execution : 60.23 second(s)
Total number of enzymes parsed : 4
Total number of found pathways : 6
Total number of failure in research about enzyme : 2
Total number of enzymes without pathway in KEGG db : 0
Total number of enzymes having only ignored pathways : 0
List of failed enzymes during search : 
['K error', 'K01']
```

>KPathwayFinder will automatically detect the parent directory of the output file