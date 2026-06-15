#! /usr/bin/env python3

import sys


input_gff3 = sys.argv[1]
threshold_kbp = int(sys.argv[2])
query_gene_list = [line.strip() for line in open(sys.argv[3]).readlines()]
target_gene_list = [line.strip() for line in open(sys.argv[4]).readlines()]

query_gene_list_dict = {}
target_gene_list_dict = {}

with open(input_gff3) as gff3:
    for line in gff3:
        line = line.rstrip()
        if line.startswith("#"):
            continue
        cols = line.split("\t")
        if cols[2] == "transcript":
            attribute = cols[8]
            gene_id = attribute.split(";")[0].split("=")[1]
            if gene_id in query_gene_list:
                if int(cols[4]) < int(cols[3]):
                    cols[3], cols[4] = cols[4], cols[3]
                query_gene_list_dict[gene_id] = (cols[0], int(cols[3]), int(cols[4]), cols[6])
            if gene_id in target_gene_list:
                if int(cols[4]) < int(cols[3]):
                    cols[3], cols[4] = cols[4], cols[3]
                target_gene_list_dict[gene_id] = (cols[0], int(cols[3]), int(cols[4]), cols[6])

for qk, qv in query_gene_list_dict.items():
    for tk, tv in target_gene_list_dict.items():
        if tv[0] == qv[0]:
            if tv[2] < qv[1] and (qv[1] - tv[2]) < 1000*threshold_kbp:
                if tv[3] == qv[3] and tv[3] == "+":
                    orientation = "NLR -> MLKL ->"
                elif tv[3] == qv[3] and tv[3] == "-":
                    orientation = "MLKL -> NLR ->"
                elif tv[3] != qv[3] and tv[3] == "+":
                    orientation = "MLKL -> <- NLR"
                elif tv[3] != qv[3] and tv[3] == "-":
                    orientation = "<- MLKL NLR ->"
                print(qk,
                      "{}:{}-{}({})".format(qv[0], qv[1], qv[2], qv[3]),
                      tk,
                      "{}:{}-{}({})".format(tv[0], tv[1], tv[2], tv[3]),
                      orientation,
                      str(int((qv[1] - tv[2]))),
                      sep="\t")
            elif qv[2] < tv[1] and (tv[1] - qv[2]) < 1000*threshold_kbp:
                if tv[3] == qv[3] and tv[3] == "+":
                    orientation = "MLKL -> NLR ->"
                elif tv[3] == qv[3] and tv[3] == "-":
                    orientation = "NLR -> MLKL ->"
                elif tv[3] != qv[3] and tv[3] == "+":
                    orientation = "<- MLKL NLR ->"
                elif tv[3] != qv[3] and tv[3] == "-":
                    orientation = "MLKL -> <- NLR"
                print(qk,
                      "{}:{}-{}({})".format(qv[0], qv[1], qv[2], qv[3]),
                      tk,
                      "{}:{}-{}({})".format(tv[0], tv[1], tv[2], tv[3]),
                      orientation,
                      str(int((tv[1] - qv[2]))),
                      sep="\t")

