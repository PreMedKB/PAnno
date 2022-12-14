#!/usr/bin/python
# -*- coding: UTF-8 -*-


import numpy as np
import re, itertools, json, os


def parse_input_allele(filtered_vcf, info):
  hap_define = info['haplotype_definition']
  hap_define_display = info['haplotype_definition_display']
  ref_hap = info['reference_haplotype']
  
  vcf_df_all = filtered_vcf.copy()
  vcf_df = vcf_df_all[vcf_df_all['#CHROM'] == info['chrom']]
  cols = vcf_df.columns.to_list()
  
  vcf_alleles = {}; vcf_alleles_display = {}
  hap_pos = list(hap_define[ref_hap].keys())
  for source_pos in hap_pos:
    # ref_hap_base, Only two loci of CYP2D6 gene will have more than one ref_hap_base
    ref_hap_base = hap_define[ref_hap][source_pos]
    ref_hap_base_display = hap_define_display[ref_hap][source_pos].split(':')[-1]
    
    # Get all possible bases at this position
    defined = []
    for key in hap_define.keys():
      defined.extend(hap_define[key][source_pos])
    defined = list(set(defined))
    
    # Transfer the positions into the format of list
    pos_rs = source_pos.split(':')
    pos = []
    tmp = pos_rs[0].split('-')
    if len(tmp) > 1:
      for p in range(int(tmp[0]), int(tmp[1])+1):
        pos.append(p)
    else:
      pos = [int(pos_rs[0])]
    
    ###### Start to parse the input vcf
    # Filter by pos and rs_id
    mat = vcf_df[(vcf_df['POS'].isin(pos)) | (vcf_df['ID'] == pos_rs[1])]
    if mat.empty:
      vcf_alleles[source_pos] = (ref_hap_base, ref_hap_base)
      vcf_alleles_display[source_pos] = 'Missing'
    else:
      is_wild_type = 1
      for index, row in mat.iterrows():
        cols = mat.columns.to_list()
        format = row[cols.index("FORMAT")].split(":")
        gt = row[-1].split(":")[format.index("GT")]
        if re.findall('0', gt) == ['0', '0']:
          continue
        else:
          ## Only process the first line which genotype is not wild type.
          ## !!! Therefore, the end of 'else' is break
          tuple_res = (); tuple_res_display = ()
          is_wild_type = 0
          ref = row[cols.index("REF")]
          alts = row[cols.index("ALT")].split(",")
          opts = [ref]; opts.extend(alts)
          gts = re.split('/|\|', gt)
          if len(gts) == 1: # chrX
            gts.append(gts[0])
          for gt_index in gts:
            base = None; base_raw = None
            if gt_index == '0':
              base = ref_hap_base; base_raw = ref_hap_base_display
            else:
              alt = opts[int(gt_index)]
              # SNP #
              if len(alt) == len(ref):
                base = alt
                base_raw = alt
              ### ! If alt was not match the definition, try to combine with the following position base and test again
              # Del #
              elif len(alt) < len(ref):
                base = 'del%s' % ref[len(alt):]
                if base not in defined:
                  pos_of_mat = mat.index.to_list()
                  pos_order = pos_of_mat.index(index)
                  if pos_order < len(pos_of_mat)-1 and mat.loc[pos_of_mat[pos_order+1], 'POS'] == row.POS+1:
                    new_row = mat.loc[pos_of_mat[pos_order+1],]
                    base = 'del%s' % ref[len(alt)+1:] + new_row.REF
                  elif int(row.POS) == 42128173 and base == 'delCTT':
                    base = 'delTCT'
                ## A smooth judge part
                if base not in defined:
                  # small indel
                  if ref_hap_base[0].startswith('ref') and base[-1] == ref_hap_base[0][-2]:
                    base = 'del' + base[4:] + ref_hap_base[0][-1]
                  # long del
                  else:
                    modd = ref_hap_base[0].replace('ref', '')
                    if re.search(modd, base):
                      matched_span = re.search(modd, base).span()
                      if modd.startswith(base[matched_span[1]:]):
                        base = 'del' + modd * int((matched_span[1] - matched_span[0])/len(modd) + 1)
                      else:
                        base = 'del' + modd * int((matched_span[1] - matched_span[0])/len(modd))
                base_raw = base
                if base not in defined:
                  print('Warning in Del!'); print(row.T); print(pos); print(base)
              # Ins #
              elif len(alt) > len(ref):
                base = 'ins%s' % alt[len(ref):]
                if base not in defined:
                  pos_of_mat = mat.index.to_list()
                  pos_order = pos_of_mat.index(index)
                  if pos_order < len(pos_of_mat)-1 and mat.loc[pos_of_mat[pos_order+1], 'POS'] == row.POS+1:
                    new_row = mat.loc[pos_of_mat[pos_order+1],]
                    base = 'ins%s' % alt[len(ref)+1:] + new_row.REF
                ## A smooth judge part
                if base not in defined:
                  # small indel
                  if ref_hap_base[0].startswith('ref') and base[-1] == ref_hap_base[0][-2]:
                    base = 'ins' + base[4:] + ref_hap_base[0][-1]
                  # long dup
                  else:
                    flag = 0
                    if ref_hap_base[0].startswith('ref') is False:
                      for r in defined:
                        if r.startswith('delins'):
                          modd = 'C'; flag = 1; break
                    else:
                      modd = ref_hap_base[0].replace('ref', '')
                    if re.search(modd, base):
                      matched_span = re.search(modd, base).span()
                      if modd.startswith(base[matched_span[1]:]):
                        base = 'ins' + modd * int((matched_span[1] - matched_span[0])/len(modd) + 1)
                      else:
                        base = 'ins' + modd * int((matched_span[1] - matched_span[0])/len(modd))
                    if flag == 1:
                      base = 'del' + base + 'C'
                base_raw = alt
                if base not in defined:
                  print('Warning in Ins or Dup!'); print(row.T); print(pos); print(base)
            ## Add the result into tuple_res
            tuple_res = tuple_res + (base,)
            tuple_res_display = tuple_res_display + (base_raw,)
          break
      
      if is_wild_type == 1:
        vcf_alleles[source_pos] = (ref_hap_base, ref_hap_base)
        vcf_alleles_display[source_pos] = ref_hap_base_display + '/' + ref_hap_base_display
      else:
        vcf_alleles[source_pos] = tuple_res
        # vcf_alleles_display[source_pos] = ';'.join(['|'.join(res) for res in list(zip(tuple_res_display[0], tuple_res_display[1]))])
        vcf_alleles_display[source_pos] = tuple_res_display[0] + '/' + tuple_res_display[1]
        if None in tuple_res:
          print('Warning! None was reported.')
  
  # Check the format of output
  fine_vcf_alleles = {}
  for source_pos in vcf_alleles.keys():
    tuple_res = ()
    for base in vcf_alleles[source_pos]:
      if type(base) != list:
        tuple_res = tuple_res + ([base],)
      else:
        tuple_res = tuple_res + (base,)
    fine_vcf_alleles[source_pos] = tuple_res
  
  return(fine_vcf_alleles, vcf_alleles_display)


def predict_diplotype(vcf_alleles, info, race):
  hap_define = info['haplotype_definition']
  # CYP2C19 order
  all_hap = list(hap_define.keys())
  if all_hap[0] == '*38':
    all_hap = ['*1', '*2', '*3', '*4', '*5', '*6', '*7', '*8', '*9', '*10', '*11', '*12', '*13', '*14', '*15', '*16', '*17', '*18', '*19', '*22', '*23', '*24', '*25', '*26', '*28', '*29', '*30', '*31', '*32', '*33', '*34', '*35', '*38', '*39']
  hap_mutated_loci = info['haplotype_mutated_loci']
  diplotype_candidates = list(itertools.combinations_with_replacement(all_hap, 2))
  ### 1st Ranking by haplotype definition
  candidate = {}
  for dip in diplotype_candidates:
    hap1 = hap_define[dip[0]]
    hap2 = hap_define[dip[1]]
    ## Calculate difference
    difference_step1 = dict(zip(vcf_alleles.keys(), [np.nan] * len(hap1)))
    for pos_rs in vcf_alleles.keys():
      defined_alleles = list(itertools.product(hap1[pos_rs], hap2[pos_rs]))
      tuple_res = vcf_alleles[pos_rs]
      alleles = list(itertools.product(tuple_res[0], tuple_res[1]))
      # Must sort the results
      defined_alleles = [sorted(ele) for ele in defined_alleles]
      alleles = [sorted(ele) for ele in alleles]
      # Extact matched
      score1 = []; score2 = []
      for allele in alleles:
        if allele in defined_alleles:
          #difference_step1[pos_rs] = 0
          score1 = [0]; score2 = [0]
          break
        else:
          diff = []
          ### Part 1: Input vcf can have more variants than definition but less is better.
          for define in defined_alleles:
            in_vcf_notin_defined = len(set(allele).difference(set(define)))
            if in_vcf_notin_defined == 1:
              score1.append(-1)
            else:
              score1.append(-2)
          ### Part 2: Haplotype muated loci. We need to make a case-by-case judgment.
          # When only one haplotype is involved in a locus, we do not need to ensure that both strands meet the requirements.
          allele_cp = allele
          for hap in dip:
            score2_hap = 0
            # It is possible to delete both items of allele for degenerate bases.
            if len(allele_cp) == 0:
              allele_cp = allele
            if pos_rs in hap_mutated_loci[hap]:
              star_define = hap_define[hap][pos_rs]
              star_matched = set(allele_cp).intersection(set(star_define))
              for m in star_matched:
                allele_cp.remove(m)
              if len(allele_cp) == 2:
                score2_hap = -99
            score2.append(score2_hap)
      # Add the results of score1 and score2
      difference_step1[pos_rs] = max(score1) + min(score2)
      # print(pos_rs, score1, score2)
    if min(difference_step1.values()) > -99:
      candidate['%s/%s' % (dip[0], dip[1])] = difference_step1
  
  # print(candidate.keys())
  # Whether is 0
  exact_match_res = []
  for dip in candidate.keys():
    # print(dip, candidate[dip].values())
    if set(candidate[dip].values()) == {0}:
      exact_match_res.append(dip)
  
  # 1. select diplotypes which 1st rank is max
  rank_step1 = {}
  for dip in candidate.keys():
    rank_step1[dip] = sum(candidate[dip].values())
  
  uniq_diff = sorted(set(rank_step1.values()))
  rank_step1_res = [k for k,v in rank_step1.items() if v == max(uniq_diff)]#; rank_step1_res
  # 2. only ranked the above diplotypes with population frequency
  dip_freq = info['diplotype_frequency']
  rank_step2 = {}
  for dip in rank_step1_res:
    rank_step2[dip] = dip_freq[dip][race]
  uniq_freq = sorted(set(rank_step2.values()))
  final_rank_res = [k for k,v in rank_step2.items() if v == max(uniq_freq)]#; final_rank_res
  return("; ".join(exact_match_res), "; ".join(rank_step1_res), "; ".join(final_rank_res))


def predict(filtered_vcf, race, gene_list):
  panno_dip_fp = os.path.join(os.path.dirname(__file__), 'assets/pgx_diplotypes.json')
  # panno_dip_fp = "./panno/assets/pgx_diplotypes.json"
  panno_dip_base = json.loads(open(panno_dip_fp).read())
  dic_diplotype = {}
  dic_diplotype_detail = {}
  for gene in gene_list:
    info = panno_dip_base[gene]
    hap_define_display = info['haplotype_definition_display']
    vcf_alleles, vcf_alleles_display = parse_input_allele(filtered_vcf, info)
    exact_match_res, rank_step1_res, final_rank_res = predict_diplotype(vcf_alleles, info, race)
    
    if final_rank_res == '':
      final_rank_res = '-'
    
    # Detail of diplotypes
    if final_rank_res != '-':
      haplotypes = set(re.split('; |/', final_rank_res))
    else:
      haplotypes = [info['reference_haplotype']]
    diplotype_details = []
    for source_pos in vcf_alleles_display.keys():
      detected_allele = vcf_alleles_display[source_pos]
      base_all = []
      for hap in haplotypes:
        chrom, nc, ng, rs, pc, base = hap_define_display[hap][source_pos].split(':')
        # position
        matchobj = re.search(r'\w\.(\d+)\_(\d+)(del|ins)(\w*)', ng)
        if matchobj:
          pos = int(matchobj.group(1))
        else:
          matchobj = re.search(r'\w\.(\d+)(\w*)', ng)
          if matchobj:
            pos = matchobj.group(1)
          else:
            print(ng)
        base_all.append(hap + ':' + base)
      identified_allele = '; '.join(base_all)
      diplotype_details.append((chrom, pos, nc, ng, rs, pc, identified_allele, detected_allele))
    
    # Collect the results
    dic_diplotype[gene] = {'exact_res': exact_match_res, 'step1_res': rank_step1_res, 'step2_res': final_rank_res, 'detail': diplotype_details}
    
  return(dic_diplotype)
