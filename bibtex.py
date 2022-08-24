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

#The format of "references" input file:
2004ApJ...604L..33Z
1980Natur.287..307B
2002A&A...388..470D
1964Thesis.....000C
'''

import sys
import os

#Check the Internet connection with timeout of 10 seconds:
import requests
def connected_to_internet(url='https://ui.adsabs.harvard.edu', timeout=10):
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        print("No internet connection available.")
    return False

if connected_to_internet()==False:
    sys.exit(3)

# Check the input file exists or not.
if not os.path.isfile('references'):
    print('File does not exist.')
    sys.exit(3)

# Delete the previous bibtex "reference.bib" file.
os.system('rm -rf cc dd? ee? references.bib')

#Additional references not on ADS:
cite1='1964Thesis.....000C'
ref1=r"""@phdthesis{1964Thesis.....000C,
  author       = {Clarke, M.},
  title        = {PhD thesis},
  year         = 1964,
  address      = {Cambridge University},
}

"""
cite2='1989QSO...M...0000H'
ref2=r"""@article1{1989QSO...M...0000H,
   author = {Hewitt, A. and Burbidge, G.},
    title = "{A New Optical Catalog of Quasi-Stellar Objects}",
     year = 1989,
  refcode = {1989QSO...M...0000H}
      url = {http://ned.ipac.caltech.edu/uri/NED::Refcode/1989QSO...M...0000H},
}

"""

# Delete the repeated lines from the input reference file 
# and Sort of the references on the basis of year.
os.system("sort references | uniq > cc")
#remove empty lines:
os.system("sed -i \'/^$/d\' cc")


# Now sorting with respect to the authors' names.
# Open an input file in the reading mode.
infile = open('cc', 'r')
outfile = open('dd1', 'w')

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup as bp

for line in infile.readlines():
    # Make the url and remove the default 'Enter' from each line in infile_name.
    url = 'https://ui.adsabs.harvard.edu/abs/' + line[0:(len(line)-1)]+'/exportcitation'
    # print(url)
    #Get the html output from the url.
    page_html = urllib3.PoolManager().request('GET', url).data.decode('utf-8')
    #Parse (i.e analyze) the html page into its parts:
    page_parse=bp(page_html,"html.parser")
    #find the location of bibtex entry:
    containers=page_parse.find("textarea",{"class":"export-textarea form-control"},{"readonly":""})
    # print(containers.text)
    #Open output file for the writing:
    if containers != None:
        outfile.write(containers.text)
    else:
        if line[0:(len(line)-1)] == cite1:
            outfile.write(ref1)
        elif line[0:(len(line)-1)] == cite2:
            outfile.write(ref2)
        elif line[0:(len(line)-1)] == cite3:
            outfile.write(ref3)
        elif line[0:(len(line)-1)] == cite4:
            outfile.write(ref4)

outfile.close()
infile.close()

os.system("grep '@' dd1 > dd2")
os.system("grep 'author' dd1 > dd3")
os.system("sed '/ /s//~/g' dd3 > dd4")
os.system("sed '/.and/s//./g' dd4 > dd5")
os.system("paste dd2 dd5 > dd6")
os.system("sort -k2 dd6 > dd7")
os.system("sed -e 's/@INPROCEEDINGS{//; s/@INBOOK{//; s/@BOOK{//; s/@PHDTHESIS{//; s/@phdthesis{//; s/@ARTICLE{//; s/@article1{//' ./dd7 > dd8")
os.system("cut -c1-19 dd8 > dd9")


# After sorting we can make the final bibtex file.
infile = open('dd9', 'r')
outfile = open('ee1', 'w')
for line in infile.readlines():
    print("Fetching the reference: "+line)
    url = 'https://ui.adsabs.harvard.edu/abs/' + line[0:(len(line)-1)]+'/exportcitation'
    page_html = urllib3.PoolManager().request('GET', url).data.decode('utf-8')
    page_parse=bp(page_html,"html.parser")
    containers=page_parse.find("textarea",{"class":"export-textarea form-control"},{"readonly":""})
    if containers != None:
        outfile.write(containers.text)
    else:
        if line[0:(len(line)-1)] == cite1:
            outfile.write(ref1)
        elif line[0:(len(line)-1)] == cite2:
            outfile.write(ref2)
        elif line[0:(len(line)-1)] == cite3:
            outfile.write(ref3)
        elif line[0:(len(line)-1)] == cite4:
            outfile.write(ref4)

outfile.close()
infile.close()



# Writing the shortcuts of journals' names.
file = open('ee2', 'w')
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

============================================\n""")
file.close()

os.system("cat ee2 ee1 > references.bib")
os.system('rm -rf cc dd? ee?')
