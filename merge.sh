#!/bin/bash

# merge all VCFs in the ./data directory and create an annovar-style file

set -euo pipefail

DATADIR="./data"
OUTDIR="./out"

for FILENAME in ${DATADIR}/*.vcf.gz
do
        echo "Processing: $FILENAME"
        VCF="${FILENAME##*/}"

        # split multiallelic
        bcftools norm -m-both -o ${OUTDIR}/temp_01_norm_${VCF%.*} $FILENAME

        # left-normalize
        bcftools norm -f /home/common-data/genome-builds/hg19_ion_torrent.fasta -o ${OUTDIR}/temp_02_left_${VCF%.*} ${OUTDIR}/temp_01_norm_${VCF%.*}
        rm ${OUTDIR}/temp_01_norm_${VCF%.*}

        # replace 'A' with '.' in FR field or it blows up 
        sed -i 's/##INFO=<ID=FR,Number=A,/##INFO=<ID=FR,Number=.,/' ${OUTDIR}/temp_02_left_${VCF%.*}

        # sort, gzip and index
        vcf-sort ${OUTDIR}/temp_02_left_${VCF%.*} > ${OUTDIR}/ready_${VCF%.*}
        rm ${OUTDIR}/temp_02_left_${VCF%.*}
        bgzip ${OUTDIR}/ready_${VCF%.*}
        tabix -p vcf ${OUTDIR}/ready_$VCF
done

# merge VCFs
echo "Merging..."
bcftools merge ${OUTDIR}/ready*.vcf.gz --threads 4 -o ${OUTDIR}/merged.vcf
rm ${OUTDIR}/ready*

# split again multiallelic sites
echo "Resplitting multiallelic sites..."
bcftools norm -m -any -o ${OUTDIR}/merged_split.vcf ${OUTDIR}/merged.vcf
rm ${OUTDIR}/merged.vcf

# convert to ANNOVAR format, keeping genotype data (format vcf4old)
echo "Converting to ANNOVAR format..."
convert2annovar.pl -format vcf4old ${OUTDIR}/merged_split.vcf -outfile ${OUTDIR}/output.avinput -includeinfo
#rm ${OUTDIR}/merged_split.vcf

echo "Done!"
