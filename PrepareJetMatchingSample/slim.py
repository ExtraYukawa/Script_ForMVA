import ROOT
import time
import os, sys
import math
import json
import optparse
from collections import OrderedDict
from math import sqrt
from common import inputFile_path, store_place
from common import GetTrigger_MC, GetMETFilter_MC, GetTrigger_Data, GetMETFilter_Data


ROOT.gSystem.Load("libGenVector.so")


def Slim_module(filein,era,mass_flag, isMC, channel):

  ROOT.gSystem.Load("libGenVector.so")
  TTC_header_path = os.path.join("script/slim_prepareJetMatch.h")
  ROOT.gInterpreter.Declare('#include "{}"'.format(TTC_header_path))


  path = str(inputFile_path[era])


  filters="(((ttc_region==1 || ttc_region==3) && ttc_l1_pt>30) || (ttc_region==2 && (ttc_l1_pt>30 || ttc_l2_pt>30))) && ttc_jets && ttc_met>30 && ttc_mll>20 && ttc_drll>0.3 && nHad_tau==0 && (ttc_2P0F || (ttc_1P1F || ttc_0P2F))"

  if isMC:
    Trigger      = GetTrigger_MC(era)
    MET_filters  = GetMETFilter_MC(era, filein)

  else:
    if channel == 'DoubleMuon':

      filters="ttc_jets && ttc_region==1 && ttc_l1_pt>30 && ttc_met>30 && ttc_mll>20 && ttc_drll>0.3 && nHad_tau==0 && (ttc_2P0F || (ttc_1P1F || ttc_0P2F))"
      channel_name = 'mm'

    elif channel == 'DoubleElectron':

      filters="ttc_jets && ttc_region==3 && ttc_l1_pt>30 && ttc_met>30 && ttc_mll>20 && ttc_drll>0.3 && nHad_tau==0 && (ttc_2P0F || (ttc_1P1F || ttc_0P2F)) && (ttc_mll<60 || ttc_mll>120)"
      channel_name = 'ee'

    elif channel == 'ElectronMuon':

      filters="ttc_jets && ttc_region==2 && (ttc_l1_pt>30 || ttc_l2_pt>30) && ttc_met>30 && ttc_mll>20 && ttc_drll>0.3 && nHad_tau==0 && (ttc_2P0F || (ttc_1P1F || ttc_0P2F))"
      channel_name = 'em'
  
    else:
      filters = ''
      channel_name = ''

    Trigger      = GetTrigger_Data(era, filein, channel)
    MET_filters  = GetMETFilter_Data(era)


  filters      = str("(" + filters + ") && (" + MET_filters + ")")

  print ("Final filters: ", filters)
  print ("mass_flag: ", mass_flag)
  print ("filein: ", filein)
  
  if isMC:
    fileOut = filein.split('.')[0]+".root"
  else:
    fileOut = filein.split('.')[0]+"_" + channel_name + ".root"

  skimstore_place = store_place + "ntuple_skim/"
  fileOut = skimstore_place + era + "/" + fileOut
  
  print ("Output file: ", fileOut)

  treeOut = "Events"

  if 'ttc_a' in filein or 'ttc_s0' in filein:
    
    if "a" in filein.split('_') and "s" in filein.split('_'):
      print ("Interference samples")
      df_filein_tree = ROOT.RDataFrame("Events",path+filein)
    elif "highmass.root" in filein.split('_'):
      print ("===> highmass samples <===")
      fileOut = filein.split('_')[0]+'_'+filein.split('_')[1]+'_'+filein.split('_')[3]+'_M'+filein.split('_')[1].upper()+filein.split('_')[2]+".root"
      fileOut = skimstore_place + era + "/" + fileOut
      print ("Output filename changed to: ", fileOut)
      df_filein_tree = ROOT.RDataFrame("Events",path+filein)
    else:
      print ("normal samples")
      fileOut = filein.split('.')[0]+'_'+mass_flag.split('_')[2]+mass_flag.split('_')[3]+".root"
      fileOut = skimstore_place + era + "/" + fileOut
      print ("Output filename changed to: ", fileOut)
      df_filein_tree_temp = ROOT.RDataFrame("Events",path+filein)
      df_filein_tree      = df_filein_tree_temp.Filter(mass_flag)
  else:
    df_filein_tree    = ROOT.RDataFrame("Events",path+filein)

  df_filein = df_filein_tree.Filter(filters)
  dOut = df_filein.Filter(str(Trigger))


  columns = ROOT.std.vector("string")()
  if isMC:
    for c in ('nJet','nMuon','nElectron','ttc_region','ttc_l1_id','ttc_l1_pdgid','ttc_l1_pt','ttc_l1_eta','ttc_l1_phi','ttc_l1_mass','ttc_l2_id','ttc_l2_pdgid','ttc_l2_pt','ttc_l2_eta','ttc_l2_phi','ttc_l2_mass','ttc_jets','ttc_met','ttc_met_phi','ttc_mll','ttc_drll','nHad_tau','ttc_2P0F','ttc_1P1F','ttc_0P2F','nGenDressedLepton','lhe_nlepton','PrefireWeight','PrefireWeight_Up','PrefireWeight_Down','genWeight','puWeight','puWeightUp','puWeightDown','Jet_btagDeepFlavB','Jet_btagDeepFlavCvB','Jet_btagDeepFlavCvL','MET_T1Smear_pt_jesTotalUp','MET_T1Smear_pt_jesTotalDown','MET_T1Smear_pt_jerUp','MET_T1Smear_pt_jerDown','MET_T1Smear_pt_unclustEnUp','MET_T1Smear_pt_unclustEnDown','MET_T1Smear_phi_jesTotalUp','MET_T1Smear_phi_jesTotalDown','MET_T1Smear_phi_jerUp','MET_T1Smear_phi_jerDown','MET_T1Smear_phi_unclustEnUp','MET_T1Smear_phi_unclustEnDown','Jet_pt','Jet_pt_jesTotalUp','Jet_pt_jesTotalDown','Jet_pt_jerUp','Jet_pt_jerDown','Jet_eta','Jet_phi','Jet_mass','Jet_mass_nom','Jet_mass_jesTotalUp','Jet_mass_jesTotalDown','Jet_mass_jerUp','Jet_mass_jerDown','Jet_puId','Jet_pt_nom','Jet_hadronFlavour','Muon_correctedUp_pt','Muon_correctedDown_pt','GenDressedLepton_eta','GenDressedLepton_phi','GenDressedLepton_pdgId','PV_npvsGood','PV_x','PV_y','PV_z','nSV','HT','n_tight_jet','tightJets_id_in24','ttc_lep1_faketag','muon_conePt','electron_conePt'):
      if not (era == '2018' and 'Prefire' in c):
        columns.push_back(c)
  else:
    for c in ('nJet','nMuon','nElectron','ttc_region','ttc_l1_id','ttc_l1_pdgid','ttc_l1_pt','ttc_l1_eta','ttc_l1_phi','ttc_l1_mass','ttc_l2_id','ttc_l2_pdgid','ttc_l2_pt','ttc_l2_eta','ttc_l2_phi','ttc_l2_mass','ttc_jets','ttc_met','ttc_met_phi','ttc_mll','ttc_drll','nHad_tau','ttc_2P0F','ttc_1P1F','ttc_0P2F','Jet_btagDeepFlavB','Jet_btagDeepFlavCvB','Jet_btagDeepFlavCvL','Jet_pt','Jet_eta','Jet_phi','Jet_mass','Jet_mass_nom','Jet_puId','Jet_pt_nom','Muon_correctedUp_pt','Muon_correctedDown_pt','PV_npvsGood','PV_x','PV_y','PV_z','nSV','HT','n_tight_jet','tightJets_id_in24','ttc_lep1_faketag','muon_conePt','electron_conePt'):
      columns.push_back(c)
  dOut.Snapshot(treeOut,fileOut,columns)

if __name__ == "__main__":
  start = time.time()
  start1 = time.clock()

  usage = 'usage: %prog [options]'
  parser = optparse.OptionParser(usage)
  parser.add_option('-e','--era', dest='era', help='era: [2016apv/2016postapv/2017/2018]', default='2018', type='string')
  parser.add_option('-i','--iin',   dest='iin',   help='input file name', default=None, type='string')
  parser.add_option('-f','--flag',  dest='flag',  help='flag',            default='dummy', type='string')
  parser.add_option('-t','--type',  dest='Type',  help='data/MC',         default='MC', type='string')
  parser.add_option('-c','--channel', dest='channel', help='[DoubleElectron/DoubleMuon/ElectronMuon]', default='DoubleElectron',type='string')

  (args,opt) = parser.parse_args()


  era = args.era
  iin = args.iin
  flag = args.flag
  isMC = (args.Type == "MC")
  channel = args.channel

  path = str(inputFile_path[era])

  print('Processing ',path+iin)
  Slim_module(iin,era,flag,isMC,channel)


  end = time.time()
  end1 = time.clock()
  print( "wall time:", end-start)
  print( "process time:", end1-start1)
