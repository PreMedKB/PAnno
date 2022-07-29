#!/usr/bin/python
# -*- coding: UTF-8 -*-


import time, os

def report(race, pgx_summary, dic_diplotype, clinical_anno_table, dosing_guideline_table, fp, sample_id):

  with open(fp, 'w+') as f:
    
    ## Style
    # css_fp = os.path.join(os.path.dirname(__file__), 'assets/custom.css')
    css_fp = 'https://raw.githack.com/premedkb/panno/main/panno/assets/custom.css'
    logo_fp = 'https://raw.githubusercontent.com/premedkb/panno/main/docs/images/panno_logo.png'
    icon_fp = 'https://raw.githubusercontent.com/premedkb/panno/main/docs/images/panno_icon.png'
    
    head_nav="""
    <!doctype html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <title>PAnno Report</title>
      <link rel="shortcut icon" href="%s">
      <script src="https://kit.fontawesome.com/e540049a97.js" crossorigin="anonymous"></script>
      <link rel="stylesheet" type="text/css" href="%s">
    </head>
    
    <body>
    <div class="side-nav-wrapper">
      <div class="side-nav">
        <ul class="mqc-nav collapse navbar-collapse">
        <h1>
          <a href="#">
            <img src="%s" alt="PAnno">
            <br class="hidden-xs">
            <small class="hidden-xs">%s</small>
          </a>
        </h1>
          <li><a href="#pgx summary" class="nav-l1"><b>&nbsp;PGx Summary</b></a></li>
          <li><a href="#toxicity" class="nav-l2">&nbsp;&nbsp;Toxicity</a></li>
          <li><a href="#dosage" class="nav-l2">&nbsp;&nbsp;Dosage</a></li>
          <li><a href="#efficacy" class="nav-l2">&nbsp;&nbsp;Efficacy</a></li>
          <li><a href="#metabolism/pk" class="nav-l2">&nbsp;&nbsp;Metabolism/PK</a></li>
          <li><a href="#dosing guideline" class="nav-l1"><b>&nbsp;Dosing Guideline</b></a></li>
          <li><a href="#diplotype detail" class="nav-l1"><b>&nbsp;Diplotype Detail</b></a></li>
          <li><a href="#pgx annotation" class="nav-l1"><b>&nbsp;PGx Annotation</b></a></li>
          <li><a href="#about" class="nav-l1"><b>&nbsp;About</b></a></li>
        </ul>
      </div>
    </div>
    
    <div class="main_page">
    """
    print(head_nav%(icon_fp, css_fp, icon_fp, 'v0.2.0'), file=f)
   
    ## Part 0: Basic information
    basic_info = """
    <h1 id="page_title">
      <a href="https://github.com/PreMedKB/PAnno" target="_blank">
        <img src="%s" alt="PAnno">
      </a>
    </h1>
    <p class="head_lead">
      An automated clinical pharmacogenomics annotation tool to report drug responses and prescribing recommendations by parsing the germline variants.
    </p>
    <blockquote>
      <p style="font-size:0.95rem;">Sample ID: %s<br>Biogeographic Group: %s<br>Report Time: %s</p>
    </blockquote>
    """
    print(basic_info%(logo_fp, sample_id, race, time.asctime(time.localtime(time.time()))), file=f)
    
    ## Part 1: Sort disclaimer
    disclaimer_short = """
    <div class="alert alert-info-yellow">
      <b>Disclaimer:</b> The PAnno report iterates as the release version changes. In the current release, you should only use it to evaluate whether PAnno will compile and run properly on your system. All information in the report is interpreted directly from the uploaded VCF file. Users recognize that they use it at their own risk.
    </div>
    """
    print(disclaimer_short, file=f)

    ## Part 2: Pharmacogenomics Annotation
    part2_header = """
    <h2 id="pgx summary"><b>PGx Summary</b></h2>
    <p class="main_lead">PAnno combines genotypes with PharmGKB's clinical annotations to summarise a patient's response to a specific drug across four dimensions, including <font color="#444"><b>toxicity</b></font>, <font color="#444"><b>dosage</b></font>, <font color="#444"><b>efficacy</b></font>, <font color="#444"><b>metabolism/PK</b></font>. Response levels are indicated using <font color="#8E529A"><b>decreased</b></font>, <font color="#653F92"><b>moderate</b></font> and <font color="#44308d"><b>increased</b></font>. Results with variant-specific prescribing guidance in professional clinical guidelines or FDA-approved drug label annotations will be labeled as <font color="#54A052"><b>Level A</b></font>, otherwise as <font color="#3978B1"><b>Level B</b></font>.</p>
    """
    print(part2_header, file=f)
    
    table_html = """
    <table id="customer_table" border="1" cellspacing="0">
      <tr>
        <th bgcolor="#ffffff" width="70px"></th>
        <th><font color="#8E529A"><i class="fa-solid fa-square-caret-down"></i> Decreased</font></th>
        <th><font color="#653F92"><i class="fa-solid fa-square-minus"></i> Moderate</font></th>
        <th><font color="#44308d"><i class="fa-solid fa-square-caret-up"></i> Increased</font></th>
      </tr>
      <tr>
        <td bgcolor="#54A052"><font color="white"><b>Level A</b></font></td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
      </tr>
      <tr>
        <td bgcolor="#3978B1"><font color="white"><b>Level B</b></font></td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
      </tr>
    </table>
    """
    
    categories = ['Toxicity', 'Dosage', 'Efficacy', 'Metabolism/PK']
    fa = dict(zip(categories, ['fa-skull-crossbones', 'fa-pills', 'fa-vial-circle-check', 'fa-disease', 'fa-feather-pointed']))
    for cat in categories:
      print('<h3 id="%s"><i class="fa-solid %s"></i><b> %s</b></h3>' % (cat.lower(), fa[cat], cat), file=f)
      i = 0
      html_input = []
      cat_pgx = pgx_summary[pgx_summary.PhenotypeCategory == cat]
      if cat_pgx.empty:
        print('<div class="alert alert-info-red">No clinical annotations matched for this category.</div>', file=f)
      else:
        response = ['Decreased', 'Moderate', 'Increased']
        levels = ['A', 'B']
        for level in levels:
          for res in response:
            tmp = cat_pgx[(cat_pgx.Response == res) & (cat_pgx.EvidenceLevel == level)]
            if tmp.empty:
              html_input.append('')
            else:
              html_input.append('; '.join(tmp.index.to_list()))
            i = i+1
        print(table_html%(html_input[0], html_input[1], html_input[2],
                          html_input[3], html_input[4], html_input[5]), file=f)
      
    ## Part 3: Dosing Guideline
    print('<h2 id="dosing guideline"><b>Dosing Guideline</b></h2>', file=f)
    print('<p class="main_lead">PAnno integrates brief guidelines of genotype-based dosing recommendations on a drug-by-drug basis. Original prescribing information was collected by PharmGKB, primarily from the <a href="http://cpicpgx.org/">Clinical Pharmacogenetics Implementation Consortium</a> (CPIC), the <a href="https://www.knmp.nl/dossiers/farmacogenetica/">Dutch Pharmacogenetics Working Group</a> (DPWG), the <a href="https://cpnds.ubc.ca/">Canadian Pharmacogenomics Network for Drug Safety</a> (CPNDS), the French National Network of Pharmacogenetics (RNPGx).</p>', file=f)
    # Drug - Detected variant or alleles - Dosing guidelines
    for drug in list(dosing_guideline_table.Drug.drop_duplicates()):
      print('<h3><b>%s</b></h3>' % drug, file=f)
      drug_sub = dosing_guideline_table[dosing_guideline_table.Drug == drug]
      for gene in list(drug_sub.Gene.drop_duplicates()):
        drug_by_gene = drug_sub[drug_sub.Gene == gene]
        # drug_by_gene.insert(drug_by_gene.shape[1], 'Report', drug_by_gene.Variant.str.cat(drug_by_gene.Alleles, sep=": "))
        print('<p><font color="#444">Related Gene: %s<br>Detected Alleles: %s</font></p>' % (gene, "; ".join(list(drug_by_gene.Report.drop_duplicates()))), file=f)
        drug_guide = drug_by_gene[['DosingURL', 'DosingSource', 'DosingAnnotation']].copy()
        drug_guide = drug_guide.drop_duplicates()
        for index, row in drug_guide.iterrows():
          if row.DosingAnnotation.startswith('There are currently no'):
            #print('<div class="alert alert-info-yellow"><a href=%s target="_blank" style="color: #8a6d3b"><i class="fa-solid fa-circle-info"></a></i><b> %s: </b>%s</div>' % (row.DosingURL, row.DosingSource, row.DosingAnnotation), file=f)
            print('<div class="alert alert-info-red"><a href=%s target="_blank" style="color: #7C3A37"><i class="fa-solid fa-circle-info"></a></i><b> %s: </b>%s</div>' % (row.DosingURL, row.DosingSource, row.DosingAnnotation), file=f)
          else:
            print('<div class="alert alert-info-blue"><a href=%s target="_blank"><i class="fa-solid fa-circle-info"></a></i><b> %s: </b>%s</div>' % (row.DosingURL, row.DosingSource, row.DosingAnnotation), file=f)
    
    ## Part 4: Diplotype Detail
    print('<h2 id="diplotype detail"><b>Diplotype Detail</b></h2>', file=f)
    print('<p class="main_lead">PAnno predicts the diplotypes for PGx genes with star (*) or named allele information, which include ABCG2, CACNA1S, CFTR, CYP2B6, CYP2C8, CYP2C9, CYP2C19, CYP3A4, CYP3A5, CYP4F2, DPYD, G6PD, MT-NR1, NUDT15, RYR1, SLCO1B1, TPMT, UGT1A1, and VKORC1. PAnno assumes that no variation occurs for the missing positions in the submitted VCFs, and the final inferred diplotypes are a composite ranking result.</p>', file=f)
    for gene in list(dic_diplotype.keys()):
      print('<h3><b>%s: %s</b></h3>' % (gene, dic_diplotype[gene]['step2_res']), file=f)
      gene_detail = dic_diplotype[gene]['detail']
      header = '<table id="customer_table" border="1" cellspacing="0">\n<tr><th>Position</th><th width="120px">rsID</th><th width="200px">Effect on Protein</th><th width="275px">Definition of Alleles</th><th width="200px">Detected Alleles</th></tr>'
      for pos_res in gene_detail:
        position = pos_res[0] + ':' + pos_res[1] + ':' + pos_res[2]
        header = header + '\n<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (position, pos_res[3], pos_res[4], pos_res[5], pos_res[6])
      header = header + '\n</table>'
      print(header, file=f)
    
    ## Part 5: PGx Annotation
    print('<h2 id="pgx annotation"><b>PGx Annotation</b></h2>', file=f)
    print('<p class="main_lead">PAnno annotates PGx-related single-locus genotypes and predicted diplotypes using the knowledge from PharmGKB, which is the basis for predicting the individual drug response in the PGx summary.</p>', file=f)
    detail = clinical_anno_table.drop(columns=['Class']).reset_index(drop = True)
    header = '<table id="customer_table" border="1" cellspacing="0">\n<tr><th width="60px"></th><th>Gene</th><th>Variant</th><th>Alleles</th><th>Drug</th><th>Evidence</th><th>Category</th><th>Function</th></tr>'
    for index, row in detail.iterrows():
      header = header + '\n<tr><td>%s <a href=%s target="_blank" style="color: #ffb30e"><i class="fa-solid fa-up-right-from-square"></i></a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (index+1, row.URL, row.Gene, row.Variant, row.Alleles, row.Drug, row.EvidenceLevel, row.PhenotypeCategory, row.Function)
    header = header + '\n</table>'
    print(header, file=f)
    
    # Part 4: About
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
          <a href="https://github.com/PreMedKB/PAnno" target="_blank">PAnno v0.2.0</a>
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

