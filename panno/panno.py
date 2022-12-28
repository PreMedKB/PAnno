#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""Console script for panno."""

from panno import genotype_resolution, clinical_annotation, pgx_report, predict_diplotype
import getopt, sys, os, re, pyranges
import pandas as pd

def main():
  
  version = 'v0.3.1'
  help = '''
  Usage: panno -s sample_id -i germline_vcf -p population -o outdir
  
  PAnno takes the variant calling format (VCF) file and population information as input
  and outputs an HTML report of drug responses with prescription recommendations.
  
  Options:
    
    -s, --sample_id TEXT            Sample ID that will be displayed in the PAnno report.
    
    -i, --germline_vcf TEXT         Unannotated VCF file, preferably germline variant.
    
    -p, --population [AAC|AME|EAS|EUR|LAT|NEA|OCE|SAS|SSA]
                                    The three-letter abbreviation for biogeographic groups:
                                    AAC (African American/Afro-Caribbean), AME (American),
                                    EAS (East Asian), EUR (European), LAT (Latino),
                                    NEA (Near Eastern), OCE (Oceanian),
                                    SAS (Central/South Asian), SSA (Sub-Saharan African).
    
    -o, --outdir TEXT               Create report in the specified output path.
    
    -v, --version                   Show the version and exit.
    
    -h, --help                      Show this message and exit.
  '''
  
  try:
    opts, args = getopt.getopt(sys.argv[1:], "hvs:i:p:o:", ["help", "version", "sample_id=", "germline_vcf=", "population=", "outdir="])
    if not opts:
      print(help)
      sys.exit()
  except getopt.GetoptError:
    print(help)
  
  for opt, arg in opts:
    if opt in ("-h", "--help"):
      print(help)
      sys.exit()
    elif opt in ("-v", "--version"):
      print(version)
      sys.exit()
    elif opt in ("-s", "--sample_id"):
      sample_id = arg
    elif opt in ("-i", "--germline_vcf"):
      germline_vcf = arg
    elif opt in ("-p", "--population"):
      population = arg
    elif opt in ("-o", "--output"):
      outdir = arg
  
  ## Check input arguments
  if 'sample_id' not in locals().keys():
    print('\nThe sample ID (-s or --sample_id) is a required parameter, please enter it.')
    sys.exit(1)
  
  if 'germline_vcf' not in locals().keys():
    print('\nThe germline VCF (-i or --germline_vcf) is a required parameter, please enter it.')
    sys.exit(1)
  elif not os.path.exists(germline_vcf):
    print('\n[ERROR] The input germline VCF file does not exist, please check your file path.')
    sys.exit(1)
  
  if 'population' not in locals().keys():
    print('\nThe population (-p or --population) is a required parameter, please enter it.')
    sys.exit(1)
  else:
    population = population.upper()
    pop_dic = {'AAC': 'African American/Afro-Caribbean', 'AME': 'American', 'SAS': 'Central/South Asian', 'EAS': 'East Asian', 'EUR': 'European', 'LAT': 'Latino', 'NEA': 'Near Eastern', 'OCE': 'Oceanian', 'SSA': 'Sub-Saharan African'}
    if population not in pop_dic.keys():
      print('\n[ERROR] The input population is not included in PAnno. Please check if the abbreviation is used correctly.')
      sys.exit(1)
  
  if 'outdir' not in locals().keys():
    print('\nThe directory for output (-o or --outdir) is a required parameter, please enter it.')
    sys.exit(1)
  elif not os.path.exists(outdir):
    print('\n[WARNING] The directory %s does not exist.' % outdir)
    try:
      print('  - PAnno is trying to create it.')
      os.mkdir(outdir)
    except:
      print('  - [ERROR] Directory creation failed. Please enter a directory that already exists to re-run PAnno.')
      sys.exit(1)
  fp = os.path.join(outdir, "%s.PAnno.html" % sample_id)
  

  ## Start running PAnno
  print('\nParsing PGx related diplotypes ...')
  dic_diplotype, dic_rs2gt, hla_subtypes = genotype_resolution.resolution(pop_dic[population], germline_vcf)
  print('Annotating clinical information ...')
  summary, prescribing_info, multi_var, single_var, phenotype_predict, clinical_anno = clinical_annotation.annotation(dic_diplotype, dic_rs2gt, hla_subtypes)
  print('Generating PAnno report ...')
  race = "%s (%s)" % (pop_dic[population], population)
  pgx_report.report(race, summary, prescribing_info, multi_var, single_var, phenotype_predict, clinical_anno, fp, sample_id)
  
  # Finish the task
  print('\nYour PAnno report has been completed and is located at %s.' % fp)
  print('\n     ^ _ ^\n\n')


if __name__ == "__main__":
  main()