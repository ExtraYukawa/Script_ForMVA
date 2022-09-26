import os,json
import sys
from os import walk
import optparse
import subprocess

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

if __name__ == "__main__":
  PWD=os.getcwd()
  wrapper_dir=PWD+'/wrapper.sh'
  usage = 'usage: %prog [options]'
  parser = optparse.OptionParser(usage)
  parser.add_option('-e', '--era', dest='era', help='[all/2016apv/2016postapv/2017/2018]',default='all',type='string')
  parser.add_option('-s', '--sampletype', dest='sampletype', help='[all/normal/interference/highmass]',default='normal',type='string')
  (args,opt) = parser.parse_args()

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
      #masses = ['250','300','350','400','550','700'] # asume this A mass
      masses = ['250'] # asume this A mass
      #S_masses = ['200','250','300','350','500','650'] # assume S mass = A-50
    else:
      signals=['a','s']
      couplings=['rtc04','rtu04']
      masses=['200','300','350','400','500','600','700'] 
      
    system_unc=["central","jesup","jesdo","jerup","jerdo","metUnslusEnup","metUnslusEndo"]

    for isig in range(0,len(signals)):
      for ic in range(0,len(couplings)):
        for im in range(0,len(masses)):
          samples_temp=prepare_condor(signals[isig],couplings[ic],masses[im])
          dir_temp=samples_temp.split('.')[0].split('/')[-1]
          print ("dir_temp: ", dir_temp)
          print ("OK------>")
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
            if Era == "2016apv" or Era == "2016postapv":
              os.system(r'cp ../../../TMVAClassification_%s.C .' %(Era))
            else:
              os.system(r'cp ../../../TMVAClassification.C TMVAClassification_%s.C' %(Era))
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
