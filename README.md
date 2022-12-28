<p align="left" margin-bottom="-2rem"> <img src="https://raw.githubusercontent.com/premedkb/panno/main/docs/images/panno_logo.png" width="40%"/> </p>

## PAnno: A Pharmacogenomics Annotation Tool for Clinical Genomic Testing

![PyPI](https://img.shields.io/pypi/v/panno?color=pink)  ![Conda](https://img.shields.io/conda/v/lyaqing/panno?color=blue&label=conda) ![AppVeyor](https://img.shields.io/appveyor/build/PreMedKB/PAnno)

PAnno reports **prescribing recommendations** and **drug response phenotypes** by parsing the germline variant call format (VCF) file from NGS and the population to which the individual belongs.

## Installation

*Prerequisite: To ensure smooth installation and usage, [Python >= 3.7](https://docs.conda.io/en/latest/miniconda.html#system-requirements) (#1 and #3 below), or [Miniconda/Anaconda](https://docs.conda.io/en/latest/miniconda.html#system-requirements) (#2 below) are required.*

1. You can install PAnno from [PyPI](https://pypi.org/project/panno/) using pip as follows:
```Shell
pip install panno==0.3.1
```

2. Alternatively, you can create a environment using [Conda](https://anaconda.org/lyaqing/panno).
```Shell
conda create -n PAnno panno=0.3.1 -c lyaqing -c conda-forge -c bioconda
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

PAnno directly uses the NGS-derived germline VCF file as input and assumes it has undergone quality control. Therefore, if the VCF file is of poor quality, inaccurate diplotypes and inappropriate clinical recommendations may be reported.

PAnno requires the VCF file aligned to the GRCh38 reference genome given the increasing generality and the built-in diplotype definition dependency version.


#### 2. Population
There are nine biogeographic groups supported by PAnno. Please use the ***three-letter abbreviation*** as input. This is to prevent errors caused by special symbols such as spaces.

**AAC** (African American/Afro-Caribbean), **AME** (American), **EAS** (East Asian), **EUR** (European), **LAT** (Latino), **NEA** (Near Eastern), **OCE** (Oceanian), **SAS** (Central/South Asian), **SSA** (Sub-Saharan African).

More information is available at https://www.pharmgkb.org/page/biogeographicalGroups.

### Output data

The report is created in `${sample_id}.html` at the `outdir` by default.

For more detailed instructions, run `panno -h`.

## Examples

The `demo` directory contains the VCF files and PAnno reports of four Coriell samples: NA10859 (European), NA19147 (African American/Afro-Caribbean), NA19785 (Latino), and HG00436 (East Asian).

In addition, we analyzed the germline variants of 88 samples which have been characterized in the GeT-RM PGx studies.

* The VCF files are available at https://github.com/PreMedKB/PAnno-analysis/tree/main/vcf.
* The PAnno reports are available at https://github.com/PreMedKB/PAnno-analysis/tree/main/report.

Here is a snapshot from the PAnno report:
<p align="center">
<img src="https://raw.githubusercontent.com/premedkb/panno/main/docs/images/panno_report.png" width="100%" />
</p>

## Core Components
A ranking model dedicated to inferring diplotypes, developed based on the **allele (haplotype) definition** and **population frequency**, was introduced in PAnno. The predictive performance was validated in comparison with four similar tools using the consensus diplotype data of the Genetic Testing Reference Materials Coordination Program (GeT-RM) as ground truth.

An annotation method was proposed to summarize prescriptions and classify drugs into **avoid use**, **use with caution**, and **routine use**, following the recommendations of the Clinical Pharmacogenetics Implementation Consortium (CPIC), etc. It further predicts phenotypes of specific drugs in terms of toxicity, dosage, efficacy, and metabolism by integrating the high-confidence clinical annotations in the Pharmacogenomics Knowledgebase (PharmGKB).

<p align="center">
<img src="https://raw.githubusercontent.com/premedkb/panno/main/docs/images/architecture.png" width="70%" />
</p>
