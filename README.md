# SmellyBuffalo
Convert WiseCondor report files  or ichor seg files to vcf

# Dependencies
    python 2.7

# Run

Smellybuffallo accepts a WiseCondor report text file and/or an ichcor seg.txt file as input, and prints a vcf file to stdout. The VCF file contains all the information and variants present in the input text file.

wisecondor:

    python SmellyBuffalo.py input.report.txt  > output.vcf

ichor:

    python SmellyBuffalo.py input.seg.txt  > output.vcf

both:

    python SmellyBuffalo.py input.seg.txt input.report.txt  > output.vcf

note: SmellyBuffalo will guess the input source based on the file ending.

# Downstream analysis
   
You may annotate the vcf file using VEP, or you can merge and create databases using SVDB. 

