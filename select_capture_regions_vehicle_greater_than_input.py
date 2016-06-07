import sys

#format of sys.argv[1]=tab delimited, 1st column=chr, 2nd column=start region, 3rd column=end region, 4th column=FC of normalized vehicle/input
def main():
	f=open('capture-regions-greater-than-input.txt', 'w')
	with open(sys.argv[1]) as input:
		for line in input:
			line=line.split('\t')
			if float(line[3].rstrip('\n'))>=1.0:
				f.write(str(line[0])+'\t'+str(line[1])+'\t'+str(line[2])+'\t'+str(line[3]))

if __name__=='__main__':
	main();
