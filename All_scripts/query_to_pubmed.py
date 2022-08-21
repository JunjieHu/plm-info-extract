import csv
import os
import re
import urllib.request
from time import sleep

# user inputs what you want to search pubmed for
query = input ("What would you like to download PubMed abstracts for? Enter your keyword(s):")

# if spaces were entered, replace them with %20 to make compatible with PubMed search
query = query.replace(" ", "%20")

# common settings between esearch and efetch
base_url = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
db = 'db=pubmed'

# esearch settings
search_eutil = 'esearch.fcgi?'
search_term = '&term=' + query
search_usehistory = '&usehistory=y'
search_rettype = '&rettype=json'

# call the esearch command for the query and read the web result
search_url = base_url+search_eutil+db+search_term+search_usehistory+search_rettype
print("this is the esearch command:\n" + search_url + "\n")
f = urllib.request.urlopen (search_url)
search_data = f.read().decode('utf-8')

# extract the total abstract count
total_abstract_count = int(re.findall("<Count>(\d+?)</Count>",search_data)[0])

# efetch settings
fetch_eutil = 'efetch.fcgi?'
retmax = 500
retstart = 0
fetch_retmode = "&retmode=text"
fetch_rettype = "&rettype=abstract"

# obtain webenv and querykey settings from the esearch results
fetch_webenv = "&WebEnv=" + re.findall ("<WebEnv>(\S+)<\/WebEnv>", search_data)[0]
fetch_querykey = "&query_key=" + re.findall("<QueryKey>(\d+?)</QueryKey>",search_data)[0]


# call efetch commands using a loop until all abstracts are obtained
run = True
all_abstracts = list()
loop_counter = 1

while run:
    loop_counter += 1
    fetch_retstart = "&retstart=" + str(retstart)
    fetch_retmax = "&retmax=" + str(retmax)
    # create the efetch url
    fetch_url = base_url+fetch_eutil+db+fetch_querykey+fetch_webenv+fetch_retstart+fetch_retmax+fetch_retmode+fetch_rettype
    print(fetch_url)
    # open the efetch url
    f = urllib.request.urlopen (fetch_url)
    fetch_data = f.read().decode('utf-8')
    # split the data into individual abstracts
    abstracts = fetch_data.split("\n\n\n")
    # append to the list all_abstracts
    #finding the starting of an article
    for abstract in abstracts:
        
        PMID=re.findall("PMID: [0-9]+", abstract)
        string=""
        for i in PMID:
          string+=i
        #we are changing to the directory where we want the pubmed files to be downloaded
        #we can change the directory address to whatever address we want the files to be saved
        os.chdir('/Users/nafisaraisa/Documents/Biomedical_Data_Science/pubmed_files')

        with open(string+".txt", "w") as f:
          if len(abstract)>5:
              f.write(str(PMID))
              f.write(abstract)
              f.close()
          else:
               partial_abstract_writer.writerow(abstract)
    # wait 2 seconds so we don't get blocked
    sleep(2)
    # update retstart to download the next chunk of abstracts
    retstart = retstart + retmax
    if retstart > total_abstract_count:
        run = False


