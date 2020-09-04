# foo_clinvar

## Summary

A test data crawler for NCBI clinvar. Automatically downloads the latest version of NCBI's ClinVar file, as a GZipped VCF. The downloaded file is parsed to generate two JSON files:

- `nodes.json`: clinical variations and
- `links.json`: links between clinvar IDs - ID and dbsnp IDs - RS.

## Installation

1. `git clone https://github.com/qhienle/foo_clinvar.git`
2. `cd foo_clinvar`
3. `docker build -t clinvar .`
4. `docker run -it clinvar`
5. `python3 clinvar_extract_links.py`
6. `head -n 25 nodes.json links.json`

For more information on usage, please type: `clinvar_extract_links.py --help`
Comments, explanations and suggestions for improvements are included in `clinvar_extract_links.py`.

## clinvar_extract_links.py

Examples of usage:

  $ clinvar_extract_links.py [--options] ftp_url
  $ clinvar_extract_links.py --help

For more information on usage, please type:

`clinvar_extract_links.py --help`

### Description

ClinVar's data files, including VCF, index (.tbi) and md5 checksums, are downloaded from NCBI's FTP site. **WARNING**: we assume that NCBI will maintain the structure of the filenames and aliases to the latest release (`clinvar.vcf.gz`).

We use (pdbio)[https://github.com/dceoy/pdbio] to expand the VCF's INFO fields into individual columns. The resulting CSV can then be imported as a pandas data frame.

### Input

Input: FTP URL (*e.g.* ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/weekly/clinvar.vcf.gz)

### Output

Output: nodes.json and links.json

## Comments and potential improvements

- [nice-to-have] Add a volume on the Docker container to store the last files downloaded, for traceability
- Add a command-line option to skip the step of pre-flight clean-up, for re-using files from previous downloads
- MD5 checksum for file corruption before parsing
- If multiprocessors or an HPC is available, it would probably be a good idea to split big files into smaller chunks for parsing in parallel *e.g.* using a job scheduler's job arrays (PBS, LSF,...), Python's multiprocessing module.
- Add this to a weekly `cron` and send e-mail notification upon run completion.

## References

- (Guide to using files from the ftp site or accessed via e-utilities)[https://www.ncbi.nlm.nih.gov/clinvar/docs/ftp_primer/]
- (ClinVar Variations in VCF Format)[https://www.ncbi.nlm.nih.gov/variation/docs/ClinVar_vcf_files/]
- (Human Variation Sets in VCF Format)[https://www.ncbi.nlm.nih.gov/variation/docs/human_variation_vcf/]
- (pdbio)[https://github.com/dceoy/pdbio]
