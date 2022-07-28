#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""Console script for panno."""

from panno import genotype_resolution, clinical_annotation, pgx_report
import getopt, sys, os

def main():
  
  version = '0.1.0'
  help = '''
  Usage: python panno.py [OPTIONS]
  
  PAnno takes the variant calling format (VCF) file and population information as input
  and outputs an HTML report of drug responses with prescription recommendations.
  
  Options:
    
    -s, --sample_id                 Sample ID that will be displayed in the PAnno report.
    
    -i, --germline_vcf              Unannotated VCF file, preferably germline variant.
    
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
  
  try:
    population = population.upper()
    pop_dic = {'AAC': 'African American/Afro-Caribbean', 'AME': 'American', 'SAS': 'Central/South Asian', 'EAS': 'East Asian', 'EUR': 'European', 'LAT': 'Latino', 'NEA': 'Near Eastern', 'OCE': 'Oceanian', 'SSA': 'Sub-Saharan African'}
    
    # Check input data
    if population not in pop_dic.keys():
      print('The input population is not included in PAnno. Please check if the abbreviation is used correctly.')
      sys.exit(1)
    if not os.path.exists(germline_vcf):
      print('The input germline VCF file does not exist.')
      sys.exit(1)
    
    if not os.path.isdir(outdir):
      outdir = os.path.dirname(outdir)
    if not os.path.exists(outdir):
      print('{0} does not exist and is trying to create it.'.format(outdir))
      os.makedir(outdir)
    
    # Start running PAnno
    print('  - Parsing PGx related genotypes ...')
    dic_diplotype, dic_rs2gt, hla_subtypes = genotype_resolution.resolution(pop_dic[population], germline_vcf)
    print('  - Annotating clinical information ...')
    pgx_summary, clinical_anno_table, dosing_guideline_table = clinical_annotation.annotation(dic_diplotype, dic_rs2gt, hla_subtypes)
    print('  - Generating PAnno report ...')
    fp = "%s/%s.PAnno.html" % (outdir, sample_id)
    pgx_report.report(pop_dic[population], pgx_summary, dic_diplotype, clinical_anno_table, dosing_guideline_table, fp, sample_id)
    
    # Finish the task
    print('  Your PAnno report has been completed and is located at %s.' % fp)
    print('\n    ^ _ ^\n\n')
  
  except:
    print('  ERROR occurred!')


if __name__ == "__main__":
  main()