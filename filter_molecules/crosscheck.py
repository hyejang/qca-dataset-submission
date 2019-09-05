#!/bin/env python


"""Load smiles files from all three test cases, check how many compounds all three retain."""


infiles = ['discrepancies_OE_removed.smi', 'discrepancies_QED_removed.smi', 'discrepancies_out.smi']
outprefix='discrepancies_combined'

removed_mols = set()

for filenm in infiles:
    file = open(filenm, 'r')
    text = file.readlines()
    smileslist = [line.split(',')[0].strip() for line in text]
    for smi in smileslist:
        removed_mols.add(smi)

print("Total number of molecules removed %s" % len(removed_mols))

# Build list of SMILES of what's retained
file = open('discrepancies_in.smi', 'r')
text = file.readlines()
file.close()
smileslist = [line.split(',')[0].strip() for line in text]
retainedlist = []
for smi in smileslist:
    if not smi in removed_mols:
        retainedlist.append(smi)

print(len(retainedlist))


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
depict_molecules(retainedlist, outprefix+'_retained.pdf')
depict_molecules(removed_mols, outprefix+'_removed.pdf')
