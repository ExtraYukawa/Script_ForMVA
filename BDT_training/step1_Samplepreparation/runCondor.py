import os
import sys
import optparse, argparse
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
    #shell.write('eval `scram r -sh`\n')
    shell.write('cd ${WORKDIR}\n')
    shell.write('source ../../script/env.sh\n')
    shell.write(command)
  condor.write('cfgFile=%s\n'%shell_file)
  condor.write('queue 1\n')

if __name__=='__main__':
  
  usage = 'usage: %prog [options]'
  parser = argparse.ArgumentParser(description=usage)
  parser.add_argument('-m', '--method', dest='method', help='[slim]',default='all', type=str)
  parser.add_argument('-e', '--era', dest='era', help='[all/2016apv/2016postapv/2017/2018]',default='all',type=str,choices=["all","2016apv","2016postapv","2017","2018"])
  parser.add_argument('-s', '--sampletype', dest='sampletype', help='[all/normal/interference/highmass]',default='normal',type=str, choices=["all","normal","interference","highmass"])
  parser.add_argument("--test", action="store_true")
  args = parser.parse_args()

  Eras_List = ['2016postapv','2016apv','2017','2018']
  Eras = []
  for Era in Eras_List:
    if args.era == 'all' or args.era == Era:
      Eras.append(Era)

  cwd = os.getcwd()
  dir_list = cwd.split('/')
  cmssw_list = []
  for dir_ in dir_list:
    cmssw_list.append(dir_)
    if 'CMSSW' in dir_: break
  cmsswBase = '/'.join(cmssw_list)
  FarmDir   = '%s/Farm_BDT'%cmsswBase
  cwd       = os.getcwd()
  os.system('mkdir -p %s'%FarmDir)
  os.system('cp %s/../../python/common.py .'%cwd)
  os.system('cp %s/../../python/DNN_application.py .'%cwd)
  os.system('cp %s/../../data/DNN_Flav_MET_threeJet_model_v2.* script/.'%cwd)
  from common import inputFile_path
  from common import GetTrainingFile, GetDataFile

  condor = open('%s/condor.sub'%FarmDir,'w')
  condor.write('output = %s/job_common.out\n'%FarmDir)
  condor.write('error  = %s/job_common.err\n'%FarmDir)
  condor.write('log    = %s/job_common.log\n'%FarmDir)
  condor.write('executable = %s/$(cfgFile)\n'%FarmDir)
  condor.write('requirements = (OpSysAndVer =?= "CentOS7")\n')
  condor.write('+JobFlavour = "longlunch"\n')
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

    if (args.method == 'slim' or args.method == 'all') and args.sampletype == 'normal':

      python_file = "%s/slim.py"%cwd

      # Training sample
      Training_list = GetTrainingFile(Era, True)
      for iin in Training_list:
        command = "python %s --era %s --train %d --iin %s"%(python_file, Era, 1, iin)
        shell_file = 'slim_%s_%s.sh'%(iin, Era)
        prepare_shell(shell_file, command, condor, FarmDir)

      # Signal sample
      coups=['rtc04','rtu04'] #gkole (21Sep2022) (as the training for highmass is done with rtc/u-04)
      cps=['A'] # No need for S0 as Efe shows the BDT shapes are same
      masses=['200','300','350','400','500','600','700']
      for cp in cps:
        for coup in coups:
          for mass in masses:
            iin = 'ttc_%s_%s.root'%(cp.lower(),coup)
            flag='GenModel_T%sToTTQ_M%s_%s_TuneCP5_13TeV_G2HDM_%s_madgraphMLM_pythia8'%(cp,cp,mass,coup)
            command = "python %s --era %s --train %d --iin %s --flag %s"%(python_file, Era, 1, iin, flag)
            shell_file = 'slim_%s_%s.sh'%(flag,Era)
            prepare_shell(shell_file, command, condor, FarmDir)

    # For interference samples
    if (args.method == 'slim' or args.method == 'all') and args.sampletype == 'interference':

      python_file = "%s/slim.py"%cwd

      #Signal sample
      print ("=="*50)
      print ("Preparing traing configuration for interference samples")
      coups=['rtc04','rtu04']
      cps=['A','S0']

      A_masses = ['250','300','350','400','550','700','800','900','1000']
      S_masses = ['200','250','300','350','500','650','750','850','950']
      for coup in coups:
          for index, mass in enumerate(A_masses):
            iin = 'ttc_a_%s_s_%s_%s.root'%(A_masses[index], S_masses[index], coup)
            # flag='GenModel_T%sToTTQ_M%s_%s_TuneCP5_13TeV_G2HDM_%s_madgraphMLM_pythia8'%(cp,cp,mass,coup)
            command = "python %s --era %s --train %d --iin %s "%(python_file, Era, 1, iin)
            shell_file = 'slim_%s_%s.sh'%(iin,Era)
            prepare_shell(shell_file, command, condor, FarmDir)

    # For highmass samples
    if (args.method == 'slim' or args.method == 'all') and args.sampletype == 'highmass':

      python_file = "%s/slim.py"%cwd

      #Signal sample
      print ("=="*50)
      print ("Preparing traing configuration for highmass samples")
      
      cps=['A']
      coups=['rtc04','rtu04']
      masses=['800','900','1000']
      
      for cp in cps:
        for coup in coups:
          for mass in masses:
            iin = 'ttc_%s_%s_%s_highmass.root'%(cp.lower(), mass, coup)
            command = "python %s --era %s --train %d --iin %s "%(python_file, Era, 1, iin)
            shell_file = 'slim_%s_%s.sh'%(iin,Era)
            print ("shell_file: ", shell_file)
            prepare_shell(shell_file, command, condor, FarmDir)

  condor.close()
  if not args.test:
    print ("Submitting Jobs on Condor")
    os.system('condor_submit %s/condor.sub'%FarmDir)

    
