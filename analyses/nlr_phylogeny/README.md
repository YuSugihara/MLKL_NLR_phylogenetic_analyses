# NLR NB-ARC phylogeny

This analysis builds a phylogeny from NLR NB-ARC domain sequences, including
NB-ARC FASTA files and NB-ARC sequences from NLRs linked to MLKL loci. The NLRs
represented here were identified with NLRtracker.

## File Map

| Step | Files used | Purpose |
| --- | --- | --- |
| Metadata | `metadata/nlr_dataset.txt` | Assemblies represented by the NB-ARC FASTA files |
| NB-ARC FASTA | `results/sequences/nlr_NB-ARC_fasta/*_NBARC.fasta` | Input NB-ARC sequences by assembly |
| MLKL-paired NB-ARC FASTA | `results/sequences/nlr_pared_with_mlkl_100k_NBARC.fasta`, `results/sequences/nlr_pared_with_mlkl_15k_NBARC.fasta` | NB-ARC sequences from NLRs paired with MLKL candidates |
| Combined filtered FASTA | `results/sequences/all_nlr_NBARC.M400m200.fasta` | M400m200 filtered and deduplicated NB-ARC sequence set |
| Trimmed alignment | `results/tree/all_nlr_NBARC.M400m200.famsa_aln.clip.fasta` | ClipKIT-trimmed FAMSA alignment used by FastTree |
| Unrooted tree | `results/tree/all_nlr_NBARC.M400m200.famsa_aln.clip.fasta.tree` | FastTree output |
| Midpoint-rooted tree | `results/tree/all_nlr_NBARC.M400m200.famsa_aln.clip.fasta.midroot.tree` | NLR NB-ARC tree |
| Tree map | `results/tree/all_nlr_NBARC.M400m200.famsa_aln.clip.fasta.tree.map` | Annotation map for tree tips |

## Workflow

### Step 01: Combine and filter NB-ARC sequences

Inputs:

- `results/sequences/nlr_NB-ARC_fasta/*_NBARC.fasta`
- `results/sequences/nlr_pared_with_mlkl_100k_NBARC.fasta`
- `results/sequences/nlr_pared_with_mlkl_15k_NBARC.fasta`

Command:

```bash
cat \
  results/sequences/nlr_NB-ARC_fasta/*_NBARC.fasta \
  results/sequences/nlr_pared_with_mlkl_*k_NBARC.fasta \
  | seqkit seq -M 400 -m 200 \
  | seqkit rmdup -n \
  | sed 's/(//g' \
  | sed 's/)//g' \
  > results/sequences/all_nlr_NBARC.M400m200.fasta
```

Output:

- `results/sequences/all_nlr_NBARC.M400m200.fasta`

### Step 02: Align, trim, infer, and midpoint-root the tree

The tree-building commands are also recorded in
`scripts/10_build_nlr_tree.sh`.

```bash
prefix="results/tree/all_nlr_NBARC.M400m200"

famsa \
  -t 4 \
  -refine_mode on \
  results/sequences/all_nlr_NBARC.M400m200.fasta \
  "${prefix}.famsa_aln.fasta"

clipkit "${prefix}.famsa_aln.fasta" \
  -m gappy \
  -g 0.9 \
  -o "${prefix}.famsa_aln.clip.fasta"

fasttreemp "${prefix}.famsa_aln.clip.fasta" \
  > "${prefix}.famsa_aln.clip.fasta.tree"

midroot() {
  python3 -c "import sys; from Bio import Phylo; tree = Phylo.read('$1', 'newick'); tree.root_at_midpoint(); Phylo.write(tree, sys.stdout, 'newick')"
}

midroot "${prefix}.famsa_aln.clip.fasta.tree" \
  > "${prefix}.famsa_aln.clip.fasta.midroot.tree"
```

Retained outputs:

- ClipKIT-trimmed alignment:
  `results/tree/all_nlr_NBARC.M400m200.famsa_aln.clip.fasta`
- FastTree output:
  `results/tree/all_nlr_NBARC.M400m200.famsa_aln.clip.fasta.tree`
- Biopython midpoint-rooted tree:
  `results/tree/all_nlr_NBARC.M400m200.famsa_aln.clip.fasta.midroot.tree`

The untrimmed FAMSA alignment is generated as
`results/tree/all_nlr_NBARC.M400m200.famsa_aln.fasta` and is used as the direct
input to ClipKIT.

## Counts

- `results/sequences/all_nlr_NBARC.M400m200.fasta`: 10,858 sequences
- `results/tree/all_nlr_NBARC.M400m200.famsa_aln.clip.fasta`: 10,858 sequences
