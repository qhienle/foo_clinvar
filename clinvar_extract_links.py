#!/usr/bin/env python

"""clinvar_extract_links

USAGE: clinvar_extract_links.py [--options] input_file

A test data crawler for NCBI clinvar to extract dbSNP's RS Identifiers. Automatically downloads the latest version of NCBI's clinvar file, as a vcf.gz. The VCF is parsed to generate two JSON files

- `nodes.json`: clinical variations and
- `links.json`: links between clinvar IDs - ID and dbsnp IDs - RS.

Input: FTP URL (*e.g.* ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/weekly/)
Output: nodes.json and links.json

For more information on ClinVar, https://www.ncbi.nlm.nih.gov/clinvar/
"""

import sys
import os
import argparse
import subprocess


__version__ = "0.1"
__author__  = "hien@vwetbench.eu"

def parse_arguments():
    """
    Get the command-line options
    """
    parser = argparse.ArgumentParser(description = "Description of App")
    parser.add_argument("-v", "--version", \
                        action = "store_true", \
                        help = "Prints the version")
    parser.add_argument("-u", "--url", \
                        nargs = '?', \
                        help = "FTP link. DEFAULT=ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/weekly/clinvar.vcf.gz")
    args  = parser.parse_args()

    if args.version:
        print(__file__ + " version " + __version__)
        sys.exit()
    elif args.url == None:
        args.url = "ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/weekly/clinvar.vcf.gz"
        print("No FTP URL provided. Using default " + args.url)
    else:
        pass
    return args

def split_file(f):
    # TODO: zcat f | split -l 1000000 - part-
    # Store and return a list of filenames
    pass

def vcf2df(vcf):
    # We use pdbio to expand the VCF's INFO fields into columns.
    # The resulting CSV can then be imported as a data frame.
    # We can use pandas' built in JSON export function to create `nodes.json`.
    pass


#=== The real stuff ============================================================

def main():
    args = parse_arguments()

    # Download the VCF file, including index and md5. We are assuming that NCBI
    # will maintain the structure of the filenames and aliases to latest release
    # We could separate the file names and treat these individually, but this
    # may add some complexity to the command-line arguments and the processing
    # and make it less transparent to the end user

    print("Downloading: " + args.url)
    subprocess.run(["wget", args.url])
    md5 = args.url + ".md5"
    print("Downloading: " + md5)
    subprocess.run(["wget", md5])
    tbi = args.url + ".tbi"
    print("Downloading: " + tbi)
    subprocess.run(["wget", args.url])

    # TODO: wget the md5 and check for file corruption before parsing

    # TODO: If multiprocessors or an HPC is available, it would probably be a
    # good idea to split big files into smaller chunks for parsing in parallel
    # *e.g.* using a job scheduler's job arrays (PBS, LSF,...), Python's
    # multiprocessing.
    # file_parts = split_file("clinvar.vcf.gz") # TODO: fix case where input filename differs

    # Parse the VCF file into a pandas dataframe, that we can manipulate and re-
    # shape, before converting to JSON.

    # Clean-up
    #os.remove("*.vcf.gz*")
    # TODO: [nice-to-have] Add a volume on the Docker container to store the last files downloaded, for traceability

if __name__ == "__main__":
    main()
