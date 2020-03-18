import argparse
import numpy
from os import listdir
from os.path import isfile, join
import os

parser = argparse.ArgumentParser("""TIDDIT --sv --bam inputfile [-o prefix] --ref ref.fasta""")
parser.add_argument('--folder'       ,type=str, help="folder containing wisecondorX output files", required=True)
parser.add_argument('--minCNV'       ,default=10000000,type=int, help="Minimum size of CNV segment")
parser.add_argument('--Zscore'       ,default=3,type=int, help="Zscore of CNV segment")
parser.add_argument('--samplesheet', type=str,required=True, help="path to samplesheet")
args= parser.parse_args()

files_in_folder=[f for f in listdir(args.folder) if isfile(join(args.folder, f))]

output_header=["SampleID","SampleType","Flowcell","Description","SampleProject","IndexID1","Index1","IndexID2","Index2","Well","Library_nM","QCFlag","QCFailure","QCWarning","Zscore_13","Zscore_18","Zscore_21","Zscore_X","Zscore_Y","Ratio_13","Ratio_18","Ratio_21","Ratio_X","Ratio_Y","Clusters","TotalReads2Clusters","MaxMisindexedReads2Clusters","IndexedReads","TotalIndexedReads2Clusters","Tags","NonExcludedSites","NonExcludedSites2Tags","Tags2IndexedReads","PerfectMatchTags2Tags","GCBias","GCR2","NCD_13","NCD_18","NCD_21","NCD_X","NCD_Y","Chr1_Coverage","Chr2_Coverage","Chr3_Coverage","Chr4_Coverage","Chr5_Coverage","Chr6_Coverage","Chr7_Coverage","Chr8_Coverage","Chr9_Coverage","Chr10_Coverage","Chr11_Coverage","Chr12_Coverage","Chr13_Coverage","Chr14_Coverage","Chr15_Coverage","Chr16_Coverage","Chr17_Coverage","Chr18_Coverage","Chr19_Coverage","Chr20_Coverage","Chr21_Coverage","Chr22_Coverage","ChrX_Coverage","ChrY_Coverage","Chr1","Chr2","Chr3","Chr4","Chr5","Chr6","Chr7","Chr8","Chr9","Chr10","Chr11","Chr12","Chr13","Chr14","Chr15","Chr16","Chr17","Chr18","Chr19","Chr20","Chr21","Chr22","ChrX","ChrY","Median_13","Median_18","Median_21","Median_X","Median_Y","Stdev_13","Stdev_18","Stdev_21","Stdev_X","Stdev_Y","FF_Formatted","FFY","FFX","DuplicationRate","Bin2BinVariance","UnfilteredCNVcalls","CNVSegment"]

print("\"" + "\",\"".join(output_header) +"\"" )

first=True
samplesheet_info=[]
samplesheet_dict={}

samples={}
#sample_out={"SampleID":"","SampleType":"Test","Flowcell":"","Description":"","SampleProject":"","IndexID":"""Index":"","Well":"","Library_nM":"","QCFlag":""}
sample_out={"Bin2BinVariance":"","UnfilteredCNVcalls":0,"SampleID":"","DuplicationRate":0,"SampleType":"Test","Flowcell":"","Description":"","CNVSegment":"","SampleProject":"","IndexID1":"","Index1":"","IndexID2":"","Index2":"","Well":"","Library_nM":"","QCFlag":"","QCFailure":"","QCWarning":"","Zscore_13":"","Zscore_18":"","Zscore_21":"","Zscore_X":"","Zscore_Y":"","Ratio_13":"","Ratio_18":"","Ratio_21":"","Ratio_X":"","Ratio_Y":"","Clusters":"","TotalReads2Clusters":"","MaxMisindexedReads2Clusters":"","IndexedReads":"","TotalIndexedReads2Clusters":"","Tags":"","NonExcludedSites":"","NonExcludedSites2Tags":"","Tags2IndexedReads":"","PerfectMatchTags2Tags":"","GCBias":"","GCR2":"","NCD_13":"","NCD_18":"","NCD_21":"","NCD_X":"","NCD_Y":"","Chr1_Coverage":"","Chr2_Coverage":"","Chr3_Coverage":"","Chr4_Coverage":"","Chr5_Coverage":"","Chr6_Coverage":"","Chr7_Coverage":"","Chr8_Coverage":"","Chr9_Coverage":"","Chr10_Coverage":"","Chr11_Coverage":"","Chr12_Coverage":"","Chr13_Coverage":"","Chr14_Coverage":"","Chr15_Coverage":"","Chr16_Coverage":"","Chr17_Coverage":"","Chr18_Coverage":"","Chr19_Coverage":"","Chr20_Coverage":"","Chr21_Coverage":"","Chr22_Coverage":"","ChrX_Coverage":"","ChrY_Coverage":"","Chr1":"","Chr2":"","Chr3":"","Chr4":"","Chr5":"","Chr6":"","Chr7":"","Chr8":"","Chr9":"","Chr10":"","Chr11":"","Chr12":"","Chr13":"","Chr14":"","Chr15":"","Chr16":"","Chr17":"","Chr18":"","Chr19":"","Chr20":"","Chr21":"","Chr22":"","ChrX":"","ChrY":"","Median_13":"","Median_18":"","Median_21":"","Median_X":"","Median_Y":"","Stdev_13":"","Stdev_18":"","Stdev_21":"","Stdev_X":"","Stdev_Y":"","FF_Formatted":"","FFY":"","FFX":""}

for line in open(args.samplesheet):
	if first:
		i=0
		for entry in line.strip().split(" "):
			samplesheet_info.append(entry)
			samplesheet_dict[entry]=i
			i+=1

		first=False
		continue
	i=0
	content=line.strip().split(" ")
	sample=content[samplesheet_dict["SampleID"]]
	samples[ sample ]=sample_out	

	for entry in content:
		if samplesheet_info[i] in sample_out:
			samples[sample][samplesheet_info[i]]=entry
		elif samplesheet_info[i] == "FCID":
			samples[sample]["Flowcell"]=entry
		elif samplesheet_info[i] == "Project":
			samples[sample]["SampleProject"]=entry
		elif samplesheet_info[i] == "index":
			samples[sample]["Index1"]=entry
		elif samplesheet_info[i] == "index2":
			samples[sample]["Index2"]=entry
		i+=1
	#print (line.strip())

ratio_21=[]
ratio_18=[]
ratio_13=[]
ratio_X=[]
ratio_Y=[]

for sample in samples:
	for file in files_in_folder:
		if file.startswith(sample) and file.endswith("_chr_statistics.txt"):
			for line in open(args.folder+ "/" + file):
				if "ratio" in line:
					continue
				content=line.strip().split("\t")
				if content[0] == "1":
					samples[sample]["Chr1_Coverage"]=str(float(content[1])+1)
				if content[0] == "2":
					samples[sample]["Chr2_Coverage"]=str(float(content[1])+1)
				if content[0] == "3":
					samples[sample]["Chr3_Coverage"]=str(float(content[1])+1)
				if content[0] == "4":
					samples[sample]["Chr4_Coverage"]=str(float(content[1])+1)
				if content[0] == "5":
					samples[sample]["Chr5_Coverage"]=str(float(content[1])+1)
				if content[0] == "6":
					samples[sample]["Chr6_Coverage"]=str(float(content[1])+1)
				if content[0] == "7":
					samples[sample]["Chr7_Coverage"]=str(float(content[1])+1)
				if content[0] == "8":
					samples[sample]["Chr8_Coverage"]=str(float(content[1])+1)
				if content[0] == "9":
					samples[sample]["Chr9_Coverage"]=str(float(content[1])+1)
				if content[0] == "10":
					samples[sample]["Chr10_Coverage"]=str(float(content[1])+1)
				if content[0] == "11":
					samples[sample]["Chr11_Coverage"]=str(float(content[1])+1)
				if content[0] == "12":
					samples[sample]["Chr12_Coverage"]=str(float(content[1])+1)
				if content[0] == "13":
					samples[sample]["Chr13_Coverage"]=str(float(content[1])+1)
					samples[sample]["Zscore_13"]=content[-1]
					samples[sample]["Ratio_13"]=str(float(content[1])+1)
					ratio_13.append(float(content[1])+1)

				if content[0] == "14":
					samples[sample]["Chr14_Coverage"]=str(float(content[1])+1)
				if content[0] == "15":
					samples[sample]["Chr15_Coverage"]=str(float(content[1])+1)
				if content[0] == "16":
					samples[sample]["Chr16_Coverage"]=str(float(content[1])+1)
				if content[0] == "17":
					samples[sample]["Chr17_Coverage"]=str(float(content[1])+1)
				if content[0] == "18":
					samples[sample]["Zscore_18"]=content[-1]
					samples[sample]["Chr18_Coverage"]=str(float(content[1])+1)
					samples[sample]["Ratio_18"]=str(float(content[1])+1)
					ratio_18.append(float(content[1])+1)

				if content[0] == "19":
					samples[sample]["Chr19_Coverage"]=str(float(content[1])+1)
				if content[0] == "20":
					samples[sample]["Chr20_Coverage"]=str(float(content[1])+1)
				if content[0] == "21":
					samples[sample]["Chr21_Coverage"]=str(float(content[1])+1)
					samples[sample]["Zscore_21"]=content[-1]
					samples[sample]["Ratio_21"]=str(float(content[1])+1)
					ratio_21.append(float(content[1])+1)

				if content[0] == "22":
					samples[sample]["Chr22_Coverage"]=str(float(content[1])+1)
				if content[0] == "X":
					samples[sample]["ChrX_Coverage"]=str(float(content[1])+1)
					samples[sample]["Ratio_X"]=str(float(content[1])+1)
					ratio_X.append(float(content[1])+1)
					samples[sample]["Zscore_X"]=content[-1]

				if "Median segment variance (per bin): " in line:
					samples[sample]["Bin2BinVariance"]=line.strip().split("Median segment variance (per bin): ")[-1].strip()
for sample in samples:
	samples[sample]["Median_X"]=numpy.median(ratio_X)
	samples[sample]["Median_18"]=numpy.median(ratio_18)
	samples[sample]["Median_21"]=numpy.median(ratio_21)
	samples[sample]["Median_13"]=numpy.median(ratio_13)

	samples[sample]["Stdev_X"]=numpy.std(ratio_X)
	samples[sample]["Stdev_18"]=numpy.std(ratio_18)
	samples[sample]["Stdev_21"]=numpy.std(ratio_21)
	samples[sample]["Stdev_13"]=numpy.std(ratio_13)

for sample in samples:
	for file in files_in_folder:
		if file.startswith(sample) and file.endswith("_aberrations.bed"):
			for line in open(args.folder+ "/" + file):
				if "start" in line:
					continue
				content=line.strip().split()
				samples[sample]["UnfilteredCNVcalls"]+=1
				if int(content[2]) - int(content[1]) > args.minCNV and abs(float(content[2])) > args.Zscore:
					samples[sample]["CNVSegment"]="Found"

for sample in samples:
	for file in files_in_folder:
		if file.startswith(sample) and file.endswith(".bam.wcx.npz"):
			a=numpy.load(args.folder + "/" + file,encoding='latin1', allow_pickle=True)
			samples[sample]["IndexedReads"]=a["quality"].item()["mapped"]
			samples[sample]["DuplicationRate"]=a["quality"].item()['filter_rmdup']/a["quality"].item()["mapped"]
			all_chr=[]
			samples[sample]["Chr1"]=sum(a["sample"].item()["1"])
			samples[sample]["Chr2"]=sum(a["sample"].item()["2"])
			samples[sample]["Chr3"]=sum(a["sample"].item()["3"])
			samples[sample]["Chr4"]=sum(a["sample"].item()["4"])
			samples[sample]["Chr5"]=sum(a["sample"].item()["5"])
			samples[sample]["Chr6"]=sum(a["sample"].item()["6"])
			samples[sample]["Chr7"]=sum(a["sample"].item()["7"])
			samples[sample]["Chr8"]=sum(a["sample"].item()["8"])
			samples[sample]["Chr9"]=sum(a["sample"].item()["9"])
			samples[sample]["Chr10"]=sum(a["sample"].item()["10"])
			samples[sample]["Chr11"]=sum(a["sample"].item()["12"])
			samples[sample]["Chr12"]=sum(a["sample"].item()["12"])
			samples[sample]["Chr13"]=sum(a["sample"].item()["13"])
			samples[sample]["Chr14"]=sum(a["sample"].item()["14"])
			samples[sample]["Chr15"]=sum(a["sample"].item()["15"])
			samples[sample]["Chr16"]=sum(a["sample"].item()["16"])
			samples[sample]["Chr17"]=sum(a["sample"].item()["17"])
			samples[sample]["Chr18"]=sum(a["sample"].item()["18"])
			samples[sample]["Chr19"]=sum(a["sample"].item()["19"])
			samples[sample]["Chr20"]=sum(a["sample"].item()["20"])
			samples[sample]["Chr21"]=sum(a["sample"].item()["21"])
			samples[sample]["Chr22"]=sum(a["sample"].item()["22"])
			samples[sample]["ChrX"]=sum(a["sample"].item()["23"])
			samples[sample]["ChrY"]=sum(a["sample"].item()["24"])
			samples[sample]["ChrY_Coverage"]=sum(a["sample"].item()["24"])/int(a["quality"].item()["mapped"])
			samples[sample]["Ratio_Y"]=samples[sample]["ChrY_Coverage"]
			ratio_Y.append(samples[sample]["Ratio_Y"])

for sample in samples:
	for file in files_in_folder:
		if file.startswith(sample) and file.endswith("PREFACE.txt"):
			for line in open(args.folder+ "/" + file):
				if "FFX" in line:
					samples[sample]["FFX"]=line.strip().split()[-1]
				if "PREFACE" in line:
					samples[sample]["FF_Formatted"]=line.strip().split()[-1]

for sample in samples:
	for file in files_in_folder:
		if file.startswith(sample) and file.endswith("AMYCNE.tab"):
			for line in open(args.folder+ "/" + file):
				if "med" in line:
					continue
				content=line.strip().split()
				samples[sample]["FFY"]="{}%".format( float(content[-1])/float(content[-2])*100 )

for sample in samples:
	samples[sample]["Median_Y"]=numpy.median(ratio_Y)
	samples[sample]["Stdev_Y"]=numpy.std(ratio_Y)

GC=[]
for sample in samples:
	AT=0
	C=0
	G=0
	for file in files_in_folder:
		if file.startswith(sample) and file.endswith(".bam"):
			with os.popen("samtools view -F 2048 -s 0.2 {}".format(args.folder + "/" +file)) as pipe:
				for line in pipe:
					for base in line.split("\t")[9]:
						if base == "A" or base == "T":
							AT+=1
						elif base == "C":
							C+=1
						elif base == "G":					
							G+=1

	samples[sample]["GCR2"]=(G+C)/(AT+G+C)
	GC.append((G+C)/(AT+G+C))	

stdev=numpy.std(GC)
if len(GC) == 1:
	stdev=1

for sample in samples:
	samples[sample]["GCBias"]=(samples[sample]["GCR2"]-numpy.average(GC))/stdev

for sample in samples:
	out=[]
	for entry in output_header:
		out.append(str(samples[sample][entry]))
	print("\"" + "\",\"".join(out) +"\"" )