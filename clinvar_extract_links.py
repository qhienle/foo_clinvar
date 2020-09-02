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

__version__ = "0.1"
__author__  = "hien@vwetbench.eu"

def parse_arguments():
    """
    Get the command-line options
    """
    parser = argparse.ArgumentParser(description="Description of App")
    parser.add_argument('infile', nargs = '?', help = "Input file. REQUIRED")
    parser.add_argument("-v", "--version", action="store_true", help = "Prints the version")
    args  = parser.parse_args()

    if args.version:
        print "{} version {}".format(__file__, __version__)
        sys.exit()
    elif args.infile == None:
        parser.print_help()
        sys.exit()
    else:
        return args

#=== The real stuff ============================================================

def main():
    args = parse_arguments()

if __name__ == "__main__":
    main()
