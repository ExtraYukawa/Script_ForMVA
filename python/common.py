import json
import ROOT
import re
import os
from collections import OrderedDict

##################
##  Basic SetUp ##
##################

cmsswBase = os.environ['CMSSW_BASE']

inputFile_path = {
  '2016apv':     '/eos/cms/store/group/phys_top/ExtraYukawa/2016apvMerged/',
  '2016postapv': '/eos/cms/store/group/phys_top/ExtraYukawa/2016postapvMerged/',
  '2017':        '/eos/cms/store/group/phys_top/ExtraYukawa/TTC_version9/',
  '2018':        '/eos/cms/store/group/phys_top/ExtraYukawa/2018/'
}

# You need to change this directory to your own directory

store_place   = '/eos/user/t/tihsu/BDT/'
inputFile_path_skim = {
  '2016apv':     store_place + "ntuple_reindex/2016apv/",
  '2016postapv': store_place + "ntuple_reindex/2016postapv/",
  '2017':        store_place + "ntuple_reindex/2017/",
  '2018':        store_place + 'ntuple_reindex/2018/'
}

subera_list = {
  '2016apv':     ['B2','C','D','E','F'],
  '2016postapv': ['F','G','H'],
  '2017':        ['B','C','D','E','F'],
  '2018':        ['A','B','C','D_0','D_1']
}

channel_list = {
  '2016apv':     {'DoubleElectron': ['SingleEG','DoubleEG'],
                  'ElectronMuon':   ['MuonEG','SingleMuon','SingleEG'],
                  'DoubleMuon':     ['SingleMuon','DoubleMuon']
                 },
  '2016postapv': {'DoubleElectron': ['SingleEG','DoubleEG'],
                  'ElectronMuon':   ['MuonEG','SingleMuon','SingleEG'],
                  'DoubleMuon':     ['SingleMuon','DoubleMuon']
                 },
  '2017':        {'DoubleElectron': ['SingleEG','DoubleEG'],
                  'ElectronMuon':   ['MuonEG','SingleMuon','SingleEG'],
                  'DoubleMuon':     ['SingleMuon','DoubleMuon']
                 },
  '2018':        {'DoubleElectron': ['EGamma'],
                  'ElectronMuon':   ['MuonEG','SingleMuon','EGamma'],
                  'DoubleMuon':     ['SingleMuon','DoubleMuon']
                 } 
}

####################
## Basic Function ##
####################

def FindProcess(era, fin_name):

  subprocess = fin_name.replace('.root','')

  jsonfile = open(os.path.join(cmsswBase + '/src/Script_ForMVA/data/sample_' + str(era) + 'UL.json'))
  samples  = json.load(jsonfile, encoding='utf-8', object_pairs_hook=OrderedDict).items()
  jsonfile.close()
  process = None

  for sample, desc in samples:
    if subprocess == sample:
      process = desc[2]
  
  return process

def GetTrainingFile(era, isTrain): # -1: drop, 0: used not for training, 1: used for training
  jsonfile = open(os.path.join(cmsswBase + '/src/Script_ForMVA/data/sample_' + str(era) + 'UL.json'))
  samples  = json.load(jsonfile, encoding='utf-8', object_pairs_hook=OrderedDict).items()
  jsonfile.close()
  TrainingFile_List = []
  for process, desc in samples:
    if desc[4] == isTrain:
      TrainingFile_List.append(str((process + ".root")))
  print(TrainingFile_List)
  return TrainingFile_List

def GetDataFile(era, channel=None):

  if channel is None:
    jsonfile = open(os.path.join(cmsswBase + '/src/Script_ForMVA/data/sample_' + str(era) + 'UL.json'))
    samples  = json.load(jsonfile, encoding='utf-8', object_pairs_hook=OrderedDict).items()
    jsonfile.close()
    datafile_list = []
    for process, desc in samples:
      if desc[1] == 0:
        datafile_list.append(str((process + ".root")))  
  else:  
    suberas = subera_list[era]
    samples = channel_list[era][channel]

    middle = '_' if '2016' in era else ''

    datafile_list = []

    for sample in samples:
      for subera in suberas:
        datafile_list.append(str(sample + middle + subera + '.root'))  

  return datafile_list

def GetTrigger_MC(era):

  jsonfile = open(os.path.join(cmsswBase + '/src/Script_ForMVA/data/DiLeptonTriggers_%s.json'%era))
  trig_list = json.load(jsonfile, encoding='utf-8')
  jsonfile.close()

  jsonfile = open(os.path.join(cmsswBase + '/src/Script_ForMVA/data/Trigger_command_%s.json'%era))
  trig_command_list = json.load(jsonfile, encoding='utf-8',object_pairs_hook=OrderedDict)
  jsonfile.close()

  ee_trigger = trig_command_list['DoubleElectron']['MC']
  em_trigger = trig_command_list['ElectronMuon']['MC']
  mm_trigger = trig_command_list['DoubleMuon']['MC']

  all_trigger = "((" + ee_trigger + ")||(" + em_trigger + ")||(" + mm_trigger + "))"

  return str(all_trigger)

def GetTrigger_Data(era, fin_name, channel):

  jsonfile = open(os.path.join(cmsswBase + '/src/Script_ForMVA/data/DiLeptonTriggers_%s.json'%era))
  run_dict = json.load(jsonfile, encoding='utf-8')
  jsonfile.close()

  jsonfile = open(os.path.join(cmsswBase + '/src/Script_ForMVA/data/Trigger_command_%s.json'%era))
  trig_command_list = json.load(jsonfile, encoding='utf-8',object_pairs_hook=OrderedDict)
  jsonfile.close()

  sample_list = channel_list[era][channel]

  dataset = None
  subera  = fin_name.replace('.root','')

  for sample in sample_list:
    if sample in fin_name:
      subera = subera.replace(str(sample),'')
      dataset = sample
  if '2016' in era:
    subera = subera.replace('_','')

  print(subera)

  DiLepton_slc_run = dict()
  Run_List = run_dict["Data"][channel][subera]

  for Name in Run_List.keys():
    DiLepton_slc_run[Name] = ROOT.std.vector('int')()
    for i in Run_List[Name]:
       DiLepton_slc_run[Name].push_back(i)

  if "EGamma" in fin_name:
    if channel == "DoubleElectron":
      Trigger = "(" + str(trig_command_list[channel]["Data"][subera]["DoubleEG"]) + ")||(" + str(trig_command_list[channel]["Data"][subera]["SingleEG"]) + ")"
    else:
      Trigger = trig_command_list[channel]["Data"][subera]["SingleEG"]
  else:
    Trigger = trig_command_list[channel]["Data"][subera][dataset]

  p1 = re.compile(r'[{](.*?)[}]', re.S)
  variables = re.findall(p1,Trigger)
  var_list = []
  for var in variables:
     Trigger = Trigger.replace(var,"")
     runs = eval(var)
     runs = [str(run) for run in runs]
     runs = ','.join(runs)
     run_command = "{" + runs + "}"
     var_list.append(run_command)

  Trigger = Trigger.format(*var_list)  

  return str(Trigger)

def GetMETFilter_MC(era, fin_name):

  jsonfile = open(os.path.join(cmsswBase + '/src/Script_ForMVA/data/%s_MET_Filters.json'%era))
  MET_list = json.load(jsonfile, encoding='utf-8',object_pairs_hook=OrderedDict)
  jsonfile.close()

  process     = FindProcess(era, fin_name)
  subprocess  = fin_name.replace('.root','')

  ######################
  ## Dict reorganized ##
  ######################

  # Skim MET dictionary and make the whole code more flexible.
  MET_list_reorganized = dict()
  for Process in MET_list["MC"]:
    for Subprocess in MET_list["MC"][Process]:
      MET_list_reorganized[Subprocess] = MET_list["MC"][Process][Subprocess]

  if 'ttc' not in fin_name:
    MET_filters = MET_list_reorganized[subprocess]
  else:
    MET_filters = MET_list_reorganized["TTTo2L"]
  MET_filter  = " && ".join(MET_filters)

  return str(MET_filter)


def GetMETFilter_Data(era):

  jsonfile = open(os.path.join(cmsswBase + '/src/Script_ForMVA/data/%s_MET_Filters.json'%era))
  MET_list = json.load(jsonfile, encoding='utf-8',object_pairs_hook=OrderedDict)
  jsonfile.close()

  MET_filters = MET_list["Data"]
  MET_filter = " && ".join(MET_filters)

  return MET_filter

def DefinePrefireWeight(df_MC_tree, era):

  if era == '2018':
    df_MC_tree = df_MC_tree.Define("PrefireWeight", "1.0f");
    df_MC_tree = df_MC_tree.Define("PrefireWeight_Up", "1.0f");
    df_MC_tree = df_MC_tree.Define("PrefireWeight_Down", "1.0f");

  return df_MC_tree

def TransFileName(iin, isMC, era, channel,mass_flag='dummy'):


  # Function to transform ntuple file name to more handful one.

  # Normal MC
  fileIn = iin.split('.')[0]+".root"

  # Data
  if not isMC:
    if channel == 'DoubleMuon':
      channel_name = 'mm'
    elif channel == 'DoubleElectron':
      channel_name = 'ee'
    elif channel == 'ElectronMuon':
      channel_name = 'em'
    fileIn = iin.split('.')[0]+"_" + channel_name + ".root"

  if 'ttc_a' in iin or 'ttc_s0' in iin:
    # Interference Signal
    if "a" in iin.split('_') and "s" in iin.split('_'):
      pass
    # highmass Signal
    elif "highmass.root" in iin.split('_'):
      fileIn = iin.split('_')[0]+'_'+iin.split('_')[1]+'_'+iin.split('_')[3]+'_M'+iin.split('_')[1].upper()+iin.split('_')[2]+".root"
    # Normal Signal
    else:
      fileIn = iin.split('.')[0]+'_'+mass_flag.split('_')[2]+mass_flag.split('_')[3]+".root"

  return fileIn

