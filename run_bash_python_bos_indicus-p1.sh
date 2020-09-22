#Example of a for loop in bash
#Lesly Lopez Fang
#hi

start=1
stop=98
step=1

for ((i=start;i<=stop;i+=step));do
  python2 calculate_d_dplus_genomewide_cows.py -infile vcf/ChrALL.vcf.gz -outfile d -p1 reference -p2 ndama -p3 indicine -p4 water_buffalo -meta pop_def_fi_breed.txt;
done


