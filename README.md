# VCF\_to\_annDB  

Create a database of allele frequencies for ANNOVAR using a group of local VCFs  

Usage:
1) Copy all relevant vcf files to the ./data directory  
...ex. recursively:  
`find \<TOP\_VCF\_DIRECTORY> -name "\*.vcf.gz\*" -exec cp "{}" ./base \;`  

2) run `merge.sh` from the main script directory to create a merged VCF in the ./out directory:  
`bash ./merge.sh`  

3) run make\_db.py to create the ANNOVAR database:  
`python3 make\_db.py out/output.avinput ~/humandb/hg19\_MyDatabase.txt`  

That's it!   
