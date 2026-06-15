# MLKL, kinase-domain, and NLR phylogenetic analyses

This repository contains three related phylogenetic analyses for MLKL
proteins, broader kinase-domain proteins, and NLR NB-ARC domains. It also
includes annotation notes for the Helixer, NLRtracker, and InterProScan
steps that generated inputs used by those analyses.

## Analyses

| Analysis | Directory | Contents |
| --- | --- | --- |
| MLKL kinase-domain phylogeny | [`analyses/mlkl_phylogeny/`](analyses/mlkl_phylogeny/) | MLKL candidate tables, MLKL-NLR pair tables, curated kinase-domain FASTA files, alignments, trees, and scripts |
| Broad kinase-domain tree | [`analyses/kinase_domain_tree/`](analyses/kinase_domain_tree/) | IPR011009 protein/domain tables, combined kinase-domain FASTA files, alignment, tree, tree map, and scripts |
| NLR NB-ARC phylogeny | [`analyses/nlr_phylogeny/`](analyses/nlr_phylogeny/) | NB-ARC FASTA files, MLKL-paired NLR sequence sets, alignments, trees, and scripts |

## Annotation Notes

| Step | Directory | What is documented |
| --- | --- | --- |
| Genome annotation and NLR/domain detection | [`analyses/annotation/`](analyses/annotation/) | Helixer command example and log-derived settings, NLRtracker command example, and InterProScan version |

Each analysis directory is self-contained and has its own README describing the
files used at each step.

## Repository Structure

```text
analyses/
  mlkl_phylogeny/
    metadata/
    scripts/
    results/
  kinase_domain_tree/
    metadata/
    scripts/
    results/
  nlr_phylogeny/
    metadata/
    scripts/
    results/
  annotation/
    metadata/
    results/
```

## Software

The versions below were identified from the recorded conda environment, retained
logs, or output file headers.

| Tool | Version |
| --- | --- |
| Python | 3.10.14 |
| Biopython | 1.83 |
| pandas | 2.2.1 |
| seqkit | 2.8.1 |
| seqtk | 1.4 |
| samtools | 1.20 |
| gffread | 0.12.7 |
| FAMSA | 2.2.2 |
| MAFFT | 7.525 |
| ClipKIT | 2.3.0 |
| FastTree | 2.1.11 |
| PhyKIT | 1.19.3 |
| pyfastx | 2.1.0 |
| Helixer | 0.3.3 |
| geenuff | 0.3.2 |
| InterProScan | 5.67-99.0 |
| NLRtracker | 1.0.3 |
| BUSCO | 5.7.1 |
| pigz | 2.8 |
| taxonkit | 0.16.0 |

Additional Python package dependencies used by the scripts are listed in
`requirements.txt`.

Install the command-line tools separately, for example with Conda/Bioconda.
