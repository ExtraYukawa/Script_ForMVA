import os,json
import sys
from os import walk
import optparse
import subprocess
from collections import OrderedDict

cmsswBase = os.environ['CMSSW_BASE']

def prepare_condor(sample,coupling,mass):
  WHICH_SAMPLE=sample
  WHICH_COUPLING=coupling
  MASS=mass
  if WHICH_SAMPLE=="a":
    SIGNAL='ttc_a_'+WHICH_COUPLING+'_MA'+MASS+'.root'
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
    if desc[5] == 1:
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
    init_input += "   TFile *input_B%d(0);\\n"%(count)
    backgroundfile_input += '   input_B%d=TFile::Open(\\"%s\\");\\n'%(count, f[0])
    backgroundfile_readtree += '   TTree *background%d     = (TTree*)input_B%d->Get(\\"SlimTree\\");\\n'%(count,count)
    addbackgroundtree += "   dataloader->AddBackgroundTree( background%d,%f\/background%d->GetEntries());\\n"%(count,f[1],count)
    count += 1
  return init_input, backgroundfile_input, backgroundfile_readtree, addbackgroundtree

if __name__ == "__main__":
  PWD=os.getcwd()
  wrapper_dir=PWD+'/wrapper.sh'
  usage = 'usage: %prog [options]'
  parser = optparse.OptionParser(usage)
  parser.add_option('-e', '--era', dest='era', help='[all/2016apv/2016postapv/2017/2018]',default='all',type='string')
  (args,opt) = parser.parse_args()

  Eras_List = ['2016postapv','2016apv','2017','2018']
  Eras = []
  for Era in Eras_List:
    if args.era == 'all' or args.era == Era:
      Eras.append(Era)
  
  # year="2018"
  for Era in Eras:

    os.system('mkdir -p %s'%Era)
    
    signals=['a','s']
    couplings=['rtc01','rtu01']
    masses=['200', '700'] #,'300','350','400','500','600','700'] #fixme gkole
    system_unc=["central","jesup","jesdo","jerup","jerdo","metUnslusEnup","metUnslusEndo"]

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
            os.system(r'cp ../../../../../script/TMVAClassification.C TMVAClassification_%s.C' %(Era))
            os.system(r'sed -i "s/INIT_INPUT/%s/g" TMVAClassification_%s.C' %(init_input,Era))
            os.system(r'sed -i "s/BACKGROUNDFILE_INPUT/%s/g" TMVAClassification_%s.C'%(backgroundfile_input,Era))
            os.system(r'sed -i "s/BACKGROUNDFILE_READTREE/%s/g" TMVAClassification_%s.C'%(backgroundfile_readtree,Era))
            os.system(r'sed -i "s/ADDBACKGROUNDTREE/%s/g" TMVAClassification_%s.C'%(addbackgroundtree,Era))
            os.system(r'sed -i "s/SYSTEMATICS/%s/g" TMVAClassification_%s.C' %(system_unc[isys], Era)) 
            os.system(r'sed -i "s/MASS/%s/g" TMVAClassification_%s.C' %(masses[im], Era)) 
            os.system(r'sed -i "s/TMVAClassification()/TMVAClassification_%s()/g" TMVAClassification_%s.C' %(Era, Era))
            
            if signals[isig]=='a':
              os.system(r'sed -i "s/PARTICLE/a/g" wrapper_%s.sh' %(Era))
              os.system(r'sed -i "s/PARTICLE/a/g" TMVAClassification_%s.C' %(Era))
              os.system(r'sed -i "s/COUP/%s/g" wrapper_%s.sh' %(couplings[ic], Era))
              os.system(r'sed -i "s/COUP/%s/g" TMVAClassification_%s.C' %(couplings[ic], Era))
              os.system(r'sed -i "s/CPART/A/g" wrapper_%s.sh' %(Era))
              os.system(r'sed -i "s/MASS/%s/g" wrapper_%s.sh' %(masses[im], Era))
              os.system(r'sed -i "s/SYST/%s/g" wrapper_%s.sh' %(system_unc[isys], Era))
            else:
              os.system(r'sed -i "s/PARTICLE/s0/g" wrapper_%s.sh' %(Era))
              os.system(r'sed -i "s/PARTICLE/s0/g" TMVAClassification_%s.C' %(Era))
              os.system(r'sed -i "s/COUP/%s/g" wrapper_%s.sh' %(couplings[ic], Era))
              os.system(r'sed -i "s/COUP/%s/g" TMVAClassification_%s.C' %(couplings[ic], Era))
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
          if signals[isig]=='s':
            os.system(r'sed -i "s/PARTICLE/s0/g" sub.jdl')
            os.system(r'sed -i "s/COUP/%s/g" sub.jdl' %(couplings[ic]))
            os.system(r'sed -i "s/CPART/S0/g" sub.jdl')
            os.system(r'sed -i "s/MASS/%s/g" sub.jdl' %(masses[im]))
          os.chdir(PWD)
