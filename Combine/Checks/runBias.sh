#!/bin/bash



#expects=( 15.31982421875 4.180908203125 3.0975341796875004 3.84521484375 3.0670166015625004 1.99127197265625 3.936767578125 3.6773681640625 4.119873046875 3.0975341796875004 5.3558349609375 6.8359375 8.97216796875 6.744384765625 )
## turn-on
#expects=( $2 )
#expects=( 0.19336 0.05051 0.02686 0.02686 0.02342 0.01892 0.03006 0.02754 0.02548 0.03357 0.03586 0.03464 0.03357 0.03448 0.03891 0.04196 0.04211 0.04181 0.04898 0.04654 0.04623 0.04776 0.06165 0.04990 0.05981 0.05173 0.04868 0.04990 0.05890 0.04761 )
#massList=( 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 )
#massList=( $1 )
#expects=( 0.19238 0.05029 0.02686 0.02686 0.02344 0.01807 0.02979 0.02783 0.02588 0.03271 0.03564 0.03369 0.03174 0.03564 0.03857 0.04248 0.04248 0.04150 0.04932 0.04346 0.04639 0.04785 0.06152 0.06006 0.05811 0.05029 0.04834 0.05225 0.05615 0.04736 )
#massList=( 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 )
#expects=( 0.04346 0.04639 0.04785 0.06152 0.06006 0.05811 0.05029 0.04834 0.05225 0.05615 0.04736 )
#massList=( 20 21 22 23 24 25 26 27 28 29 30 )
expects=( 0.0620 )
massList=( 24 )
#expects=( 0.0468 )
#massList=( 22 )
# 6 9 geV left
### need to reRun: 1(1) 12(1) 15 17(1)  8(1) 10(1) 13(1) 14(1) 15(1) 18(1) 19(1) 20(1) 21(1) 22(1) 23(1) 24(1) 25(1) 26(1) 28(1) 29(1) 30(1)
### re run expects=( 0.1934 0.0320 0.0483 0.0420 0.0273 0.0325 0.0351 0.0363 0.0389 0.0418 0.0491 0.0514 0.0462 0.0468 0.0595 0.0574 0.0632 0.0519 0.0453 0.0513 0.0476)
#expects=( 0.02979 0.02783 0.02588 0.03271 )
#massList=( 7 8 9 10 )



nExp=${#expects[@]}

lable='run2'
#channel='mu'

#massList=( 1 2 3 4 5 6 7 8 9 10 15 20 25 30 )
 
nMass=${#massList[@]}

inPath="/afs/cern.ch/work/z/zewang/private/flashggfit/CMSSW_10_2_13/src/flashggFinalFit/Signal/ALP_SigModel_param_UL/fit_results_runII"
outPath="/afs/cern.ch/work/z/zewang/private/flashggfit/BiasStudy/CMSSW_10_2_13/src/flashggFinalFit/Combine/Checks/UL_turn_on"

for ((iBin=0; iBin<$nMass; iBin++))
    do

    if [ $# -ne 0 ];then
        if [[ ${massList[ $iBin ]} -ne $1 ]];then
          continue
        fi
    #    if [[ ${years[ $jBin ]} != $2 ]];then
    #      continue
    #    fi
    fi
    #rm -rf "$outPath/M${massList[$iBin]}" 
    #mkdir "$outPath/M${massList[$iBin]}" 

    rm datacard_ALPmass${massList[$iBin]}.root
    cp "$inPath/M${massList[$iBin]}/datacard_ALPmass${massList[$iBin]}.root" .

    #rm -rf ./UL/M${massList[$iBin]}/*
    
    #rm -rf ./BiasToys_M${massList[$iBin]}
    #rm -rf ./BiasFits_M${massList[$iBin]}
    rm -rf ./BiasPlots_M${massList[$iBin]}

    #./RunBiasStudy.py -d datacard_ALPmass${massList[$iBin]}.root -o M${massList[$iBin]} -t -n 2000 -e ${expects[$iBin]}
    #./RunBiasStudy.py -d datacard_ALPmass${massList[$iBin]}.root -o M${massList[$iBin]} -n 2000 -e ${expects[$iBin]} -f -c " --cminDefaultMinimizerType Minuit2 --cminDefaultMinimizerStrategy 0 --cminDefaultMinimizerTolerance 0.1 --cminFallbackAlgo Minuit2,0:0.2 --cminFallbackAlgo Minuit2,0:0.4 --X-rtd REMOVE_CONSTANT_ZERO_POINT=1 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 --setParameters MH=125,r=0.01 --freezeParameters MH" 
    ./RunBiasStudy.py -d datacard_ALPmass${massList[$iBin]}.root -o M${massList[$iBin]} -p --gaussianFit -n 2000 -e ${expects[$iBin]}

    #cp -r ./BiasToys "$outPath/M${massList[$iBin]}"
    #cp -r ./BiasFits "$outPath/M${massList[$iBin]}"
    #cp -r ./BiasPlots "$outPath/M${massList[$iBin]}"

    #rm higgsCombine_*

    #if [ $1 -eq 0 ]; then
        #rm -rf "$outPath/M${massList[$iBin]}/BiasToys"
        #./RunBiasStudy.py -d datacard_ALPmass${massList[$iBin]}.root -t -n 2000 -e ${expects[$iBin]}
        #cp -r ./BiasToys "$outPath/M${massList[$iBin]}"
        #rm -rf BiasToys
    #elif [ $1 -eq 1 ]; then
        #cp -r "$outPath/M${massList[$iBin]}/BiasToys" .
        #rm -rf "$outPath/M${massList[$iBin]}/BiasFits"
        #./RunBiasStudy.py -d datacard_ALPmass${massList[$iBin]}.root -n 2000 -e ${expects[$iBin]} -f -c "--cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 --freezeParameters MH" 
        #cp -r ./BiasFits "$outPath/M${massList[$iBin]}"
        #rm -rf ./BiasToys
        #rm -rf ./BiasFits
    #elif [ $1 -eq 2 ]; then
        #cp -r "$outPath/M${massList[$iBin]}/BiasToys" .
        #cp -r "$outPath/M${massList[$iBin]}/BiasFits" .
        #rm -rf "$outPath/M${massList[$iBin]}/BiasPlots"
        #./RunBiasStudy.py -d datacard_ALPmass${massList[$iBin]}.root -p --gaussianFit -n 2000 -e ${expects[$iBin]}
        #rm -rf ./BiasToys 
        #rm -rf ./BiasFits 
        #cp -r ./BiasPlots "$outPath/M${massList[$iBin]}"
        #rm -rf ./BiasPlots
        #mv datacard_ALPmass${massList[$iBin]}.root "$outPath/M${massList[$iBin]}"
    #fi

    

done