#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 11:36:43 2021

@author: roberto
"""

import os, sys

def make_db(avinput, dbname):
    sampleindex = None
    numsamples = None
    if not dbname.endswith(".txt"):
        dbname += ".txt"
    directory, name = os.path.split(dbname)
    # remove "hg19_" and ".txt"
    dbcore = name[5:-4]
    with open(dbname, 'w') as outfile:
        outfile.write("#Chr\tStart\tEnd\tRef\tAlt\t"+dbcore+"_freq\t"+dbcore+"_count\n")
        for i, line in enumerate(open(avinput, "r")):
            data = line.strip().split('\t')
            # chr, start, end, ref, alt
            newline = data[:5]
            if newline[0].startswith("chr"):
                newline[0] = newline[0][3:]
            if sampleindex is None:
                for ix, d in enumerate(data):
                    if d.startswith("GT:"):
                        sampleindex = ix+1
                        break
            if numsamples is None:
                numsamples = len(data)-sampleindex
            alt = 0
            for sample in data[sampleindex:]:
                for count in [sample[0], sample[2]]:
                    alt += {'0':0, '.':0, '1':1}[count]
            # alt fraction
            newline.append('{:.3f}'.format(alt/(2*numsamples)))
            
            newline.append('{}/{}'.format(alt, 2*numsamples))
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
        
    
