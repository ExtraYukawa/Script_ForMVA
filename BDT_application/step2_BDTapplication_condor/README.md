- Normal samples
```
python prepare_condor.py --era 2016apv
```

- highmass:
```
python prepare_condor.py --era 2016apv -s highmass
```

- inteference:
```
python prepare_condor.py --era 2016apv -s interference
```

** Repeat for other era's: 2016postapv, 2017, 2018

- Submit to condor:
```
sh submit.sh
condor_q
```

- Run to extract BDT final output for limit computation
```
sh extract.sh
```

put the final BDT outputs under e.g., /eos/cms/store/group/phys_top/ExtraYukawa/<BDT_yourchoice>/BDT_output/2018/
