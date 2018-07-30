# SmellyBuffalo
Convert WiseCondor report files to vcf

# Dependencies
    python 2.7

# Run

Smellybuffallo accepts the WiseCondor report text file as input, and prints a vcf file to stdout. The VCF file contains all the information and variants present in the input text file.

    python SmellyBuffalo.py input.report.txt  > output.vcf

# Downstream analysis
   
You may annotate the vcf file using VEP, or you can merge and create databases using SVDB. 

