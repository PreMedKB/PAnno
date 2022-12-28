import getopt, sys, os
from panno import genotype_resolution, clinical_annotation, pgx_report, predict_diplotype

demos = {'NA10859':'EUR', 'NA19147': 'AAC', 'NA19785':'LAT', 'HG00436':'EAS'}
pop_dic = {'AAC': 'African American/Afro-Caribbean', 'AME': 'American', 'SAS': 'Central/South Asian', 'EAS': 'East Asian', 'EUR': 'European', 'LAT': 'Latino', 'NEA': 'Near Eastern', 'OCE': 'Oceanian', 'SSA': 'Sub-Saharan African'}

for sample_id in demos.keys():
  germline_vcf = "./demo/%s.pgx.vcf" % sample_id
  population = demos[sample_id]
  race=pop_dic[population]
  outdir="./demo"
  
  ## Start running PAnno
  print('\nParsing PGx related genotypes ...')
  dic_diplotype, dic_rs2gt, hla_subtypes = genotype_resolution.resolution(pop_dic[population], germline_vcf)
  
  print('Annotating clinical information ...')
  summary, prescribing_info, multi_var, single_var, phenotype_predict, clinical_anno = clinical_annotation.annotation(dic_diplotype, dic_rs2gt, hla_subtypes)
  
  print('Generating PAnno report ...')
  race = "%s (%s)" % (pop_dic[population], population)
  fp = os.path.join(outdir, "%s.PAnno.html" % sample_id)
  pgx_report.report(race, summary, prescribing_info, multi_var, single_var, phenotype_predict, clinical_anno, fp, sample_id)

