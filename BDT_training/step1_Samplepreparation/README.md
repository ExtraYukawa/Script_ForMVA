simply by using "python slim.py" to get the inputs for the BDT training, several things to be stressed:

1. for each coupilng typy, e.g., rtc, only one coupling strength will be used, since we already checked that the BDT score of rtc 01/04/08/10 are almost the same

2. after obtaining the root file, move them to the eos region for further BDT training which will be implemeted through condor, e.g., the 2018 inputs are put in /eos/cms/store/group/phys_top/ExtraYukawa/BDT/BDT_input_forTraining/2018/

3. "Slim_module('ttc_'+cps[ic].lower()+'_'+coups[icp]+'.root',ntemp*0.5, flag)", this line means that half of the MC sample events will be used for training (except TTto1L), the other half will be used for application and for signal extraction. (we will use data-driven events to estimate the fake contribution, so all the MC events of TTto1L will be used for training)
