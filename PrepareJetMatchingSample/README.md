## Step0 Skim ntuple
Get the config files, note that for `era` option, by default runs all eras.
- For low mass
```
python runCondor.py --era 2016apv --step 0
```

- For highmass
```
python runCondor.py --era 2016apv --step 0 -s highmass
```

- For interference samples:
```
python runCondor.py --era 2016apv --step 0 -s interference
```

simply by using "python slim.py" to get the skim ntuples. Results are stored in `${EOSDIR}/ntuple_skim/`.

1. for each coupilng typy, e.g., rtc, only one coupling strength will be used, since we already checked that the BDT score of rtc 01/04/08/10 are almost the same

2. Output directory is assigned in `python/common.py`. 
3. Source env.sh to set up python environment. May need virtualenv to reduce warning message.

## Step1 Run combination
Get the Jet combination in each events and saved in h5 format. Results are stored in `${EOSDIR}/dataframe/`. Since we stake the dataframe event by event, it will take extremely long time for running ntuple with O(100,000) Events. Here, we define `batchsize=5000` in `runCondor.py` to accelerate the whole process. The whole procedure takes only about 30 ~ 40 minutes now. You can still change the batchsize to speed up the whole process.
```
python runCondor.py --step 1
python runCondor.py --step 1 -s highmass
python runCondor.py --step 1 -s interference
```
## Step2 Run combination
Run Jet index algorithm and add new branch in TTree. Results are stored in `${EOSDIR}/ntuple_reindex/`.
```
python runCondor.py --step 2
python runCondor.py --step 2 -s highmass
python runCondor.py --step 2 -s interference
```

