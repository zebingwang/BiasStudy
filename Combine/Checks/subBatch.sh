#!/bin/bash

#expects=( 0.19238 0.05029 0.02686 0.02686 0.02344 0.01807 0.02979 0.02783 0.02588 0.03271 0.03564 0.03369 0.03174 0.03564 0.03857 0.04248 0.04248 0.04150 0.04932 0.04346 0.04639 0.04785 0.06152 0.06006 0.05811 0.05029 0.04834 0.05225 0.05615 0.04736 )
#massList=( 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 )

#expects=( 0.03271 0.03564 0.03369 0.03174 0.03564 0.03857 0.04248 0.04248 0.04150 0.04932 0.04346 0.04639 0.04785 0.06152 0.06006 0.05811 0.05029 0.04834 0.05225 0.05615 0.04736 )
#massList=( 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 )
#expects=( 0.02686 0.02344 0.01807 )
#massList=( 4 5 6 )

#expects=( 0.0336 )
#massList=( 10 )

expects=( 0.0581 )
massList=( 24 )
nMass=${#massList[@]}

for ((iBin=0; iBin<$nMass; iBin++))
    do


    
    cp /afs/cern.ch/work/z/zewang/private/flashggfit/BiasStudy/CMSSW_10_2_13/src/flashggFinalFit/Combine/Checks/runbatch.jdl runbatch_${massList[$iBin]}.jdl
    cp /afs/cern.ch/work/z/zewang/private/flashggfit/BiasStudy/CMSSW_10_2_13/src/flashggFinalFit/Combine/Checks/runbatch.sh runbatch_${massList[$iBin]}.sh
    sed -i "s/MASS/${massList[$iBin]}/g" runbatch_${massList[$iBin]}.sh
    sed -i "s/EXPLIM/${expects[$iBin]}/g" runbatch_${massList[$iBin]}.sh
    sed -i "s/MASS/${massList[$iBin]}/g" runbatch_${massList[$iBin]}.jdl

    condor_submit ./runbatch_${massList[$iBin]}.jdl

done