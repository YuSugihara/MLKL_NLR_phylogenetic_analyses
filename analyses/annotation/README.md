# Genome annotation and NLR/domain detection

This directory documents the upstream annotation steps that generated protein
and domain inputs used by the MLKL, kinase-domain, and NLR phylogenetic
analyses. The raw genome FASTA files, full Helixer outputs, and raw NLRtracker
directories are not included.

The upstream Helixer/NLRtracker annotation dataset is archived on Zenodo:
https://doi.org/10.5281/zenodo.20703384. Please cite this DOI when using the
annotation files.

## File Map

| File | Purpose |
| --- | --- |
| `metadata/assembly_list.txt` | Assemblies represented in the downstream analyses |
| `metadata/assembly_species.tsv` | Assembly-to-species/taxonomic-lineage table |
| `results/tables/busco_liliopsida_odb10_results.tsv` | BUSCO results for the Helixer-predicted protein FASTA files |
| `results/tables/busco_liliopsida_odb10_summary.tsv` | BUSCO results with species lineage information |

## Helixer

Helixer was used to predict gene models from genome FASTA files with this
command structure:

```bash
Helixer.py \
  --lineage land_plant \
  --species GCF_001433935.1 \
  --fasta-path GCF_001433935.1_IRGSP-1.0_genomic.fna \
  --gff-output-path GCF_001433935.1_IRGSP-1.0_genomic_helixer.gff \
  --temporary-dir helixer_temp/
```

Helixer was run with the
`helixer-docker_helixer_v0.3.3_cuda_11.8.0-cudnn8.sif` Singularity image and
the parameters below.

| Setting | Value |
| --- | --- |
| Helixer version | `0.3.3` |
| lineage | `land_plant` |
| model | `land_plant_v0.3_a_0080.h5` |
| config | `config/helixer_config.yaml` |
| batch size | `32` |
| compression | `gzip` |
| subsequence length | `64152` |
| overlap core length | `48114` |
| overlap offset | `32076` |
| window size | `100` |
| edge threshold | `0.1` |
| peak threshold | `0.8` |
| minimum coding length | `100` |
| temporary directory | `helixer_temp/` |
| multiprocessing | enabled |
| overlap mode | enabled |
| geenuff version | `0.3.2` |

Protein and CDS FASTA files were generated from the Helixer GFF3 output, for
example:

```bash
gffread GCF_001433935.1_IRGSP-1.0_genomic_helixer.gff \
  -g GCF_001433935.1_IRGSP-1.0_genomic.fna \
  -x GCF_001433935.1_IRGSP-1.0_genomic_helixer_cds.fasta
```

```bash
gffread GCF_001433935.1_IRGSP-1.0_genomic_helixer.gff \
  -g GCF_001433935.1_IRGSP-1.0_genomic.fna \
  -y GCF_001433935.1_IRGSP-1.0_genomic_helixer_protein.fasta
```

The protein FASTA files were used for NLRtracker and InterProScan. The CDS FASTA
files were generated as part of the annotation dataset, although they were not
used directly for the final phylogenetic analyses in this repository.

## NLRtracker

NLRtracker was run on the Helixer-predicted protein FASTA files. The retained
execution scripts show this command structure:

```bash
NLRtracker.sh \
  -s GCF_001433935.1_IRGSP-1.0_genomic_helixer_protein.fasta \
  -o nlrtracker_GCF_001433935.1_IRGSP-1.0_genomic_helixer_protein \
  -d NLRtracker/module/InterProScan_5.67-99.0.list \
  -c 50
```

The `-d` option points to the NLRtracker InterProScan list file. The retained
InterProScan GFF3 outputs report InterProScan version `5.67-99.0`.

## BUSCO

BUSCO was run on the Helixer-predicted protein FASTA files using the
`liliopsida_odb10` lineage dataset:

```bash
busco \
  -m proteins \
  -l liliopsida_odb10 \
  -i GCF_001433935.1_IRGSP-1.0_genomic_helixer_protein.fasta \
  -o busco_GCF_001433935.1 \
  -c 60
```

The curated BUSCO tables included here are:

- `results/tables/busco_liliopsida_odb10_results.tsv`: BUSCO result columns for
  the assemblies used in the downstream analyses.
- `results/tables/busco_liliopsida_odb10_summary.tsv`: the same BUSCO result
  columns together with the corresponding species lineage fields.
- `metadata/assembly_species.tsv`: assembly accession, species/taxon label, and
  lineage fields used to interpret the BUSCO table. The `Lineage (reformat)`
  column was generated with taxonkit.
