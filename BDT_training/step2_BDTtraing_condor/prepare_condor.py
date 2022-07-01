import os,json
import sys
from os import walk

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

if __name__ == "__main__":
  PWD=os.getcwd()
  wrapper_dir=PWD+'/wrapper.sh'
  year="2018"
  signals=['a','s']
  couplings=['rtc01','rtu01']
  masses=['200','300','350','400','500','600','700']
  system_unc=["central","jesup","jesdo","jerup","jerdo","metUnslusEnup","metUnslusEndo"]

  for isig in range(0,len(signals)):
    for ic in range(0,len(couplings)):
      for im in range(0,len(masses)):
        samples_temp=prepare_condor(signals[isig],couplings[ic],masses[im])
        dir_temp=samples_temp.split('.')[0].split('/')[-1]
        os.mkdir(dir_temp)
        os.chdir(dir_temp)
        PWDSEC=os.getcwd()
        for isys in range(0,len(system_unc)):
          os.mkdir(dir_temp+'_'+str(isys))
          os.chdir(dir_temp+'_'+str(isys))
          os.system(r'cp ../../wrapper.sh .')
          os.system(r'sed -i "s/SIGNALROOT/%s/g" wrapper.sh' %(samples_temp))
          os.system(r'sed -i "s/YEAR/%s/g" wrapper.sh' %(year))
          os.system(r'cp ../../TMVAClassification.C .')
          os.system(r'sed -i "s/SYSTEMATICS/%s/g" TMVAClassification.C' %(system_unc[isys])) 
          os.system(r'sed -i "s/MASS/%s/g" TMVAClassification.C' %(masses[im])) 
          if signals[isig]=='a':
            os.system(r'sed -i "s/PARTICLE/a/g" wrapper.sh')
            os.system(r'sed -i "s/PARTICLE/a/g" TMVAClassification.C')
            os.system(r'sed -i "s/COUP/%s/g" wrapper.sh' %(couplings[ic]))
            os.system(r'sed -i "s/COUP/%s/g" TMVAClassification.C' %(couplings[ic]))
            os.system(r'sed -i "s/CPART/A/g" wrapper.sh')
            os.system(r'sed -i "s/MASS/%s/g" wrapper.sh' %(masses[im]))
            os.system(r'sed -i "s/SYST/%s/g" wrapper.sh' %(system_unc[isys]))
          else:
            os.system(r'sed -i "s/PARTICLE/s0/g" wrapper.sh')
            os.system(r'sed -i "s/PARTICLE/s0/g" TMVAClassification.C')
            os.system(r'sed -i "s/COUP/%s/g" wrapper.sh' %(couplings[ic]))
            os.system(r'sed -i "s/COUP/%s/g" TMVAClassification.C' %(couplings[ic]))
            os.system(r'sed -i "s/CPART/S0/g" wrapper.sh')
            os.system(r'sed -i "s/MASS/%s/g" wrapper.sh' %(masses[im]))
            os.system(r'sed -i "s/SYST/%s/g" wrapper.sh' %(system_unc[isys]))
          os.chdir(PWDSEC)
        os.system(r'cp ../sub.jdl .')
        os.system(r'sed -i "s/NUMBER/%s/g" sub.jdl' %(len(system_unc)))
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
