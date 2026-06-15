# MLKL phylogeny analysis

This directory contains the curated MLKL protein tables, MLKL-NLR linkage
tables, IPR011009 kinase-domain FASTA files, alignments, and trees used for the
MLKL phylogeny.

## Directory Layout

- `metadata/`: species metadata and InterPro target-domain IDs.
- `scripts/`: Python scripts and shell command records used in this analysis.
- `results/intermediate/`: intermediate files for MLKL detection and MLKL-NLR
  linkage. Parsed InterProScan tables are compressed as
  `00_ips_result_tables.zip`.
- `results/sequences/`: combined FASTA files used for MLKL kinase-domain tree
  building.
- `results/tree/`: tree inputs, alignments, Newick trees, annotation map, and
  clade lists.
- `results/tables/`: MLKL and MLKL-NLR tables, including versions filtered to
  the final tree sequence set.

## Key Outputs

- Midpoint-rooted MLKL tree:
  `results/tree/80_all_mlkl_proteins_with_Pm13.IPR011009.M400m150.local_aln.clip.fasta.midroot.tree`
- Trimmed alignment used for tree inference:
  `results/tree/80_all_mlkl_proteins_with_Pm13.IPR011009.M400m150.local_aln.clip.fasta`
- MLKL table filtered to the final tree sequence set:
  `results/tables/50_mlkl_table_filtered.tsv`
- MLKL-NLR pair tables filtered to the final tree sequence set:
  `results/tables/60_mlkl_nlr_pair_table_100kbp_filtered.tsv` and
  `results/tables/60_mlkl_nlr_pair_table_15kbp_filtered.tsv`
- Tree annotation map:
  `results/tree/80_all_mlkl_proteins_with_Pm13.IPR011009.M400m150.local_aln.clip.fasta.tree.map`

## Workflow

The steps below describe how the included MLKL tables, MLKL-NLR linkage tables,
and tree files were generated from domain annotation, protein FASTA, NLR
annotation, and genome annotation files. Genome annotation and NLR annotation
commands are documented separately in `../annotation/`. NLR candidates used for
MLKL-NLR linkage were identified with NLRtracker.

The command snippets show the working paths used in the analysis. In this
GitHub directory, the intermediate `00_` to `41_` outputs are organized under
`results/intermediate/`; `00_ips_result_tables/` is compressed as
`results/intermediate/00_ips_result_tables.zip` and expands back to the original
`00_ips_result_tables/` directory.

### Step 01: Identify MLKL proteins and extract IPR011009 regions

Inputs:

- `metadata/00_species_table.tsv`
- `metadata/target_id_list.txt`
- InterProScan GFF3 output
- Protein FASTA

Commands:

```bash
python3 scripts/00_reformat_interproscan_gff3.py "${interproscan_result}" \
  > results/00_ips_result_tables/${ncbi_id}.tsv

python3 scripts/10_target_fisher.py \
  metadata/target_id_list.txt \
  results/00_ips_result_tables/${ncbi_id}.tsv \
  > results/10_detected_MLKL_tables/${ncbi_id}_detected_mlkl.tsv

cut -f 1 results/10_detected_MLKL_tables/${ncbi_id}_detected_mlkl.tsv \
  > results/10_detected_MLKL_tables/${ncbi_id}_detected_mlkl.txt

samtools faidx \
  -r results/10_detected_MLKL_tables/${ncbi_id}_detected_mlkl.txt \
  "${proteome_fasta}" \
  | seqtk seq -l0 \
  > results/20_MLKL_seqs/$(basename "${proteome_file}" .fasta.gz)_detected_mlkl.fasta

samtools faidx \
  results/20_MLKL_seqs/$(basename "${proteome_file}" .fasta.gz)_detected_mlkl.fasta \
  ${ipr011009_regions} \
  | seqtk seq -l0 \
  > results/20_MLKL_seqs/$(basename "${proteome_file}" .fasta.gz)_detected_mlkl.IPR011009.fasta
```

Retained files from this step:

- Parsed InterProScan tables:
  `results/intermediate/00_ips_result_tables.zip`
- MLKL detection tables:
  `results/intermediate/10_detected_MLKL_tables/${ncbi_id}_detected_mlkl.tsv`
- MLKL protein FASTA files:
  `results/intermediate/20_MLKL_seqs/${ncbi_id}_detected_mlkl.fasta`
- MLKL IPR011009 FASTA files:
  `results/intermediate/20_MLKL_seqs/${ncbi_id}_detected_mlkl.IPR011009.fasta`
- Combined MLKL IPR011009 FASTA included in this repository:
  `results/sequences/22_all_mlkl_proteins.IPR011009.fasta`

### Step 02: Identify NLRs and MLKL-NLR linkage

Inputs:

- NLRtracker table
- Genome annotation GFF3
- MLKL protein ID list from Step 01

Commands:

The locus search was run for `distance=100` and `distance=15`.

```bash
awk -F'\t' '$2 == "NLR"' "${nlrtracker_result}" \
  | cut -f 1 \
  > results/30_NLR_list/${ncbi_id}_NLR_list.txt

awk '$3 == "CDS"' "${gff3}" \
  | gffread \
  > results/40_NLR_MLKL_group/${ncbi_id}_temp.gff3

python3 scripts/40_locus_group.py \
  results/40_NLR_MLKL_group/${ncbi_id}_temp.gff3 \
  100 \
  results/10_detected_MLKL_tables/${ncbi_id}_detected_mlkl.txt \
  results/30_NLR_list/${ncbi_id}_NLR_list.txt \
  > results/40_NLR_MLKL_group/${ncbi_id}_temp.gff3.100kbp_locus_group.tsv

python3 scripts/40_locus_group.py \
  results/40_NLR_MLKL_group/${ncbi_id}_temp.gff3 \
  15 \
  results/10_detected_MLKL_tables/${ncbi_id}_detected_mlkl.txt \
  results/30_NLR_list/${ncbi_id}_NLR_list.txt \
  > results/40_NLR_MLKL_group/${ncbi_id}_temp.gff3.15kbp_locus_group.tsv

cut -f 1 results/40_NLR_MLKL_group/${ncbi_id}_temp.gff3.${distance}kbp_locus_group.tsv \
  | sort \
  | uniq \
  > results/40_NLR_MLKL_group/${ncbi_id}_temp.gff3.${distance}kbp_mlkl_uniq_list.txt

cut -f 3 results/40_NLR_MLKL_group/${ncbi_id}_temp.gff3.${distance}kbp_locus_group.tsv \
  | sort \
  | uniq \
  > results/40_NLR_MLKL_group/${ncbi_id}_temp.gff3.${distance}kbp_nlr_uniq_list.txt

samtools faidx \
  -r results/40_NLR_MLKL_group/${ncbi_id}_temp.gff3.${distance}kbp_mlkl_uniq_list.txt \
  "${proteome_fasta}" \
  | seqtk seq -l0 \
  > results/40_NLR_MLKL_group/${ncbi_id}_temp.gff3.${distance}kbp_mlkl_uniq.fasta

samtools faidx \
  -r results/40_NLR_MLKL_group/${ncbi_id}_temp.gff3.${distance}kbp_nlr_uniq_list.txt \
  "${proteome_fasta}" \
  | seqtk seq -l0 \
  > results/40_NLR_MLKL_group/${ncbi_id}_temp.gff3.${distance}kbp_nlr_uniq.fasta
```

Retained files from this step:

- NLR ID lists:
  `results/intermediate/30_NLR_list/${ncbi_id}_NLR_list.txt`
- MLKL-NLR locus tables:
  `results/intermediate/40_NLR_MLKL_group/${ncbi_id}_temp.gff3.100kbp_locus_group.tsv`
  and
  `results/intermediate/40_NLR_MLKL_group/${ncbi_id}_temp.gff3.15kbp_locus_group.tsv`
- Unique MLKL and NLR protein ID lists from the locus tables:
  `results/intermediate/40_NLR_MLKL_group/${ncbi_id}_temp.gff3.${distance}kbp_mlkl_uniq_list.txt`
  and
  `results/intermediate/40_NLR_MLKL_group/${ncbi_id}_temp.gff3.${distance}kbp_nlr_uniq_list.txt`
- Unique MLKL and NLR FASTA files extracted from the protein FASTA:
  `results/intermediate/40_NLR_MLKL_group/${ncbi_id}_temp.gff3.${distance}kbp_mlkl_uniq.fasta`
  and
  `results/intermediate/40_NLR_MLKL_group/${ncbi_id}_temp.gff3.${distance}kbp_nlr_uniq.fasta`

The downstream formatted pair tables are
`results/tables/60_mlkl_nlr_pair_table_100kbp.tsv` and
`results/tables/60_mlkl_nlr_pair_table_15kbp.tsv`.

### Step 03: Merge MLKL-NLR locus outputs

The locus outputs from Step 02 were merged by distance threshold.
The merged files are retained here because they are the direct inputs used to
make the formatted `60_` pair tables.

Commands:

```bash
cat results/40_NLR_MLKL_group/*.100kbp_locus_group.tsv \
  > results/41_merged_locus_group/41_all_locus_group_100kbp.tsv

cat results/40_NLR_MLKL_group/*.100kbp_mlkl_uniq.fasta \
  > results/41_merged_locus_group/41_all_paired_mlkl_uniq_100kbp.fasta

cat results/40_NLR_MLKL_group/*.100kbp_nlr_uniq.fasta \
  > results/41_merged_locus_group/41_all_paired_nlr_uniq_100kbp.fasta

cat results/40_NLR_MLKL_group/*.15kbp_locus_group.tsv \
  > results/41_merged_locus_group/41_all_locus_group_15kbp.tsv

cat results/40_NLR_MLKL_group/*.15kbp_mlkl_uniq.fasta \
  > results/41_merged_locus_group/41_all_paired_mlkl_uniq_15kbp.fasta

cat results/40_NLR_MLKL_group/*.15kbp_nlr_uniq.fasta \
  > results/41_merged_locus_group/41_all_paired_nlr_uniq_15kbp.fasta
```

Retained files:

- `results/intermediate/41_merged_locus_group/41_all_locus_group_100kbp.tsv`
- `results/intermediate/41_merged_locus_group/41_all_locus_group_15kbp.tsv`
- `results/intermediate/41_merged_locus_group/41_all_paired_mlkl_uniq_100kbp.fasta`
- `results/intermediate/41_merged_locus_group/41_all_paired_mlkl_uniq_15kbp.fasta`
- `results/intermediate/41_merged_locus_group/41_all_paired_nlr_uniq_100kbp.fasta`
- `results/intermediate/41_merged_locus_group/41_all_paired_nlr_uniq_15kbp.fasta`

### Step 04: Format MLKL and MLKL-NLR tables

The retained final tables in `results/tables/` were generated from the MLKL
detection and locus-linkage outputs.

Representative commands:

```bash
cat results/10_detected_MLKL_tables/*_detected_mlkl.tsv \
  > results/tables/10_all_detected_mlkl.tsv

cat results/20_MLKL_seqs/*_detected_mlkl.fasta \
  > results/sequences/21_all_mlkl_proteins.fasta

cat results/20_MLKL_seqs/*_detected_mlkl.IPR011009.fasta \
  > results/sequences/22_all_mlkl_proteins.IPR011009.fasta

python3 scripts/50_format_mlkl_table.py \
  results/tables/10_all_detected_mlkl.tsv \
  results/sequences/21_all_mlkl_proteins.fasta \
  results/sequences/22_all_mlkl_proteins.IPR011009.fasta \
  > results/tables/50_mlkl_table.tsv
```

Included curated table outputs:

- `results/tables/50_mlkl_table.tsv`
- `results/tables/60_mlkl_nlr_pair_table_100kbp.tsv`
- `results/tables/60_mlkl_nlr_pair_table_15kbp.tsv`
- `results/tables/70_summary_table_100kbp.tsv`
- `results/tables/70_summary_table_15kbp.tsv`

The `60_` tables were generated from the retained Step 03 inputs:

```bash
python3 scripts/60_format_mlkl-nlr_pair_table.py \
  results/41_merged_locus_group/41_all_locus_group_100kbp.tsv \
  results/41_merged_locus_group/41_all_paired_mlkl_uniq_100kbp.fasta \
  results/41_merged_locus_group/41_all_paired_nlr_uniq_100kbp.fasta \
  > results/tables/60_mlkl_nlr_pair_table_100kbp.tsv

python3 scripts/60_format_mlkl-nlr_pair_table.py \
  results/41_merged_locus_group/41_all_locus_group_15kbp.tsv \
  results/41_merged_locus_group/41_all_paired_mlkl_uniq_15kbp.fasta \
  results/41_merged_locus_group/41_all_paired_nlr_uniq_15kbp.fasta \
  > results/tables/60_mlkl_nlr_pair_table_15kbp.tsv
```

In this GitHub directory, these inputs are stored under
`results/intermediate/41_merged_locus_group/`, and the formatted outputs are
stored under `results/tables/`.

`scripts/70_generate_summary_table.py` summarizes formatted MLKL-NLR tables
when a compact summary is needed.

### Step 05: Build the final MLKL kinase-domain tree

The tree-building commands are also recorded in
`scripts/80_build_final_mlkl_tree.sh`.

```bash
input_fasta="results/sequences/80_all_mlkl_proteins_with_Pm13.IPR011009.fasta"
tree_dir="results/tree"
prefix="${tree_dir}/80_all_mlkl_proteins_with_Pm13.IPR011009.M400m150"

cat \
  results/sequences/Pm13_WGO47752.1_IPR011009.fasta \
  results/sequences/22_all_mlkl_proteins.IPR011009.fasta \
  > "${input_fasta}"

seqkit seq -M 400 -m 150 "${input_fasta}" \
  > "${prefix}.fasta"

mafft --maxiterate 1000 --localpair "${prefix}.fasta" \
  | seqtk seq -l0 \
  | tr ":" "_" \
  > "${prefix}.local_aln.fasta"

clipkit "${prefix}.local_aln.fasta" \
  -m gappy \
  -g 0.9 \
  -o "${prefix}.local_aln.clip.fasta"

fasttreemp "${prefix}.local_aln.clip.fasta" \
  > "${prefix}.local_aln.clip.fasta.tree"

midroot() {
  python3 -c "import sys; from Bio import Phylo; tree = Phylo.read('$1', 'newick'); tree.root_at_midpoint(); Phylo.write(tree, sys.stdout, 'newick')"
}

midroot "${prefix}.local_aln.clip.fasta.tree" \
  > "${prefix}.local_aln.clip.fasta.midroot.tree"
```

Outputs:

- MLKL plus Pm13 IPR011009 FASTA:
  `results/sequences/80_all_mlkl_proteins_with_Pm13.IPR011009.fasta`
- Length-filtered tree input:
  `results/tree/80_all_mlkl_proteins_with_Pm13.IPR011009.M400m150.fasta`
- MAFFT alignment:
  `results/tree/80_all_mlkl_proteins_with_Pm13.IPR011009.M400m150.local_aln.fasta`
- ClipKIT-trimmed alignment:
  `results/tree/80_all_mlkl_proteins_with_Pm13.IPR011009.M400m150.local_aln.clip.fasta`
- FastTree output:
  `results/tree/80_all_mlkl_proteins_with_Pm13.IPR011009.M400m150.local_aln.clip.fasta.tree`
- Biopython midpoint-rooted tree:
  `results/tree/80_all_mlkl_proteins_with_Pm13.IPR011009.M400m150.local_aln.clip.fasta.midroot.tree`

## Curated Tree-Set Tables

The files below contain the MLKL and MLKL-NLR rows corresponding to the
sequence set retained in
`results/tree/80_all_mlkl_proteins_with_Pm13.IPR011009.M400m150.fasta`.

- `results/tables/50_mlkl_table_filtered.tsv`
- `results/tables/60_mlkl_nlr_pair_table_100kbp_filtered.tsv`
- `results/tables/60_mlkl_nlr_pair_table_15kbp_filtered.tsv`

The tree annotation map is retained as:

- `results/tree/80_all_mlkl_proteins_with_Pm13.IPR011009.M400m150.local_aln.clip.fasta.tree.map`

Tree coloring was performed with [Iroki](https://www.iroki.net/viewer) using
the tree annotation map.

## Notes

- The tree is referred to as an MLKL tree, but the aligned region is the
  IPR011009 kinase-domain region. Some proteins carry additional N-terminal or
  C-terminal domains.
- `GCA_030411765.1_CM059506.1_002082.1` is present in
  `results/sequences/22_all_mlkl_proteins.IPR011009.fasta` and
  `results/tables/50_mlkl_table.tsv`, but it is absent from the final tree
  input and filtered tables. Its IPR011009 region is 88 aa long, so it was
  removed by the `seqkit seq -M 400 -m 150` length filter in Step 05.
- The final tree was midpoint-rooted with Biopython.
