#!/bin/bash
echo "Starting job"
echo "copying proxy file to /tmp area"
echo "start running"
cd /afs/cern.ch/work/z/zewang/private/flashggfit/BiasStudy/CMSSW_10_2_13/src
cmsenv

cd ./flashggFinalFit/Combine/Checks
./runBias_v1.sh 1 0.1934

echo "running done"