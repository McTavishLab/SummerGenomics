
#!/usr/bin/env bash
#examples on how to label the files 
##im sure there are ways to make it so that we dont have to manually input everything? ?
sample=
sample.1= 
sample.2=
sample.trimmed_1=
sample.trimmed_2=
sample.single=
reference_genome=
mapping=sample.sam
mapping_2=sample.fixmate.bam
mapping_3=sample.sorted.bam
mapping_4=sample.sorted.dedup.bam
mapping_5=sample.sorted.dedup.q20.bam
#steps needed for grabbing data from ncbi 
fastq-dump --split-files $sample    
sickle pe -f sample.1 -r sample.2 -o sample.trimmed_1 -p sample.trimmed_2 -s sample.single 
fastqc -o sample.trimmed_1 some_directory/*.fastq.gz ## repeat with other trimmed data    
bwa index $reference_genome
samtools fadix $reference_genome
bwa mem $reference_genome $sample.trimmed_1 $sample.trimmed_2 > $mappings
#Preprocessing the alignment 
samtools sort -n -O sam $mapping | samtools fixmate -m -O bam - $mapping_2
samtools sort -O bam -o $mapping_3 $mapping_2
samtools markdup -r -S $mapping_3 $mapping_4
samtools view -h -b -q 20 $mapping_4 > $mapping_5
#creating vcf
##add any other alignments you want in the vcf
samtools mpileup -u -g -f $reference_genome $sample_one $sample_two  | bcftools call -v -m -O z -o $vcf_name
##Filtering vcf
vcftools --gzvcf $vcf_name --remove-indels --maf $MAF --max-missing $MISS --minQ $QUAL --recode --stdout | gzip -c > $VCF_OUT
#we only want chromosome data 
#chromIDs can be found:https://www.ncbi.nlm.nih.gov/assembly/GCF_002263795.1
bcftools view test.vcf.bgz --regions   NC_037328.1, NC_037329.1, NC_037330.1, NC_037331.1, NC_037332.1, NC_037333.1, NC_037334.1, NC_037335.1, NC_037336.1, NC_037337.1, NC_037338.1, NC_037339.1, NC_037340.1, NC_037341.1, NC_037342.1, NC_037343.1, NC_037344.1, NC_037345.1, NC_037346.1, NC_037347.1, NC_037348.1, NC_037349.1, NC_037350.1, NC_037351.1, NC_037352.1, NC_037353.1, NC_037354.1, NC_037355.1, NC_037356.1, NC_037357.1 >   ChrALL.vcf
####STRUCTURE PLOTS
## creating Vcf for structure plots this vcf is only used for structure plot 
vcftools --remove-indv $outgroup --vcf $VCF_OUT --recode --out $no_outgroup.vcf 
#remove multiallelic-sites can be combined for when chroms are pulled out  
bcftools view --max-alleles 2 --exclude-types indels $no_outgroup > $no_ma_no_outgroup
#vcf to bed format 
plink2 --vcf $no_ma_no_outgroup --double-id --allow-extra-chr --set-missing-var-ids @:# --make-bed -out $bed_files
#fastStrucutre 
python structure.py -K 3 --input=genotypes --output=genotypes_output
python distruct.py -K 3--input=test/testoutput_simple --output=test/testoutput_simple_distruct.svg
##calculate D+ genomewide use the following 
#have a meta file with "samplename in vcf\tsimple name"
bash ../SharedRepos/SummerGenomics/run_bash_python_bos_indicus-p1.sh

## for networks use vcf with outgroup
## make sure that this vcf has an outgroup!
#add the outgroup by doing 
vcftools --keep ../../water_buffalo_2.sorted.dedup.q20.bam --gzvcf vcf_for_structure_plot.vcf.gz --recode --out waterbuff_only.vcf.gzgit clone https://github.com/crsl4/PhyloNetworks.jl.git
bcftools merge vcf_structure_filtered.vcf.gz waterbuff_only.vcf.gz > filtered_and_waterbuff.vcf
#you will need the scripts folder 
##maybe move the scripts folder into the folder where you want to place your analysis in 
mkdir input 
mkdir input/nexus 
mkdir fasta 
mkdir vcf
mkdir raxml 
mkdir raxml/bootstrap
mkdir astral 
mkdir snaq
#subset vcfs into 50K wqindows 
python creatingwindows.py $vcf_name $vcf_subset $window_size 
#convert the subsets into fasta & nexus files 
bash converting_windowa_to_vcf.sh #(does all this )
mv *.nex input/nexus/.
##we ran the raxml and astral part for the networks 
###make sure to give the raxml.pl file the astral directory 
../scripts/raxml.pl --seqdir=input/nexus --raxmldir=raxml --astraldir=astral > mylog 2>&1 &
java -jar astral -i raxml/besttrees.tre -b astral/BSlistfiles -r 100 -o astral/astral.tre > astral/astral.screenlog 2>&1
##Then in Julia 
using PhyloNetworks
using PhyloPlots
using RCall 
using Distributed #allows you to  run the anaylsis on multiple processors 
##this just loads in the trees 
raxmlCF = readTrees2CF("raxml/besttrees.tre", writeTab=false, writeSummary=false)
astraltree = readMultiTopology("astral/astral.tre")[102] 
#estimating networks 
net0= snaq!(astraltree, raxmlCF, hmax=0, filename="net0_raxml") ## no hybrids
net1= snaq!(net0, raxmlCF, hmax=1, filename="net1_raxml") ## 1 hybridization event 
net2= snaq!(net1, raxmlCF, hmax=2, filename="net2_raxml") ## 2 hybridization events 
#ploting the created networks 
##root the network at outgroup
rootatnode!(net0, "outgroup")
plot(net0, :R);
##repeat for other networks 
#to see hybridization events b 
plot(net1, :R, showGamma=true);
##check which hybridization is most likely 
scores = [net0.loglik, net1.loglik, net2.loglik]
R"pdf"("score-vs-h.pdf", width=4, height=4);
R"plot"(x=0:2, y=scores, type="b", xlab="number of hybridizations h",
        ylab="network score");
R"dev.off"();

## bootstrapping 
bootTrees = readBootstrapTrees("astral/BSlistfiles")
bootnet = bootsnaq(net0, bootTrees, hmax=1, nrep=50, runs=3,
                   filename="bootsnaq1_raxmlboot")
bootnet = readMultiTopology("bootsnaq1_raxmlboot.out");

rootatnode!(net1, "6")
rotate!(net1, -4)

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





