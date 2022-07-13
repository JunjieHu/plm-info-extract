import sys
import urllib.request, urllib.error, urllib.parse
import json
import os
import re
from pprint import pprint
from urllib.request import Request, urlopen

REST_URL = "http://data.bioontology.org"
API_KEY = "a67212fc-49ae-45d0-ad42-755746744b60"

#defining variables:
#output:this is the heading of the resulting files
output="From"+"\t" + "To" +"\t" + "Match type" +"\t"  + "String_Matched"+"\t" +"Ontology"+ "\t"+"Ontology ID"


#path: this is the path to the pubmed files that are used as input
#the path will be taken from the user as the first argument from the command line
path=sys.argv[1]

#new path:this is path where the resulting directory is
#the new path is taken from the user as the 2nd argument from the command line
new_path =sys.argv[2]



#defining functions:
def get_json(url):
    opener = urllib.request.build_opener()
    opener.addheaders = [('Authorization', 'apikey token=' + API_KEY)]
    return json.loads(opener.open(url).read())



# Read text File:
#takes a .txt file as input
#reads the content of the file in a string and extract the abstract from the file
#returns the abstract
def read_text_file(file_path):
    with open(file_path, 'r') as f:
        #reading the file into a string called content
        content=f.read()
        #ab_start and ab_end are the start and end indexes of the abstract respectively
        ab_start = re.search('AB  - ', content).end()
        ab_end = re.search('[A-Z]+[ ]* - ', content[ab_start:]).start() + ab_start
        abstract= content[ab_start : ab_end]
        return abstract



#print_annotations:
#takes a file, annotations, abstract(text_to_annotate),and get_class as input. get_class is set to True by default
#creates a file with the same name as the input file
#the resulting file contains string matched, begin and end index of the string matched, ontology, ontology ID, and match type
#print out all the information that goes into a resulting file
def print_annotations(file, annotations, text_to_annotate,get_class=True):
    for result in annotations:
        class_details = result["annotatedClass"]
        if get_class:
            try:
                class_details = get_json(result["annotatedClass"]["links"]["self"])
            except urllib.error.HTTPError:
                print(f"Error retrieving {result['annotatedClass']['@id']}")
                continue

	
	#changing to the directory that has all the pubmed files
        os.chdir(new_path)

	#if the file already does not exist, open the file in "w" mode and write the output
        if os.path.exists(file):
            append_write = 'a' # append if already exists

        else:
            append_write = 'w' # make a new file if not
            with open(file, 'w') as f:
                f.write(output + "\n")




	#iterating through the loop
        for annotation in result["annotations"]:
       	    output_string=str(annotation["from"])
            output_string+= "\t"+str(annotation["to"])
            string_matched=text_to_annotate[annotation["from"]-1:annotation["to"]]
            output_string+="\t" + annotation["matchType"]
            output_string+= "\t" + string_matched
            try:
                output_string+="\t" + class_details["prefLabel"] #prefLabel is the ontology
            except TypeError:
                output_string+="Error"
                continue

            output_string+="\t" + class_details["links"]["ontology"]
            with open(file,append_write) as f:
                f.write(output_string + "\n")
                print(output_string)


#main():
#iterate through a loop and calls read_text_file, get_jason, and print_annotations functions
def main():
	# Change the directory to where the pubmed files are saved
	os.chdir(path)

	# iterate through all file
	for file in os.listdir():
    	# Check whether file is in txt format or not
    		if file.endswith(".txt"):
        		file_path = f"{path}/{file}"
			#new_file is the file name which is to be annotated
        		new_file=os.path.join(new_path,file)
        		print(file)
        		with open(new_file, 'w') as f:
             			f.write(output + "\n")

			# calling functions
			#call  read text file function
        		text_to_annotate=read_text_file(file_path)

			# Annotate using the provided text
        		annotations = get_json(REST_URL + "/annotator?ontologies=HP&text=" + urllib.parse.quote(text_to_annotate))

			# Print out annotation details
        		print_annotations(new_file, annotations, text_to_annotate)

if __name__ == "__main__":
    main()


