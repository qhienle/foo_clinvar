# foo_clinvar

A test data crawler for NCBI clinvar. Automatically downloads the latest version of NCBI's clinvar file, as a vcf.gz. The VCF is parsed to generate two JSON files

- `nodes.json`: clinical variations and 
- `links.json`: links between clinvar IDs - ID and dbsnp IDs - RS.

Input: FTP URL
Output: nodes.json and links.json

