#!/bin/bash



for i in $( cat TableS2.csv ); 
    do
        SRSNUM=$(echo $i | cut -d ',' -f 7 | grep SRS)
        #if CHECK IF variable SRSNUM has content?, THEN do the next steps
        echo srsnum is $SRSNUM
        SRR=$(esearch -db sra -query $SRSNUM | efetch --format runinfo | cut -d ',' -f 1 | grep SRR)
        echo srr is $SRR >> srrnumbers.txt
        #Prefetch those files
        # And then fastq-dump them? Myabe as part of a differnet script?
    done


#esearch -db sra -query SRS1512526 | efetch --format runinfo | cut -d ',' -f 1 | grep SRR | xargs prefetch