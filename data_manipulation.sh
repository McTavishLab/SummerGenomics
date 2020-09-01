
#!/usr/bin/env bash


#strip ".sorted.dedup.q20.bam" out of label ids

### INSERT CODE FOR HOW WE GOT TO 'vcf_structure_filtered.vcf.gz'


##Set soem varibales for filenames, so it easy to re-run without overwriting data
STUB="ALL"
BEDNAME="ALL.AUTO"


## the vcf_structure_filtered.vcf.gz is not in the bzip format bcftools wants
## unzipping and bgzipping fixes that
## This file is for population analyses, and doesn't have outgroups.
gunzip -c vcf_structure_filtered.vcf.gz | bgzip  > ${STUB}.vcf.bgz

##Check file format
htsfile ${STUB}.vcf.bgz

## Index
bcftools index ${STUB}.vcf.bgz 

## GEt sample names from vcf file
bcftools query -l ${STUB}.vcf.bgz > samplenames.txt

## Use python script to pull population labels for sname names, and write out to csv file
## CSV file can be used for labelling in R
python get_label_pops.py -map label_match.csv -in samplenames.txt -out samplenames.csv

#get all autosomes from csv file (That I made from labels shown at https://www.ncbi.nlm.nih.gov/assembly/GCF_002263795.1)
CHRMS=$(head -n30 ChrmIDS.csv | tail -n29  | cut -d, -f2)

# Sample the vcf to the 29 autosomes
bcftools view ${STUB}.vcf.bgz --regions $CHRMS > ChrALL.vcf

# Filter to bi-allelic , with a minor allele frequency of 0.1 or greater.
plink2 --recode vcf bgz --vcf ChrALL.vcf --max-alleles 2 --min-alleles 2 --maf 0.1 --keep-allele-order --allow-extra-chr --make-bed --out $BEDNAME


## Admixture demands chromosomes as integers
## This rewrites the BIM file from plink to use chromosome numbers
while IFS='' read -r LINE || [ -n "${LINE}" ]; do
    echo "processing line: ${LINE}";
    ID=$(echo ${LINE} | cut -d, -f2);
    INT=$(echo ${LINE} | cut -d, -f3);
    sed -i "s/$ID/$INT/g" ALL.biallelic-only.bim
done < ChrmIDS.csv;

# Run admixture on the bed files, and the updated BIM file
admixture ALL.biallelic-only.bed 6

BED_FILE=ALL.biallelic-only.bed
OUTDIR=admix_results
mkdir -p $OUTDIR

for K in {2..12}; do
    CMD="cd $OUTDIR; dist/admixture_linux-1.3.0/admixture --cv -j8 $BED_FILE $K" #Normally you should give --cv as first option to admixture
    echo $CMD
done





