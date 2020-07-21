#Example of a for loop in bash
#Lesly Lopez Fang
#hi

start=1
stop=100
step=1

for ((i=start;i<=stop;i+=step));do
  python2 calculate_d_genomewide_cows.py -infile ../Data/summer.vcf.gz -outfile ../Results/D_Dplus_genomewide_p1bt_p2_sanga_indicus_p3_bi_p4_bb.csv -p1 bos_taurus -p2 sanga_indicus -p3 bos_indicus -p4 bison_bison -meta ../Data/meta_cow_summer.csv;
done


