import os
import sys
import optparse, argparse
import subprocess
import json
import ROOT
from collections import OrderedDict


def GetEntries(pathIn, iin):
  fin = ROOT.TFile(pathIn + "/" + iin, 'R')
  tree_name = 'Events'
  t = fin.Get(tree_name)
  nentries = t.GetEntries()
  return nentries


def CheckStatus(pathIn, iin, tag):
  fin = os.path.join(pathIn, iin.replace(".root", "_" + str(tag) + ".h5"))
  return (not (os.path.getsize(fin) == 0))


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
  parser = argparse.ArgumentParser(description=usage)
  parser.add_argument('-m', '--method', dest='method', help='[slim]',default='all', type=str)
  parser.add_argument('-e', '--era', dest='era', help='[all/2016apv/2016postapv/2017/2018]',default='all',type=str,choices=["all","2016apv","2016postapv","2017","2018"])
  parser.add_argument('-s', '--sampletype', dest='sampletype', help='[all/normal/interference/highmass]',default='normal',type=str, choices=["all","normal","interference","highmass"])
  parser.add_argument("--test", action="store_true")
  parser.add_argument("--resubmit", action="store_true")
  parser.add_argument("--step", dest='step', help='0:Generate ntuple, 1: run Combination, 2: run algorithm and mergeResult', default=0, type=int, choices=[0,1,2,3])
  args = parser.parse_args()

  Eras_List = ['2016postapv','2016apv','2017','2018']
  Eras = []
  for Era in Eras_List:
    if args.era == 'all' or args.era == Era:
      Eras.append(Era)


  cmsswBase = os.environ['CMSSW_BASE']
  FarmDir   = '%s/Farm_BDT'%cmsswBase
  cwd       = os.getcwd()
  os.system('mkdir -p %s'%FarmDir)
  os.system('cp %s/../python/common.py .'%cwd)
  batchsize = 5000

  from common import inputFile_path, store_place
  from common import GetTrainingFile, GetDataFile, TransFileName

  condor = open('%s/condor.sub'%FarmDir,'w')
  condor.write('output = %s/job_common.out\n'%FarmDir)
  condor.write('error  = %s/job_common.err\n'%FarmDir)
  condor.write('log    = %s/job_common.log\n'%FarmDir)
  condor.write('executable = %s/$(cfgFile)\n'%FarmDir)
  condor.write('requirements = (OpSysAndVer =?= "CentOS7")\n')
  condor.write('request_GPUs = 1\n')
  condor.write('+JobFlavour = "espresso"\n')

  cwd = os.getcwd()

  for Era in Eras:
  
    template = "%s/../script/slim.h"%cwd
    era_header = "script/slim_%s.h"%Era
    template_fake = "%s/../script/slim_fake.h"%cwd
    era_header_fake = "script/slim_fake_%s.h"%Era

    os.system('mkdir -p script')
    os.system('cat %s | sed "s/EraToBeReplaced/%s/g" > %s'%(template,Era,era_header))
    os.system('cat %s | sed "s/EraToBeReplaced/%s/g" > %s'%(template_fake,Era,era_header_fake))
    os.system('mkdir -p %s/ntuple_skim/%s'%(store_place,Era))
    os.system('mkdir -p %s/dataframe/%s'%(store_place,Era))
    os.system('mkdir -p %s/ntuple_reindex/%s'%(store_place,Era))
 
    path = inputFile_path[Era]

    if (args.method == 'slim' or args.method == 'all') and args.sampletype == 'normal':

      python_file = "%s/slim.py"%cwd

      # MC sample
      Training_list = GetTrainingFile(Era, True)
      nonTraining_list = GetTrainingFile(Era, False)
      Production_list = Training_list + nonTraining_list
      for iin in Production_list:
        if args.step == 0:
          command = "python %s --era %s --iin %s\n"%(python_file, Era, iin)
          shell_file = 'preslim_step0_%s_%s.sh'%(iin, Era)
          prepare_shell(shell_file, command, condor, FarmDir)

        elif args.step == 1:  
          nEntries = GetEntries(store_place + "/ntuple_skim/" + Era, TransFileName(iin, True, Era, None))
          for tag in range((nEntries//batchsize)+1):
            command =  "source ${WORKDIR}/env.sh\n"
            command += "python addEntry.py --era %s --iin %s --from %d --to %d --tag %d\n"%(Era, iin, batchsize*tag, min(batchsize*(tag+1),nEntries), tag)
            shell_file = 'preslim_step1_%s_%s_%d.sh'%(iin, Era, tag)
            if ((args.resubmit and not CheckStatus(store_place + "/dataframe/" + Era, TransFileName(iin, True, Era, None), tag)) or not args.resubmit):
               if args.resubmit:
                 print("Resubmit %s"%shell_file)
               prepare_shell(shell_file, command, condor, FarmDir)

        elif args.step == 2:
          command =  "source ${WORKDIR}/env.sh\n"
          command += "python MergeResult.py --era %s --iin %s\n"%(Era, iin)
          shell_file = 'preslim_step2_%s_%s.sh'%(iin, Era)
          prepare_shell(shell_file, command, condor, FarmDir)

        elif args.step == 3:
          command =  "source ${WORKDIR}/env.sh\n"
          command += "python ScanResult.py --era %s --iin %s\n"%(Era, iin)
          shell_file = 'preslim_step3_%s_%s.sh'%(iin, Era)
          prepare_shell(shell_file, command, condor, FarmDir)



      # data sample

      for channel in ['DoubleElectron','DoubleMuon','ElectronMuon']:
        FileList = GetDataFile(Era,channel)
        print ("=="*50)
        print ("FileList: ", FileList)

        for iin in FileList:
          if args.step == 0:
            shell_file = 'preslim_step0_data_%s_%s_%s.sh'%(iin,Era,channel)
            command = "python %s --era %s --channel %s --iin %s --type data\n"%(python_file, Era, channel, iin)
            prepare_shell(shell_file, command, condor, FarmDir)
          elif args.step == 1:  
            nEntries = GetEntries(store_place + "/ntuple_skim/" + Era, TransFileName(iin, False, Era, channel))
            for tag in range((nEntries//batchsize)+1):
              command =  "source ${WORKDIR}/env.sh\n"
              command += "python addEntry.py --era %s --iin %s --channel %s --type data --from %d --to %d --tag %d\n"%(Era, iin, channel, batchsize*tag, min(batchsize*(tag+1),nEntries), tag)
              shell_file = 'preslim_step1_data_%s_%s_%s_%d.sh'%(iin, Era, channel, tag)
              if ((args.resubmit and not CheckStatus(store_place + "/dataframe/" + Era, TransFileName(iin, False, Era, channel), tag)) or not args.resubmit):
                if args.resubmit:
                  print("Resubmit %s"%shell_file)
                prepare_shell(shell_file, command, condor, FarmDir)
          elif args.step == 2:
            shell_file = 'preslim_step2_data_%s_%s_%s.sh'%(iin,Era,channel)
            command =  "source ${WORKDIR}/env.sh\n"
            command += "python MergeResult.py --era %s --channel %s --iin %s --type data\n"%(Era, channel, iin)
            prepare_shell(shell_file, command, condor, FarmDir)
          elif args.step == 3:
            shell_file = 'preslim_step3_data_%s_%s_%s.sh'%(iin,Era,channel)
            command =  "source ${WORKDIR}/env.sh\n"
            command += "python ScanResult.py --era %s --channel %s --iin %s --type data\n"%(Era, channel, iin)
            prepare_shell(shell_file, command, condor, FarmDir)


      #Signal sample

      coups=['rtc04','rtu04'] #gkole (21Sep2022) (as the training for highmass is done with rtc/u-04)
      cps=['A'] # No need for S0 as Efe shows the BDT shapes are same
      masses=['200','300','350','400','500','600','700']
      for cp in cps:
        for coup in coups:
          for mass in masses:            
            iin = 'ttc_%s_%s.root'%(cp.lower(),coup)
            flag='GenModel_T%sToTTQ_M%s_%s_TuneCP5_13TeV_G2HDM_%s_madgraphMLM_pythia8'%(cp,cp,mass,coup)
            if args.step == 0:
              command = "python %s --era %s --iin %s --flag %s\n"%(python_file, Era, iin, flag)
              shell_file = 'preslim_step0_%s_%s.sh'%(flag,Era)
              prepare_shell(shell_file, command, condor, FarmDir)
            elif args.step == 1:
              nEntries = GetEntries(store_place + "/ntuple_skim/" + Era, TransFileName(iin, True, Era, None, flag))
              for tag in range((nEntries//batchsize)+1):
                command =  "source ${WORKDIR}/env.sh\n"
                command += "python addEntry.py --era %s --iin %s --flag %s --from %d --to %d --tag %d\n"%(Era, iin,flag, batchsize*tag, min(batchsize*(tag+1),nEntries), tag)
                shell_file = 'preslim_step1_%s_%s_%d.sh'%(flag, Era, tag)
                if ((args.resubmit and not CheckStatus(store_place + "/dataframe/" + Era, TransFileName(iin, True, Era, None,flag), tag)) or not args.resubmit):
                  if args.resubmit:
                    print("Resubmit %s"%shell_file)
                  prepare_shell(shell_file, command, condor, FarmDir)
            elif args.step == 2:
              command =  "source ${WORKDIR}/env.sh\n"
              command += "python MergeResult.py --era %s --iin %s --flag %s\n"%(Era, iin, flag)
              shell_file = 'preslim_step2_%s_%s.sh'%(flag,Era)
              prepare_shell(shell_file, command, condor, FarmDir)

            elif args.step == 3:
              command =  "source ${WORKDIR}/env.sh\n"
              command += "python ScanResult.py --era %s --iin %s --flag %s\n"%(Era, iin, flag)
              shell_file = 'preslim_step3_%s_%s.sh'%(flag,Era)
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
            if args.step == 0:
              command = "python %s --era %s --iin %s \n"%(python_file, Era, iin)
              shell_file = 'preslim_step0_%s_%s.sh'%(iin,Era)
              prepare_shell(shell_file, command, condor, FarmDir)
            elif args.step == 1:  
              nEntries = GetEntries(store_place + "/ntuple_skim/" + Era, TransFileName(iin, True, Era, None))
              for tag in range((nEntries//batchsize)+1):
                command =  "source ${WORKDIR}/env.sh\n"
                command += "python addEntry.py --era %s --iin %s --from %d --to %d --tag %d\n"%(Era, iin, batchsize*tag, min(batchsize*(tag+1),nEntries), tag)
                shell_file = 'preslim_step1_%s_%s_%d.sh'%(iin, Era, tag)
                if ((args.resubmit and not CheckStatus(store_place + "/dataframe/" + Era, TransFileName(iin, True, Era, None), tag)) or not args.resubmit):
                  if args.resubmit:
                    print("Resubmit %s"%shell_file)
                  prepare_shell(shell_file, command, condor, FarmDir)
            elif args.step == 2:
              command =  "source ${WORKDIR}/env.sh\n"
              command += "python MergeResult.py --era %s --iin %s\n"%(Era, iin)
              shell_file = 'preslim_step2_%s_%s.sh'%(iin,Era)
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
            if args.step == 0:
              command = "python %s --era %s --iin %s \n"%(python_file, Era, iin)
              shell_file = 'preslim_step0_%s_%s.sh'%(iin,Era)
              print ("shell_file: ", shell_file)
              prepare_shell(shell_file, command, condor, FarmDir)
            elif args.step == 1:  
              nEntries = GetEntries(store_place + "/ntuple_skim/" + Era, TransFileName(iin, True, Era, None))
              for tag in range((nEntries//batchsize)+1):
                command =  "source ${WORKDIR}/env.sh\n"
                command += "python addEntry.py --era %s --iin %s --from %d --to %d --tag %d\n"%(Era, iin, batchsize*tag, min(batchsize*(tag+1),nEntries), tag)
                shell_file = 'preslim_step1_%s_%s_%d.sh'%(iin, Era, tag)
                if ((args.resubmit and not CheckStatus(store_place + "/dataframe/" + Era, TransFileName(iin, True, Era, None), tag)) or not args.resubmit):
                  if args.resubmit:
                    print("Resubmit %s"%shell_file)
                  prepare_shell(shell_file, command, condor, FarmDir)
            elif args.step == 2:
              command =  "source ${WORKDIR}/env.sh\n"
              command += "python MergeResult.py --era %s --iin %s\n"%(Era, iin)
              shell_file = 'preslim_step2_%s_%s.sh'%(iin,Era)
              prepare_shell(shell_file, command, condor, FarmDir)



  condor.close()
  if not args.test:
    print ("Submitting Jobs on Condor")
    os.system('condor_submit %s/condor.sub'%FarmDir)

    
