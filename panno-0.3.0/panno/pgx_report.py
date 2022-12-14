#!/usr/bin/python
# -*- coding: UTF-8 -*-


import time, os, base64
from itertools import *


def report (race, summary, prescribing_info, multi_var, single_var, phenotype_predict, clinical_anno, fp, sample_id):
  with open(fp, 'w+', encoding="utf-8") as f:
    ## Style
    css_fp = os.path.join(os.path.dirname(__file__), 'assets/custom.css')
    logo_fp = os.path.join(os.path.dirname(__file__), 'assets/panno_logo.png')
    icon_fp = os.path.join(os.path.dirname(__file__), 'assets/panno_icon.png')
    # css_fp = os.path.join('./panno/assets/custom.css')
    # logo_fp = os.path.join('./panno/assets/panno_logo.png')
    # icon_fp = os.path.join('./panno/assets/panno_icon.png')
    logo_base64 = base64.b64encode(open(logo_fp, "rb").read()).decode()
    icon_base64 = base64.b64encode(open(icon_fp, "rb").read()).decode()
    
    head_nav="""
    <!doctype html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta http-equiv="X-UA-Compatible" content="IE=edge">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>PAnno Report</title>
      <link rel="shortcut icon" href="data:image/png;base64,%s">
      <script src="https://kit.fontawesome.com/e540049a97.js" crossorigin="anonymous"></script>
      <style type="text/css">%s</style>
    </head>
    
    <body>
    <div class="side-nav-wrapper">
      <div class="side-nav">
        <ul class="mqc-nav collapse navbar-collapse">
        <h1>
          <a href="#">
            <img src="data:image/png;base64,%s" alt="PAnno">
            <br class="hidden-xs">
            <small class="hidden-xs">%s</small>
          </a>
        </h1>
          <li><a href="#summary" class="nav-l1"><b>&nbsp;&nbsp;Summary</b></a></li>
          <li><a href="#prescribing info" class="nav-l1"><b>&nbsp;&nbsp;Prescribing Info</b></a></li>
          <li><a href="#diplotype detail" class="nav-l1"><b>&nbsp;&nbsp;Diplotype Detail</b></a></li>
          <li><a href="#multi-variant" class="nav-l2">&nbsp;&nbsp;&nbsp;&nbsp;Multi-variant allele</a></li>
          <li><a href="#single-variant" class="nav-l2">&nbsp;&nbsp;&nbsp;&nbsp;Single-variant allele</a></li>
          <li><a href="#phenotype prediction" class="nav-l1"><b>&nbsp;&nbsp;Phenotype Prediction</b></a></li>
          <li><a href="#clinical annotation" class="nav-l1"><b>&nbsp;&nbsp;Clinical Annotation</b></a></li>
          <li><a href="#about" class="nav-l1"><b>&nbsp;&nbsp;About</b></a></li>
        </ul>
      </div>
    </div>
    
    <div class="main_page">
    """
    print(head_nav%(icon_base64, open(css_fp).read(), icon_base64, 'v0.3.0'), file=f)
   
    ## Part 0: Basic information
    basic_info = """
    <h1 id="page_title">
      <a href="https://github.com/PreMedKB/PAnno" target="_blank">
        <img src="data:image/png;base64,%s" title="PAnno">
      </a>
    </h1>
    <p class="head_lead">
      An automated clinical pharmacogenomics annotation tool to report drug responses and prescribing recommendations by parsing the germline variants.
    </p>
    <blockquote>
      <p style="font-size:0.95rem;">Sample ID: %s<br>Biogeographic Group: %s<br>Report Time: %s</p>
    </blockquote>
    """
    print(basic_info%(logo_base64, sample_id, race, time.asctime(time.localtime(time.time()))), file=f)
    
    ## Part 1: Sort disclaimer
    disclaimer_short = """
    <div class="alert alert-info-yellow">
      <b>Disclaimer:</b> The PAnno report iterates as the release version changes. In the current release, you should only use it to evaluate whether PAnno will compile and run properly on your system. All information in the report is interpreted directly from the uploaded VCF file. Users recognize that they use it at their own risk.
    </div>
    """
    print(disclaimer_short, file=f)

    ## Part 2: Pharmacogenomics Annotation
    part2_header = """
    <h2 id="summary"><b>Summary</b></h2>
    <p class="main_lead">
        Drugs are classified to indicate whether the clinical guidelines recommend a prescribing change based on the given diplotypes. Original prescribing information was collected by PharmGKB, primarily from the <a href="http://cpicpgx.org/">Clinical Pharmacogenetics Implementation Consortium</a> (CPIC), the <a href="https://www.knmp.nl/dossiers/farmacogenetica/">Dutch Pharmacogenetics Working Group</a> (DPWG), the <a href="https://cpnds.ubc.ca/">Canadian Pharmacogenomics Network for Drug Safety</a> (CPNDS), the French National Network of Pharmacogenetics (RNPGx).
    </p>
    
    """
    print(part2_header, file=f)
    
    print('<b class="sum-A">Avoid use</b><br><div class="sum-info">Avoidance of the drug is clearly stated in the prescription for the given diplotype.</div>',file=f)
    
    header = '<table id="drug_table" border="1" cellspacing="0">\n'
    i = 0
    while i<len(summary['Avoid']):
      header = header + '<tr>'
      if summary['Avoid'][i] is not None:
        a1 = summary['Avoid'][i]
      else:
        a1 = ''
      if (i+1) < len(summary['Avoid']):
        a2 = summary['Avoid'][i+1]
      else:
        a2 = ''
      if (i+2) < len(summary['Avoid']):
        a3 = summary['Avoid'][i+2]
      else:
        a3 = ''
      if (i+3) < len(summary['Avoid']):
        a4 = summary['Avoid'][i+3]
      else:
        a4 = ''
      if (i+4) < len(summary['Avoid']):
        a5 = summary['Avoid'][i+4]
      else:
        a5 = ''
      if (i+5) < len(summary['Avoid']):
        a6 = summary['Avoid'][i+5]
      else:
        a6 = ''
      if (i+6) < len(summary['Avoid']):
        a7 = summary['Avoid'][i+6]
      else:
        a7 = ''
      header = header + '<td><a href="#%s">%s</a></td><td><a href="#%s">%s</a></td><td><a href="#%s">%s</a></td><td><a href="#%s">%s</a></td><td><a href="#%s">%s</a></td><td><a href="#%s">%s</a></td><td><a href="#%s">%s</a></td>' % (a1,a1,a2,a2,a3,a3,a4,a4,a5,a5,a6,a6,a7,a7)
      header = header + '</tr>'
      i = i+7
    header = header + '\n</table>'
    print(header, file=f)
    
    print('<b class="sum-U">Use with caution</b><br><div class="sum-info">Prescribing changes are recommended for the given diplotypes, e.g., dose adjustments and alternative medications. In addition, prescriptions that differ in specific populations or require consideration of multiple diplotypes are included in this category.</div>',file=f)
    header = '<table id="drug_table" border="1" cellspacing="0">\n'
    i = 0
    while i<len(summary['Caution']):
      header = header + '<tr>'
      if summary['Caution'][i] is not None:
        a1 = summary['Caution'][i]
      else:
        a1 = ''
      if (i+1) < len(summary['Caution']):
        a2 = summary['Caution'][i+1]
      else:
        a2 = ''
      if (i+2) < len(summary['Caution']):
        a3 = summary['Caution'][i+2]
      else:
        a3 = ''
      if (i+3) < len(summary['Caution']):
        a4 = summary['Caution'][i+3]
      else:
        a4 = ''
      if (i+4) < len(summary['Caution']):
        a5 = summary['Caution'][i+4]
      else:
        a5 = ''
      if (i+5) < len(summary['Caution']):
        a6 = summary['Caution'][i+5]
      else:
        a6 = ''
      if (i+6) < len(summary['Caution']):
        a7 = summary['Caution'][i+6]
      else:
        a7 = ''
      header = header + '<td><a href="#%s">%s</a></td><td><a href="#%s">%s</a></td><td><a href="#%s">%s</a></td><td><a href="#%s">%s</a></td><td><a href="#%s">%s</a></td><td><a href="#%s">%s</a></td><td><a href="#%s">%s</a></td>' % (a1,a1,a2,a2,a3,a3,a4,a4,a5,a5,a6,a6,a7,a7)
      header = header + '</tr>'
      i = i+7
    header = header + '\n</table>'
    print(header, file=f)
    
    print('<b class="sum-R">Routine use</b><br><div class="sum-info">There is no recommended prescribing change for the given diplotype.</div>',file=f)
    header = '<table id="drug_table" border="1" cellspacing="0">\n'
    i = 0
    while i<len(summary['Routine']):
      header = header + '<tr>'
      if summary['Routine'][i] is not None:
        a1 = summary['Routine'][i]
      else:
        a1 = ''
      if (i+1) < len(summary['Routine']):
        a2 = summary['Routine'][i+1]
      else:
        a2 = ''
      if (i+2) < len(summary['Routine']):
        a3 = summary['Routine'][i+2]
      else:
        a3 = ''
      if (i+3) < len(summary['Routine']):
        a4 = summary['Routine'][i+3]
      else:
        a4 = ''
      if (i+4) < len(summary['Routine']):
        a5 = summary['Routine'][i+4]
      else:
        a5 = ''
      if (i+5) < len(summary['Routine']):
        a6 = summary['Routine'][i+5]
      else:
        a6 = ''
      if (i+6) < len(summary['Routine']):
        a7 = summary['Routine'][i+6]
      else:
        a7 = ''
      header = header + '<td><a href="#%s">%s</a></td><td><a href="#%s">%s</a></td><td><a href="#%s">%s</a></td><td><a href="#%s">%s</a></td><td><a href="#%s">%s</a></td><td><a href="#%s">%s</a></td><td><a href="#%s">%s</a></td>' % (a1,a1,a2,a2,a3,a3,a4,a4,a5,a5,a6,a6,a7,a7)
      header = header + '</tr>'
      i = i+7
    header = header + '\n</table>'
    print(header, file=f)
   
    ## Part 3: Prescribing Info
    print('<h2 id="prescribing info"><b>Prescribing Info</b></h2>', file=f)
    
    for drug in list(prescribing_info.Drug.drop_duplicates()):
      print('<h3 id="%s"><b>%s</b></h3>' % (drug,drug), file=f)
      drug_sub = prescribing_info[prescribing_info.Drug == drug]
      for gene in list(drug_sub.Gene.drop_duplicates()):
        drug_by_gene = drug_sub[drug_sub.Gene == gene]
        # Clean the output
        phenotype = list(drug_by_gene.Phenotype.drop_duplicates())
        diplotype = list(drug_by_gene.Diplotype.drop_duplicates())
        if len(phenotype) > 1:
          # print(phenotype)
          phenotype = [phenotype[0]]
        # if len(diplotype) > 1:
        #   print(diplotype)
        
        print('<p><font color="#444">Gene: %s; Diplotype: %s; Phenotype: %s</font></p>' % (gene, ''.join(diplotype) , ''.join(phenotype)), file=f)
       
        drug_guide = drug_by_gene[['PAID', 'Source', 'Summary']].copy()
        drug_guide = drug_guide.drop_duplicates()
        for index, row in drug_guide.iterrows():
          if row.Summary.startswith('There are currently no'):
            print('<div class="alert alert-info-red"><a href=%s target="_blank" style="color: #7C3A37"><i class="fa-solid fa-circle-info"></a></i><b> %s: </b>%s</div>' % ("https://www.pharmgkb.org/guidelineAnnotation/"+row.PAID, row.Source, row.Summary), file=f)
          else:
            print('<div class="alert alert-info-blue"><a href=%s target="_blank"><i class="fa-solid fa-circle-info"></a></i><b> %s: </b>%s</div>' % ("https://www.pharmgkb.org/guidelineAnnotation/"+row.PAID, row.Source, row.Summary), file=f)
    
    ## Part 4: Diplotype Detail
    print('<h2 id="diplotype detail"><b>Diplotype Detail</b></h2>', file=f)
    print('<p class="main_lead">The PAnno model was applied to the prediction of diplotypes involving multi-variant variants. The genes involved include CYP2B6, CYP2C19, CYP2C8, CYP2C9, CYP2D6, CYP3A4, CYP3A5, CYP4F2, DPYD, NUDT15, SLCO1B1, TPMT, and UGT1A1. PAnno assumes that no variation occurs for the missing positions in the submitted VCFs, and the final inferred diplotypes are a composite ranking result.</p>', file=f)
    
    print('<h3 id="multi-variant"><b>Multi-variant allele</b></h3>', file=f)
    for gene in ["CYP2B6", "CYP2C8", "CYP2C9", "CYP2C19", "CYP2D6", "CYP3A4", "CYP3A5", "CYP4F2", "DPYD", "NUDT15", "SLCO1B1", "TPMT", "UGT1A1"]:
      diplotype_by_gene = multi_var[multi_var.Gene == gene]
      print('<h3><b>%s: %s</b></h3>' % (gene, ''.join(list(diplotype_by_gene.Diplotype.drop_duplicates()))), file=f)
      if (gene == "CYP2B6"):# & ("*29/*30" in list(diplotype_by_gene.Diplotype.drop_duplicates())):
        print('<div class="alert alert-info-red">Please notice that CYP2B6*29, CYP2B6*30 were not considered in the current version, which could potentially have an impact on the results.</div>', file=f)
      if (gene == "CYP2C19"):# & ("*36/*37" in list(diplotype_by_gene.Diplotype.drop_duplicates())):
        print('<div class="alert alert-info-red">Please notice that CYP2C19*36, CYP2C19*37 were not considered in the current version, which could potentially have an impact on the results.</div>', file=f)
      if (gene == "CYP2D6"):# & ("*5/*13/*61/*63/CNV" in list(diplotype_by_gene.Diplotype.drop_duplicates())):
        print('<div class="alert alert-info-red">Please notice that CYP2D6*5, CYP2D6*13, CYP2D6*61, CYP2D6*63, CYP2D6*68 and CYP2D6 CNVs were not considered in the current version, which could potentially have an impact on the results.</div>', file=f)
      if (gene == "SLCO1B1"):# & ("*48/*49" in list(diplotype_by_gene.Diplotype.drop_duplicates())):
        print('<div class="alert alert-info-red">Please notice that SLCO1B1*48, SLCO1B1*49 were not considered in the current version, which could potentially have an impact on the results.</div>', file=f)
      header = '<table id="customer_table" border="1" cellspacing="0">\n<tr><th>Position</th><th>Variant</th><th>Effect on Protein</th><th>Definition of Alleles</th><th>Detected Alleles</th></tr>'
      for index,row in diplotype_by_gene.iterrows():
        header = header + '\n<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (row['Position'], row['Variant'] , row['Effect on Protein'], row['Definition of Alleles'], row['Detected Alleles'])
      header = header + '\n</table>'
      print(header, file=f)
    
    print('<h3 id="single-variant"><b>Single-variant allele</b></h3>', file=f)
    header = '<table id="customer_table" border="1" cellspacing="0">\n<tr><th width="200px">Gene</th><th width="200px">Variant</th><th width="200px">Detected Alleles</th></tr>'
    for index, row in single_var.iterrows():
      header = header + '\n<tr><td>%s</td><td>%s</td><td>%s</td></tr>' % (row.Gene, row.Variant, row['Detected Alleles'])
    header = header + '\n</table>'
    print(header, file=f)
    
    ## Part 5: Phenotype Prediction
    print('<h2 id="phenotype prediction"><b>Phenotype Prediction</b></h2>', file=f)
    print('<p class="main_lead">For the clinically available drugs, PAnno integrates the effects of multiple diplotypes for each drug in terms of toxicity, dosage, efficacy, and metabolism. The predicted phenotypes are based on the original annotations described in the following section, and the integrated phenotypes are indicated as decreased, normal, and increased.</p>', file=f)
    header = '<table id="customer_table" border="1" cellspacing="0">\n<tr><th>Drug</th><th>Toxicity</th><th>Dosage</th><th>Efficacy</th><th>Metabolism</th></tr>'
    for drug in list(phenotype_predict.Drug.drop_duplicates()):
      drug_sub = phenotype_predict[phenotype_predict.Drug == drug]
      toxicity = ''
      dosage = ''
      efficacy = ''
      metabolism = ''
      other = ''
      for index, row in drug_sub.iterrows():
        if row.PhenotypeCategory == 'Toxicity':
          toxicity = row.Prediction
        if row.PhenotypeCategory == 'Dosage':
          dosage = row.Prediction
        if row.PhenotypeCategory == 'Efficacy':
          efficacy = row.Prediction
        if row.PhenotypeCategory == 'Metabolism':
          metabolism = row.Prediction
        if row.PhenotypeCategory == 'Other':
          other = row.Prediction
      
      # End of one drug
      if toxicity == '':
        toxicity = '-'
      if dosage == '':
        dosage = '-'
      if efficacy == '':
        efficacy = '-'
      if metabolism == '':
        metabolism = '-'
      header = header + '\n<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (drug, toxicity, dosage, efficacy, metabolism)
    
    header = header + '\n</table>'
    print(header, file=f)
    
    # Part 6: Clinical Annotation
    print('<h2 id="clinical annotation"><b>Clinical Annotation</b></h2>', file=f)
    print('<p class="main_lead">PAnno annotates PGx-related diplotypes using the high-confidence clinical annotations from PharmGKB (1A, 1B, 2A, 2B), which is the basis for predicting the phenotypes in the above section.</p>', file=f)
    
    header = '<table id="atable" border="1" cellspacing="0">\n<tr><th>Drug</th><th>Category</th><th>Gene</th><th>Variant</th><th>Diplotype</th><th>Level</th><th>Phenotype</th><th>Annotation</th></tr>'
    for drug in list(clinical_anno.Drug.drop_duplicates()):
      drug_sub = clinical_anno[clinical_anno.Drug == drug]
      # There needs to be a value dedicated to statistics corresponding to several catagories.
      count = len(drug_sub.PhenotypeCategory.drop_duplicates())
      header = header + '\n<tr><td rowspan="%s">%s</td>' % (len(drug_sub)+count,drug)
      for category in ['Toxicity','Dosage','Efficacy','Metabolism','Other']:
        drug_by_cat = drug_sub[drug_sub.PhenotypeCategory == category].sort_values(by=['EvidenceLevel', 'Gene', 'Variant', 'Diplotype'])
        if len(drug_by_cat) > 0:
          header = header + '\n<td rowspan="%s">%s</td></tr>' % (len(drug_by_cat)+1,category)
          for index, row in drug_by_cat.iterrows():
            header = header + '\n<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td><a href=%s target="_blank"><i class="fa-solid fa-circle-info"></a></i></td></tr>' % (row.Gene, row.Variant, row.Diplotype,  row.EvidenceLevel, row.PAnnoPhenotype, "https://www.pharmgkb.org/clinicalAnnotation/"+str(row.CAID))
    header = header + '\n</table>'
    print(header, file=f)
    
    # Part 7: About
    disclaimer = """
    <h2 id="about"><b>About</b></h2>
    <p class="main_lead">
      The report incorporates analyses of peer-reviewed studies and other publicly available information identified by PAnno by State Key Laboratory of Genetic Engineering from the School of Life Sciences and Human Phenome Institute, Fudan University, Shanghai, China. These analyses and information may include associations between a molecular alteration (or lack of alteration) and one or more drugs with potential clinical benefit (or potential lack of clinical benefit), including drug candidates that are being studied in clinical research.<br>
      <em>Note:</em> A finding of biomarker alteration does not necessarily indicate pharmacologic effectiveness (or lack thereof) of any drug or treatment regimen; a finding of no biomarker alteration does not necessarily indicate lack of pharmacologic effectiveness (or effectiveness) of any drug or treatment regimen.<br>
      <em>No Guarantee of Clinical Benefit:</em> This Report makes no promises or guarantees that a particular drug will be effective in the treatment of disease in any patient. This report also makes no promises or guarantees that a drug with a potential lack of clinical benefit will provide no clinical benefit.<br>
      <em>Treatment Decisions are Responsibility of Physician:</em> Drugs referenced in this report may not be suitable for a particular patient. The selection of any, all, or none of the drugs associated with potential clinical benefit (or potential lack of clinical benefit) resides entirely within the discretion of the treating physician. Indeed, the information in this report must be considered in conjunction with all other relevant information regarding a particular patient, before the patient's treating physician recommends a course of treatment. Decisions on patient care and treatment must be based on the independent medical judgment of the treating physician, taking into consideration all applicable information concerning the patient's condition, such as patient and family history, physical examinations, information from other diagnostic tests, and patient preferences, following the standard of care in a given community. A treating physician's decisions should not be based on a single test, such as this test or the information contained in this report.<br>
      When using results obtained from PAnno, you agree to cite PAnno.
    </p>
    </div>

    <div class="footer">
      <p>
        <strong>
          <a href="https://github.com/PreMedKB/PAnno" target="_blank">PAnno v0.3.0</a>
        </strong>
        - Written by Yaqing Liu, et al.,
        available at <a href="https://github.com/PreMedKB/PAnno" target="_blank">GitHub</a>,
        <a href="https://pypi.python.org/pypi/panno/" target="_blank">PyPI</a>, and <a href="http://anaconda.org/" target="_blank">Conda</a>.
        <br>
        Copyright &copy; 2021-2022 Center for Pharmacogenomics, Fudan University, China. All Rights Reserved.
      </p>
    </div>
    
    </body>
    </html>
    """
    print(disclaimer, file=f)

