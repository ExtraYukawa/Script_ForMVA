#!/bin/bash -e 
echo "TEST FIRST" 
echo "copy input root file"
eos cp /eos/cms/store/group/phys_top/ExtraYukawa/BDT/BDT_input_forTraining/YEAR/SIGNALROOT .

for f in /eos/cms/store/group/phys_top/ExtraYukawa/BDT/BDT_input_forTraining/YEAR/*.root
do
#echo $f | grep -v "ttc" | xargs echo $f | xargs eos cp $f . #fixme (just to copy ONLY background files)
eos cp $f .
done

PWD=`pwd`
HOME=$PWD
echo $HOME 
export SCRAM_ARCH=slc7_amd64_gcc700
source /cvmfs/cms.cern.ch/cmsset_default.sh
eval `scramv1 project CMSSW CMSSW_10_6_29`
cd $PWD/CMSSW_10_6_29
ls -lrth
eval `scramv1 runtime -sh`

cd #PWD
echo "TEST DIR"

root -b -l TMVAClassification.C 

echo "Finished Training!!!"
ls -lrth
rm -rf CMSSW_10_6_29

echo "make tar with weight xml file"
tar zcf aa.tar.gz dataset_ttc_PARTICLE_COUP_MCPARTMASS_SYST
#echo "make tar with weight xml and output ROOT file"
#tar zcf aa.tar.gz dataset_ttc_PARTICLE_COUP_MCPARTMASS_SYST TMVA_ttc_PARTICLE_COUP_MCPARTMASS_SYST.root
echo "Delete all the root files"
rm *.root
#ls *.root | grep -v "output.root" |xargs rm
ls -lrth
