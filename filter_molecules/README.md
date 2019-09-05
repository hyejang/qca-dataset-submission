# Molecule filtering


Here I'm (David Mobley) experimenting with molecule filtering; we need to begin ensuring datasets -- especially those we're using for testing and benchmarking -- focus on drug-like compounds.

### Filtering resources

Several options have been proposed for filtering datasets:
- Pat Walters’ RD-filters: https://github.com/PatWalters/rd_filters?files=1 (and blog post http://practicalcheminformatics.blogspot.com/2018/08/filtering-chemical-libraries.html )
- OpenEye filtering also: https://docs.eyesopen.com/toolkits/cpp/molproptk/filter_theory.html#filter-theory-variations-of-filters -- BlockBuster, Drug, Lead, or Fragment
- QED for druglikeness: see https://www.rdkit.org/docs/source/rdkit.Chem.QED.html in RDKit and https://www.ncbi.nlm.nih.gov/pubmed/22270643 for paper

Here I intend to experiment with one or more of these. 
