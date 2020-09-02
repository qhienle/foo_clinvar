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

#=== The real stuff ============================================================

def main():
    args = parse_arguments()

    # Download the VCF file, including index and md5. We are assuming that NCBI
    # will maintain the structure of the filenames and aliases to latest release
    # We could separate the file names and treat these individually, but this
    # may add some complexity to the command-line arguments and the processing
    # and make it less transparent to the end user

    glob_files = args.url + "*"
    print("Downloading files: " + glob_files)
    subprocess.call(["wget", glob_files])

    # TODO: wget the md5 and check for file corruption before parsing

    # Parse the VCF file

    # Clean-up
    #os.remove("*.vcf.gz*")
    # TODO: [nice-to-have] Add a volume on the Docker container to store the last files downloaded, for traceability

if __name__ == "__main__":
    main()
