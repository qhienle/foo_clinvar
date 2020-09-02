#!/usr/bin/env python

"""AppName

USAGE: clinvar_extract_links.py [--options] input_file

A test data crawler for NCBI clinvar. Automatically downloads the latest version of NCBI's clinvar file, as a vcf.gz. The VCF is parsed to generate two JSON files

- `nodes.json`: clinical variations and
- `links.json`: links between clinvar IDs - ID and dbsnp IDs - RS.

Input: FTP URL (*e.g.* ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/weekly/)
Output: nodes.json and links.json
"""

import sys
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
                        help = "FTP link. DEFAULT=ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/weekly/clinvar.vcf.gz.md5")
    args  = parser.parse_args()

    if args.version:
        print(__file__ + " version " + __version__)
        sys.exit()
    elif args.url == None:
        #args.url = "ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/weekly/"
        args.url = "ftp://ftp.ncbi.nlm.nih.gov/"
        print("No FTP URL provided. Using default " + args.url)
    else:
        pass
    return args

#=== The real stuff ============================================================

def main():
    args = parse_arguments()

    # Download the VCF file
    print("Downloading file from " + args.url)
    subprocess.call(["wget", args.url])

    #TODO: wget the md5 and check for file corruption before parsing

    # Parse the VCF file

if __name__ == "__main__":
    main()
