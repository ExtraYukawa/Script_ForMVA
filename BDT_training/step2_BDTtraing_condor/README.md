- Normal samples
```
python prepare_condor.py --era 2016postapv
```

- Highmass:
```
python prepare_condor.py --era 2016postapv -s highmass
```

- Inteference:
```
python prepare_condor.py --era 2016postapv -s interference
```

- Run to extract xml weight
```
sh extract.sh
```

- After having all the BDT weights files, put them under e.g., /eos/cms/store/group/phys_top/ExtraYukawa/BDT/BDT_weights/2018/
```
cp -r 2016postapv/* /eos/cms/store/group/phys_top/ExtraYukawa/BDT/BDT_weights/2016postapv/
```