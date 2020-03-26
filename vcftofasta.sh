#!/bin/bash

#subsets vcf and turns to fasta
subset_vcf_python_script=subset_vcf.py
#SOD1
SOD1_chrom_num=NC_037328
SOD1_start_position=3824612
SOD1_end_position=3833280
#PRLH
PRLH_chrom_num=NC_037349.1
PRLH_start_position=10030000
PRLH_end_position=11000000
#BTA22
BTA22_chrom_num=NC_037330.1
BTA22_start_position=117013542
BTA22_end_position=117014310

###Ogaden
ogaden_name_vcf= 
ogaden_SOD1_outfi=../../Data/vcf/ogaden_SOD1.vcf
ogaden_PRLH_outfi=../../Data/vcf/ogaden_PRLH.vcf
ogaden_BTA22_outfi=../../Data/vcf/ogaden_BTA22.vcf

#SOD1
python2 ${subset_vcf_python_script} ${ogaden_name_vcf} ${ogaden_SOD1_outfi} ${SOD1_chrom_num} ${SOD1_start_position} ${SOD1_end_position}
#PRLH
python2 ${subset_vcf_python_script} ${ogaden_name_vcf} ${ogaden_PRLH_outfi} ${PRLH_chrom_num} ${PRLH_start_position} ${PRLH_end_position}
#BTA22
python2 ${subset_vcf_python_script} ${ogaden_name_vcf} ${ogaden_BTA22_outfi} ${BTA22_chrom_num} ${BTA22_start_position} ${BTA22_end_position}


###N'dama
ndama_name_vcf= 
ndama_SOD1_outfi=../../Data/vcf/ndama_SOD1.vcf
ndama_PRLH_outfi=../../Data/vcf/ndama_PRLH.vcf
ndama_BTA22_outfi=../../Data/vcf/ndama_BTA22.vcf

#SOD1
python2 ${subset_vcf_python_script} ${ndama_name_vcf} ${ndama_SOD1_outfi} ${SOD1_chrom_num} ${SOD1_start_position} ${SOD1_end_position}
#PRLH
python2 ${subset_vcf_python_script} ${ndama_name_vcf} ${ndama_PRLH_outfi} ${PRLH_chrom_num} ${PRLH_start_position} ${PRLH_end_position}
#BTA22
python2 ${subset_vcf_python_script} ${ndama_name_vcf} ${ndama_BTA22_outfi} ${BTA22_chrom_num} ${BTA22_start_position} ${BTA22_end_position}

