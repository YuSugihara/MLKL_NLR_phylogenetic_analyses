#! /usr/bin/env python3

import sys


target_id_file = sys.argv[1]
target_table_file = sys.argv[2]

target_id_dict = {i:line.rstrip("\n").split(",") for i, line in enumerate(open(target_id_file, 'r').readlines())}

def check_target_id(target_id_dict, line):
    detected_ids = {i:[] for i, target_ids in target_id_dict.items()}
    for i, target_ids in target_id_dict.items():
        for target_id in target_ids:
            if target_id in line:
                detected_ids[i].append(target_id)
    return detected_ids

with open(target_table_file, 'r') as f:
    for line in f:
        line = line.rstrip("\n")
        cols = line.split("\t")
        detected_ids = check_target_id(target_id_dict, line)
        if min([len(ids) for ids in detected_ids.values()]) > 0:
            detected_ids_line = {i:",".join(ids) for i, ids in detected_ids.items()}
            print(cols[0], "\t".join(detected_ids_line.values()), "\t".join(cols[1:]), sep="\t")
