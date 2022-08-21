import urllib. request
import nltk.data
import sys
import json
import os
import re
from pprint import pprint
from urllib.request import Request, urlopen
from nltk.tokenize import sent_tokenize

  
REST_URL = "http://data.bioontology.org"
API_KEY = "a67212fc-49ae-45d0-ad42-755746744b60"

#defining variables:
#output:this is the heading of the resulting files
output="PMID-sentence_num"+'\t'+"From"+"\t" + "To" +"\t"  + "String_Matched"+"\t" +"Ontology"+ "\t" + "Sentence"
print(output)


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
#Use of KEYSTRING to find the asbtract following a same pattern in all pubmed files
	KEYSTRING = 'Author information:'
	
	#string conatines the PMID
	string=""
	
	#abstract contains the abstract
	abstract=""
	
	#read the file
	with open(input_file, 'r') as f:
		content=f.read()

		#temp is index of the KEYSTRING
		temp=content.find(KEYSTRING)
		if not temp==-1:
			start_idx=int(content[temp:].find("\n\n"))+int(temp)
			end_idx=int(content.find("DOI"))
			abs=(content[start_idx:end_idx])
			real_abs=abs.split('\n')
			
			for i in real_abs:
				line=i.strip()
				abstract+=line+" "
			
			#text is a list with all the lines of the abstract
			#sent_tokenize extracts sentences from the abstract that was previously extracted from the files
			text=sent_tokenize(abstract)
			
			#find the PMID of the file
			PMID=re.findall("PMID: [0-9]+", content)
			try:
				string=PMID[0]	
			
				#given an outfile file, write the abstract in it
				with open(abs_file, "w") as f:
					f.write(string+'\n')
					for i in text:
						f.write(i)
				
					#return the PMID and the list of sentences from the abstract
					return text, string
			except:
					pass	






#print_annotations:
#takes PMID, a file,path to the resulting directory(new_path),  annotations, abstract(text_to_annotate),sentence number in the abstract, and get_class as input. get_class is set to True by default
#creates a file with the PMID as the name
#the resulting file contains string matched, begin and end index of the string matched, ontology, sentence
#print out all the information that goes into a resulting file
def print_annotations(PMID, file, new_path, annotations,text_to_annotate,sentence_num, get_class=True):
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
			output_string=str(PMID)+ "-" +str( sentence_num)
			output_string+="\t" + str(annotation["from"]-1)
			output_string+= "\t"+str(annotation["to"]-1)
			string_matched=text_to_annotate[annotation["from"]-1:annotation["to"]]
			output_string+= "\t" + string_matched
			try:
				output_string+="\t" + class_details["prefLabel"] #prefLabel is the ontology
			except TypeError:
				output_string+="Error"
				continue
			output_string+='\t' + text_to_annotate
			with open(file,"a") as f:
				f.write(output_string+'\n')
				print(output_string)
				f.close()
		

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
	

	# iterate through all file
	for file in os.listdir():
    		# Check whether file is in txt format or not
		if file.endswith(".txt"):
			#iterating through all the files saved in the directory
			# making teh files
			input_file = os.path.join(joined_pubmed_path, file)
			abstract_file = os.path.join(joined_abs_path,file)
			tag_file=os.path.join(joined_new_path, file)

			#calling the read_abstract function which returns the abstract
			try:
				abstract, PMID= read_text_file(input_file, abstract_file)
				string=""
				for i in PMID[6:]:
					string+=i
				#sentence_num is the number of sentence in the abstract
				sentence_num=1
				for i in abstract:
					# Annotate using the provided text
					annotations = get_json(REST_URL + "/annotator?ontologies=HP&text=" + urllib.parse.quote(str(i)))
					# Print out annotation details
					print_annotations(string, file,joined_new_path, annotations, i, sentence_num)
					sentence_num=sentence_num + 1
			except TypeError:
				print("error")

			

			
if __name__=="__main__":
	main()



