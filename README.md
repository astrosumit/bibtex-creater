# bibtex-creater

Program to make bibtex file using the bibcodes of references in ADS:

This program reads the bibliography codes one-by one from an input file "references" and download the bibtex entry from ADS and then put them in a "reference.bib" file in the alphabetical order of the authors' names. For the same authors, it will sort the entries on the basis of years. For the same authors and year of publication, it will sort with respect to the volume and page numbers of the publications. It will also take care of the repeated bibliography entries. It will delete any previously created "reference.bib" file and make a new one.

The format of "references" input file:

2004ApJ...604L..33Z

1980Natur.287..307B

2002A&A...388..470D



Usage:

Include the following line in your .tex file:

\bibliography{references}
