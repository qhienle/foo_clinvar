#!/usr/bin/env python

"""clinvar_extract_links

USAGE: clinvar_extract_links.py [--options] ftp_url
       clinvar_extract_links.py --help

A test data crawler for NCBI clinvar. Automatically downloads the latest version of NCBI's ClinVar file, as a GZipped VCF. The downloaded file is parsed to generate two JSON files:

- `nodes.json`: clinical variations and
- `links.json`: links between clinvar IDs - ID and dbsnp IDs - RS.

Input: FTP URL (*e.g.* ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/weekly/clinvar.vcf.gz)
Output: nodes.json and links.json

For more information on ClinVar, https://www.ncbi.nlm.nih.gov/clinvar/
"""

import sys, os, io
import argparse
import subprocess
import pandas
import glob
import gzip


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

def remove_previous():
    # Remove files from previous runs, based on default options
    # TODO: Use glob to get a file list of *.vcf.gz* and *.json ?
    rm_files = ["clinvar.vcf.gz", "clinvar.vcf.gz.md5", "clinvar.vcf.gz.tbi", "links.json", "nodes.json"]
    for file in rm_files:
        try:
            os.remove(file)
        except FileNotFoundError:
            print("File not found: " + file)

def split_file(gzfile, max_lines=100000):
    # TODO: zcat f | split -l 1000000 - part-
    # Split big file and return a list of filenames
    count_lines = 1
    count_files = 1
    outfiles = []
    with gzip.open(gzfile, "rb") as gz:
        outfile = "part-" + str(count_files) + ".vcf"
        part = open(outfile, "wb")
        for line in gz:
            if count_lines <= max_lines:
                part.write(line)
                count_lines += 1
            else:
                part.close()
                outfiles.append(outfile)
                count_lines = 1
                count_files += 1
                outfile = "part-" + str(count_files) + ".vcf"
                part = open(outfile, "wb")
                part.write(line)
        part.close()
        outfiles.append(outfile)
    return outfiles

def pdbio_vcf2df(vcf):
    # We use (pdbio)[https://github.com/dceoy/pdbio] to expand the VCF's
    # INFO fields into individual columns. The resulting CSV can then be
    # imported as a pandas data frame.
    csv_data = subprocess.check_output(["pdbio", "vcf2csv", "--expand-info", vcf])
    csv_data_stream = io.BytesIO(csv_data)
    return pandas.read_csv(csv_data_stream)

#=== The real stuff ============================================================

def main():
    args   = parse_arguments()
    infile = os.path.basename(args.url)
    print("Processing " + infile + "\n")

    # Remove existing files from previous downloads and runs
    # TODO: [nice-to-have] Add a volume on the Docker container to store the
    # last files downloaded, for traceability
    # TODO: Add a command-line option to skip this step, for re-using files
    # from previous downloads

    remove_previous()

    # Download the VCF file, including index and md5. We are assuming that NCBI
    # will maintain the structure of the filenames and aliases to the latest
    # release.

    print("Downloading: " + args.url)
    subprocess.run(["wget", args.url])
    # Convenient to have if we ever decide to use `vcftools` or `bcftools`
    # tbi = args.url + ".tbi"
    # print("Downloading: " + tbi)
    # subprocess.run(["wget", tbi])
    md5 = args.url + ".md5"
    print("Downloading: " + md5)
    subprocess.run(["wget", md5])

    # TODO: checksum for file corruption before parsing

    # TODO: If multiprocessors or an HPC is available, it would probably be a
    # good idea to split big files into smaller chunks for parsing in parallel
    # *e.g.* using a job scheduler's job arrays (PBS, LSF,...), Python's
    # multiprocessing module.

    vcf_parts = split_file(infile)
    print("First file to be processed " + vcf_parts[0])

    # Parse the VCF file into a pandas dataframe, that we can manipulate and re-
    # shape, before converting to JSON.

    for part in vcf_parts:
        count = 0
        # pdbio_vcf2df requires the file name extension
        df = pdbio_vcf2df("tests/foo.vcf.gz")
        df.to_json("nodes.json", orient = "records", indent = 2)

        # Create the `links.json` file
        links = df[["ID", "INFO_RS"]]
        links.to_json("links.json", orient="records", indent = 2)

        os.remove(part)
        # For the sake of example, we only process the first file
        # TODO: adapt this for loop for multiprocessing/job arrays
        count += 1
        if count >= 1:
            break

    # Clean up
    # TODO: Join the nodes.json and links.json resulting from splitted-files,
    # and remove all parts
    for file in glob.glob("vcfpart-*"):
        os.remove(file)

    # TODO: Add this to a weekly `cron` and send e-mail notification upon run
    # completion.

if __name__ == "__main__":
    main()
