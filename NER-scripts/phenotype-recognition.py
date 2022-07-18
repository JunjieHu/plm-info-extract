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

#defining functions:
def get_json(url):
	try:
		opener = urllib.request.build_opener()
		opener.addheaders = [('Authorization', 'apikey token=' + API_KEY)]
		return json.loads(opener.open(url).read())# Read text File:
	except urllib.error.HTTPError:
		print("Error")
		exit(1)

#takes a .txt file as input
#reads the content of the file in a string and extract the abstract from the file
#returns the abstract
def read_text_file(input_file, abs_file=None):
        KEYSTRING = 'AB  -'
        text = []
        find_abstract = False
        for line in open(input_file, 'r', encoding="utf8", errors='ignore'):
                # Find the first line of the abstract
                if line.startswith(KEYSTRING):
                        text.append(line[len(KEYSTRING):].strip())
                        find_abstract = True
                # Read the following lines in the abstract
                elif line.startswith('    ') and find_abstract:
                        text.append(line.strip())
                # Skip the other lines
                else:
                        abstract = False
                        if find_abstract:
                                break
        text = ' '.join(text)
        # When given an output file, write the abstract to it
        if abs_file is not None:
                with open(abs_file, 'w') as fout:
                        fout.write(text)
        return text

#print_annotations:
#takes a file, annotations, abstract(text_to_annotate),and get_class as input. get_class is set to True by default
#creates a file with the same name as the input file
#the resulting file contains string matched, begin and end index of the string matched, ontology, ontology ID, and match type
#print out all the information that goes into a resulting file
def print_annotations(file, new_path, annotations, text_to_annotate,get_class=True):
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
	#if the user does not provide 3 arguments
	if not len(sys.argv)==4:
		print("The program requires exactly 3 arguments. You entered more or less than 3")
		sys.exit(1)

	# directories for inputs/abstracts/gene-tags:
	#directory where pubmed files are saved, taken as the 1st argument from the command line
	pubmed_path = sys.argv[1]

	#directory where the pubmed abstracts are saved, taken as the 2nd argument from the command line
	abs_path = sys.argv[2]

	#directory where the resulting files are saved, taken as the 3rd argument from the command line
	new_path=sys.argv[3]



	#the path we are currently in:
	current_path=os.getcwd()

	#making an absolute path from the given relative path
	if not os.path.isabs(pubmed_path):
		joined_pubmed_path=os.path.join(current_path, pubmed_path)
	else:
		joined_pubmed_path=pubmed_path

	if not os.path.isabs(abs_path):
		joined_abs_path=os.path.join(current_path, abs_path)
	else:
		joined_abs_path=abs_path

	if not os.path.isabs(new_path):
		joined_new_path=os.path.join(current_path, new_path)
	else:
		joined_new_path=new_path
	#changing to pubmed_path
	os.chdir(joined_pubmed_path)
	
	#heading
	print(output+ "\n")
	# iterate through all file
	for file in os.listdir():
    		# Check whether file is in txt format or not
		if file.endswith(".txt"):
			print(file+ '\n')
			#iterating through all the files saved in the directory
			# Step 1. Read the files
			input_file = os.path.join(joined_pubmed_path, file)
			abstract_file = os.path.join(joined_abs_path, file)
			tag_file=os.path.join(joined_new_path, file)

			#calling the read_abstract function which returns the abstract
			abstract = read_text_file(input_file, abstract_file)
			text_to_annotate=abstract
			
			# Annotate using the provided text
			annotations = get_json(REST_URL + "/annotator?ontologies=HP&text=" + urllib.parse.quote(text_to_annotate))
			# Print out annotation details
			print_annotations(file,joined_new_path, annotations, text_to_annotate)

if __name__ == "__main__":
    main()
