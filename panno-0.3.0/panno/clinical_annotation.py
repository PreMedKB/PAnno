#!/usr/bin/python
# -*- coding: UTF-8 -*-


import sqlite3, os, re
import pandas as pd
import numpy as np


def annotation(dic_diplotype, dic_rs2gt, hla_subtypes):
  
  ## Connected database
  pgx_kb_fp = os.path.join(os.path.dirname(__file__), 'assets/pgx_kb.sqlite3')
  # pgx_kb_fp = "./panno/assets/pgx_kb.sqlite3"
  conn = sqlite3.connect(pgx_kb_fp)
  cursor = conn.cursor()
  
  # DiplotypePhenotype
  dip_phe = cursor.execute("SELECT Gene, Allele1, Allele2, ActivityScore, Phenotype FROM DiplotypePhenotype;")
  dip_phe = cursor.fetchall()
  dip_phe_df = pd.DataFrame(dip_phe, columns=['Gene', 'Allele1', 'Allele2', 'ActivityScore', 'Phenotype'])
  # Guidelines: CPIC, DPWG, RNPGx, CPNDS
  guide = cursor.execute("SELECT * FROM GuidelineMerge WHERE Source NOT IN ('AusNZ', 'SEFF', 'ACR', 'CFF');")
  guide = cursor.fetchall()
  guide_df = pd.DataFrame(guide, columns=['ID', 'Source', 'PAID', 'Summary', 'Phenotype', 'Genotype', 'Recommendation', 'Avoid', 'Alternate', 'Dosing', 'Gene', 'Drug', 'GeneID', 'DrugID'])
  rule = cursor.execute("SELECT Gene, Variant, Allele1, Allele2, Phenotype, GuidelineID FROM GuidelineRule;")
  rule = cursor.fetchall()
  rule_df = pd.DataFrame(rule, columns=['Gene', 'Variant', 'Allele1', 'Allele2', 'Phenotype', 'GuidelineID'])
  rule_df1 = rule_df[rule_df.Allele2 != '']
  rule_df2 = rule_df[rule_df.Allele2 == '']
  
  #### Matched rules
  matched_ids = []
  detected_allele = [] # Gene, Variant, Diplotype, Phenotype
  # 1. Diplotypes
  for gene in dic_diplotype.keys():
    for panno_dip in dic_diplotype[gene]['step2_res'].split("; "):
      if panno_dip != '-':
        allele1 = panno_dip.split("/")[0]; allele2 = panno_dip.split("/")[1]
        # Match phenotype from CPIC tables, if there is no matched items, use the res.Phenotype
        sub_dip_phe = pd.concat([dip_phe_df[(dip_phe_df.Gene == gene) & (dip_phe_df.Allele1 == allele1) & (dip_phe_df.Allele2 == allele2)], dip_phe_df[(dip_phe_df.Gene == gene) & (dip_phe_df.Allele1 == allele2) & (dip_phe_df.Allele2 == allele1)]], axis = 0)
        # rule_df1
        res = pd.concat([rule_df1[(rule_df1.Gene == gene) & (rule_df1.Allele1 == allele1) & (rule_df1.Allele2 == allele2)], rule_df1[(rule_df1.Gene == gene) & (rule_df1.Allele1 == allele2) & (rule_df1.Allele2 == allele1)]], axis = 0)
        matched_ids.extend(res.GuidelineID.to_list())
        if res.empty is False:
          if sub_dip_phe.empty is False:
            phenotype = sub_dip_phe.Phenotype.to_list()[0]
          else:
            phenotype = '-'#res.Phenotype.to_list()[0]
          detected_allele.append([gene, res.Variant.to_list()[0], panno_dip, phenotype])
        # rule_df2
        res = rule_df2[(rule_df2.Gene == gene) & ((rule_df2.Allele1 == allele1) | (rule_df2.Allele1 == allele2))]
        matched_ids.extend(res.GuidelineID.to_list())
        if res.empty is False:
          if sub_dip_phe.empty is False:
            phenotype = sub_dip_phe.Phenotype.to_list()[0]
          else:
            phenotype = '-'#res.Phenotype.to_list()[0]
          detected_allele.append([gene, res.Variant.to_list()[0], panno_dip, phenotype])
  
  # 2. SNP/Indels
  rsids = rule_df[rule_df.Variant.str.startswith('rs')].Variant.drop_duplicates().to_list()
  for rsid in rsids:
    if rsid in dic_rs2gt.keys():
      allele1 = dic_rs2gt[rsid][0]; allele2 = dic_rs2gt[rsid][1]
      res = pd.concat([rule_df1[(rule_df1.Gene == gene) & (rule_df1.Allele1 == allele1) & (rule_df1.Allele2 == allele2)], rule_df1[(rule_df1.Gene == gene) & (rule_df1.Allele1 == allele2) & (rule_df1.Allele2 == allele1)]], axis = 0)
      matched_ids.extend(res.GuidelineID.to_list())
      if res.empty is False:
        detected_allele.append([gene, res.Variant.to_list()[0], '%s%s' % (allele1, allele2), res.Phenotype.to_list()[0]])
  
  # 3. HLA
  detected_hla = []
  hla_df = rule_df[rule_df.Gene.str.startswith('HLA')]
  for index, row in hla_df.iterrows():
    gene = row.Gene; var = row.Allele1
    if var in hla_subtypes[gene].keys():
      if hla_subtypes[gene][var] == 0:
        phenotype = 'negative'
        detected = 'Zero copy'
        hla_var = '%s%s %s' % (gene, var, phenotype)
      else:
        phenotype = 'positive'
        hla_var = '%s%s positive' % (gene, var, phenotype)
        if hla_subtypes[gene][var] == 1:
          detected = 'One copy'
        else:
          detected = 'Two copies'
      if hla_var == row.Variant:
        matched_ids.append(row.GuidelineID)
    else:
      phenotype = '-'
      detected = 'Missing'
    detected_hla.append([gene, var, detected, phenotype])
  
  # Matched guidelines
  mg = guide_df[guide_df.ID.isin(matched_ids)]
  # 1. Avoid
  avoid_df = mg[mg.Avoid == 1]
  avoid_drug = avoid_df.Drug.drop_duplicates().to_list(); len(avoid_drug)
  # 2. Caution
  caution_df = mg[(mg.Drug.isin(avoid_drug) == False) & ((mg.Alternate == 1) | (mg.Dosing == 1))]
  caution_drug = caution_df.Drug.drop_duplicates().to_list(); len(caution_drug)
  # 3. Routine
  routine_df = mg[(mg.Drug.isin(avoid_drug) == False) & (mg.Drug.isin(caution_drug) == False)]
  routine_drug = routine_df.Drug.drop_duplicates().to_list(); len(routine_drug)
  
  ###--------- Section 1: Summary ---------###
  avoid_drug.sort(); caution_drug.sort(); routine_drug.sort()
  summary = {'Avoid': avoid_drug, 'Caution': caution_drug, 'Routine': routine_drug}
  ###--------- Section 2: Prescribing Info ---------###
  detected_allele.extend(detected_hla)
  prescribing_info = pd.DataFrame(detected_allele, columns=['Gene', 'Variant', 'Diplotype', 'Phenotype']).drop_duplicates().merge(mg.drop(columns=['Phenotype']), on=['Gene'])
  prescribing_info = prescribing_info[['Drug', 'Gene', 'Variant', 'Diplotype', 'Phenotype', 'Summary', 'Recommendation', 'Source', 'PAID', 'Avoid', 'Alternate', 'Dosing']].sort_values(by=['Drug'])
  ###--------- Section 3: Diplotype Detail ---------###
  # Gene list: 53 genes, contains rs12777823 which does not has gene symbol
  # gene_list = cursor.execute("SELECT DISTINCT Gene FROM ClinAnn WHERE EvidenceLevel IN ('1A', '1B', '2A', '2B') OR Gene IN (SELECT DISTINCT Gene FROM GuidelineMerge);")
  # gene_list = cursor.fetchall()
  # single = ["CFTR", "SLCO1B1", "-", "VKORC1", "UGT1A6", "CYP2C19", "CYP2A6", "CYP2B6", "CYP2C8", "CYP2C9", "MTHFR", "CYP3A4", "TPMT", "CYP3A5", "ABCG2", "ALDH2", "UGT1A1", "NUDT15", "CYP2D6", "G6PD", "CES1", "APOE", "DPYD", "IFNL3", "IFNL4", "F5", "CHRNA5", "RYR1", "ACE", "SLC28A3", "CACNA1S", "CYP4F2", "XRCC1", "TNF", "KIF6", "ADRB2", "ATIC", "ADD1", "EGFR", "XPNPEP2", "MT-RNR1", "MT-ND1", "ITPA", "FCGR3A", "RARG", "SCN1A", "SLC19A1", "NAT2", "HLA-A", "HLA-B", "HLA-C", "HLA-DRB1", "HLA-DPB1"]
  
  ## MultiVar
  multi = ["CACNA1S", "CFTR", "CYP2B6", "CYP2C8", "CYP2C9", "CYP2C19", "CYP2D6", "CYP3A4", "CYP3A5", "CYP4F2", "DPYD", "NUDT15", "RYR1", "SLCO1B1", "TPMT", "UGT1A1"]
  multi_df = []
  for gene in multi:
    gene_detail = dic_diplotype[gene]['detail']
    for pos_res in gene_detail:
      # chrom, pos, nc, ng, rs, pc, identified_allele, detected_allele
      position = str(pos_res[0]) + ':' + str(pos_res[1])
      multi_df.append([gene, dic_diplotype[gene]['step2_res'], position, pos_res[4], pos_res[5], pos_res[6], pos_res[7]])
  
  multi_var = pd.DataFrame(multi_df, columns=['Gene', 'Diplotype', 'Position', 'Variant', 'Effect on Protein', 'Definition of Alleles', 'Detected Alleles'])
  
  ## SingleVar
  # 1. HLA
  hla_list = cursor.execute("SELECT DISTINCT Gene, Allele1 FROM ClinAnn WHERE Gene LIKE 'HLA%' AND EvidenceLevel != 3;")
  hla_list = cursor.fetchall()
  for item in hla_list:
    gene = item[0]; var = item[1]
    if var in hla_subtypes[gene].keys():
      if hla_subtypes[gene][var] == 0:
        phenotype = 'negative'
        detected = 'Zero copy'
      else:
        phenotype = 'positive'
        if hla_subtypes[gene][var] == 1:
          detected = 'One copy'
        else:
          detected = 'Two copies'
    else:
      phenotype = '-'
      detected = 'Missing'
    detected_hla.append([gene, var, detected, phenotype])
  detected_hla_df = pd.DataFrame(detected_hla, columns=['Gene', 'Variant', 'Detected Alleles', 'Phenotype']).drop(columns=['Phenotype'])
  
  # 1. SNP/Indel
  rsid_anno = cursor.execute('SELECT Gene, Variant FROM ClinAnn WHERE EvidenceLevel != 3 AND Variant LIKE "rs%";')
  rsid_anno = cursor.fetchall()
  rsid_anno_df = pd.DataFrame(rsid_anno, columns = ['Gene', 'Variant'])
  rsid_guide_df = rule_df[rule_df.Variant.str.startswith('rs')][['Gene', 'Variant']]
  rsid_df = pd.concat([rsid_anno_df, rsid_guide_df], axis = 0).drop_duplicates().reset_index(drop = True)
  rsid_df.insert(2, 'Detected Alleles', 'Missing')
  for index, row in rsid_df.iterrows():
    rsid = row.Variant
    if row.Variant in dic_rs2gt.keys():
      allele1 = dic_rs2gt[rsid][0]; allele2 = dic_rs2gt[rsid][1]
      row['Detected Alleles'] = '%s/%s' % (allele1, allele2)
    rsid_df.iloc[index] = row
  
  single_var = pd.concat([rsid_df, detected_hla_df], axis = 0).drop_duplicates().sort_values(by=['Gene', 'Variant'])
  
  
  ######## Find ClinAnn and extract the table
  ann = cursor.execute("SELECT * FROM ClinAnn WHERE EvidenceLevel != '3';")# OR (Gene IN (SELECT Gene FROM GuidelineMerge) AND Drug IN (SELECT Drug FROM GuidelineMerge));")
  ann = cursor.fetchall()
  ann_df = pd.DataFrame(ann, columns=['ID', 'CAID', 'Gene', 'Variant', 'Allele1', 'Allele2', 'Annotation1', 'Annotation2', 'Function1', 'Function2', 'Score1', 'Score2', 'CPICPhenotype', 'PAnnoPhenotype', 'Drug', 'Phenotypes', 'EvidenceLevel', 'LevelOverride', 'LevelModifier', 'Score', 'PMIDCount', 'EvidenceCount', 'Specialty', 'PhenotypeCategory'])
  ann_df.PhenotypeCategory = ann_df.PhenotypeCategory.replace('Metabolism/PK', 'Metabolism')
  
  # 1. Filter by variant
  ann_df_retain = pd.DataFrame()
  for index, row in single_var.iterrows():
    if row['Detected Alleles'] != 'Missing':
      if row['Variant'].startswith('rs'):
        allele1 = row['Detected Alleles'].split('/')[0]
        allele2 = row['Detected Alleles'].split('/')[1]
        res = ann_df[(ann_df.Gene == row.Gene) & (ann_df.Variant == row.Variant) & (((ann_df.Allele1 == allele1) & (ann_df.Allele2 == allele2)) | ((ann_df.Allele1 == allele2) & (ann_df.Allele2 == allele1)))]
        res.insert(0, 'VariantNew', row['Variant'])
        res.insert(1, 'Diplotype', row['Detected Alleles'])
      elif row['Detected Alleles'] != 'Zero copy':
        res = ann_df[(ann_df.Gene == row.Gene) & ((ann_df.Allele1 == row.Variant) | (ann_df.Allele2 == row.Variant))]
        res.insert(0, 'VariantNew', row['Variant'])
        res.insert(1, 'Diplotype', row['Detected Alleles'])
      ann_df_retain = pd.concat([ann_df_retain, res])
  
  for index, row in multi_var[['Gene', 'Diplotype']].drop_duplicates().iterrows():
    gene = row.Gene
    allele1 = row.Diplotype.split('/')[0]; allele2 = row.Diplotype.split('/')[1]
    res = ann_df[(ann_df.Gene == row.Gene) & (((ann_df.Allele1 == allele1) & (ann_df.Allele2 == allele2)) | ((ann_df.Allele1 == allele2) & (ann_df.Allele2 == allele1)))]
    res.insert(0, 'VariantNew', '')
    res.insert(1, 'Diplotype', row.Diplotype)
    ann_df_retain = pd.concat([ann_df_retain, res])
  
  # 2. Filter by drug, remove the avoid use drugs
  ann_df_retain = ann_df_retain[ann_df_retain.Drug.isin(routine_drug + caution_drug)].reset_index(drop = True)
  # # Check whether drugs are included in ann_df
  # for drug in routine_drug + caution_drug:
  #   if ann_df_retain[ann_df_retain.Drug == drug].empty:
  #     print(drug)
  

  ###--------- Section 4: Phenotype Prediction ---------###
  # Categorize by phenotypes and drugs
  ann_df_retain.insert(0, 'PAnnoScore', np.nan)
  for index, row in ann_df_retain.iterrows():
    if np.isnan(row.Score2) and row.Variant.startswith('rs'):
      row.PAnnoScore = row.Score1 + row.Score1
    else:
      row.PAnnoScore = row.Score1 + row.Score2
    ann_df_retain.iloc[index] = row
  
  phenotype_predict = pd.DataFrame()
  categories = ['Toxicity', 'Dosage', 'Efficacy', 'Metabolism', 'Other']
  for cat in categories:
    cat_df = ann_df_retain[ann_df_retain.PhenotypeCategory == cat]
    # Calculating cat_pgx
    cat_pgx = cat_df.groupby("Drug")[['PAnnoScore']].mean()
    cat_pgx_count = cat_df.groupby("Drug")[['PAnnoScore']].count().rename(columns={'PAnnoScore': 'Count'})
    cat_pgx = cat_pgx.merge(cat_pgx_count, left_index=True, right_index=True)
    cat_pgx['PhenotypeCategory'] = cat
    cat_pgx['Prediction'] = ''
    cat_pgx.insert(0, 'Drug', cat_pgx.index)
    cat_pgx = cat_pgx.reset_index(drop=True)
    for index, row in cat_pgx.iterrows():
      if row.PAnnoScore <= 1.5:
        cat_pgx.loc[index, 'Prediction'] = 'Decreased'
      elif row.PAnnoScore >= 2.5:
        cat_pgx.loc[index, 'Prediction'] = 'Increased'
      else:
        cat_pgx.loc[index, 'Prediction'] = 'Normal'
    phenotype_predict = pd.concat([phenotype_predict, cat_pgx]).sort_values(by=['Drug'])
  
  ###--------- Section 5: Clinical Annotation ---------###
  clinical_anno = ann_df_retain[['Drug', 'Gene', 'VariantNew', 'Diplotype', 'PhenotypeCategory', 'EvidenceLevel', 'PAnnoPhenotype', 'CAID']].rename(columns={'VariantNew': 'Variant'}).sort_values(by=['Drug'])
  
  cursor.close()
  conn.close()
  
  return(summary, prescribing_info, multi_var, single_var, phenotype_predict, clinical_anno)
