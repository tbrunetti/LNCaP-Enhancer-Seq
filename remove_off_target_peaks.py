import sys

def main():
	
	temp=[]
	with open(sys.argv[1]) as input:
		for line in input:
			data=line.split('\t')
			temp.append(data)

	#use this part first
	#f=open('final-peaks-no-offtargets.txt', 'w')
	#f3=open('off-target-peaks.txt', 'w')
	#for x in range(0, len(temp)):
	#	if temp[x][4]=='FALSE\n':
	#		for i in range(0, len(temp[0])-1):
	#			f.write(str(temp[x][i])+'\t')
	#		f.write(str(temp[x][len(temp[0])-1]))
	#	else:
	#		for v in range(0, len(temp[0])-1):
	#			f3.write(str(temp[x][v])+'\t')
	#		f3.write(str(temp[v][len(temp[0])-1]))

	temp2=[]
	with open(sys.argv[2]) as input:
		for line in input:
			data=line.split('\t')
			temp2.append(data)
		
	f2=open('final-peaks-no-offtargets-with-fold-enrichments.txt', 'w')
	
	#for x in range(0, len(temp)):
	#	if temp[x][3]=='':
	#		for z in range(0, len(temp[0])-1):
	#			f2.write(str(temp[x][z])+'\t')
	#		f2.write(str(temp[x][len(temp[0])-1]))

	#	else:
	#		for i in range(0, len(temp2)):
	#			if temp[x][3]==temp2[i][3]:
	#				print 'here'
	#				for z in range(0, len(temp[0])-1):
	#					f2.write(str(temp[x][z])+'\t')
	#				f2.write(str(temp[x][len(temp[0])-1].rstrip('\n'))+'\t'+str(temp2[i][8]))
	#				break;

	peakIDs=[temp2[x][3] for x in range(0, len(temp2))]	
	
	for x in range(0, len(temp)):
		if temp[x][3] not in peakIDs:
			for z in range(0, len(temp[0])-1):
				f2.write(str(temp[x][z])+'\t')
			f2.write(str(temp[x][len(temp[0])-1]))


if __name__=='__main__':
	main();