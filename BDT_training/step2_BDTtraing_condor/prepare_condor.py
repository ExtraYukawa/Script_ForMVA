import os,json
import sys
from os import walk
import optparse, argparse
import subprocess
from collections import OrderedDict
import ROOT

os.system('cp ../../python/common.py .')
from common import inputFile_path, cmsswBase


def prepare_condor(sample,coupling,mass):
  WHICH_SAMPLE=sample
  WHICH_COUPLING=coupling
  MASS=mass
  if WHICH_SAMPLE=="a":
    SIGNAL='ttc_a_'+WHICH_COUPLING+'_MA'+MASS+'.root'
  elif WHICH_SAMPLE=="interference":
    SIGNAL='ttc_a_'+MASS+'_s_'+str(int(MASS)-50)+'_'+WHICH_COUPLING+'.root'
  else:
    SIGNAL='ttc_s0_'+WHICH_COUPLING+'_MS0'+MASS+'.root'

  sample=SIGNAL
  return sample

def GetBackgroundList(era):
  jsonfile = open(os.path.join(cmsswBase + '/src/Script_ForMVA/data/sample_' + str(era) + 'UL.json'))
  samples  = json.load(jsonfile, encoding='utf-8', object_pairs_hook=OrderedDict).items()
  jsonfile.close()
  BackgroundFile_List = []
  for process, desc in samples:
    if desc[4] == 1:
      BackgroundFile_List.append((str((process + ".root")),desc[0]))
  return BackgroundFile_List

def prepare_BackgroundCommand(era):
  
  Background_List = GetBackgroundList(era)
  count = 1
  init_input = "\\n"
  backgroundfile_input = "\\n"
  backgroundfile_readtree = "\\n"
  addbackgroundtree = "\\n"
  for f in Background_List:
    ftemp= ROOT.TFile.Open((inputFile_path[era] + f[0]));
    ttemp= ftemp.Get("nEventsGenWeighted");
    init_input += "   TFile *input_B%d(0);\\n"%(count)
    backgroundfile_input += '   input_B%d=TFile::Open(\\"%s\\");\\n'%(count, f[0])
    backgroundfile_readtree += '   TTree *background%d     = (TTree*)input_B%d->Get(\\"SlimTree\\");\\n'%(count,count)
    addbackgroundtree += "   dataloader->AddBackgroundTree( background%d,%f\/%f);\\n"%(count,f[1],float(ttemp.GetBinContent(1)/100000))
#    addbackgroundtree += "   dataloader->AddBackgroundTree( background%d,%f\/background%d->GetEntries());\\n"%(count,f[1],count)
    ftemp.Close()

    count += 1
  return init_input, backgroundfile_input, backgroundfile_readtree, addbackgroundtree

if __name__ == "__main__":
  PWD=os.getcwd()
  wrapper_dir=PWD+'/wrapper.sh'
  usage = 'usage: %prog [options]'
  parser = argparse.ArgumentParser(description=usage)
  parser.add_argument('-e', '--era', dest='era', help='[all/2016apv/2016postapv/2017/2018]',default='all',type=str, choices=["all","2016apv","2016postapv","2017","2018"])
  parser.add_argument('-s', '--sampletype', dest='sampletype', help='[all/normal/interference/highmass]',default='normal',type=str, choices=["all","normal","interference","highmass"])
  args = parser.parse_args()

  Eras_List = ['2016postapv','2016apv','2017','2018']
  Eras = []
  for Era in Eras_List:
    if args.era == 'all' or args.era == Era:
      Eras.append(Era)
  
  # Loop over Eras
  for Era in Eras:

    os.system('mkdir -p %s'%Era)
    if args.sampletype == 'highmass':
      signals=['a']
      couplings=['rtc04','rtu04']
      masses=['800','900','1000']
    elif args.sampletype == 'interference':
      signals=['interference']
      couplings=['rtc04','rtu04']
      masses = ['250','300','350','400','550','700','800','900','1000'] # asume this A mass
      # masses = ['350'] # asume this A mass
      # S_masses = ['200','250','300','350','500','650','750','850','900'] # assume S mass = A-50
    else:
      signals=['a']
      couplings=['rtc04','rtu04'] #keep in mind (rtc01, vs rtc04)
      masses=['200','300','350','400','500','600','700']
      
    system_unc=["central"]

    init_input, backgroundfile_input, backgroundfile_readtree, addbackgroundtree = prepare_BackgroundCommand(Era)
    print(init_input)

    for isig in range(0,len(signals)):
      for ic in range(0,len(couplings)):
        for im in range(0,len(masses)):
          samples_temp=prepare_condor(signals[isig],couplings[ic],masses[im])
          dir_temp=samples_temp.split('.')[0].split('/')[-1]
          print ("dir_temp: ", dir_temp)
          os.system('rm -rf %s/%s'%(Era,dir_temp))
          os.mkdir(Era+'/'+dir_temp)
          os.chdir(Era+'/'+dir_temp)
          print ("cwd: ", os. getcwd())
          PWDSEC=os.getcwd()
          for isys in range(0,len(system_unc)):
            os.mkdir(dir_temp+'_'+str(isys))
            os.chdir(dir_temp+'_'+str(isys))
            os.system(r'cp ../../../wrapper.sh wrapper_%s.sh' %(Era))
            os.system(r'sed -i "s/SIGNALROOT/%s/g" wrapper_%s.sh' %(samples_temp, Era))
            os.system(r'sed -i "s/YEAR/%s/g" wrapper_%s.sh' %(Era, Era))
            os.system(r'sed -i "s/TMVAClassification.C/TMVAClassification_%s.C/g" wrapper_%s.sh' %(Era, Era))
            os.system(r'cp ../../../TMVAClassification.C TMVAClassification_%s.C' %(Era))
            os.system(r'sed -i "s/INIT_INPUT/%s/g" TMVAClassification_%s.C' %(init_input,Era))
            os.system(r'sed -i "s/BACKGROUNDFILE_INPUT/%s/g" TMVAClassification_%s.C'%(backgroundfile_input,Era))
            os.system(r'sed -i "s/BACKGROUNDFILE_READTREE/%s/g" TMVAClassification_%s.C'%(backgroundfile_readtree,Era))
            os.system(r'sed -i "s/ADDBACKGROUNDTREE/%s/g" TMVAClassification_%s.C'%(addbackgroundtree,Era))
            os.system(r'sed -i "s/SYSTEMATICS/%s/g" TMVAClassification_%s.C' %(system_unc[isys], Era)) 
            
            os.system(r'sed -i "s/TMVAClassification()/TMVAClassification_%s()/g" TMVAClassification_%s.C' %(Era, Era))
            
            if signals[isig]=='a':
              os.system(r'sed -i "s/PARTICLE/a/g" wrapper_%s.sh' %(Era))
              os.system(r'sed -i "s/PARTICLE/a/g" TMVAClassification_%s.C' %(Era))
              os.system(r'sed -i "s/MASS/%s/g" TMVAClassification_%s.C' %(masses[im], Era)) 
              os.system(r'sed -i "s/COUP/%s/g" wrapper_%s.sh' %(couplings[ic], Era))
              os.system(r'sed -i "s/COUP/%s/g" TMVAClassification_%s.C' %(couplings[ic], Era))
              os.system(r'sed -i "s/CPART/A/g" wrapper_%s.sh' %(Era))
              os.system(r'sed -i "s/MASS/%s/g" wrapper_%s.sh' %(masses[im], Era))
              os.system(r'sed -i "s/SYST/%s/g" wrapper_%s.sh' %(system_unc[isys], Era))
            elif signals[isig]=='interference':
              #os.system(r'sed -i "s/PARTICLE/a_s/g" wrapper_%s.sh' %(Era))
              os.system(r'sed -i "s/PARTICLE/a_s/g" TMVAClassification_%s.C' %(Era))
              #os.system(r'sed -i "s/COUP/%s/g" wrapper_%s.sh' %(couplings[ic], Era))
              os.system(r'sed -i "s/COUP/%s/g" TMVAClassification_%s.C' %(couplings[ic], Era))
              #os.system(r'sed -i "s/CPART/A_S/g" wrapper_%s.sh' %(Era))
              #os.system(r'sed -i "s/MASS/%s/g" wrapper_%s.sh' %(masses[im]+'_'+str(int(masses[im])-50), Era))
              
              os.system(r'sed -i "s/MASS/%s/g" TMVAClassification_%s.C' %(masses[im]+'_'+str(int(masses[im])-50), Era))
              os.system(r'sed -i "s/SYST/%s/g" wrapper_%s.sh' %(system_unc[isys], Era))
              os.system(r'sed -i "s/PARTICLE_COUP_MCPARTMASS/a_%s_s_%s_%s/g" wrapper_%s.sh' %(masses[im], str(int(masses[im])-50), couplings[ic], Era))
            else:
              os.system(r'sed -i "s/PARTICLE/s0/g" wrapper_%s.sh' %(Era))
              os.system(r'sed -i "s/PARTICLE/s0/g" TMVAClassification_%s.C' %(Era))
              os.system(r'sed -i "s/COUP/%s/g" wrapper_%s.sh' %(couplings[ic], Era))
              os.system(r'sed -i "s/COUP/%s/g" TMVAClassification_%s.C' %(couplings[ic], Era))
              os.system(r'sed -i "s/MASS/%s/g" TMVAClassification_%s.C' %(masses[im], Era)) 
              os.system(r'sed -i "s/CPART/S0/g" wrapper_%s.sh' %(Era))
              os.system(r'sed -i "s/MASS/%s/g" wrapper_%s.sh' %(masses[im], Era))
              os.system(r'sed -i "s/SYST/%s/g" wrapper_%s.sh' %(system_unc[isys], Era))
            os.chdir(PWDSEC)
            
          # changes for submit jdl file
          os.system(r'cp ../../sub.jdl .')
          os.system(r'sed -i "s/NUMBER/%s/g" sub.jdl' %(len(system_unc)))
          os.system(r'sed -i "s/TMVAClassification.C/TMVAClassification_%s.C/g" sub.jdl' %(Era))
          os.system(r'sed -i "s/wrapper.sh/wrapper_%s.sh/g" sub.jdl' %(Era))
          
          if signals[isig]=='a':
            os.system(r'sed -i "s/PARTICLE/a/g" sub.jdl')
            os.system(r'sed -i "s/COUP/%s/g" sub.jdl' %(couplings[ic]))
            os.system(r'sed -i "s/CPART/A/g" sub.jdl')
            os.system(r'sed -i "s/MASS/%s/g" sub.jdl' %(masses[im]))
          elif signals[isig]=='interference':
            #os.system(r'sed -i "s/PARTICLE/a_s/g" sub.jdl')
            #os.system(r'sed -i "s/COUP/%s/g" sub.jdl' %(couplings[ic]))
            #os.system(r'sed -i "s/CPART/A_S/g" sub.jdl')
            #os.system(r'sed -i "s/MASS/%s/g" sub.jdl' %(masses[im]))
            os.system(r'sed -i "s/ttc_PARTICLE_COUP_MCPARTMASS/%s/g" sub.jdl' %(dir_temp))
          if signals[isig]=='s':
            os.system(r'sed -i "s/PARTICLE/s0/g" sub.jdl')
            os.system(r'sed -i "s/COUP/%s/g" sub.jdl' %(couplings[ic]))
            os.system(r'sed -i "s/CPART/S0/g" sub.jdl')
            os.system(r'sed -i "s/MASS/%s/g" sub.jdl' %(masses[im]))
          os.chdir(PWD)
