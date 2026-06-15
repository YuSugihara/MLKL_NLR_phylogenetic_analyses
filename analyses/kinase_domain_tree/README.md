# Kinase-domain tree

This analysis builds a tree from proteins identified by InterProScan as
containing IPR011009. The focal monocot assemblies are:

- `GCF_001433935.1`: Oryza sativa
- `GCA_005286985.2`: Setaria viridis
- `GCA_032878535.1`: Musa acuminata

The combined FASTA also includes the MLKL/Pm13 kinase-domain sequence set used
for comparison.

## File Map

| Step | Files used | Purpose |
| --- | --- | --- |
| Metadata | `metadata/kinase_dataset.txt` | Assemblies included in this analysis |
| Metadata | `metadata/target_id_list.txt` | InterPro target ID used for selecting IPR011009 proteins |
| Domain detection scripts | `scripts/00_reformat_interproscan_gff3.py`, `scripts/10_target_fisher.py`, `scripts/20_get_domain_regions.py` | Parse InterProScan output, select IPR011009 proteins, and define IPR011009 coordinates |
| Detected kinase tables | `results/tables/*_detected_kinase.tsv` | Proteins identified with IPR011009 |
| Domain-region tables | `results/tables/*_detected_kinase_regions.tsv` | IPR011009 coordinates used for FASTA extraction |
| Combined kinase FASTA | `results/sequences/kinase_IPR011009.fasta` | Combined IPR011009 FASTA before length filtering and deduplication |
| Filtered FASTA | `results/sequences/kinase_IPR011009.M400m150.fasta` | Sequence set retained for the kinase-domain tree |
| Trimmed alignment | `results/tree/kinase_IPR011009.M400m150.famsa_aln.clip.fasta` | ClipKIT-trimmed FAMSA alignment used by FastTree |
| Tree | `results/tree/kinase_IPR011009.M400m150.famsa_aln.clip.fasta.tree` | Kinase-domain tree |
| Tree map | `results/tree/kinase_IPR011009.M400m150.famsa_aln.clip.fasta.tree.map` | Annotation map for tree tips |

## Workflow

### Step 01: Identify IPR011009 proteins

Inputs:

- `metadata/kinase_dataset.txt`
- `metadata/target_id_list.txt`
- InterProScan GFF3 output

Scripts:

- `scripts/00_reformat_interproscan_gff3.py`: converts InterProScan GFF3 output
  into tabular format.
- `scripts/10_target_fisher.py`: selects proteins containing the target
  InterPro ID.
- `scripts/20_get_domain_regions.py`: extracts the IPR011009 coordinate ranges
  used for FASTA extraction.

Representative commands:

```bash
python3 scripts/00_reformat_interproscan_gff3.py "${interproscan_result}" \
  > results/tables/${ncbi_id}_interproscan.tsv

python3 scripts/10_target_fisher.py \
  metadata/target_id_list.txt \
  results/tables/${ncbi_id}_interproscan.tsv \
  > results/tables/${ncbi_id}_detected_kinase.tsv

python3 scripts/20_get_domain_regions.py \
  results/tables/${ncbi_id}_detected_kinase.tsv \
  SUPERFAMILY_IPR011009 \
  > results/tables/${ncbi_id}_detected_kinase_regions.tsv
```

The parsed InterProScan table represented here as
`results/tables/${ncbi_id}_interproscan.tsv` is the same per-assembly table as
`00_ips_result_tables/${ncbi_id}.tsv` in
`../mlkl_phylogeny/results/intermediate/00_ips_result_tables.zip`; the kinase
workflow uses only the three focal assemblies listed above.

Included outputs:

- `results/tables/GCF_001433935.1_detected_kinase.tsv`
- `results/tables/GCF_001433935.1_detected_kinase_regions.tsv`
- `results/tables/GCA_005286985.2_detected_kinase.tsv`
- `results/tables/GCA_005286985.2_detected_kinase_regions.tsv`
- `results/tables/GCA_032878535.1_detected_kinase.tsv`
- `results/tables/GCA_032878535.1_detected_kinase_regions.tsv`

### Step 02: Build the kinase-domain tree

The tree-building commands are also recorded in
`scripts/30_build_kinase_tree.sh`.

```bash
input_fasta="results/sequences/kinase_IPR011009.fasta"
prefix="results/tree/kinase_IPR011009.M400m150"

seqkit seq -M 400 -m 150 "${input_fasta}" \
  | seqkit rmdup -n \
  > results/sequences/kinase_IPR011009.M400m150.fasta

famsa \
  -t 4 \
  -refine_mode on \
  -gt upgma \
  results/sequences/kinase_IPR011009.M400m150.fasta \
  "${prefix}.famsa_aln.fasta"

clipkit "${prefix}.famsa_aln.fasta" \
  -m gappy \
  -g 0.7 \
  -o "${prefix}.famsa_aln.clip.fasta"

fasttreemp "${prefix}.famsa_aln.clip.fasta" \
  > "${prefix}.famsa_aln.clip.fasta.tree"
```

Retained outputs:

- Length-filtered and deduplicated FASTA:
  `results/sequences/kinase_IPR011009.M400m150.fasta`
- ClipKIT-trimmed alignment:
  `results/tree/kinase_IPR011009.M400m150.famsa_aln.clip.fasta`
- FastTree output:
  `results/tree/kinase_IPR011009.M400m150.famsa_aln.clip.fasta.tree`

The untrimmed FAMSA alignment is generated as
`results/tree/kinase_IPR011009.M400m150.famsa_aln.fasta` and is used as the
direct input to ClipKIT.

## Counts

- `results/sequences/kinase_IPR011009.fasta`: 5,268 sequences
- `results/sequences/kinase_IPR011009.M400m150.fasta`: 4,947 sequences
- `results/tree/kinase_IPR011009.M400m150.famsa_aln.clip.fasta`: 4,947 sequences
