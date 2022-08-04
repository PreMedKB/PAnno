<p align="left" margin-bottom="-2rem"> <img src="https://raw.githubusercontent.com/premedkb/panno/main/docs/images/panno_logo.png" width="40%"/> </p>

## PAnno: A Pharmacogenomics Annotation Tool for Clinical Genomic Testing

![PyPI](https://img.shields.io/pypi/v/panno?color=pink)  ![Conda](https://img.shields.io/conda/v/lyaqing/panno?color=blue&label=conda) ![AppVeyor](https://img.shields.io/appveyor/build/PreMedKB/PAnno)

PAnno reports drug responses and prescribing recommendations by parsing the germline variant call format (VCF) file from NGS and the population to which the individual belongs.

## Installation

***Prerequisite: To ensure smooth installation and usage, [Python >= 3.7](https://docs.conda.io/en/latest/miniconda.html#system-requirements) (#1 and #3 below), or [Miniconda/Anaconda](https://docs.conda.io/en/latest/miniconda.html#system-requirements) (#2 below) are required.***

1. You can install PAnno from [PyPI](https://pypi.org/project/panno/) using pip as follows:
```Shell
pip install panno==0.2.3
```

2. Alternatively, you can create a environment using [Conda](https://anaconda.org/lyaqing/panno).
```Shell
conda create -n PAnno panno=0.2.3 -c lyaqing -c conda-forge -c bioconda
conda activate PAnno
```

3. If you would like the development version instead, the command is:
```Shell
pip install --upgrade --force-reinstall git+https://github.com/PreMedKB/PAnno.git
# Or download first and install later
git clone https://github.com/PreMedKB/PAnno.git; pip install PAnno
```

## Usage
Once installed, you can use PAnno by navigating to your VCF file and entering the corresponding three-letter abbreviation of the population:

```Shell
panno -s sample_id -i germline_vcf -p population -o outdir
```

* Required arguments
```Shell
-s, --sample_id TEXT            Sample ID that will be displayed in the PAnno report.

-i, --germline_vcf TEXT         Unannotated VCF file, preferably germline variant.

-p, --population [AAC|AME|EAS|EUR|LAT|NEA|OCE|SAS|SSA]
                                The three-letter abbreviation for biogeographic groups:
                                AAC (African American/Afro-Caribbean), AME (American),
                                EAS (East Asian), EUR (European), LAT (Latino),
                                NEA (Near Eastern), OCE (Oceanian),
                                SAS (Central/South Asian), SSA (Sub-Saharan African).

-o, --outdir TEXT               Create report in the specified output path.
```

### Input data
#### 1. Germline VCF file

PAnno directly uses the NGS-derived germline VCF file as input and assumes it has undergone quality control. Therefore, if the VCF file is of poor quality, inaccurate genotypes and inappropriate clinical recommendations may be reported.

PAnno requires the VCF file aligned to the GRCh38 reference genome given the increasing generality and the built-in diplotype definition dependency version.


#### 2. Population
There are nine biogeographic groups supported by PAnno. Please use the ***three-letter abbreviation*** as input. This is to prevent errors caused by special symbols such as spaces.

**AAC** (African American/Afro-Caribbean), **AME** (American), **EAS** (East Asian), **EUR** (European), **LAT** (Latino), **NEA** (Near Eastern), **OCE** (Oceanian), **SAS** (Central/South Asian), **SSA** (Sub-Saharan African).

More information is available at https://www.pharmgkb.org/page/biogeographicalGroups.

### Output data

The report is created in `${sample_id}.html` at the `outdir` by default.

For more detailed instructions, run `panno -h`.

## Examples
We analyzed the germline variants of 88 samples from the GeT-RM PGx study using PAnno.

* The VCF files are available at https://github.com/PreMedKB/PAnno-analysis/tree/main/vcf.
* The PAnno reports are available at https://github.com/PreMedKB/PAnno-analysis/tree/main/report.

Here is a snapshot from the PAnno report:
<p align="center">
<img src="https://raw.githubusercontent.com/premedkb/panno/main/docs/images/panno_report.png" width="100%" />
</p>

## Core Components
PAnno provides an end-to-end clinical pharmacogenomics decision support solution by resolving, annotating, and reporting germline variants in individuals.

<p align="center">
<img src="https://raw.githubusercontent.com/premedkb/panno/main/docs/images/architecture.png" width="40%" />
</p>

### PAnno ranking model for diplotype inference
Genotype resolution aims to extract the alleles of small variants (SNVs and Indels) and the diplotypes related to PGx from the user-submitted VCF file. PAnno processes the “GT” information to obtain all relevant single-locus genotypes. Afterwards, the genotypes of small variants will be passed to clinical annotation directly, while the genotypes related to diplotype definitions will be passed to the PAnno ranking model.

The ranking model dedicated to inferring diplotype developed based on allele definitions and population allele frequencies was introduced in PAnno. The predictive performance for diplotype was validated in comparison with four similar tools using the consensus diplotype data of the Genetic Testing Reference Materials Coordination Program (GeT-RM) as ground truth.
<p align="center">
<img src="https://raw.githubusercontent.com/premedkb/panno/main/docs/images/diplotype_inference.png" width="80%" />
</p>

### PAnno annotation method for predicting drug response at individual level
An annotation method was further proposed to summarize ***the drug response level*** (<b>decreased</b>, <b>moderate</b>, and <b>increased</b>) and ***the level of clinical evidence*** (<b>A</b> and <b>B</b>) for the resolved genotypes.

PAnno annotation method translates the literal PGx knowledge about genotypes into quantitative scores. The association between multiple genotypes and a single drug is then further translated into an individual-level association with this drug. Then the individual responses to specific drugs are reported in terms of the strength of the response and the reliability of the evidence.

<p align="center">
<img src="https://raw.githubusercontent.com/premedkb/panno/main/docs/images/clinical_annotation.png" width="60%" />
</p>