import ROOT
import optparse
import os, sys
import json
from collections import OrderedDict


def GetNEvent(fin,nick):

  highmass  = False
  interfere = False
  standard  = False

  if ("highmass" in nick): 
    highmass = True
  elif (("a" in nick) and ("s" in nick)):
    interfere = True
  else:
    standard  = True

  d = OrderedDict()

  filein = ROOT.TFile.Open(fin)
  ttemp = filein.Get('Events')

  if standard:
      coup= nick[-5:]
      cp = 'A' if ('a' in nick) else 'S0'
      masses=['200','300','350','400','500','600','700']
      for mass in masses:
        flag='GenModel_T%sToTTQ_M%s_%s_TuneCP5_13TeV_G2HDM_%s_madgraphMLM_pythia8'%(cp,cp,mass,coup)
        key = nick + "_M" + cp + str(mass)
        d[key] = [ttemp.GetEntries(flag)]
    
  if highmass or interfere:
     d[nick] = [ttemp.GetEntries()]
 
  json_string = json.dumps(d)
  json_string = json_string.replace(",",",\n").replace("{","{\n ").replace("}","\n}")
  print(json_string)
  with open('nevents.json', 'w') as outfile:
    outfile.write(json_string)

if __name__ == "__main__":
  
  usage  = 'usage: %prog [options]'
  parser = optparse.OptionParser(usage)
  parser.add_option('-f', '--fin', dest='fin', help='',default='output.root',type='string')
  parser.add_option('-n', '--nick',dest='nick',help='nick',default='nick',type='string')
  (args,opt) = parser.parse_args()

  GetNEvent(args.fin, args.nick)

