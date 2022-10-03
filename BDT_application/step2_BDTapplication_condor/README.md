- Normal samples
```
python prepare_condor.py --era 2016postapv
```

- highmass:
```
python prepare_condor.py --era 2016postapv -s highmass
```

- inteference:
```
python prepare_condor.py --era 2016postapv -s interference
```

- Submit to condor:
```
sh submit.sh
condor_q
```

- Run to extract BDT final output for limit computation
```
sh extract.sh
```

put the final BDT outputs under e.g., /eos/cms/store/group/phys_top/ExtraYukawa/BDT/BDT_output/2018/
