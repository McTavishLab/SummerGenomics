

dna = open('sequence.fasta')
dna_total = dna.read()

t_length = len(file_contents)
a_total = file_contents.count('A')
a_percent = ((a_total / t_length)) * 100

g_total = file_contents.count('G')
g_percent = ((g_total) / (t_length)) * 100

t_total = file_contents.count('T')
t_percent = ((t_total / t_length)) * 100

c_total = file_contents.count('C')
c_percent = ((c_total) / (t_length)) * 100

print('dna_total')

print("The total of A bases is " + str(a_total))
print("The total of G bases is " + str(g_total))
print("The total of T bases is " + str(t_total))
print("The total of C bases is " + str(c_total))

print('The total length of the sample is' + str(t_length) + " bases")
print('The percent of A in the sample is' + str(round(a_percent, 2) + "%")
print('The percent of G in the sample is' + str(round(g_percent, 2) + "%")
print('The percent of T in the sample is' + str(round(t_percent, 2) + "%")
print('The percent of C in the sample is' + str(round(c_content, 2) + "%")
