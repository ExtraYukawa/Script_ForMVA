import os,json
import sys
from os import walk

def prepare_condor(signal,coupling,mass):
  WHICH_SAMPLE=signal
  WHICH_COUPLING=coupling
  MASS=mass
  if WHICH_SAMPLE=="a":
    SIGNAL='ttc_a_'+WHICH_COUPLING+'_MA'+MASS+'.root'
  else:
    SIGNAL='ttc_s0_'+WHICH_COUPLING+'_MS0'+MASS+'.root'

  sample=SIGNAL
  return sample

if __name__ == "__main__":
  PWD=os.getcwd()
  wrapper_dir=PWD+'/wrapper.sh'
  year="2018"
  signals=['a','s']
  couplings=['rtc01','rtc04','rtc08','rtc10','rtu01','rtu04','rtu08','rtu10']
  masses=['200','300','350','400','500','600','700']

  for isig in range(0,len(signals)):
    for ic in range(0,len(couplings)):
      for im in range(0,len(masses)):
        samples_temp=prepare_condor(signals[isig],couplings[ic],masses[im])
        dir_temp=samples_temp.split('.')[0].split('/')[-1]
        os.mkdir(dir_temp)
        os.chdir(dir_temp)
        PWDSEC=os.getcwd()
        os.system(r'cp ../wrapper.sh .')
        os.system(r'sed -i "s/SIGNALROOT/%s/g" wrapper.sh' %(samples_temp))
        os.system(r'sed -i "s/YEAR/%s/g" wrapper.sh' %(year))
        os.system(r'cp ../TMVAClassificationApplication.C .')
        os.system(r'sed -i "s/MASS/%s/g" TMVAClassificationApplication.C' %(masses[im])) 
        os.system(r'sed -i "s/YEAR/%s/g" TMVAClassificationApplication.C' %(year))
        os.system(r'sed -i "s/LUMI/59800/g" TMVAClassificationApplication.C')
        if signals[isig]=='a':
          os.system(r'sed -i "s/MSIGTYPE/MA/g" wrapper.sh')
          os.system(r'sed -i "s/CSIGTYPE/A/g" TMVAClassificationApplication.C')
          os.system(r'sed -i "s/SIGTYPE/a/g" wrapper.sh')
          os.system(r'sed -i "s/SIGTYPE/a/g" TMVAClassificationApplication.C')
          if 'rtc' in couplings[ic]:
            os.system(r'sed -i "s/COUPLING/rtc01/g" wrapper.sh')
          if 'rtu' in couplings[ic]:
            os.system(r'sed -i "s/COUPLING/rtu01/g" wrapper.sh')
          os.system(r'sed -i "s/COUPLING/%s/g" TMVAClassificationApplication.C' %(couplings[ic]))
          os.system(r'sed -i "s/MASS/%s/g" wrapper.sh' %(masses[im]))
        else:
          os.system(r'sed -i "s/MSIGTYPE/MS0/g" wrapper.sh')
          os.system(r'sed -i "s/CSIGTYPE/S0/g" TMVAClassificationApplication.C')
          os.system(r'sed -i "s/SIGTYPE/s0/g" wrapper.sh')
          os.system(r'sed -i "s/SIGTYPE/s0/g" TMVAClassificationApplication.C')
          if 'rtc' in couplings[ic]:
            os.system(r'sed -i "s/COUPLING/rtc01/g" wrapper.sh')
          if 'rtu' in couplings[ic]:
            os.system(r'sed -i "s/COUPLING/rtu01/g" wrapper.sh')
          os.system(r'sed -i "s/COUPLING/%s/g" TMVAClassificationApplication.C' %(couplings[ic]))
          os.system(r'sed -i "s/MASS/%s/g" wrapper.sh' %(masses[im]))
        os.system(r'cp ../sub.jdl .')
        if signals[isig]=='a':
          os.system(r'sed -i "s/MSIGTYPE/MA/g" sub.jdl')
          os.system(r'sed -i "s/SIGTYPE/a/g" sub.jdl')
          os.system(r'sed -i "s/COUPLING/%s/g" sub.jdl' %(couplings[ic]))
          os.system(r'sed -i "s/MASS/%s/g" sub.jdl' %(masses[im]))
        if signals[isig]=='s':
          os.system(r'sed -i "s/MSIGTYPE/MS0/g" sub.jdl')
          os.system(r'sed -i "s/SIGTYPE/s0/g" sub.jdl')
          os.system(r'sed -i "s/COUPLING/%s/g" sub.jdl' %(couplings[ic]))
          os.system(r'sed -i "s/MASS/%s/g" sub.jdl' %(masses[im]))
        os.chdir(PWD)
