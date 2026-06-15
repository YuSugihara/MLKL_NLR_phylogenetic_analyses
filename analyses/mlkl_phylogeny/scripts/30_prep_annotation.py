#! /usr/bin/env python3

import sys
import glob
from Bio import SeqIO


detected_protein_tables = glob.glob("{}/*.tsv".format(sys.argv[1]))
fasta_file = sys.argv[2]

n_terminal_domain_dict = {}
for detected_protein_table in sorted(detected_protein_tables):
    with open(detected_protein_table, 'r') as f:
        for line in f:
            n_terminal_domain = ""
            line = line.rstrip()
            cols = line.split('\t')
            protein_id = cols[0]
            if "IPR036537" in line:
                n_terminal_domain += "1,"
            else:
                n_terminal_domain += "0,"
            if "IPR045766" in line:
                n_terminal_domain += "1,"
            else:
                n_terminal_domain += "0,"
            if "IPR010632" in line:
                n_terminal_domain += "1"
            else:
                n_terminal_domain += "0"
            n_terminal_domain_dict[protein_id] = n_terminal_domain

records = SeqIO.parse(fasta_file, 'fasta')
for record in records:
    protein_id = "_".join(record.id.split("_")[:-1])
    print(record.id, n_terminal_domain_dict[protein_id], sep=",")

        