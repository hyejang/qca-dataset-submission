#!/bin/env python

# Utilizes RDKit implementation of QED algorithm (https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3524573/)
# as documented https://www.rdkit.org/docs/source/rdkit.Chem.QED.html to filter a molecule set

import sys

insmiles = sys.argv[1]
outprefix = sys.argv[2]

#Threshold score for removing molecules; I arbitrarily picked this without any testing.
threshold = 0.5

# Process
from rdkit import Chem
import rdkit.Chem.QED as QED

# Read in input file
file = open(insmiles, 'r')
text = file.readlines()
file.close()

# Set up storage for fails/successes
retained = []
filtered_out = []

# Process and extract molecules
for line in text:
    # Get an RDMol
    smi = line.split(',')[0].strip()
    rdmol = Chem.MolFromSmiles(smi, sanitize=False)

    # calculate QED
    val = QED.default(rdmol)

    if val > threshold:
        retained.append(smi)
    else:
        filtered_out.append(smi)

print('Retained %s molelecules and removed %s using a threshold of %.2f' % (len(retained), len(filtered_out), threshold))

# Save data
file = open(outprefix+'_removed.smi', 'w')
for smi in filtered_out:
    file.write('%s\n' % smi)
file.close()
file = open(outprefix+'_retained.smi', 'w')
for smi in retained:
    file.write('%s\n' % smi)
file.close()


# Depict molecules
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
depict_molecules(filtered_out, outprefix+'_removed.pdf')
depict_molecules(retained, outprefix+'_retained.pdf')
