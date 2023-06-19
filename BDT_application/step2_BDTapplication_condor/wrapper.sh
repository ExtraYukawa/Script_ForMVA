#!/bin/bash -e 
echo "TEST FIRST" 
echo "copy input root file"
cp /eos/user/t/tihsu/BDT/BDT_application_input/YEAR/SIGNALROOT .
cp /eos/user/t/tihsu/BDT/BDT_application_input/YEAR/aa.tar.gz .
tar zxf aa.tar.gz
rm aa.tar.gz
PWD=`pwd`
HOME=$PWD

# copy BDT weights, one central weight and six systematic weights
mkdir BDT_weights_0
cd BDT_weights_0
cp /eos/user/t/tihsu/BDT/BDT_weight/YEAR/ttc_SIGTYPE_COUPLING_MSIGTYPEMASS/ttc_SIGTYPE_COUPLING_MSIGTYPEMASS_0/dataset_ttc_SIGTYPE_COUPLING_MSIGTYPEMASS_central/weights/TMVAClassification_BDTG.weights.xml .
cd $HOME

mkdir BDT_weights_1
cd BDT_weights_1
cp /eos/user/t/tihsu/BDT/BDT_weight/YEAR/ttc_SIGTYPE_COUPLING_MSIGTYPEMASS/ttc_SIGTYPE_COUPLING_MSIGTYPEMASS_1/dataset_ttc_SIGTYPE_COUPLING_MSIGTYPEMASS_jesup/weights/TMVAClassification_BDTG.weights.xml .
cd $HOME

mkdir BDT_weights_2
cd BDT_weights_2
cp /eos/user/t/tihsu/BDT/BDT_weight/YEAR/ttc_SIGTYPE_COUPLING_MSIGTYPEMASS/ttc_SIGTYPE_COUPLING_MSIGTYPEMASS_2/dataset_ttc_SIGTYPE_COUPLING_MSIGTYPEMASS_jesdo/weights/TMVAClassification_BDTG.weights.xml .
cd $HOME

mkdir BDT_weights_3
cd BDT_weights_3
cp /eos/user/t/tihsu/BDT/BDT_weight/YEAR/ttc_SIGTYPE_COUPLING_MSIGTYPEMASS/ttc_SIGTYPE_COUPLING_MSIGTYPEMASS_3/dataset_ttc_SIGTYPE_COUPLING_MSIGTYPEMASS_jerup/weights/TMVAClassification_BDTG.weights.xml .
cd $HOME

mkdir BDT_weights_4
cd BDT_weights_4
cp /eos/user/t/tihsu/BDT/BDT_weight/YEAR/ttc_SIGTYPE_COUPLING_MSIGTYPEMASS/ttc_SIGTYPE_COUPLING_MSIGTYPEMASS_4/dataset_ttc_SIGTYPE_COUPLING_MSIGTYPEMASS_jerdo/weights/TMVAClassification_BDTG.weights.xml .
cd $HOME

mkdir BDT_weights_5
cd BDT_weights_5
cp /eos/user/t/tihsu/BDT/BDT_weight/YEAR/ttc_SIGTYPE_COUPLING_MSIGTYPEMASS/ttc_SIGTYPE_COUPLING_MSIGTYPEMASS_5/dataset_ttc_SIGTYPE_COUPLING_MSIGTYPEMASS_metUnslusEnup/weights/TMVAClassification_BDTG.weights.xml .
cd $HOME

mkdir BDT_weights_6
cd BDT_weights_6
cp /eos/user/t/tihsu/BDT/BDT_weight/YEAR/ttc_SIGTYPE_COUPLING_MSIGTYPEMASS/ttc_SIGTYPE_COUPLING_MSIGTYPEMASS_6/dataset_ttc_SIGTYPE_COUPLING_MSIGTYPEMASS_metUnslusEndo/weights/TMVAClassification_BDTG.weights.xml .
cd $HOME

mkdir BDT_weights_7
cd BDT_weights_7
cp /eos/user/t/tihsu/BDT/BDT_weight/YEAR/ttc_SIGTYPE_COUPLING_MSIGTYPEMASS/ttc_SIGTYPE_COUPLING_MSIGTYPEMASS_7/dataset_ttc_SIGTYPE_COUPLING_MSIGTYPEMASS_muPtup/weights/TMVAClassification_BDTG.weights.xml .
cd $HOME

mkdir BDT_weights_8
cd BDT_weights_8
cp /eos/user/t/tihsu/BDT/BDT_weight/YEAR/ttc_SIGTYPE_COUPLING_MSIGTYPEMASS/ttc_SIGTYPE_COUPLING_MSIGTYPEMASS_8/dataset_ttc_SIGTYPE_COUPLING_MSIGTYPEMASS_muPtdo/weights/TMVAClassification_BDTG.weights.xml .
cd $HOME


echo $HOME 
export SCRAM_ARCH=slc7_amd64_gcc700
source /cvmfs/cms.cern.ch/cmsset_default.sh
eval `scramv1 project CMSSW CMSSW_10_6_29`
cd $PWD/CMSSW_10_6_29
ls -lrth
eval `scramv1 runtime -sh`

cd #PWD
echo "TEST DIR"

root -b -l TMVAClassificationApplication.C
echo "Run complete!!"
ls -lrth
tar zcf output.tar.gz TMVApp_*.root
ls *.root | grep -v "TMVApp_*.root" | xargs rm
rm -r BDT_weights_*
echo "end!!!"
ls -lrth
rm -rf CMSSW_10_6_29
ls -lrth
