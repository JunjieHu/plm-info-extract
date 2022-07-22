#!/bin/bash


#copy the first 4796 lines to train.tsvn from data.tsv
#skip the first line since it is the header
sed -n 2,4797p data.tsv>train.tsv

#copy the last 534 lines to test.tsv from data.tsv
tail -n 535 data.tsv>test.tsv
