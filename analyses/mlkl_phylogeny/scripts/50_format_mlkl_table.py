#! /usr/bin/env python3

import sys
from Bio import SeqIO


input_table = sys.argv[1]
input_full_length_fasta = sys.argv[2]
input_kinase_domain_fasta = sys.argv[3]

record_full_length_dict = SeqIO.to_dict(SeqIO.parse(input_full_length_fasta, 'fasta'))
record_kinase_domain_dict = SeqIO.to_dict(SeqIO.parse(input_kinase_domain_fasta, 'fasta'))

with open(input_table) as f:
    for line in f:
        line = line.rstrip("\n")
        cols = line.split("\t")
        protein_id = cols[0]
        ncbi_id = "_".join(protein_id.split("_")[0:2])
        kinase_domain_line = [str(v.seq) for k, v in record_kinase_domain_dict.items() if protein_id in k]
        if len(kinase_domain_line) > 2:
            print("Error: more than 2 kinase domains found for", protein_id, file=sys.stderr)
        print(ncbi_id, line, record_full_length_dict[protein_id].seq, "\t".join(kinase_domain_line), sep="\t")
