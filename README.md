# Pre-train LM for Information Extraction

## Meeting Note:
- 06/13/2022
Name entity recognition (NER): using the bioportal annotator API [LINK](http://data.bioontology.org/documentation) and [python script](https://github.com/ncbo/ncbo_rest_sample_code/blob/master/python/python3/annotate_text.py)

## Related Papers
- Mintz et al. ACL'09. [Distant supervision for relation extraction without labeled data](https://aclanthology.org/P09-1113.pdf)
- Riedel et al. ECML PKDD'10. [Modeling Relations and Their Mentions without
Labeled Text](https://link.springer.com/content/pdf/10.1007/978-3-642-15939-8_10.pdf)
- Thillaisundaram et al. BioNLP'19. [Biomedical relation extraction with pre-trained language representations
and minimal task-specific architecture](https://aclanthology.org/D19-5713.pdf)
- Verga, et al. NAACL'18. [Simultaneously Self-Attending to All Mentions for
Full-Abstract Biological Relation Extraction](https://aclanthology.org/N18-1080.pdf)
- Ye et al. NAACL'19. [Distant Supervision Relation Extraction with Intra-Bag
and Inter-Bag Attentions](https://aclanthology.org/N19-1288.pdf)
- Alt et al. ACL'19. [Fine-tuning Pre-Trained Transformer Language Models to Distantly
Supervised Relation Extraction](https://aclanthology.org/P19-1134.pdf)
- Wang et al. ACL'22. [OIE@OIA: an Adaptable and Efficient Open Information Extraction
Framework](https://aclanthology.org/2022.acl-long.430.pdf)









**Instructions to run the whole pipeline:**
This tool downloads all the PubMed files related to the topic given as an input value, recognizes the gene and phenotype mentioned in each sentence of the abstract does relation extraction, and finally saves all the positive and negative results in separate Html files. The positive result file has all the sentences with their PMID and sentence number discussing an association between the gene and phenotype. The negative results file has all the sentences with their PMID and sentence number that do not discuss an association between the gene and phenotype. We have used the bioportal annotator for phenotype recognition, scispcay for gene recognition, and the biobert-pytorch/relation-extraction model for training and testing. 





**1. Creating a virtual environment:**
-To use this tool, we first have to run the following command:
python -m venv .env
source .env/bin/activate






**2. Cloning the biobert-pytorch**
-we run the following command to clone the biobert-pytorch repository 
git clone https://github.com/dmis-lab/biobert-py





**3. Installation:**
  -we have to run the following commands to install some packages or models
  1. Install transformers :
  pip install transformers==3.0.0

  2. Install the nltk, which will tokenize the abstract
  pip install nltk

  3. Install scispacy
  pip install scispacy

  4. Install pandas
  pip install pandas

  5. Install Pytorch
  pip3 install torch torchvision torchaudio

  6. Install scikit-learn
  pip install scikit-learn

  7. Install the en_ner_craft_md; this will be used for gene_recognition
  pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.0/en_ner_craft_md-0.5.0.tar.gz

**Note: One may have to install more packages based on their working environment. For more information about installation, check https://github.com/dmis-lab/biobert-pytorch and https://github.com/allenai/scispacy **





**4. Saving the scripts:**
` -We will go to the biobert-pytorch/relation-extraction directory. Then save the query_to_pubmed, phenotype_recognition.py, gene_recognition.py convert_to_biobert.py, Evaluate.sh, convert_test_results.py scripts in that directory from the All-scripts.
  -we will create a directory called datasets within relation-extraction where the test.tsv file will be saved.
  -We will also create output directory where the test_results.txt file will be saved
  
  




**5. Running the scripts**
  1. First run the query_to_pubmed.py file, which will take the term we are searching for as the input value
  2. Run the phenotype_recognition.py with three command line arguments: the first argument is the address of the directory where the PubMed files are saved, the second argument is the directory where the abstracts will be saved, and the third argument is the address to the directory where we want the resulting files to be saved
  3. Run the gene_recognition.py script with two command line arguments: the first argument is the address to the directory where the resulting files of the phenotype_recognition.py are saved, and the second argument is the address to the directory where we want the resulting data.tsv file of this script to be saved
  4. Run the convert_to_biobert.py; this script converts the data.tsv file into a format that is accepted by the biobert model. The resulting file will be saved in the datasets directory that we previously created
  5. Run the evaluate.sh which will save a test_results.txt file in the output directory that has all the predictions
  6. Run the convert_test_results.py. This script saves all the positive predictions into the positive_results.html and negative predictions into the negative_results.html file in the same directory where the data.tsv file is saved. The resulting files contain sentences with their PMID and sentence number with the gene and phenotype in a different colors. 
  
  
**Note: In all the scripts, one needs to change the directory address based on where they want the files to be saved.** 
  






  
