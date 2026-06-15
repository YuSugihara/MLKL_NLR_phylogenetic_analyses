#!/usr/bin/env bash
set -euo pipefail

# Rebuild the final MLKL kinase-domain tree from the curated IPR011009 FASTA.
# Run from the project root.

input_fasta="results/sequences/80_all_mlkl_proteins_with_Pm13.IPR011009.fasta"
tree_dir="results/tree"
prefix="${tree_dir}/80_all_mlkl_proteins_with_Pm13.IPR011009.M400m150"

mkdir -p "${tree_dir}"

midroot() {
  python3 -c "import sys; from Bio import Phylo; tree = Phylo.read('$1', 'newick'); tree.root_at_midpoint(); Phylo.write(tree, sys.stdout, 'newick')"
}

seqkit seq -M 400 -m 150 "${input_fasta}" > "${prefix}.fasta"

mafft --maxiterate 1000 --localpair "${prefix}.fasta" \
  | seqtk seq -l0 \
  | tr ":" "_" \
  > "${prefix}.local_aln.fasta"

clipkit "${prefix}.local_aln.fasta" \
  -m gappy \
  -g 0.9 \
  -o "${prefix}.local_aln.clip.fasta"

fasttreemp "${prefix}.local_aln.clip.fasta" > "${prefix}.local_aln.clip.fasta.tree"

midroot "${prefix}.local_aln.clip.fasta.tree" > "${prefix}.local_aln.clip.fasta.midroot.tree"
