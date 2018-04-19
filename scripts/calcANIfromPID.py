# coding: utf-8
import pandas as pd
import sys, os
__author__ = "Sarah Stevens"
__email__ = "sstevens2@wisc.edu"

def usage():
	print "Usage: calcANIfromPID.py PIDonlyFile"
	print "Calculates the ANI from a PIDonly file made by parsePID.py"

if len(sys.argv) != 2:
	usage()
	exit()

# Get argument
filename=sys.argv[1]
aniFileHeader='filename\tref\tmeta\thits\tANI\tmetaReads\tpercentMapped\n'
regANILine='{}\t{}\t{}\t{}\t{}\t{}\t{}\n'
ref, meta = os.path.basename(filename).split('-vs-')
meta = meta.split('.')[0]
ref = os.path.splitext(ref)[0]

## Getting genome size
metaReadsFile = open('metaReads.txt','r')
metaReads = int()
fdname=False
outname='ani_{}-vs-{}.txt'.format(ref,meta)
for line in metaReadsFile:
	if meta in line:
		metaReads=int(line.split(' ')[1].rstrip())
		break
metaReadsFile.close()

if os.stat(filename).st_size == 0: #Checking to see if file is empty (which would happen if no reads recruited)
	if os.path.exists(outname):
		# Makes a ani file if none exists or writes line to existing one.
		with open(outname,'a') as outfile:
			outfile.write(regANILine.format(filename,ref,meta,'0', 'NA', metaReads, '0')) #Records ani for 0 hits
	else:
		with open(outname,'a') as outfile:
			outfile.write(aniFileHeader)
			outfile.write(regANILine.format(filename,ref,meta,'0', 'NA', metaReads, '0'))
else: #if file is not empty
	pid_df= pd.read_table(filename, header=None) #Read in file
	# Makes a ani file if none exists or writes line to existing one.
	if os.path.exists(outname):
		with open(outname,'a') as outfile:
			outfile.write(regANILine.format(filename,ref, meta, pid_df[3].count(), pid_df[3].mean(), metaReads, pid_df[3].count()/float(metaReads)))
	else:
		with open(outname,'a') as outfile:
			outfile.write(aniFileHeader)
			outfile.write(regANILine.format(filename,ref, meta, pid_df[3].count(), pid_df[3].mean(), metaReads, pid_df[3].count()/float(metaReads)))
