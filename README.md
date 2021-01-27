# VCF\_to\_annDB  

Create a database of allele frequencies for ANNOVAR using a group of local VCFs  

## Required software:  
#### bcftools and htslib  
http://www.htslib.org/download/  
#### vcftools  
https://vcftools.github.io/downloads.html  
#### ANNOVAR
https://annovar.openbioinformatics.org/en/latest/user-guide/download/  


## Usage:
1) Copy all relevant vcf files to the ./data directory  
...ex. recursively:  
`find <TOP_LEVEL_VCF_DIRECTORY> -name "*.vcf.gz*" -exec cp "{}" . \;`  

2) run `merge.sh` from the main script directory to create a merged VCF in the ./out directory:  
`bash ./merge.sh`  

3) run make\_db.py to create the ANNOVAR database:  
`python3 make_db.py out/output.avinput ~/humandb/hg19_MyDatabase.txt`  

That's it!   
