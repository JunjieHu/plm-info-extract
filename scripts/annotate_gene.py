import os
import scispacy
import spacy
import en_ner_craft_md

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
            find_abstract = False
    text = ' '.join(text)
    # When given an output file, write the abstract to it
    if output_file is not None:
        with open(output_file, 'w') as fout:
            fout.write(text)
    return text

# directories for inputs/abstracts/gene-tags
ROOT = '/data/hulab/junjieh/plm-info-extract'
in_dir = f'{ROOT}/data'
abs_dir = f'{ROOT}/outputs/abstract'
tag_dir = f'{ROOT}/outputs/genes'

# Create the nlp model
nlp = en_ner_craft_md.load()

# Make the directory if it does not exist
for dir in [abs_dir, tag_dir]:
    if not os.path.exists(dir):
        os.makedirs(dir)

for file in os.listdir(in_dir):
    # Step 1. Read the files
    print(f'=====Reading {file}=====')
    input_file = f'{in_dir}/{file}'
    abstract_file = f'{abs_dir}/{file}'
    abstract = read_abstract(input_file, abstract_file)
    
    # Step 2. Annoate file
    print(f'======Annotating {file}====')
    doc = nlp(abstract)
    tag_file = f'{tag_dir}/{file}'
    with open(tag_file, 'w') as fout:
        fout.write('WordFrom\tWordTo\tCharFrom\tCharTo\tText\tLabel\n')
        for x in doc.ents:
            if x.label_ == 'GGP':
                fout.write(f'{x.start}\t{x.end}\t{x.start_char}\t{x.end_char}\t{x.text}\t{x.label_}\n')


