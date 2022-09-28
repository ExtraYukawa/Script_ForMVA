import os
import sys
import optparse
import subprocess
import json
import ROOT
from collections import OrderedDict

def prepare_shell(shell_file, command, condor, FarmDir):

  cwd       = os.getcwd()
  with open('%s/%s'%(FarmDir,shell_file), 'w') as shell:
    shell.write('#!/bin/bash\n')
    shell.write('WORKDIR=%s\n'%cwd)
    shell.write('cd %s\n'%cmsswBase)
    shell.write('eval `scram r -sh`\n')
    shell.write('cd ${WORKDIR}\n')
    shell.write(command)
  condor.write('cfgFile=%s\n'%shell_file)
  condor.write('queue 1\n')

if __name__=='__main__':
  
  usage = 'usage: %prog [options]'
  parser = optparse.OptionParser(usage)
  parser.add_option('-m', '--method', dest='method', help='[data/slim_mc/slim_data/...]',default='all', type='string')
  parser.add_option('-e', '--era', dest='era', help='[all/2016apv/2016postapv/2017/2018]',default='all',type='string')
  parser.add_option('-s', '--sampletype', dest='sampletype', help='[all/normal/interference/highmass]',default='normal',type='string')
  (args,opt) = parser.parse_args()

  Eras_List = ['2016postapv','2016apv','2017','2018']
  Eras = []
  for Era in Eras_List:
    if args.era == 'all' or args.era == Era:
      Eras.append(Era)

  cmsswBase = os.environ['CMSSW_BASE']
  FarmDir   = '%s/Farm_BDT'%cmsswBase
  cwd       = os.getcwd()
  os.system('mkdir -p %s'%FarmDir)
  os.system('cp %s/../../python/common.py .'%cwd)

  from common import inputFile_path
  from common import GetTrainingFile, GetDataFile

  condor = open('%s/condor.sub'%FarmDir,'w')
  condor.write('output = %s/job_common.out\n'%FarmDir)
  condor.write('error  = %s/job_common.err\n'%FarmDir)
  condor.write('log    = %s/job_common.log\n'%FarmDir)
  condor.write('executable = %s/$(cfgFile)\n'%FarmDir)
  condor.write('requirements = (OpSysAndVer =?= "CentOS7")\n')
  condor.write('+JobFlavour = "tomorrow"\n')
  condor.write('+MaxRuntime = 7200\n')

  cwd = os.getcwd()

  for Era in Eras:
  
    template = "%s/../../script/slim.h"%cwd
    era_header = "script/slim_%s.h"%Era
    template_fake = "%s/../../script/slim_fake.h"%cwd
    era_header_fake = "script/slim_fake_%s.h"%Era

    os.system('mkdir -p script')
    os.system('cat %s | sed "s/EraToBeReplaced/%s/g" > %s'%(template,Era,era_header))
    os.system('cat %s | sed "s/EraToBeReplaced/%s/g" > %s'%(template_fake,Era,era_header_fake))
    os.system('mkdir -p sample/%s'%Era)
 
    path = inputFile_path[Era]
    if (args.method == 'slim_mc' or args.method == 'all') and args.sampletype == 'normal':
      print ("Creating configuration for slim_mc")
      python_file = "%s/slim_mc.py"%cwd

      # Training sample
      Training_list = GetTrainingFile(Era, True)
      print ("=="*50)
      print ("Training_list: ", Training_list)
      
      for iin in Training_list:
        # if not iin == 'TTTo2L.root': continue #Meng confirmed on 7Sep2022
        command = "python %s --era %s --train %d --iin %s"%(python_file, Era, 1, iin)
        shell_file = 'slim_mc_%s_%s.sh'%(iin, Era)
        prepare_shell(shell_file, command, condor, FarmDir)

      # nonTraining sample
      nonTraining_list = GetTrainingFile(Era, False)
      print ("=="*50)
      print ("nonTraining_list: ", nonTraining_list)
      
      for iin in nonTraining_list:
        command = "python %s --era %s --train %d --iin %s"%(python_file, Era, 0, iin)
        shell_file = 'slim_mc_%s_%s.sh'%(iin,Era)
        prepare_shell(shell_file, command, condor, FarmDir)

      # Signal sample
      coups=['rtc01','rtc04','rtc08','rtc10','rtu01','rtu04','rtu08','rtu10']
      cps=['A','S0']
      masses=['200','300','350','400','500','600','700']

      for cp in cps:
        for coup in coups:
          for mass in masses:
            iin = 'ttc_%s_%s.root'%(cp.lower(),coup)
            flag='GenModel_T%sToTTQ_M%s_%s_TuneCP5_13TeV_G2HDM_%s_madgraphMLM_pythia8'%(cp,cp,mass,coup)
            command = "python %s --era %s --train %d --iin %s --flag %s"%(python_file, Era, 1, iin, flag)
            shell_file = 'slim_mc_%s_%s.sh'%(flag,Era)
            prepare_shell(shell_file, command, condor, FarmDir)
    

    #====================
    #Highmass samples
    #====================

    if (args.method == 'slim_mc' or args.method == 'all') and args.sampletype == 'highmass':
      print ("Creating configuration for highmass samples using slim_mc")
      python_file = "%s/slim_mc.py"%cwd

      print ("=="*50)

      coups=['rtc04','rtu04']
      cps=['A']
      masses=['800','900','1000']

      for cp in cps:
        for coup in coups:
          for mass in masses:
            iin = 'ttc_%s_%s_%s_highmass.root'%(cp.lower(), mass, coup)
            command = "python %s --era %s --train %d --iin %s "%(python_file, Era, 1, iin)
            shell_file = 'slim_mc_%s_%s.sh'%(iin,Era)
            print ("shell_file: ", shell_file)
            prepare_shell(shell_file, command, condor, FarmDir)
    
    #====================
    #Interference samples
    #====================
    if (args.method == 'slim_mc' or args.method == 'all') and args.sampletype == 'interference' :
      print ("=="*50)
      print ("Creating configuration for interference samples using slim_mc")
      python_file = "%s/slim_mc.py"%cwd

      print ("=="*50)
      
      coups=['rtc04','rtu04']
      
      A_masses = ['250','300','350','400','550','700']
      S_masses = ['200','250','300','350','500','650']
      for coup in coups:
          for index, mass in enumerate(A_masses):
            iin = 'ttc_a_%s_s_%s_%s.root'%(A_masses[index], S_masses[index], coup)
            command = "python %s --era %s --train %d --iin %s "%(python_file, Era, 1, iin)
            shell_file = 'slim_%s_%s.sh'%(iin,Era)
            prepare_shell(shell_file, command, condor, FarmDir)
      
    #====================
    # Data run
    #====================
    if (args.method == 'slim_data' or args.method == 'all') and args.sampletype == 'normal':
      print ("Creating configuration for slim_data")
      
      python_file = "%s/slim_data.py"%cwd

      for channel in ['DoubleElectron','DoubleMuon','ElectronMuon']:
        FileList = GetDataFile(Era,channel)
        print ("=="*50)
        print ("FileList: ", FileList)
        
        for iin in FileList:
          shell_file = 'slim_data_%s_%s_%s.sh'%(iin,Era,channel)
          command = "python %s --era %s --channel %s --iin %s"%(python_file, Era, channel, iin)
          prepare_shell(shell_file, command, condor, FarmDir)
  
    if (args.method == 'slim_fakelep_mc' or args.method == 'all') and args.sampletype == 'normal':
      print ("Creating configuration for slim_falelep_mc")
      
      python_file = "%s/slim_fakelep_mc.py"%cwd

      for channel in ['DoubleElectron','DoubleMuon','ElectronMuon']:

        Training_list = GetTrainingFile(Era, True)
        print ("=="*50)
        print ("Training_list: ", Training_list)

        for iin in Training_list:
          if "TTTo1L" in  iin: continue
          command = "python %s --era %s --train %d --iin %s --channel %s"%(python_file, Era, 1, iin, channel)
          shell_file = 'slim_fakelep_mc_%s_%s_%s.sh'%(iin, Era, channel)
          prepare_shell(shell_file, command, condor, FarmDir)

        nonTraining_list = GetTrainingFile(Era, False)
        print ("=="*50)
        print ("nonTraining_list: ", nonTraining_list)

        for iin in nonTraining_list:
          command = "python %s --era %s --train %d --iin %s --channel %s"%(python_file, Era, 0, iin, channel)
          shell_file = 'slim_fakelep_mc_%s_%s_%s.sh'%(iin,Era,channel)
          prepare_shell(shell_file, command, condor, FarmDir)

    if (args.method == 'slim_fakelep_data' or args.method=='all') and args.sampletype == 'normal':
      print ("Creating configuration for slim_fakelep_data")
      
      python_file = "%s/slim_fakelep_data.py"%cwd
      for channel in ['DoubleElectron','DoubleMuon','ElectronMuon']:
        DataList = GetDataFile(Era, channel)
        print ("=="*50)
        print ("DataList: ", DataList)
        
        for iin in DataList: 
          command  = "python %s --era %s --train %d --iin %s --channel %s"%(python_file, Era, 0, iin, channel)
          shell_file = 'slim_fakelep_data_%s_%s_%s.sh'%(iin, Era, channel)
          prepare_shell(shell_file, command, condor, FarmDir)
  
  condor.close()
  os.system('condor_submit %s/condor.sub'%FarmDir)

    
