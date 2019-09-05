#!/bin/env python

"""rdfilters expects a SMILES file which has a SMILES string followed by a compound name; ours here have only SMILES. Add names and write out."""

import sys

infile = sys.argv[1]
outfile = sys.argv[2]

file = open(infile, 'r')
text = file.readlines()
file.close()
file = open(outfile, 'w')
for (idx, line) in enumerate(text):
    file.write(line.strip()+' mol%s\n' % idx)
file.close()
