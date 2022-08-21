import os
import re

#input_file: this is the test_results.txt where all predictions are saved
input_file="/Users/nafisaraisa/Desktop/relation-extraction/output/test_results.txt"
#actual_file: this is the data.tsv file where all the information like pstart, pend, gstart, gend, sentencve, PLID are saved
actual_file="/Users/nafisaraisa/documents/Biomedical_Data_Science/project_data/data.tsv"


TAB = '    '
GSTART_TAG = '<b style="color:red;">'
PSTART_TAG = '<b style="color:blue;">'
ENDTAG = '</b>'


def write_a_row(items, fout, prefix):
	fout.write(f'{prefix}<tr>\n')
	for item in items:
		fout.write(f'{prefix}{TAB}<td>{item}</td>\n')
	fout.write(f'{prefix}</tr>\n')


def annotate_sentence(text, pstart, pend, gstart, gend):
	pend+=1
	gend+=1
	if pstart < gstart:
		new_text = text[:pstart] + PSTART_TAG + text[pstart:pend] + ENDTAG + text[pend:gstart] + GSTART_TAG + text[gstart:gend] + ENDTAG + text[gend:]
	else:
		new_text = text[:gstart] + GSTART_TAG + text[gstart:gend] + ENDTAG + text[gend:pstart] + PSTART_TAG + text[pstart:pend] + ENDTAG + text[pend:]
	return new_text


def main():
	#resulting files
	new_file_positive="/Users/nafisaraisa/documents/Biomedical_Data_Science/project_data/positive_results.html"
	new_file_negative="/Users/nafisaraisa/documents/Biomedical_Data_Science/project_data/negative_results.html"
	
	# Open a file handler
	#positive results
	fout = open(new_file_positive, 'w')
	fout.write(f'<table>\n{TAB}<thead>')
	# write the header
	header = 'PMID-sentence_num\tSentence'.split('\t')
	write_a_row(header, fout, prefix=TAB+TAB)
	fout.write(f'{TAB}</thead>')
	

	#negative results:	
	mout = open(new_file_negative, 'w')
	mout.write(f'<table>\n{TAB}<thead>')
	# write the header
	header = 'PMID-sentence_num\tSentence'.split('\t')
	write_a_row(header, mout, prefix=TAB+TAB)
	mout.write(f'{TAB}</thead>')
	

	#opening the test_results.txt file
	with open(input_file, 'r') as f:
		#reading the file
		content=f.read()
		
		#is_header is true for the title of the test_results.txt file
		is_header=True
		
		#splitting in lines
		line=content.split("\n")

		#opening and reading the data.tsv file that has index, PMID, pstart, pend, string_matched, ontology, gstart, gend, label, gene, sentence
		with open(actual_file, 'r') as m:
			info=m.read()
			each_line=info.split("\n")
		
		
		#iterating through every line of test_results.txt to get each prediction
		for i in line:
			if is_header:
				is_header=False
			else:
				#splitting by items in the line
				test_item=i.split("\t")
				if len(test_item)>1:
					for i in each_line:
						#original_ietm refers to every item from a single line in the data.tsv file
						original_item=i.split("\t")
						
						#checking if the index of the test_results.txt file and the data.tsv file are same
						if test_item[0]==original_item[0]:
							
							#if test_item[1]==1, the results is True indicating tehre is a relation between the gene and phenotype
							if test_item[1]=='1':
								new_line=[str(original_item[1])]
								text = original_item[6]
								pstart, pend, gstart, gend = int(original_item[2]), int(original_item[3]), int(original_item[7]), int(original_item[8])
								new_text = annotate_sentence(text, pstart, pend, gstart, gend)
								new_line.append(new_text)
								write_a_row(new_line, fout, prefix=TAB)

							else:
								new_line=[str(original_item[1])]
								text = original_item[6]
								pstart, pend, gstart, gend = int(original_item[2]), int(original_item[3]), int(original_item[7]), int(original_item[8])
								new_text = annotate_sentence(text, pstart, pend, gstart, gend)
								new_line.append(new_text)
								write_a_row(new_line, mout, prefix=TAB)
								
	# close a file handler
	fout.close()
	mout.close()


if __name__=="__main__" :
	main()
