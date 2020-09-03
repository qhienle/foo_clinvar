# foo_clinvar

## Summary

A test data crawler for NCBI clinvar. Automatically downloads the latest version of NCBI's ClinVar file, as a GZipped VCF. The downloaded file is parsed to generate two JSON files:

- `nodes.json`: clinical variations and
- `links.json`: links between clinvar IDs - ID and dbsnp IDs - RS.

Examples:

  $ clinvar_extract_links.py [--options] ftp_url
  $ clinvar_extract_links.py --help

For more information on usage, please type:

`clinvar_extract_links.py --help`

## Description

ClinVar's data files, including VCF, index (.tbi) and md5 checksums, are downloaded from NCBI's FTP site. **WARNING**: we assume that NCBI will maintain the structure of the filenames and aliases to the latest release (`clinvar.vcf.gz`).

We use (pdbio)[https://github.com/dceoy/pdbio] to expand the VCF's INFO fields into individual columns. The resulting CSV can then be imported as a pandas data frame.

### Input

Input: FTP URL

### Output

Output: nodes.json and links.json


## References

- (Guide to using files from the ftp site or accessed via e-utilities)[https://www.ncbi.nlm.nih.gov/clinvar/docs/ftp_primer/]
- (ClinVar Variations in VCF Format)[https://www.ncbi.nlm.nih.gov/variation/docs/ClinVar_vcf_files/]
- (Human Variation Sets in VCF Format)[https://www.ncbi.nlm.nih.gov/variation/docs/human_variation_vcf/]
- (pdbio)[https://github.com/dceoy/pdbio]
