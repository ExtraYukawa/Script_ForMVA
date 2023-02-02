Get the config files:
- For low mass
```
python runCondor.py --era 2016apv
```

- For highmass
```
python runCondor.py --era 2016postapv -s highmass
```

- For interference samples:
```
python runCondor.py --era 2016postapv -s interference
```

simply by using "python slim.py" to get the inputs for the BDT training, several things to be stressed:

1. for each coupilng typy, e.g., rtc, only one coupling strength will be used, since we already checked that the BDT score of rtc 01/04/08/10 are almost the same

2. after obtaining the root file, move them to the eos region for further BDT training which will be implemeted through condor, e.g., the 2018 inputs are put in /eos/cms/store/group/phys_top/ExtraYukawa/BDT/BDT_input_forTraining/2018/

3. Source env.sh to set up python environment. May need virtualenv to reduce warning message.
4. Need to modify output directory to your own directory. Current: `/eos/user/t/tihsu/BDT/ntuple_skim`
