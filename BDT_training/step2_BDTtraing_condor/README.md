## Training is done in following way:

- Normal samples
```
python prepare_condor.py --era 2016apv
```

- Highmass:
```
python prepare_condor.py --era 2016apv -s highmass
```

- Inteference:
```
python prepare_condor.py --era 2016apv -s interference
```

** Repeat for other era's: 2016postapv, 2017, 2018

- Run to extract xml weight
```
sh extract.sh
```

- After having all the BDT weights files, put them under e.g., /eos/cms/store/group/phys_top/ExtraYukawa/<BDT_yourchoice>/BDT_weights/
```
cp -rv 2016postapv/* /eos/cms/store/group/phys_top/ExtraYukawa/<BDT_yourchoice>/BDT_weights/2016apv/
```