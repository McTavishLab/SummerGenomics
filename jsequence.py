from __future__ import division
# prevents Python from rounding numbers below 1 to 0

cowfile = open("sequence.fasta")
file_contents = cowfile.read()
print(file_contents)
bos_length = len(file_contents)
print("The length of the sample is " + str(bos_length) + " bases")

g_count = file_contents.count('G')
# count the numbers of Gs in the fragment
print("The number of guanine bases is " + str(g_count))
g_content = ((g_count) / (bos_length)) * 100
# divides the amount of Gs by the length of the entire fragment
print{"The proportion of guanine in the sample is " + str(g_content) + "%"}
# add str to numerical values when printing to avoid syntax error

a_count = file_contents.count('A')
print("The number of adenine bases is " + str(a_count))
a_content = ((a_count / bos_length)) * 100
print{"The proportion of adenine in the sample is " + str(a_content) + "%"}

t_count = file_contents.count('T')
print("The number of thymine bases is " + str(t_count))
t_content = ((t_count / bos_length)) * 100
print{"The proportion of thymine in the sample is " + str(t_content) +"%"}

c_count = file_contents.count('C')
print("The number of cytosine bases is " + str(c_count))
c_content = ((c_count) / (bos_length)) * 100
print{"The proportion of cytosine in the sample is " + str(c_content)+"%"}