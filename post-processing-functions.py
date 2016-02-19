import sys
import csv
from multiprocessing import Pool
import os
import time

#sys.argv[1]=choose post-processing method: FC_Values_Only, Nearest_Gene_FC


#----------------------------------Paramters for FC_Values_Only---------------------------------
#sys.argv[x]=(optional, split, mostly used to large files to speed up processing time) 
#			bed file of regions, 4th column is FC values, 5th is stdDev if available
#			split <file> -n <int chunks>


#---------------------------------Parameters for Nearest_Gene_FC--------------------------------
#file format: 1st col=FC; 2nd col=std dev or blank column; 3rd col=gene name; 4th col=distance
#			  from TSS; optional remaining columns need to be added in pairs in same 3rd and 4th
#			  column format; NO HEADERS!



finalResults=[]

def extractFC(fileLocation):
	meetRequirements=[]
	FClimit=1.1
	print 'pool has started processing data'
	with open(fileLocation) as input:
		for line in input:
			line=line.split('\t')
			if line[3]=='#DIV/0!':
				continue;
			if float(line[3].rstrip('\n'))>=FClimit:
				line[len(line)-1]=line[len(line)-1].rstrip()
				meetRequirements.append(line)

			else:
				removed=open('locations-that-do-not-meet-FC-requirements.txt', 'a+')
				removed.write(str(line))	
	return meetRequirements			

def closestGenes():
	genesFC={}
	maxDistToGene=50000
	with open(sys.argv[2]) as input:
		for line in input:
			line=line.split('\t')
			for x in range(2, len(line), 2):
				if line[x].replace(" ", "")=='NONE' or line[x].replace(" ","")=='':
					continue;
				elif line[x].replace(" ", "") in genesFC and abs(int(line[x+1]))<=maxDistToGene:
					genesFC[line[x].replace(" ", "")]=genesFC[line[x].replace(" ", "")]+float(line[0])
				elif line[x].replace(" ","") not in genesFC and abs(int(line[x+1]))<=maxDistToGene:
					genesFC[line[x].replace(" ", "")]=float(line[0])
	return genesFC	

def retrieveResults(meetRequirements):
	print "Received results at "+ str(time.ctime())
	finalResults.extend(meetRequirements)


if __name__=='__main__':
	pool=Pool(processes=1)
	
	if sys.argv[1]=='FC_Values_Only':
		for i in range(2, len(sys.argv)):
			address=os.getcwd()+'/'+str(sys.argv[i])
			print address
			pool.apply_async(extractFC, kwds={"fileLocation":address}, callback=retrieveResults)
		pool.close()
		pool.join()
	
		print "The number of remaining regions is "+str(len(finalResults))
		print "Writing data to file..."

		with open('post-processing-results.txt', 'w') as f:
			csvWrite=csv.writer(f)
			csvWrite.writerows(finalResults)
	
	elif sys.argv[1]=='Nearest_Gene_FC':
		f2=open('genes-summation-of-FC.txt', 'w')
		genesFC=closestGenes();
		for key in genesFC:
			f2.write(str(key)+'\t'+str(genesFC[key])+'\n')	
	
