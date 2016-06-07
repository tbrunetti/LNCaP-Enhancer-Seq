import sys

def main():
	#input is merged bed file output from mergebed
	
	temp=[]
	with open(sys.argv[1]) as input:
		for line in input:
			data=line.split('\t')
			temp.append(data)

	window=250

	f=open('midpoint-newWindows-for-peakCalls.bed', 'w')

	for x in range(0, len(temp)):
		newSummit=(int(temp[x][1])+int(temp[x][2]))/2
		downstream=newSummit+window
		upstream=newSummit-window
		if upstream<0:
			upstream=0
		f.write(str(temp[x][0])+'\t'+str(upstream)+'\t'+str(downstream)+'\t'+str(temp[x][3]))


if __name__=='__main__':
	main();