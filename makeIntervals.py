import sys

def main():
	#input is filtered peaks file from MACS 2.0 in tab delimited text format
	temp=[]
	with open(sys.argv[1]) as input:
		for line in input:
			data=line.split('\t')
			temp.append(data)

	#number of base pairs upstream and downstream from summit
	window=250

	f=open('windowsDefined_in_calledPeaks.txt', 'w')

	identifier=''
	for x in range(0, len(temp)):
		upstreamLoc=int(temp[x][4])-window
		downstreamLoc=int(temp[x][4])+window
		if upstreamLoc<0:
			upstreamLoc=0;
		if 'vehicle-input' in temp[x][9]:
			identifier='vehicle-input' 
		elif 'dht-vehicle' in temp[x][9]:
			identifier='dht-vehicle'
		elif 'dht-input' in temp[x][9]:
			identifier='dht-input'
		else:
			identifier='NA'
		f.write(str(temp[x][0])+'\t'+str(upstreamLoc)+'\t'+str(downstreamLoc)+'\t'+identifier+'\n')

if __name__=='__main__':
	main();
