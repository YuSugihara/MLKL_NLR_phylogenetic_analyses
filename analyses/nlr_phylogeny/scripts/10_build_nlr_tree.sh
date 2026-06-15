#!/usr/bin/env bash
set -euo pipefail

# Build the all-NLR NB-ARC tree from curated per-assembly and MLKL-paired FASTA.
# Run from analyses/nlr_phylogeny.

prefix="results/tree/all_nlr_NBARC.M400m200"

mkdir -p results/tree

cat results/sequences/nlr_NB-ARC_fasta/*_NBARC.fasta \
    results/sequences/nlr_pared_with_mlkl_*k_NBARC.fasta \
  | seqkit seq -M 400 -m 200 \
  | seqkit rmdup -n \
  | sed 's/(//g' \
  | sed 's/)//g' \
  > results/sequences/all_nlr_NBARC.M400m200.fasta

famsa -t 4 \
  -refine_mode on \
  results/sequences/all_nlr_NBARC.M400m200.fasta \
  "${prefix}.famsa_aln.fasta"

clipkit "${prefix}.famsa_aln.fasta" \
  -m gappy \
  -g 0.9 \
  -o "${prefix}.famsa_aln.clip.fasta"

fasttreemp "${prefix}.famsa_aln.clip.fasta" > "${prefix}.famsa_aln.clip.fasta.tree"

midroot() {
  python3 -c "import sys; from Bio import Phylo; tree = Phylo.read('$1', 'newick'); tree.root_at_midpoint(); Phylo.write(tree, sys.stdout, 'newick')"
}

midroot "${prefix}.famsa_aln.clip.fasta.tree" > "${prefix}.famsa_aln.clip.fasta.midroot.tree"
