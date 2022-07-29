<p align="left" margin-bottom="-2rem"> <img src="https://raw.githubusercontent.com/premedkb/panno/main/docs/images/panno_logo.png" width="40%"/> </p>

## PAnno: A Pharmacogenomics Annotation Tool for Clinical Genomic Testing

![PyPI](https://img.shields.io/pypi/v/panno?color=pink)  ![Conda](https://img.shields.io/conda/v/lyaqing/panno?color=blue&label=conda) ![AppVeyor](https://img.shields.io/appveyor/build/PreMedKB/PAnno)

PAnno reports drug responses and prescribing recommendations by parsing the germline variant call format (VCF) file from NGS and the population to which the individual belongs. PAnno provides an end-to-end clinical pharmacogenomics decision support solution by resolving, annotating, and reporting germline variants in individuals.

A ranking model dedicated to inferring diplotype developed based on allele definitions and population allele frequencies was introduced in PAnno. The predictive performance for diplotype was validated in comparison with four similar tools using the consensus diplotype data of the Genetic Testing Reference Materials Coordination Program (GeT-RM) as ground truth.

An annotation method was further proposed to summarize ***the drug response level*** (<b>decreased</b>, <b>moderate</b>, and <b>increased</b>) and ***the level of clinical evidence*** (<b>A</b> and <b>B</b>) for the resolved genotypes.

<p align="center">
<img src="https://raw.githubusercontent.com/premedkb/panno/main/docs/images/architecture.png" width="40%" />
</p>

## Status
PAnno is still under _active development_. In the current release, you should only use it to evaluate whether PAnno will compile and run properly on your system. All information in the PAnno report is interpreted directly from the uploaded VCF file. Users recognize that they are using PAnno at their own risk.

## Installation
You can install PAnno from [PyPI](https://pypi.org/project/panno/) using pip as follows:
```Shell
pip install panno
```

Alternatively, you can install using [Anaconda](https://anaconda.org/lyaqing/panno):
```Shell
conda install -c lyaqing panno
```

If you would like the development version instead, the command is:
```Shell
pip install --upgrade --force-reinstall git+https://github.com/PreMedKB/PAnno.git
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
There are nine biogeographic groups supported by PAnno:

**AAC** (African American/Afro-Caribbean), **AME** (American), **EAS** (East Asian), **EUR** (European), **LAT** (Latino), **NEA** (Near Eastern), **OCE** (Oceanian), **SAS** (Central/South Asian), **SSA** (Sub-Saharan African).

More information is available at https://www.pharmgkb.org/page/biogeographicalGroups.

Please use the ***three-letter abbreviation*** as input. This is to prevent errors caused by special symbols such as spaces.

### Output data

The report is created in `${sample_id}.html` at the `outdir` by default.

For more detailed instructions, run `panno -h`.

## Examples
We analyzed the germline variants of 88 samples from the GeT-RM PGx study using PAnno. The generated PGx report is available at https://github.com/PreMedKB/PAnno-analysis/report.

Here is a snapshot from the PAnno report:
<p align="center">
<img src="https://raw.githubusercontent.com/premedkb/panno/main/docs/images/panno_report.png" width="100%" />
</p>

## Core Components
### PAnno ranking model for diplotype inference
Genotype resolution aims to extract the alleles of small variants (SNVs and Indels) and the diplotypes related to PGx from the user-submitted VCF file. PAnno processes the “GT” information to obtain all relevant single-locus genotypes. Afterwards, the genotypes of small variants will be passed to clinical annotation directly, while the genotypes related to diplotype definitions will be passed to the PAnno ranking model. The output diplotypes with the highest ranking will then be annotated.
<p align="center">
<img src="https://raw.githubusercontent.com/premedkb/panno/main/docs/images/diplotype_inference.png" width="80%" />
</p>

### PAnno annotation method for predicting drug response at individual level
This component aims to discover the “drug-genotype-response-evidence” relationship. PAnno annotation method translates the literal PGx knowledge about genotypes into quantitative scores. The association between multiple genotypes and a single drug is then further translated into an individual-level association with this drug. Then the individual responses to specific drugs are reported in terms of the strength of the response and the reliability of the evidence.
<p align="center">
<img src="https://raw.githubusercontent.com/premedkb/panno/main/docs/images/clinical_annotation.png" width="60%" />
</p>