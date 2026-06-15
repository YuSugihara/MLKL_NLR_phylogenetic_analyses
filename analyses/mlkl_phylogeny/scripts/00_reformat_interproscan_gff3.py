#! /usr/bin/env python3

import sys
import pandas as pd


input_interproscan_gff3_file = sys.argv[1]

def join_lists(x):
    x = list(x)
    if len(x) > 0:
        return ';'.join(map(str, list(x)))
    else:
        return ""

with open(input_interproscan_gff3_file, 'r') as f:
    annotation_dict = {}
    for line in f:
        if line.startswith("#"):
            continue
        else:
            cols = line.strip().split("\t")
            protein_id = cols[0]
            if len(cols) < 9:
                continue
            database = cols[1]
            attribute = cols[8]
            if protein_id not in annotation_dict:
                annotation_dict[protein_id] = {"InterPro": [], 
                                               "Pfam": [], 
                                               "Gene3D": [], 
                                               "SUPERFAMILY": [],
                                               "SMART":[],
                                               "ProSiteProfiles": [],
                                               "CDD": [],
                                               "PRINTS": [],
                                               }
            if "Name=" in attribute:
                name = attribute.split("Name=")[1].split(";")[0]
                name = name + ":" + cols[3] + "-" + cols[4]
                if name.startswith("G3DSA"):
                    annotation_dict[protein_id]["Gene3D"].append(name.replace("G3DSA:", ""))
                elif name.startswith("SSF"):
                    annotation_dict[protein_id]["SUPERFAMILY"].append(name)
                elif name.startswith("SM"):
                    annotation_dict[protein_id]["SMART"].append(name)
                elif name.startswith("PS"):
                    annotation_dict[protein_id]["ProSiteProfiles"].append(name)
                elif name.startswith("PF"):
                    annotation_dict[protein_id]["Pfam"].append(name)
                elif name.startswith("cd"):
                    annotation_dict[protein_id]["CDD"].append(name)
                elif name.startswith("PR"):
                    annotation_dict[protein_id]["PRINTS"].append(name)
                else:
                    print("Unknown domain type:", name, file=sys.stderr)
            if 'Dbxref="InterPro:' in attribute:
                interproscan_id = attribute.split(';Dbxref="InterPro:')[1].split('"')[0]
                interproscan_id = "{}_{}:{}-{}".format(database, interproscan_id, cols[3], cols[4])
                annotation_dict[protein_id]["InterPro"].append(interproscan_id)

df = pd.DataFrame.from_dict(annotation_dict, orient='index')
df.index.name = 'seqname'
df.map(join_lists).to_csv(sys.stdout, sep="\t")
