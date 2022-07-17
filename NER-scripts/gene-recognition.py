import sys
import os
import scispacy
import spacy
import en_ner_craft_md
import re




#defining functions:
#read_abstract:
#takes a .txt file as input and creates a file with the same name as the input file as output
#returns the abstract
def read_abstract(input_file, output_file=None):
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
	if output_file is not None:
		with open(output_file, 'w') as fout:
			fout.write(text)
	return text

		 
			


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

	
	# Create the nlp model
	nlp = en_ner_craft_md.load()

	#heading
	print('From\tTo\tText\tLabel\n')
	
	#the path we are currently in:
	current_path=os.getcwd()
	
	#making an absolute path from the given relative path
	joined_pubmed_path=os.path.join(current_path, pubmed_path)
	joined_abs_path=os.path.join(current_path, abs_path)
	joined_new_path=os.path.join(current_path, new_path)
	
	#changing directory:
	os.chdir(joined_pubmed_path)

	# Make the directory if it does not exist
	for file in os.listdir():
		if file.endswith(".txt"):
			print(file+ '\n')
			#iterating through all the files saved in the directory
			# Step 1. Read the files
			input_file = os.path.join(joined_pubmed_path, file)
			abstract_file = os.path.join(joined_abs_path,file)
			#calling the read_abstract function which returns the abstract
			abstract = read_abstract(input_file, abstract_file)
	
			# Step 2. Annoate file
			doc = nlp(abstract)
			tag_file = os.path.join(joined_new_path,file)
			with open(tag_file, 'w') as fout:
				fout.write('From\tTo\tText\tLabel\n')
				for x in doc.ents:
					if x.label_ == 'GGP':
						fout.write(f'{x.start_char}\t{x.end_char-1}\t{x.text}\t{x.label_}\n')
						print(f'{x.start_char}\t{x.end_char-1}\t{x.text}\t{x.label_}\n')
						





if __name__=="__main__" :
	main()
