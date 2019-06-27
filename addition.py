import sys

print("The name of the script is")
print(sys.argv[0])

print("The number of arguments is")
print(len(sys.argv))

print("all of the arguments are")
print(sys.argv)
#do some addition

#How would we print out the first argument, after the name of the script?
print("the first arg is:")
print(sys.argv[1])

#How would we print out the first argument, after the name of the script?
print("the second arg is:")
print(sys.argv[2])


x = int(sys.argv[1])
y = int(sys.argv[2])
z = x+y
#print out the value
print("The answer is")
print(z)
