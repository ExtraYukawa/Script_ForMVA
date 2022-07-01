#!/bin/bash -e 
echo "TEST FIRST" 
echo "copy input root file"
eos cp /eos/cms/store/group/phys_top/ExtraYukawa/BDT_input/YEAR/SIGNALROOT .
eos cp /eos/cms/store/group/phys_top/ExtraYukawa/BDT_input/YEAR/tttJ.root .
eos cp /eos/cms/store/group/phys_top/ExtraYukawa/BDT_input/YEAR/TTTo1L.root .
eos cp /eos/cms/store/group/phys_top/ExtraYukawa/BDT_input/YEAR/TTTo2L.root .
eos cp /eos/cms/store/group/phys_top/ExtraYukawa/BDT_input/YEAR/tttt.root .
eos cp /eos/cms/store/group/phys_top/ExtraYukawa/BDT_input/YEAR/tttW.root .
eos cp /eos/cms/store/group/phys_top/ExtraYukawa/BDT_input/YEAR/ttWtoLNu.root .
eos cp /eos/cms/store/group/phys_top/ExtraYukawa/BDT_input/YEAR/ttWW.root .
eos cp /eos/cms/store/group/phys_top/ExtraYukawa/BDT_input/YEAR/ttWZ.root .
eos cp /eos/cms/store/group/phys_top/ExtraYukawa/BDT_input/YEAR/ttZ.root .
eos cp /eos/cms/store/group/phys_top/ExtraYukawa/BDT_input/YEAR/ttZtoQQ.root .
eos cp /eos/cms/store/group/phys_top/ExtraYukawa/BDT_input/YEAR/ttZZ.root .
eos cp /eos/cms/store/group/phys_top/ExtraYukawa/BDT_input/YEAR/tzq.root .
eos cp /eos/cms/store/group/phys_top/ExtraYukawa/BDT_input/YEAR/WWW.root .
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
rm *.root
echo "end!!!"
ls -lrth
rm -rf CMSSW_10_6_29
tar zcf aa.tar.gz dataset_ttc_PARTICLE_COUP_MCPARTMASS_SYST
#ls *.root | grep -v "output.root" |xargs rm
ls -lrth
