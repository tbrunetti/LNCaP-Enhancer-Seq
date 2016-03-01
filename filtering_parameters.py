import sys

def removeReadCounts():

	coverageCountMin=10
	f=open('filtered-all-reps-min-coverage-'+str(coverageCountMin)+'-'+str(sys.argv[1][:-4])+'.txt', 'w')
	with open(sys.argv[1]) as input:
		for line in input:
			lowInputCounts=0
			line=line.split('\t')
			if float(line[8])<coverageCountMin:
				lowInputCounts=lowInputCounts+1
			if float(line[9])<coverageCountMin:
				lowInputCounts=lowInputCounts+1
			if float(line[10])<coverageCountMin:
				lowInputCounts=lowInputCounts+1
			if float(line[11])<coverageCountMin:
				lowInputCounts=lowInputCounts+1
			if lowInputCounts>0:
				continue;
			lowExpCounts=0
			if float(line[4])<coverageCountMin:
				lowExpCounts=lowExpCounts+1
			if float(line[5])<coverageCountMin:
				lowExpCounts=lowExpCounts+1
			if float(line[6])<coverageCountMin:
				lowExpCounts=lowExpCounts+1
			if float(line[7])<coverageCountMin:
				lowExpCounts=lowExpCounts+1
			if lowExpCounts>0:
				continue;
			else:
				for i in range(0, len(line)-1):
					f.write(str(line[i])+'\t')
				f.write(str(line[len(line)-1]))

def selectFCvalues():
	foldChangeThreshold=1.0
	f=open('filtered-greater-than-'+str(foldChangeThreshold)+'-FC-'+str(sys.argv[1][:-4])+'.txt', 'w')
	with open(sys.argv[1]) as input:
		for line in input:
			line=line.split('\t')
			if float(line[20])>=foldChangeThreshold:
				for i in range(0, len(line)-1):
					f.write(str(line[i])+'\t')
				f.write(str(line[len(line)-1]))

def matchVehToDHT():
	#input files should be in the following format tab-delimited text:
	#columns1-3=bed file format aka chr, start, end
	#column 4= FC
	#column 5=standard dev
	#column 6=peak/region ID
	veh={}
	dht={}
	#f=open('filtered-FC-1.0-threshold-applied-regs-shared-by-veh-and-dht.txt', 'w')
	f=open('filtered-veh-FC-1.1-threshold-DHT-FC-1.0-threshold.txt', 'w')
	with open(sys.argv[1]) as input:
		for line in input:
			line=line.split('\t')
			veh[line[5].rstrip('\n')]=line

	with open(sys.argv[2]) as input:
		for line in input:
			line=line.split('\t')
			print line
			dht[line[5].rstrip('\n')]=line

	regsVeh=[key for key in veh]
	regsDht=[key for key in dht]

	regsShared=set(regsVeh).intersection(regsDht)

	for x in regsShared:
		for i in range(0, len(veh[x])-1):
			f.write(str(veh[x][i])+'\t')
		f.write(str(dht[x][3])+'\t'+str(dht[x][4])+'\t'+str(x)+'\n')

def matchVehDHTtoEachIndividualReplicate():
	#input files should be in the following format tab-delimited text:
	#columns1-4=FC replicates
	#column 5= peakID
	veh={}
	dht={}
	#f=open('filtered-FC-1.0-threshold-applied-regs-shared-by-veh-and-dht.txt', 'w')
	f=open('filtered-veh-FC-replicate-comparison.txt', 'w')
	#the vehicle/input file
	with open(sys.argv[1]) as input:
		for line in input:
			line=line.split('\t')
			veh[line[4].rstrip('\n')]=line

	#the DHT/input file
	with open(sys.argv[2]) as input:
		for line in input:
			line=line.split('\t')
			dht[line[4].rstrip('\n')]=line

	regsVeh=[key for key in veh]
	regsDht=[key for key in dht]

	regsShared=set(regsVeh).intersection(regsDht)

	for x in regsShared:
		for i in range(0, len(veh[x])-1):
			f.write(str(veh[x][i])+'\t')
		f.write(str(dht[x][0])+'\t'+str(dht[x][1])+'\t'+str(dht[x][2])+'\t'+str(dht[x][3])+'\t'+str(x)+'\n')

if __name__=='__main__':
	removeReadCounts();
	#selectFCvalues();
	#matchVehToDHT();
	#matchVehDHTtoEachIndividualReplicate();