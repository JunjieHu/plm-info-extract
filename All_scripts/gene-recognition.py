import sys
import os
import scispacy
import spacy
import en_ner_craft_md
import re
			


def main():

	#if the user does not provide 2 arguments, print an error statement
	if not len(sys.argv)==3:
		print("The program requires exactly 2 arguments. You entered more or less than 2")
		sys.exit(1)

	
	# directories for input and output:
	#directory where sentences with a phenotype mention are saved, taken as the 1st argument from the command line
	pubmed_path = sys.argv[1]
	#directory where the resulting data.tsv file will be saved, taken as 2nd argument
	new_path=sys.argv[2]


	
	# Create the nlp model
	nlp = en_ner_craft_md.load()

	
	#the path we are currently in:
	current_path=os.getcwd()
	
	#making an absolute path from the given relative path
	if not os.path.isabs(pubmed_path):
		joined_pubmed_path=os.path.join(current_path, pubmed_path)
	else:
		joined_pubmed_path=pubmed_path

	
	if not os.path.isabs(new_path):
		joined_new_path=os.path.join(current_path, new_path)
	else:
		joined_new_path=new_path
	
	new_file=joined_new_path
	os.chdir(new_file)
	with open("data.tsv", 'w') as f:
		f.write('Index\tPMID\tphen_sidx\tphen_eidx\tstring_matched\tontology\tsentence\tgen_sidx\tgen_eidx\tText\tLabel\n')
		print('Index\tPMID\tphen_sidx\tphen_eidx\tstring_matched\tontology\tsentence\tgen_sidx\tgen_eidx\tText\tLabel\n')
		f.close()
	
	
	#changing to the directory where the input files are saved
	os.chdir(joined_pubmed_path)
	index=0
	for file in os.listdir():
		if file.endswith(".txt"):
			print(file+ '\n')
			#iterating through all the files saved in the directory
			# Step 1. Read the files
			input_file = os.path.join(joined_pubmed_path, file)
			#calling the read_abstract function which returns the abstract
			is_header=True
			for i in  open(input_file):
				line=i.strip()	
				item=line.split("\t")
				if len(item)>5:
					sentence=str(item[5])
					# Annoate file
					doc = nlp(sentence)
					if is_header:
						is_header=False
					else:
						
						for x in doc.ents:
							if x.label_ == 'GGP':
								new_line=str(index)
								new_line+='\t'+line
								new_line+='\t'+ str(x.start_char)
								new_line+='\t' + str(x.end_char-1)
								new_line+='\t' + str(x.text)
								new_line+='\t' + str(x.label_)
								os.chdir(new_path)
								with open("data.tsv", 'a') as f:
									f.write(new_line+ '\n')
									print(new_line)
									index+=1
									print("\n")
									f.close()
				else:
					print("Error")			




if __name__=="__main__" :
	main()

