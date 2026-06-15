#! /usr/bin/env python3

import sys
from Bio import SeqIO


input_table = sys.argv[1]
input_mlkl_fasta = sys.argv[2]
input_nlr_fasta = sys.argv[3]

record_mlkl_dict = SeqIO.to_dict(SeqIO.parse(input_mlkl_fasta, 'fasta'))
record_nlr_dict = SeqIO.to_dict(SeqIO.parse(input_nlr_fasta, 'fasta'))

with open(input_table) as f:
    for line in f:
        line = line.rstrip("\n")
        cols = line.split("\t")
        mlkl_protein_id = cols[0]
        nlr_protein_id = cols[2]
        ncbi_id = "_".join(mlkl_protein_id.split("_")[0:2])
        print(ncbi_id, "\t".join(cols[0:2]), record_mlkl_dict[mlkl_protein_id].seq, "\t".join(cols[2:4]), record_nlr_dict[nlr_protein_id].seq, "\t".join(cols[4:]), sep="\t")
