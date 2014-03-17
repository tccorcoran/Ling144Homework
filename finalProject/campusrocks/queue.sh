#!/bin/tcsh

foreach f (/afs/cats.ucsc.edu/users/q/tcorcora/sluice/feature_files/ablation/train/*.dat)
    qsub -pe orte 10 -o out -e err q.sh $f

end
