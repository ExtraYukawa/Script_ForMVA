## Get the config files and run the whole process with condor:
- For low mass
```
python runCondor.py --era 2016apv
```

- For highmass
```
python runCondor.py --era 2016apv -s highmass
```

- For interference samples:
```
python runCondor.py --era 2016apv -s interference
```
** Repeat for other era's: 2016postapv, 2017, 2018

Some files need to produce here (2016apv)
```
cd sample/2016apv
hadd -f data_ee.root *_B2_ee.root *_C_ee.root *_D_ee.root *_E_ee.root *_F_ee.root
hadd -f data_mm.root *_B2_mm.root *_C_mm.root *_D_mm.root *_E_mm.root *_F_mm.root
hadd -f data_em.root *_B2_em.root *_C_em.root *_D_em.root *_E_em.root *_F_em.root

hadd -f fakelep_ee.root DoubleEG_*_fake_ee.root SingleEG_*_fake_ee.root
hadd -f fakelep_mm.root DoubleMuon_*_fake_mm.root SingleMuon_*_fake_mm.root
hadd -f fakelep_em.root MuonEG_*_fake_em.root SingleEG_*_fake_em.root SingleMuon_*_fake_em.root
```

- Some files need to produce here (2016postapv)
```
cd sample/2016postapv
hadd -f data_ee.root *_F_ee.root *_G_ee.root *_H_ee.root
hadd -f data_mm.root *_F_mm.root *_G_mm.root *_H_mm.root
hadd -f data_em.root *_F_em.root *_G_em.root *_H_em.root

hadd -f fakelep_ee.root DoubleEG_*_fake_ee.root SingleEG_*_fake_ee.root
hadd -f fakelep_mm.root DoubleMuon_*_fake_mm.root SingleMuon_*_fake_mm.root
hadd -f fakelep_em.root MuonEG_*_fake_em.root SingleEG_*_fake_em.root SingleMuon_*_fake_em.root

```
- Some files need to produce here (2017)
```
cd sample/2017
ls DoubleEG*_ee.root SingleEG*_ee.root | grep -v fake | xargs hadd -f data_ee.root
ls DoubleMuon*_mm.root SingleMuon*_mm.root | grep -v fake | xargs hadd -f data_mm.root
ls MuonEG*_em.root SingleMuon*_em.root SingleEG*_em.root | grep -v fake | xargs hadd -f data_em.root

ls DoubleEG*fake_ee.root SingleEG*fake_ee.root | xargs hadd -f fakelep_ee.root
ls DoubleMuon*fake_mm.root SingleMuon*fake_mm.root | xargs hadd -f fakelep_mm.root
ls MuonEG*fake_em.root SingleMuon*fake_em.root SingleEG*fake_em.root | xargs hadd -f fakelep_em.root
```

- Some files need to produce here (2018)
```
cd sample/2018
ls EGamma*_ee.root | grep -v fake | xargs hadd -f data_ee.root
ls DoubleMuon*_mm.root SingleMuon*_mm.root | grep -v fake | xargs hadd -f data_mm.root
ls MuonEG*_em.root SingleMuon*_em.root | grep -v fake | xargs hadd -f data_em.root

ls EGamma*fake_ee.root | xargs hadd -f fakelep_ee.root
ls DoubleMuon*fake_mm.root SingleMuon*fake_mm.root | xargs hadd -f fakelep_mm.root
ls MuonEG*fake_em.root SingleMuon*fake_em.root | xargs hadd -f fakelep_em.root
```


- Make tar with all file
```  
aa.tar.gz is the compressed file of all the root files except those signal files for easy condor submission
ls *.root | grep -v ttc_ | xargs tar zcf aa.tar.gz
```

- After having all the inputs root files, put them under e.g., /eos/cms/store/group/phys_top/ExtraYukawa/<BDT_yourchoice>/BDT_input_application/
e.g.
```
cp -v * /eos/cms/store/group/phys_top/ExtraYukawa/<BDT_yourchoice>/BDT_input_application/2016apv/
```

