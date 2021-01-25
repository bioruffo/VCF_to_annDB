#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 11:36:43 2021

@author: roberto
"""

import os, sys

def make_db(avinput, dbname):
    maxexamples = 5 # number of example samples for alt alleles
    sampleindex = None
    numsamples = None
    if not dbname.endswith(".txt"):
        dbname += ".txt"
    directory, name = os.path.split(dbname)
    # remove "hg19_" and ".txt"
    dbcore = name[5:-4]
    with open(dbname, 'w') as outfile:
        outfile.write("#Chr\tStart\tEnd\tRef\tAlt\t"+dbcore+"_freq\t"+dbcore+"_count\tExamples\n")
        for i, line in enumerate(open(avinput, "r")):
            if line.startswith("##"):
                continue
            elif line.startswith("#CHR"):
                header = line.strip().split("\t")
                samplenames = header[header.index("FORMAT")+1:]
                print(len(samplenames), 'samples:', ', '.join(samplenames))
                continue
            data = line.strip().split('\t')
            # chr, start, end, ref, alt
            newline = data[:5]
            # if chromosomes are "chr1", "chr2"... then ANNOVAR will only use the first data column.
            # if chromosomes are named "1", "2"... then ANNOVAR will use all columns in its output. 
            if newline[0].startswith("chr"):
                newline[0] = newline[0][3:]
            # get the first index of genotype data
            if sampleindex is None:
                for ix, d in enumerate(data):
                    if d.startswith("GT:"):
                        sampleindex = ix+1
                        break
            # get the total number of samples
            if numsamples is None:
                numsamples = len(data)-sampleindex
                assert numsamples == len(samplenames)
            alt = 0
            altexamples = []
            for n, sample in enumerate(data[sampleindex:]):
                has_alt = False
                for count in [sample[0], sample[2]]:
                    # multiallelic VCFs are not good for us.
                    if count not in ['0', '1', '.']:
                        print("Unknown genotype '{}'".format(count))
                        if count == "2":
                            print("Are you using a multiallelic VCF? Please split multiallelic lines before using this script.")
                        print("Aborting script execution.")
                        sys.exit()
                    addalt = {'0':0, '.':0, '1':1}[count]
                if addalt > 0 and len(altexamples) < maxexamples:
                    altexamples.append(samplenames[n])
                alt += addalt
            # alt fraction
            newline.append('{:.3f}'.format(alt/(2*numsamples)))
            # "alt alleles / total alleles"
            newline.append('{}/{}'.format(alt, 2*numsamples))
            # Example data with the alleles
            newline.append(','.join(altexamples))
            newline = '\t'.join(newline) + '\n'
            outfile.write(newline)
            if (i+1) % 50000 == 0:
                print(i+1, 'lines done...')
    print("Done.")
                
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 make_db.py inputfile outputdb")
        print("inputfile should be an ANNOVAR file (from `convert2annovar.pl ...`)")
        print("outputdb will be the ANNOVAR-formatted database.")
        print(sys.argv)
    else:
        avinput = sys.argv[1]
        dbname = sys.argv[2]
        make_db(avinput, dbname)
        
    
