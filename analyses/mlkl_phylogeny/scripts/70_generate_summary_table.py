#! /usr/bin/env python3

import os
import sys
import glob


input_species_table = {line.split("\t")[0]: line.split("\t")[1].rstrip("\n") for line in open(sys.argv[1]).readlines()}
distance = sys.argv[2]
result_dirname = sys.argv[3]

for k, v in input_species_table.items():
    n_mlkl = len([line for line in open(f"{result_dirname}/10_detected_MLKL_tables/{k}_detected_mlkl.txt").readlines()])
    n_nlr = len([line for line in open(f"{result_dirname}/30_NLR_list/{k}_NLR_list.txt").readlines()])

    locus_group_table = os.path.basename(glob.glob(f"{result_dirname}/40_NLR_MLKL_group/{k}*.{distance}kbp_locus_group.tsv")[0])
    pair_mlkl_list = os.path.basename(glob.glob(f"{result_dirname}/40_NLR_MLKL_group/{k}*.{distance}kbp_mlkl_uniq_list.txt")[0])
    pair_nlr_list = os.path.basename(glob.glob(f"{result_dirname}/40_NLR_MLKL_group/{k}*.{distance}kbp_nlr_uniq_list.txt")[0])

    n_pair = len([line for line in open(f"{result_dirname}/40_NLR_MLKL_group/{locus_group_table}").readlines()])
    n_paired_mlkl = len([line for line in open(f"{result_dirname}/40_NLR_MLKL_group/{pair_mlkl_list}").readlines() if line.split("\t")[0] != ""])
    n_paired_nlr = len([line for line in open(f"{result_dirname}/40_NLR_MLKL_group/{pair_nlr_list}").readlines() if line.split("\t")[0] != ""])
    print(k, v, n_mlkl, n_nlr, n_pair, n_paired_mlkl, n_paired_nlr, sep="\t")
