#!/usr/bin/env python3

# Split files into specified chunks of lines

import gzip

class FileSplitter:
    def __init__(self):
        pass

    def split_file(self, gzfile, max_lines=100000):
        count_lines = 1
        count_files = 1
        outfiles = []
        with gzip.open(infile, "rb") as gz:
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

if __name__ == "__main__":
    infile = "clinvar.vcf.gz"
    splitter = FileSplitter()
    files = splitter.split_file(infile)
    print(files)
