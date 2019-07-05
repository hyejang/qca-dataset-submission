#!/usr/bin/env python

"""
Generate a PDF of all small molecules in the JSON dataset.
"""
import gzip

# Read the compressed dataset
#with gzip.open('optimization_inputs.json.gz', 'r') as f:
#    data = json.loads(f.read().decode('utf-8'))

# Extract SMILES
#smiles_list = [ item['cmiles_identifiers']['canonical_isomeric_smiles'] for item in data ]

infile = open('SureChEMBL_20190101_19.smi', 'r')
smiles_list = infile.readlines()
smiles_list = [ smiles.strip() for smiles in smiles_list ]
infile.close()
print(smiles_list)

# Build OEMols
from openeye import oechem
oemols = list()
for smiles in smiles_list:
    oemol = oechem.OEMol()
    oechem.OESmilesToMol(oemol, smiles)
    oemols.append(oemol)

# Generate a PDF of all molecules in the set
pdf_filename = 'optimization_inputs.pdf'

from openeye import oedepict
itf = oechem.OEInterface()
PageByPage = True
suppress_h = True
rows = 10
cols = 6
ropts = oedepict.OEReportOptions(rows, cols)
ropts.SetHeaderHeight(25)
ropts.SetFooterHeight(25)
ropts.SetCellGap(2)
ropts.SetPageMargins(10)
report = oedepict.OEReport(ropts)
cellwidth, cellheight = report.GetCellWidth(), report.GetCellHeight()
opts = oedepict.OE2DMolDisplayOptions(cellwidth, cellheight, oedepict.OEScale_Default * 0.5)
opts.SetAromaticStyle(oedepict.OEAromaticStyle_Circle)
pen = oedepict.OEPen(oechem.OEBlack, oechem.OEBlack, oedepict.OEFill_On, 1.0)
opts.SetDefaultBondPen(pen)
oedepict.OESetup2DMolDisplayOptions(opts, itf)
for i, mol in enumerate(oemols):
    cell = report.NewCell()
    mol_copy = oechem.OEMol(mol)
    oedepict.OEPrepareDepiction(mol_copy, False, suppress_h)
    disp = oedepict.OE2DMolDisplay(mol_copy, opts)
    oedepict.OERenderMolecule(cell, disp)
    #oedepict.OEDrawCurvedBorder(cell, oedepict.OELightGreyPen, 10.0)

oedepict.OEWriteReport(pdf_filename, report)
