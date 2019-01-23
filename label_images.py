import sys
import os
from shutil import copyfile
import re

## Code to add genus and species to corresponding spnr in .spnr files

def labelimages(image, csvinventory):
    for root, dirs, files in os.walk(directory):
        for name in sorted(files):
            if name.endswith(".spnr"):
                ## get absolutepath because of git annex
                absolutimpath = os.path.realpath(os.path.join(root, name))
                ##print(absolutimpath)

                ## get backup copy of each .spnr file
                copyfile(absolutimpath, absolutimpath+'.bak')
                ## open .spnr files and copy spnr and path to corresponding lists
                with open(absolutimpath) as spnr:
                    spnr_ocr = spnr.readline()
                    spnr_ocr = spnr_ocr.rstrip()
                    stream = open(csvinventory, 'r')
                    for line in stream:

                        csv_match = re.search(r'(UA\.201[4,5]{1}\.\d{4}),(\w+),(\w+)', line)
                        csv_speciesNr = csv_match.group(1)

                        if spnr_ocr == csv_speciesNr:
                            csv_genus = csv_match.group(2)
                            csv_species = csv_match.group(3)
                            file = open(root + "/" + name + '.spnr', 'w')
                            file.write(csv_speciesNr)
                            file.write('\n')
                            file.write(csv_genus)
                            file.write('\n')
                            file.write(csv_species)
                            file.close()
                            print('spnr: {}, genus: {}, species: {}'.format(csv_speciesNr, csv_genus, csv_species))



## run code by entering the directory where .spnr files are and where merged csv file is
if len(sys.argv) != 3:
    sys.stderr.write(
        'Usage: label_images.py <path to directory containing .spnr files, path to inventory csv>\n')
    sys.exit(1)
else:
    directory = sys.argv[1]
    csvinventory = sys.argv[2]


labelimages(directory, csvinventory)