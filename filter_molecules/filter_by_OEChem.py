#!/bin/env python

"""
Filter a set of SMILES via MolPropTK
"""

from openeye import oechem
from openeye import oemolprop
from oemolprop import *


filter = oemolprop.OEFilter(OEFilterType_BlockBuster)
outprefix = 'discrepancies_OE'

infile = open('discrepancies_in.smi','r')
outfile_rm = open(outprefix+'_removed.smi', 'w')
outfile_rt = open(outprefix+'_retained.smi', 'w')
retained = []
removed = []
mols_retained = []
mols_removed = []

text = infile.readlines()
smiles = []
for line in text:
    smi = line.split(',')[0].strip()
    smiles.append(smi)
infile.close()

for smi in smiles:
    mol = oechem.OEMol()
    oechem.OEParseSmiles(mol, smi)
    if filter(mol):
        retained.append(smi)
        mols_retained.append(mol)
        outfile_rt.write(smi+'\n')
    else:
        removed.append(smi)
        mols_removed.append(mol)
        outfile_rm.write(smi+'\n')
outfile_rt.close()
outfile_rm.close()


print("Retained %s molecules of %s..." % (len(retained), len(smiles)))

def depict_molecules(smiles_list, pdf_filename):
    # Build OEMols
    from openeye import oechem
    oemols = list()
    for smiles in smiles_list:
        oemol = oechem.OEMol()
        oechem.OESmilesToMol(oemol, smiles)
        oemols.append(oemol)


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


# Generate a PDF of all molecules in the set
depict_molecules(removed, outprefix+'_removed.pdf')
depict_molecules(retained, outprefix+'_retained.pdf')
