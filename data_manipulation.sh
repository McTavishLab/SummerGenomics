

#strip ".sorted.dedup.q20.bam" out of label ids

### INSERT CODE FOR HOW WE GOT TO 'vcf_structure_filtered.vcf.gz'

STUB="ALL"
BEDNAME="ALL.AUTO"

gunzip -c vcf_structure_filtered.vcf.gz | bgzip  > ${STUB}.vcf.bgz

bcftools index ${STUB}.vcf.bgz 


bcftools query -l ${STUB}.vcf.bgz > samplenames.txt
python get_label_pops.py -map label_match.csv -in samplenames.txt -out samplenames.csv



#CHRMS="NC_037328.1, NC_037329.1, NC_037330.1, NC_037331.1, NC_037332.1, NC_037333.1, NC_037334.1, NC_037335.1, NC_037336.1, NC_037337.1, NC_037338.1, NC_037339.1, NC_#037340.1, NC_037341.1, NC_037342.1, NC_037343.1, NC_037344.1, NC_037345.1, NC_037346.1, NC_037347.1, NC_037348.1, NC_037349.1, NC_037350.1, NC_037351.1, NC_037352.1, NC_037353.1, NC_037354.1, NC_037355.1, NC_037356.1, NC_037357.1"

#get all autosomes
CHRMS=$(head -n30 ChrmIDS.csv | tail -n29  | cut -d, -f2)

bcftools view ${STUB}.vcf.bgz --regions $CHRMS   >   ChrALL.vcf

plink2 --recode vcf bgz --vcf ChrALL.vcf --max-alleles 2 --min-alleles 2 --maf 0.1 --keep-allele-order --allow-extra-chr --make-bed --out $BEDNAME


## Admixture demands chromosomes as integers

while IFS='' read -r LINE || [ -n "${LINE}" ]; do
    echo "processing line: ${LINE}";
    ID=$(echo ${LINE} | cut -d, -f2);
    INT=$(echo ${LINE} | cut -d, -f3);
    sed -i "s/$ID/$INT/g" ALL.biallelic-only.bim
done < ChrmIDS.csv;


admixture ALL.biallelic-only.bed 6

#!/usr/bin/env bash

BED_FILE=ALL.biallelic-only.bed
OUTDIR=admix_results
mkdir -p $OUTDIR

for K in {2..12}; do
    CMD="cd $OUTDIR; dist/admixture_linux-1.3.0/admixture --cv -j8 $BED_FILE $K" #Normally you should give --cv as first option to admixture
    echo $CMD
    # sbatch -c 8 --mem 12000 --wrap="$CMD"
done





