import sys
import seaborn as sns
import pandas
from operator import itemgetter
import matplotlib.pyplot as plt
import plotly
import plotly.plotly as pyplot
 
pyplot.sign_in('tbrunetti', '72r07ya8dr')

from plotly.graph_objs import Scatter
from plotly.graph_objs import Bar
from plotly.graph_objs import Layout
import plotly.graph_objs as go

def compareEnhancerNumber():

	#the format of each file should be in the following order, without headers:
	#'chromosome', 'start', 'end', 'fold change', 'standard deviation', 'region ID'
	#standard deviation can be an empty column, used more as a place holder
	#sys.argv[1]=input-vs-vehicle
	#sys.argv[2]=input-vs-dht
	#sys.argv[3]=vehicle-vs-input
	temp=[]
	with open(sys.argv[1]) as input:
		for line in input:
			temp.append(line.split('\t')+['input-vehicle'])
	
	with open(sys.argv[2]) as input:
		for line in input:
			temp.append(line.split('\t')+['input-DHT'])
	
	with open(sys.argv[3]) as input:
		for line in input:
			temp.append(line.split('\t')+['vehicle-DHT'])
	headers=['chromosome', 'start', 'end', 'Log2(FC)', 'standard deviation', 'region ID', 'dataset']
	#puts temp into a convenient dataframe to be used with seaborn package
	data=pandas.DataFrame(temp, columns=headers)
	#convert the fold change column into a float
	data[['Log2(FC)']]=data[['Log2(FC)']].astype(float)

	#boxplot comparing the total number of active enhancers with their repective fold change values
	sns.plt.title("Enhancer activity of filtered AR capture regions", fontsize=30)
	sns.boxplot(x='Log2(FC)', y='dataset', data=data)
	sns.plt.show()

def distanceToTSS():
	temp=[]
	with open(sys.argv[1]) as input:
		for line in input:
			line=line.split('\t')
			line[len(line)-1]=line[len(line)-1].rstrip('\n')
			temp.append(line)
	headers=['TSS distance', '# of unique genes', 'dataset']
	data=pandas.DataFrame(temp, columns=headers)
	data[['# of unique genes']]=data[['# of unique genes']].astype(float)

	sns.plt.title('Total number of unique genes with TSS distance')
	sns.barplot(x='TSS distance', y='# of unique genes', hue='dataset', data=data)
	sns.plt.show()

#compares the top x enhancers for each dataset with their relative standard deviations
def topEnhancers():
	temp=[]
	with open(sys.argv[1]) as input:
		for line in input:
			line=line.split('\t')
			line[len(line)-1]=line[len(line)-1].rstrip('\n')
			temp.append(line)
	headers=['gene', 'sum of fold change', 'group']
	data=pandas.DataFrame(temp, columns=headers)
	data[['sum of fold change']]=data[['sum of fold change']].astype(float)

def waterfallPlotFCallRegions():
	#new index is just regions renumbered from 1-end continuously
	temp=[]
	with open(sys.argv[1]) as input:
		for line in input:
			line=line.split('\t')
			line[len(line)-1]=line[len(line)-1].rstrip('\n')
			temp.append(line)

	headers=['region ID', 'fold change', 'std dev', 'new Index']
	#must be sorted to get waterfall plot
	sortedTemp=sorted(temp, key=itemgetter(1))
	newIndexSorted=[sortedTemp[i] +[i] for i in range(len(sortedTemp))]
	data=pandas.DataFrame(newIndexSorted, columns=headers)
	data[['fold change', 'std dev']]=data[['fold change', 'std dev']].astype(float)
	#print data
	plotly.offline.plot({
		"data":[Scatter(
			x=data['new Index'], 
			y=data['fold change'], 
			mode='lines',
			line=dict(width=0.5, color='rgb(0,0,153)') 
			#error_y=dict(type='percent', value=data['std dev'])
			)],
		
		"layout":go.Layout(
			title='Fold change values normalized DHT Over Input',
			xaxis=dict(title='filtered capture regions'),
			yaxis=dict(title='fold change (DHT/Input)'),
			margin=dict(t=100, r=100, b=100, l=100),
			width=1300,
			height=700,
			autosize=False,
			shapes=[dict(type='line', x0=0, y0=1, x1=14000, y1=1,
			line=dict(color='rgb(153, 0, 0)',
				width=2,
				dash='dashdot'))])
	})

def barGraphLogBase2FC():
	#sys.argv is a list of tab-delimted files with the first line being header
	#first column is gene name, 2nd column is average fold change
	#each list represents a different group of data
	temp=[]
	headers=['FC<=-2.0', 'FC=-1.5', 'FC=-1.0', 'FC=-0.5', 'FC=-0.5<x<0', 'FC=0<x<0.5', 'FC=0.5', 'FC=1.0', 'FC=1.5', 'FC>=2.0']
	for i in range(1, len(sys.argv)):
		neg20=0
		neg15=0
		neg10=0
		neg05=0
		lessZero=0
		greaterZero=0
		pos05=0
		pos10=0
		pos15=0
		pos20=0
		with open(sys.argv[i]) as input:
			for line in input:
				line=line.split('\t')
				line[len(line)-1]=line[len(line)-1].rstrip('\n')
				if abs(float(line[1]))<0.5:
					if float(line[1])>0:
						greaterZero=greaterZero+1
					else:
						lessZero=lessZero+1
				elif abs(float(line[1]))>=0.5 and abs(float(line[1]))<1.0:
					if float(line[1])>0:
						pos05=pos05+1
					else:
						neg05=neg05+1
				elif abs(float(line[1]))>=1.0 and abs(float(line[1]))<1.5:
					if float(line[1])>0:
						pos10=pos10+1
					else:
						neg10=neg10+1
				elif abs(float(line[1]))>=1.5 and abs(float(line[1]))<2.0:
					if float(line[1])>0:
						pos15=pos15+1
					else:
						neg15=neg15+1
				elif abs(float(line[1]))>=2.0:
					if float(line[1])>0:
						pos20=pos20+1
					else:
						neg20=neg20+1
	
		temp.append([neg20, neg15, neg10, neg05, lessZero, greaterZero, pos05, pos10, pos15, pos20])

	print temp[0]
	plotly.offline.plot({
		"data":[go.Bar(x=headers,
		y=temp[0],
		marker=dict(color=['rgb(153, 0, 0)', 'rgb(255, 0, 0)', 'rgb(255, 51, 51)', 'rgb(255, 102, 102)', 'rgb(255, 153, 153)', 'rgb(153, 255, 153)', 'rgb(102, 255, 102)', 'rgb(51, 255, 51)', 'rgb(0, 255, 0)', 'rgb(0 153, 0)'],))],
		
		"layout":go.Layout(title='Number of Regions of Enhancer Activity in Vehicle vs. DHT',
			xaxis=dict(title='Log2(FC)'),
			yaxis=dict(title='Number of Capture Regions'),
			annotations=[
			dict(x=xi,
				y=yi,
				text=str(yi),
				xanchor='center',
				yanchor='bottom',
				showarrow=False,
				) for xi, yi in zip(headers,temp[0])])
		
		})

def heatmapTopUpDownRegulate():
	#sys.argv[1]=one column with a list of genes to search for
	#sys.argv[1+i]=two columns, tab delimited list of genes in columns one, logBase2 FC in column2
	geneListToSearch=[]
	with open(sys.argv[1]) as input:
		for line in input:
			line=line.rstrip('\n')
			geneListToSearch.append(line)

	genes={geneListToSearch[key]:[] for key in range(0, len(geneListToSearch))}
	
	#formatted in this way, so plotly can be used to graph the heatmap
	inputVsVeh=[]
	inputVsDHT=[]
	vehVsDHT=[]
	geneHeaders=[]
	for i in range(1, len(sys.argv)):
		with open(sys.argv[i]) as input:
			for line in input:
				line=line.split('\t')
				if line[0] in genes:
					genes[line[0]]=genes[line[0]]+[float(line[1].rstrip('\n')), i]
					
	#these serves as place holders for is the gene was not found in a particular group
	for key in genes:
		if 2 not in genes[key]:
			genes[key]=genes[key]+[float(0.0), 2]
		if 3 not in genes[key]:
			genes[key]=genes[key]+[float(0.0), 3]
		if 4 not in genes[key]:
			genes[key]=genes[key]+[float(0.0), 4]
	
	for key in genes:
		geneHeaders.append(key)
		inputVsVeh.append(genes[key][0])
		inputVsDHT.append(genes[key][2])
		vehVsDHT.append(genes[key][4])	

	#plotly heatmap
	plotly.offline.plot({
		"data":[go.Heatmap(
			z=[inputVsVeh, inputVsDHT, vehVsDHT],
			x=geneHeaders,
			y=['input vs vehicle', 'input vs DHT', 'vehicle vs DHT'],
			colorscale=[[0.0, 'rgb(153, 0, 0)'], [0.125, 'rgb(255, 0,0)'], [0.25, 'rgb(255, 102, 102)'], [0.375, 'rgb(255, 153, 153)'], [0.50, 'rgb(96, 96, 96)'],
			[0.625, 'rgb(153, 255, 153)'], [0.75, 'rgb(102, 255, 102)'], [0.875, 'rgb(0, 255, 0)'], [1.0, 'rgb(0,153,0)']])
			],
		"layout":go.Layout(
			title='Log2 fold change of top regulated genes within 50kb of TSS',
			margin=dict(t=100, r=100, b=100, l=100),
			width=1300,
			height=350,
			autosize=False)
		})
if __name__=="__main__":	
	#compareEnhancerNumber();
	#distanceToTSS();
	waterfallPlotFCallRegions();
	#barGraphLogBase2FC();
	#heatmapTopUpDownRegulate();
	