import ROOT
import time
import os
import math
import optparse
from math import sqrt
from common import inputFile_path
from common import GetDataFile, GetTrigger_Data, GetMETFilter_Data


def Slim_module(filein,nin,mass_flag, channel,era):

  ROOT.gSystem.Load("libGenVector.so")
  TTC_header_path = os.path.join("script/slim_fake_%s.h"%era)
  ROOT.gInterpreter.Declare('#include "{}"'.format(TTC_header_path))

  
  path = str(inputFile_path[era])

  if channel == 'DoubleMuon':

    filters="ttc_jets && ttc_region==1 && ttc_l1_pt>30 && ttc_met>30 && ttc_mll>20 && ttc_drll>0.3 && nHad_tau==0 && ttc_2P0F"
    channel_name = 'mm'

  elif channel == 'DoubleElectron':

    filters="ttc_jets && ttc_region==3 && ttc_l1_pt>30 && ttc_met>30 && ttc_mll>20 && ttc_drll>0.3 && nHad_tau==0 && ttc_2P0F && (ttc_mll<60 || ttc_mll>120)"
    channel_name = 'ee'

  elif channel == 'ElectronMuon':

    filters="ttc_jets && ttc_region==2 && (ttc_l1_pt>30 || ttc_l2_pt>30) && ttc_met>30 && ttc_mll>20 && ttc_drll>0.3 && nHad_tau==0 && ttc_2P0F"
    channel_name = 'em'

  else:
    filters = ''
    channel_name = ''

  Trigger      = GetTrigger_Data(era, filein, channel)
  MET_filters  = GetMETFilter_Data(era)

  filters      = str("(" + filters + ")&&(" + MET_filters + ")")


  fileOut = filein.split('.')[0]+"_" + channel_name + ".root"
  fileOut = "sample/" + era + "/" + fileOut
  treeOut = "SlimTree"
  nevent=nin

  df_filein_tree_temp = ROOT.RDataFrame("Events",path+filein)
  df_filein_tree = df_filein_tree_temp.Range(int(nevent))

  df_filein = df_filein_tree.Filter(filters)
  dOut      = df_filein.Filter(str(Trigger))

  dOut = dOut.Define("j1_FlavB","Jet_btagDeepFlavB[tightJets_id_in24[0]]")\
             .Define("j1_FlavCvB","Jet_btagDeepFlavCvB[tightJets_id_in24[0]]")\
             .Define("j1_FlavCvL","Jet_btagDeepFlavCvL[tightJets_id_in24[0]]")\
             .Define("j2_FlavB","Jet_btagDeepFlavB[tightJets_id_in24[1]]")\
             .Define("j2_FlavCvB","Jet_btagDeepFlavCvB[tightJets_id_in24[1]]")\
             .Define("j2_FlavCvL","Jet_btagDeepFlavCvL[tightJets_id_in24[1]]")\
             .Define("j3_FlavB","Jet_btagDeepFlavB[tightJets_id_in24[2]]")\
             .Define("j3_FlavCvB","Jet_btagDeepFlavCvB[tightJets_id_in24[2]]")\
             .Define("j3_FlavCvL","Jet_btagDeepFlavCvL[tightJets_id_in24[2]]")\
             .Define("dr_j1j2","deltaR_jet(Jet_pt,Jet_eta,Jet_phi,Jet_mass,tightJets_id_in24,1)")\
             .Define("dr_j1j3","deltaR_jet(Jet_pt,Jet_eta,Jet_phi,Jet_mass,tightJets_id_in24,2)")\
             .Define("dr_j2j3","deltaR_jet(Jet_pt,Jet_eta,Jet_phi,Jet_mass,tightJets_id_in24,3)")\
             .Define("m_j1j2","mjj(Jet_pt,Jet_eta,Jet_phi,Jet_mass,tightJets_id_in24,1)")\
             .Define("m_j1j3","mjj(Jet_pt,Jet_eta,Jet_phi,Jet_mass,tightJets_id_in24,2)")\
             .Define("m_j2j3","mjj(Jet_pt,Jet_eta,Jet_phi,Jet_mass,tightJets_id_in24,3)")

  columns = ROOT.std.vector("string")()
  for c in ('ttc_region','HT','j1_pt','j1_eta','j1_phi','j1_mass','j2_pt','j2_eta','j2_phi','j2_mass','j3_pt','j3_eta','j3_phi','j3_mass','j1_FlavB','j1_FlavCvB','j1_FlavCvL','j2_FlavB','j2_FlavCvB','j2_FlavCvL','j3_FlavB','j3_FlavCvB','j3_FlavCvL','PV_npvsGood','PV_x','PV_y','PV_z','nSV','ttc_l1_pt','ttc_l1_eta','ttc_l1_phi','ttc_l1_mass','ttc_l2_pt','ttc_l2_eta','ttc_l2_phi','ttc_l2_mass','ttc_met','ttc_met_phi','ttc_mll','ttc_mllj1','ttc_mllj2','ttc_mllj3','dr_j1j2','dr_j1j3','dr_j2j3','m_j1j2','m_j1j3','m_j2j3'):
    columns.push_back(c)
  dOut.Snapshot(treeOut,fileOut,columns)


if __name__ == "__main__":
  start = time.time()
  start1 = time.clock()

  usage = 'usage: %prog [options]'
  parser = optparse.OptionParser(usage)
  parser.add_option('-e','--era', dest='era', help='era: [2016apv/2016postapv/2017/2018]', default='2018', type='string')
  parser.add_option('-c','--channel',dest='channel',help='[DoubleElectron/DoubleMuon/ElectronMuon]', default='DoubleElectron',type='string')
  parser.add_option('-i','--iin',dest='iin',help='input file', default=None, type='string')

  (args,opt) = parser.parse_args()

  era = args.era
  channel = args.channel
  iin = args.iin

  path = str(inputFile_path[era])

  print('Processing ',iin)
  ftemp=ROOT.TFile.Open(path+iin)
  ttemp=ftemp.Get('Events') 
  ntemp=ttemp.GetEntriesFast()
  Slim_module(iin,ntemp,'dummy',channel,era)
  ftemp.Close()

  end = time.time()
  end1 = time.clock()
  print "wall time:", end-start
  print "process time:", end1-start1
