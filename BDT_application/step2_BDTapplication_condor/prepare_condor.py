import os,json
import sys
from os import walk
import optparse
import subprocess

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
  usage = 'usage: %prog [options]'
  parser = optparse.OptionParser(usage)
  parser.add_option('-e', '--era', dest='era', help='[all/2016apv/2016postapv/2017/2018]',default='all',type='string')
  (args,opt) = parser.parse_args()

  Eras_List = ['2016postapv','2016apv','2017','2018']
  Eras = []
  for Era in Eras_List:
    if args.era == 'all' or args.era == Era:
      Eras.append(Era)
  
  
  for Era in Eras:
    os.system('mkdir -p %s'%Era)
    signals=['a','s']
    couplings=['rtc01','rtc04','rtc08','rtc10','rtu01','rtu04','rtu08','rtu10']
    masses=['200','300','350','400','500','600','700']

    for isig in range(0,len(signals)):
      for ic in range(0,len(couplings)):
        for im in range(0,len(masses)):
          samples_temp=prepare_condor(signals[isig],couplings[ic],masses[im])
          dir_temp=samples_temp.split('.')[0].split('/')[-1]
          print ("dir_temp: ", dir_temp)
          os.mkdir(Era+'/'+dir_temp)
          os.chdir(Era+'/'+dir_temp)
          print ("cwd: ", os. getcwd())
          PWDSEC=os.getcwd()
          os.system(r'cp ../../wrapper.sh wrapper_%s.sh' %(Era))
          os.system(r'sed -i "s/SIGNALROOT/%s/g" wrapper_%s.sh' %(samples_temp, Era))
          os.system(r'sed -i "s/YEAR/%s/g" wrapper_%s.sh' %(Era, Era))
          os.system(r'sed -i "s/TMVAClassificationApplication.C/TMVAClassificationApplication_%s.C/g" wrapper_%s.sh' %(Era, Era))
          if Era == "2016apv" or Era == "2016postapv":
            os.system(r'cp ../../TMVAClassificationApplication_%s.C .' %(Era) )
          else:
            os.system(r'cp ../../TMVAClassificationApplication.C TMVAClassificationApplication_%s.C' %(Era) )
          os.system(r'sed -i "s/MASS/%s/g" TMVAClassificationApplication_%s.C' %(masses[im], Era)) 
          os.system(r'sed -i "s/YEAR/%s/g" TMVAClassificationApplication_%s.C' %(Era, Era))
          os.system(r'sed -i "s/TMVAClassificationApplication()/TMVAClassificationApplication_%s()/g" TMVAClassificationApplication_%s.C' %(Era, Era))

          # Luminosity need to change accordingly
          if Era == "2016apv":
            os.system(r'sed -i "s/LUMI/19520/g" TMVAClassificationApplication_%s.C' %(Era))
          elif Era == "2016postapv":
            os.system(r'sed -i "s/LUMI/16810/g" TMVAClassificationApplication_%s.C' %(Era))
          elif Era == "2017":
            os.system(r'sed -i "s/LUMI/41480/g" TMVAClassificationApplication_%s.C' %(Era))
          else:
            os.system(r'sed -i "s/LUMI/59830/g" TMVAClassificationApplication_%s.C' %(Era))
          
          if signals[isig]=='a':
            os.system(r'sed -i "s/MSIGTYPE/MA/g" wrapper_%s.sh' %(Era))
            os.system(r'sed -i "s/CSIGTYPE/A/g" TMVAClassificationApplication_%s.C' %(Era))
            os.system(r'sed -i "s/SIGTYPE/a/g" wrapper_%s.sh' %(Era))
            os.system(r'sed -i "s/SIGTYPE/a/g" TMVAClassificationApplication_%s.C' %(Era))
            if 'rtc' in couplings[ic]:
              os.system(r'sed -i "s/COUPLING/rtc01/g" wrapper_%s.sh' %(Era))
            if 'rtu' in couplings[ic]:
              os.system(r'sed -i "s/COUPLING/rtu01/g" wrapper_%s.sh' %(Era))
            os.system(r'sed -i "s/COUPLING/%s/g" TMVAClassificationApplication_%s.C' %(couplings[ic], Era))
            os.system(r'sed -i "s/MASS/%s/g" wrapper_%s.sh' %(masses[im], Era))
          else:
            os.system(r'sed -i "s/MSIGTYPE/MS0/g" wrapper_%s.sh' %(Era))
            os.system(r'sed -i "s/CSIGTYPE/S0/g" TMVAClassificationApplication_%s.C' %(Era))
            os.system(r'sed -i "s/SIGTYPE/s0/g" wrapper_%s.sh' %(Era))
            os.system(r'sed -i "s/SIGTYPE/s0/g" TMVAClassificationApplication_%s.C' %(Era))
            if 'rtc' in couplings[ic]:
              os.system(r'sed -i "s/COUPLING/rtc01/g" wrapper_%s.sh' %(Era))
            if 'rtu' in couplings[ic]:
              os.system(r'sed -i "s/COUPLING/rtu01/g" wrapper_%s.sh' %(Era))
            os.system(r'sed -i "s/COUPLING/%s/g" TMVAClassificationApplication_%s.C' %(couplings[ic], Era))
            os.system(r'sed -i "s/MASS/%s/g" wrapper_%s.sh' %(masses[im], Era))
          # Copy the sub.jdl file
          os.system(r'cp ../../sub.jdl .')
          os.system(r'sed -i "s/wrapper.sh/wrapper_%s.sh/g" sub.jdl' %(Era))
          os.system(r'sed -i "s/TMVAClassificationApplication.C/TMVAClassificationApplication_%s.C/g" sub.jdl' %(Era))
          
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
