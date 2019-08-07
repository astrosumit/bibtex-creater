# Program to make bibtex file using the bibcodes of references in ADS

'''
This program reads the bibliography codes one-by one from an
input file "references" and download the bibtex entry from
ADS and then put them in a "reference.bib" file in the
alphabetical order of the authors' names. For the same
authors, it will sort the entries on the basis of years. For
the same authors and year of publication, it will sort with
respect to the volume and page numbers of the publications.
It will also take care of the repeated bibliography entries.
It will delete any previously created "reference.bib" file
and make a new one.

The future scope of improvement: For the same authors and
year of publication, the program should add 'a','b','c'
identifiers in the year.


#The format of "references" input file:
2004ApJ...604L..33Z
1980Natur.287..307B
2002A&A...388..470D
'''

import sys
import os

# Check the input file exists or not.
if not os.path.isfile('references'):
    print('File does not exist.')
    sys.exit(3)

# Delete the previous bibtex "reference.bib" file.
os.system('rm -rf cc dd? ee? references.bib')

# Delete the repeated lines from the input reference file 
# and Sort of the references on the basis of year.
os.system("sort references | uniq > cc")

'''
# Sort of the references on the basis of year.
os.system("cut -c1-4 cc > cc1")
os.system("paste cc cc1 > cc2")
os.system("sort -n -k2 cc2 > cc3")
os.system("cut -f1 cc3 > cc4")
'''

# Now sorting with respect to the authors' names.
# Open an input file in the reading mode.
infile = open('cc', 'r')

import urllib3

for line in infile.readlines():
    # Make the url and remove the default 'Enter' from each line in infile_name.
    url = 'http://cdsads.u-strasbg.fr/cgi-bin/nph-bib_query?bibcode=' + \
        line[0:(len(line)-1)]+'&data_type=BIBTEX&db_key=AST%26nocookieset=1'
    # print(url)
    # Get the output from the url.
    url_output = urllib3.PoolManager().request('GET', url).data.decode('utf-8')
    # print(url_output)
    # Open an output file for the writing in append mode.
    outfile = open('dd1', 'a+')
    for x in url_output:
        outfile.write(x)

    outfile.close()

infile.close()

os.system("grep '@' dd1 > dd2")
os.system("grep 'author' dd1 > dd3")
os.system("sed '/ /s//~/g' dd3 > dd4")
os.system("sed '/.and/s//./g' dd4 > dd5")
os.system("paste dd2 dd5 > dd6")
os.system("sort -k2 dd6 > dd7")
os.system("sed -e 's/@INPROCEEDINGS{//; s/@INBOOK{//; s/@ARTICLE{//' ./dd7 > dd8")
os.system("cut -c1-19 dd8 > dd9")


# After sorting we can make the final bibtex file.
infile = open('dd9', 'r')
for line in infile.readlines():
    print("Fetching the reference: "+line)
    # Make the url and remove the default 'Enter' from each line in infile_name.
    url = 'http://cdsads.u-strasbg.fr/cgi-bin/nph-bib_query?bibcode=' + \
        line[0:(len(line)-1)]+'&data_type=BIBTEX&db_key=AST%26nocookieset=1'
    # print(url)
    # Get the output from the url.
    url_output = urllib3.PoolManager().request('GET', url).data.decode('utf-8')
    # print(url_output)
    # Open an output file for the writing in append mode.
    outfile = open('ee1', 'a+')
    for x in url_output:
        outfile.write(x)

    outfile.close()

infile.close()


os.system("grep -v 'Query Results from the ADS Database' ee1 > ee2")
os.system("grep -v 'Retrieved 1 abstracts' ee2 > ee3")

# Writing the shortcuts of journals' names.
file = open('ee4', 'w')
file.write("""%@string{mnras = 'MNRAS'}
%@string{solphys='Sol.~Phys.'}
%@string{jgr='J.~Geophys.~Res.'}
%@string{grl='Geophycal.~Res.~Lett.'}
%@string{apj='ApJ'}
%@string{apjl='ApJL'}
%@string{aap='A\&A'}
%@string{aapr='A\&A Rev.'}
%@string{araa='ARA\&A'}
%@string{APJL='Astrophys. Journal Lett.'}
%@string{AAP='Astron. Astroph.'}
%@string{pasj='PASJ'}
%@string{nat='Nature'}
%@string{na='New Astronomy'}
%@string{ssr='Space Science Reviews'}
%@string{aj='Astronomical Journal'}

============================================""")
file.close()

os.system("cat ee4 ee3 > references.bib")
os.system('rm -rf cc dd? ee?')
