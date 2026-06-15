#!/usr/bin/env bash
set -euo pipefail

# Build the broad kinase-domain tree from the curated IPR011009 FASTA.
# Run from analyses/kinase_domain_tree.

input_fasta="results/sequences/kinase_IPR011009.fasta"
prefix="results/tree/kinase_IPR011009.M400m150"

mkdir -p results/tree

seqkit seq -M 400 -m 150 "${input_fasta}" \
  | seqkit rmdup -n \
  > "results/sequences/kinase_IPR011009.M400m150.fasta"

famsa -t 4 \
  -refine_mode on \
  -gt upgma \
  "results/sequences/kinase_IPR011009.M400m150.fasta" \
  "${prefix}.famsa_aln.fasta"

clipkit "${prefix}.famsa_aln.fasta" \
  -m gappy \
  -g 0.7 \
  -o "${prefix}.famsa_aln.clip.fasta"

fasttreemp "${prefix}.famsa_aln.clip.fasta" > "${prefix}.famsa_aln.clip.fasta.tree"
