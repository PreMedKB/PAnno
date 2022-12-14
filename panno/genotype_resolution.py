#!/usr/bin/python
# -*- coding: UTF-8 -*-


from panno import predict_diplotype
import re, os, pyranges
import pandas as pd

def resolution(race, germline_vcf):
  
  panno_bed_fp = os.path.join(os.path.dirname(__file__), 'assets/pgx_loci.bed')
  # panno_bed_fp='./panno/assets/pgx_loci.bed'
  ## Filter loci based on PharmGKB's bed file: delete all loci in the user's vcf that are not in the panno.bed file
  ## Extract the user's bed file: skip the lines starting with '##'
  vcf = []
  vcf_bed = []
  with open(germline_vcf, "r", encoding = "utf-8") as file:
    for line in file:
      if 'CHROM' in line:
        colnames = line.strip().split('\t')
      if line[0] != '#':
        info = line.strip().split('\t')
        vcf.append(info)
        vcf_bed.append([info[0], info[1], info[1]])
  
  vcf_bed_df = pd.DataFrame(vcf_bed, columns=['Chromosome', 'Start', 'End'])
  panno_bed = pd.read_csv(panno_bed_fp, sep="\t", names=['Chromosome', 'Start', 'End', 'rsid'])
  vcf_bed_df['Chromosome'] = vcf_bed_df['Chromosome'].map(lambda x: re.sub('chr|Chr|CHR', '', x)).astype('str')
  panno_bed['Chromosome'] = panno_bed['Chromosome'].map(lambda x: re.sub('chr|Chr|CHR', '', x)).astype('str')
  
  ## Filter the BED of the input VCF based on the overlap with PAnno BED
  gr1, gr2 = pyranges.PyRanges(vcf_bed_df), pyranges.PyRanges(panno_bed.iloc[:,:3])
  # pyranges will not process the item with equal start and end, which is different from pybedtools
  gr1.End, gr2.End = gr1.End + 1, gr2.End + 1
  filter_bed = gr1.overlap(gr2).df
  filter_bed.End = filter_bed.End - 1
  
  ## Convert the input VCF into a data frame and filter it
  vcf_df = pd.DataFrame(vcf, columns=colnames)
  vcf_df.loc[:,'#CHROM'] = vcf_df['#CHROM'].map(lambda x: re.sub('chr|Chr|CHR', '', x)).astype('str')
  vcf_df.loc[:,colnames[1]] = vcf_df[colnames[1]].astype('int32')
  filter_bed = filter_bed.iloc[:, 0:2].rename(columns={'Chromosome': colnames[0], 'Start': colnames[1]})
  filtered_vcf = pd.merge(vcf_df, filter_bed, how='inner', on=colnames[:2])
  
  ## Class 1: Diplotype
  gene_list = ["G6PD", "MT-RNR1", "ABCG2", "CACNA1S", "CFTR", "IFNL3", "VKORC1", "RYR1",
              "CYP2B6", "CYP2C8", "CYP2C9", "CYP2C19", "CYP2D6",
              "CYP3A4", "CYP3A5", "CYP4F2", "DPYD", "NUDT15",
              "SLCO1B1", "TPMT", "UGT1A1"]
  dic_diplotype = predict_diplotype.predict(filtered_vcf, race, gene_list)
  ## Class 2: HLA genes
  hla_subtypes = {"HLA-A": {}, "HLA-B": {}, "HLA-C": {}, "HLA-DRB1": {}, "HLA-DPB1": {}}
  ## Class 3: Genotypes of detected positions
  dic_rs2gt = {}
  format_index = colnames.index("FORMAT")
  # Reload panno_bed
  panno_bed_rsid = panno_bed.dropna()
  for index, row in filtered_vcf.iterrows():
    info = row.to_list()
    format = info[format_index].split(":")
    gt_index = format.index("GT")
    gt = info[-1].split(":")[gt_index]
    if re.findall('0', gt) == ['0', '0']:
      genotype = 0
    elif re.findall('0', gt) == ['0']:
      genotype = 1
    else:
      genotype = 2
    # HLA genes
    if row[0].startswith('HLA'):
      gene = row[0].split('*')[0]
      if gene in hla_subtypes.keys():
        hla_subtypes[gene].update({'*%s' % row[0].split('*')[1]: genotype})
      # hla_subtypes[row[0]] = genotype
    # If the variant was within the clinical relevant list, add it into dis_rs2gt
    tmp = panno_bed_rsid[(panno_bed_rsid.Chromosome == info[0]) & (panno_bed_rsid.Start == info[1])].rsid.to_list()
    if tmp != []:
      rsids = tmp
    elif info[2] in panno_bed_rsid.rsid.to_list(): # The genome coordinates of a rsID may not complete.
      rsids = [info[2]]
    else:
      rsids = None
    
    if rsids:
      ref = info[3]
      alts = info[4].split(',')
      alleles = [ref] + alts
      var = []
      for g in re.split('\||/', gt):
        var.append(alleles[int(g)])
      for rsid in rsids:
        # Variants in chrX, chrY
        if len(var) == 1:
          var.append('')
        dic_rs2gt[rsid] = tuple(var)
  
  return(dic_diplotype, dic_rs2gt, hla_subtypes)