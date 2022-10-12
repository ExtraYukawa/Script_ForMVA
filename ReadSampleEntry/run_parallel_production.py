import os
import sys
import optparse
import subprocess
import json
import parallel_utils
import ROOT
from collections import OrderedDict

if __name__ == '__main__':

  usage  = 'usage: %prog [options]'
  parser = optparse.OptionParser(usage)
  parser.add_option('-e', '--era', dest='era', help='[all/2016apv/2016postapv/2017/2018]',default='all',type='string')
  (args,opt) = parser.parse_args()

  cmsswBase = os.environ['CMSSW_BASE']

  Eras_List = ['2016postapv','2016apv','2017','2018']
  Eras = []

  os.system("mkdir -p data")
  os.system("mkdir -p Farm")
  for Era in Eras_List:
    if args.era == 'all' or args.era == Era:
      Eras.append(Era)

  for era in Eras:
    os.system("mkdir -p data/%s"%era)

    ###################
    ## Read DAS name ##
    ###################
  
    # read json file

    jsonfile = open(os.path.join(cmsswBase + '/src/Script_ForMVA/data/samples' + str(era) + '_signal.json'))
    samples  = json.load(jsonfile, encoding='utf-8', object_pairs_hook=OrderedDict).items()
    jsonfile.close()

    # json: [key] nick: [nick ,DAS name]

    command_list = []

    for sample, desc in samples:
      nick = desc[0]
      DAS  = desc[1]
      if(("highmass" in sample) or ('a' in sample and 's' in sample)): 
        continue
      os.system("python read_filelist_from_das.py --nick %s --query %s --era %s --outputfile Farm/%s_%s.sh"%(nick,DAS,era,nick,era))
      command_list.append("sh Farm/%s_%s.sh"%(nick,era)) 

  parallel_utils.submit_jobs(command_list, 8) # command_list, nParallel job
