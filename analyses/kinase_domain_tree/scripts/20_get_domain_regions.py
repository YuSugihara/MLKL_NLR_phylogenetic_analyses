#! /usr/bin/env python3

import sys

input_table = sys.argv[1]
query_string = sys.argv[2]

with open(input_table, "r") as input_table:
    for line in input_table.readlines():
        line = line.rstrip("\n")
        cols = line.split("\t")
        interproscan_ids = cols[2].split(";")
        for interproscan_id in interproscan_ids:
            if query_string in interproscan_id:
                print(interproscan_id.replace("SUPERFAMILY_IPR011009", cols[0]))
        