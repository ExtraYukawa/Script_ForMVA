import ROOT
import time
import os, sys
import math
import json
import optparse
from collections import OrderedDict
from math import sqrt
from common import inputFile_path,inputFile_path_skim
from common import GetTrigger_MC, GetMETFilter_MC, TransFileName


ROOT.gSystem.Load("libGenVector.so")


def Slim_module(filein,nin,mass_flag,era):

  TTC_header_path = os.path.join("script/slim_"+era+".h")
  ROOT.gInterpreter.Declare('#include "{}"'.format(TTC_header_path))

  path = str(inputFile_path_skim[era])


  filters="(((ttc_region==1 || ttc_region==3) && ttc_l1_pt>30) || (ttc_region==2 && (ttc_l1_pt>30 || ttc_l2_pt>30))) && ttc_jets && ttc_met>30 && ttc_mll>20 && ttc_drll>0.3 && nHad_tau==0 && ttc_2P0F"

  filters      = str(filters)

  print ("Final filters: ", filters)
  print ("mass_flag: ", mass_flag)
  print ("filein: ", filein)
  fileOut = filein.split('.')[0]+".root"
  fileOut = "sample/" + era + "/" + fileOut
  
  print ("Output file: ", fileOut)

  treeOut = "SlimTree"
  nevent=nin
  if 'TTTo1L' in filein:
    nevent=2*nin

  if 'ttc_a' in filein or 'ttc_s0' in filein:
    
    if "a" in filein.split('_') and "s" in filein.split('_'):
      print ("===> Interference samples <===")
      df_filein_tree_temp = ROOT.RDataFrame("Events",path+filein)
      df_filein_tree = df_filein_tree_temp.Range(int(nevent))
    elif (("MA800" in filein) or ("MA900" in filein) or ("MA1000" in filein)):
      print ("===> highmass samples <===")
      df_filein_tree_temp = ROOT.RDataFrame("Events",path+filein)
      df_filein_tree = df_filein_tree_temp.Range(int(nevent))
    else:
      print ("===> normal samples <===")
      df_filein_tree_temp = ROOT.RDataFrame("Events",path+filein)
      df_filein_tree = df_filein_tree_temp.Range(int(nevent))
  else:
    df_filein_tree_temp = ROOT.RDataFrame("Events",path+filein)
    df_filein_tree = df_filein_tree_temp.Range(int(nevent))

  df_filein_tree = df_filein_tree.Define("genweight","puWeight*genWeight/abs(genWeight)")
  dOut = df_filein_tree.Filter(filters)
  dOut = dOut.Define("j1_pt",   "Jet_pt[JetMatched_idx[0]]")\
             .Define("j1_eta",  "Jet_eta[JetMatched_idx[0]]")\
             .Define("j1_phi",  "Jet_phi[JetMatched_idx[0]]")\
             .Define("j1_mass", "Jet_mass[JetMatched_idx[0]]")\
             .Define("j1_FlavB","Jet_btagDeepFlavB[JetMatched_idx[0]]")\
             .Define("j1_FlavCvB","Jet_btagDeepFlavCvB[JetMatched_idx[0]]")\
             .Define("j1_FlavCvL","Jet_btagDeepFlavCvL[JetMatched_idx[0]]")\
             .Define("j2_pt",   "Jet_pt[JetMatched_idx[1]]")\
             .Define("j2_eta",  "Jet_eta[JetMatched_idx[1]]")\
             .Define("j2_phi",  "Jet_phi[JetMatched_idx[1]]")\
             .Define("j2_mass", "Jet_mass[JetMatched_idx[1]]")\
             .Define("j2_FlavB","Jet_btagDeepFlavB[JetMatched_idx[1]]")\
             .Define("j2_FlavCvB","Jet_btagDeepFlavCvB[JetMatched_idx[1]]")\
             .Define("j2_FlavCvL","Jet_btagDeepFlavCvL[JetMatched_idx[1]]")\
             .Define("j3_pt",   "Jet_pt[JetMatched_idx[2]]")\
             .Define("j3_eta",  "Jet_eta[JetMatched_idx[2]]")\
             .Define("j3_phi",  "Jet_phi[JetMatched_idx[2]]")\
             .Define("j3_mass", "Jet_mass[JetMatched_idx[2]]")\
             .Define("j3_FlavB","Jet_btagDeepFlavB[JetMatched_idx[2]]")\
             .Define("j3_FlavCvB","Jet_btagDeepFlavCvB[JetMatched_idx[2]]")\
             .Define("j3_FlavCvL","Jet_btagDeepFlavCvL[JetMatched_idx[2]]")\
             .Define("ttc_l1_pt_muPtup", "muPtcorr(ttc_l1_pt, ttc_l1_id, ttc_l1_pdgid, Muon_correctedUp_pt)")\
             .Define("ttc_l1_pt_muPtdo", "muPtcorr(ttc_l1_pt, ttc_l1_id, ttc_l1_pdgid, Muon_correctedDown_pt)")\
             .Define("ttc_l2_pt_muPtup", "muPtcorr(ttc_l2_pt, ttc_l2_id, ttc_l2_pdgid, Muon_correctedUp_pt)")\
             .Define("ttc_l2_pt_muPtdo", "muPtcorr(ttc_l2_pt, ttc_l2_id, ttc_l2_pdgid, Muon_correctedDown_pt)")\
             .Define("ttc_met_jesup","MET_T1Smear_pt_jesTotalUp")\
             .Define("ttc_met_jesdo","MET_T1Smear_pt_jesTotalDown")\
             .Define("ttc_met_jerup","MET_T1Smear_pt_jerUp")\
             .Define("ttc_met_jerdo","MET_T1Smear_pt_jerDown")\
             .Define("ttc_met_unclusterEup","MET_T1Smear_pt_unclustEnUp")\
             .Define("ttc_met_unclusterEdo","MET_T1Smear_pt_unclustEnDown")\
             .Define("ttc_met_phi_jesup","MET_T1Smear_phi_jesTotalUp")\
             .Define("ttc_met_phi_jesdo","MET_T1Smear_phi_jesTotalDown")\
             .Define("ttc_met_phi_jerup","MET_T1Smear_phi_jerUp")\
             .Define("ttc_met_phi_jerdo","MET_T1Smear_phi_jerDown")\
             .Define("ttc_met_phi_unclusterEup","MET_T1Smear_phi_unclustEnUp")\
             .Define("ttc_met_phi_unclusterEdo","MET_T1Smear_phi_unclustEnDown")\
             .Define("dr_j1j2","deltaR_jet(Jet_pt,Jet_eta,Jet_phi,Jet_mass,JetMatched_idx,1)")\
             .Define("dr_j1j3","deltaR_jet(Jet_pt,Jet_eta,Jet_phi,Jet_mass,JetMatched_idx,2)")\
             .Define("dr_j2j3","deltaR_jet(Jet_pt,Jet_eta,Jet_phi,Jet_mass,JetMatched_idx,3)")\
             .Define("HT_jesup","HT_jesr(tightJets_id_in24, Jet_pt_jesTotalUp, Jet_pt_jesTotalDown, Jet_pt_jerUp, Jet_pt_jerDown, 0, nJet)")\
             .Define("HT_jesdo","HT_jesr(tightJets_id_in24, Jet_pt_jesTotalUp, Jet_pt_jesTotalDown, Jet_pt_jerUp, Jet_pt_jerDown, 1, nJet)")\
             .Define("HT_jerup","HT_jesr(tightJets_id_in24, Jet_pt_jesTotalUp, Jet_pt_jesTotalDown, Jet_pt_jerUp, Jet_pt_jerDown, 2, nJet)")\
             .Define("HT_jerdo","HT_jesr(tightJets_id_in24, Jet_pt_jesTotalUp, Jet_pt_jesTotalDown, Jet_pt_jerUp, Jet_pt_jerDown, 3, nJet)")\
             .Define("ttc_mllj1","mllj_jesr(ttc_l1_pt,ttc_l1_eta,ttc_l1_phi,ttc_l1_mass,ttc_l2_pt,ttc_l2_eta,ttc_l2_phi,ttc_l2_mass,Jet_pt_nom,Jet_eta,Jet_phi,Jet_mass_nom,JetMatched_idx,1)")\
             .Define("ttc_mllj2","mllj_jesr(ttc_l1_pt,ttc_l1_eta,ttc_l1_phi,ttc_l1_mass,ttc_l2_pt,ttc_l2_eta,ttc_l2_phi,ttc_l2_mass,Jet_pt_nom,Jet_eta,Jet_phi,Jet_mass_nom,JetMatched_idx,2)")\
             .Define("ttc_mllj3","mllj_jesr(ttc_l1_pt,ttc_l1_eta,ttc_l1_phi,ttc_l1_mass,ttc_l2_pt,ttc_l2_eta,ttc_l2_phi,ttc_l2_mass,Jet_pt_nom,Jet_eta,Jet_phi,Jet_mass_nom,JetMatched_idx,3)")\
             .Define("ttc_mllj1_jesup","mllj_jesr(ttc_l1_pt,ttc_l1_eta,ttc_l1_phi,ttc_l1_mass,ttc_l2_pt,ttc_l2_eta,ttc_l2_phi,ttc_l2_mass,Jet_pt_jesTotalUp,Jet_eta,Jet_phi,Jet_mass_jesTotalUp,JetMatched_idx,1)")\
             .Define("ttc_mllj2_jesup","mllj_jesr(ttc_l1_pt,ttc_l1_eta,ttc_l1_phi,ttc_l1_mass,ttc_l2_pt,ttc_l2_eta,ttc_l2_phi,ttc_l2_mass,Jet_pt_jesTotalUp,Jet_eta,Jet_phi,Jet_mass_jesTotalUp,JetMatched_idx,2)")\
             .Define("ttc_mllj3_jesup","mllj_jesr(ttc_l1_pt,ttc_l1_eta,ttc_l1_phi,ttc_l1_mass,ttc_l2_pt,ttc_l2_eta,ttc_l2_phi,ttc_l2_mass,Jet_pt_jesTotalUp,Jet_eta,Jet_phi,Jet_mass_jesTotalUp,JetMatched_idx,3)")\
             .Define("ttc_mllj1_jesdo","mllj_jesr(ttc_l1_pt,ttc_l1_eta,ttc_l1_phi,ttc_l1_mass,ttc_l2_pt,ttc_l2_eta,ttc_l2_phi,ttc_l2_mass,Jet_pt_jesTotalDown,Jet_eta,Jet_phi,Jet_mass_jesTotalDown,JetMatched_idx,1)")\
             .Define("ttc_mllj2_jesdo","mllj_jesr(ttc_l1_pt,ttc_l1_eta,ttc_l1_phi,ttc_l1_mass,ttc_l2_pt,ttc_l2_eta,ttc_l2_phi,ttc_l2_mass,Jet_pt_jesTotalDown,Jet_eta,Jet_phi,Jet_mass_jesTotalDown,JetMatched_idx,2)")\
             .Define("ttc_mllj3_jesdo","mllj_jesr(ttc_l1_pt,ttc_l1_eta,ttc_l1_phi,ttc_l1_mass,ttc_l2_pt,ttc_l2_eta,ttc_l2_phi,ttc_l2_mass,Jet_pt_jesTotalDown,Jet_eta,Jet_phi,Jet_mass_jesTotalDown,JetMatched_idx,3)")\
             .Define("ttc_mllj1_jerup","mllj_jesr(ttc_l1_pt,ttc_l1_eta,ttc_l1_phi,ttc_l1_mass,ttc_l2_pt,ttc_l2_eta,ttc_l2_phi,ttc_l2_mass,Jet_pt_jerUp,Jet_eta,Jet_phi,Jet_mass_jerUp,JetMatched_idx,1)")\
             .Define("ttc_mllj2_jerup","mllj_jesr(ttc_l1_pt,ttc_l1_eta,ttc_l1_phi,ttc_l1_mass,ttc_l2_pt,ttc_l2_eta,ttc_l2_phi,ttc_l2_mass,Jet_pt_jerUp,Jet_eta,Jet_phi,Jet_mass_jerUp,JetMatched_idx,2)")\
             .Define("ttc_mllj3_jerup","mllj_jesr(ttc_l1_pt,ttc_l1_eta,ttc_l1_phi,ttc_l1_mass,ttc_l2_pt,ttc_l2_eta,ttc_l2_phi,ttc_l2_mass,Jet_pt_jerUp,Jet_eta,Jet_phi,Jet_mass_jerUp,JetMatched_idx,3)")\
             .Define("ttc_mllj1_jerdo","mllj_jesr(ttc_l1_pt,ttc_l1_eta,ttc_l1_phi,ttc_l1_mass,ttc_l2_pt,ttc_l2_eta,ttc_l2_phi,ttc_l2_mass,Jet_pt_jerDown,Jet_eta,Jet_phi,Jet_mass_jerDown,JetMatched_idx,1)")\
             .Define("ttc_mllj2_jerdo","mllj_jesr(ttc_l1_pt,ttc_l1_eta,ttc_l1_phi,ttc_l1_mass,ttc_l2_pt,ttc_l2_eta,ttc_l2_phi,ttc_l2_mass,Jet_pt_jerDown,Jet_eta,Jet_phi,Jet_mass_jerDown,JetMatched_idx,2)")\
             .Define("ttc_mllj3_jerdo","mllj_jesr(ttc_l1_pt,ttc_l1_eta,ttc_l1_phi,ttc_l1_mass,ttc_l2_pt,ttc_l2_eta,ttc_l2_phi,ttc_l2_mass,Jet_pt_jerDown,Jet_eta,Jet_phi,Jet_mass_jerDown,JetMatched_idx,3)")\
             .Define("ttc_mllj1_muPtup","mllj_jesr(ttc_l1_pt_muPtup,ttc_l1_eta,ttc_l1_phi,ttc_l1_mass,ttc_l2_pt_muPtup,ttc_l2_eta,ttc_l2_phi,ttc_l2_mass,Jet_pt_nom,Jet_eta,Jet_phi,Jet_mass_nom,JetMatched_idx,1)")\
             .Define("ttc_mllj2_muPtup","mllj_jesr(ttc_l1_pt_muPtup,ttc_l1_eta,ttc_l1_phi,ttc_l1_mass,ttc_l2_pt_muPtup,ttc_l2_eta,ttc_l2_phi,ttc_l2_mass,Jet_pt_nom,Jet_eta,Jet_phi,Jet_mass_nom,JetMatched_idx,2)")\
             .Define("ttc_mllj3_muPtup","mllj_jesr(ttc_l1_pt_muPtup,ttc_l1_eta,ttc_l1_phi,ttc_l1_mass,ttc_l2_pt_muPtup,ttc_l2_eta,ttc_l2_phi,ttc_l2_mass,Jet_pt_nom,Jet_eta,Jet_phi,Jet_mass_nom,JetMatched_idx,3)")\
             .Define("ttc_mllj1_muPtdo","mllj_jesr(ttc_l1_pt_muPtdo,ttc_l1_eta,ttc_l1_phi,ttc_l1_mass,ttc_l2_pt_muPtdo,ttc_l2_eta,ttc_l2_phi,ttc_l2_mass,Jet_pt_nom,Jet_eta,Jet_phi,Jet_mass_nom,JetMatched_idx,1)")\
             .Define("ttc_mllj2_muPtdo","mllj_jesr(ttc_l1_pt_muPtdo,ttc_l1_eta,ttc_l1_phi,ttc_l1_mass,ttc_l2_pt_muPtdo,ttc_l2_eta,ttc_l2_phi,ttc_l2_mass,Jet_pt_nom,Jet_eta,Jet_phi,Jet_mass_nom,JetMatched_idx,2)")\
             .Define("ttc_mllj3_muPtdo","mllj_jesr(ttc_l1_pt_muPtdo,ttc_l1_eta,ttc_l1_phi,ttc_l1_mass,ttc_l2_pt_muPtdo,ttc_l2_eta,ttc_l2_phi,ttc_l2_mass,Jet_pt_nom,Jet_eta,Jet_phi,Jet_mass_nom,JetMatched_idx,3)")\
             .Define("ttc_mll_muPtup","mll(ttc_l1_pt_muPtup,ttc_l1_eta,ttc_l1_phi,ttc_l1_mass,ttc_l2_pt_muPtup,ttc_l2_eta,ttc_l2_phi,ttc_l2_mass)")\
             .Define("ttc_mll_muPtdo","mll(ttc_l1_pt_muPtdo,ttc_l1_eta,ttc_l1_phi,ttc_l1_mass,ttc_l2_pt_muPtdo,ttc_l2_eta,ttc_l2_phi,ttc_l2_mass)")\
             .Define("mjj", "mll(j1_pt,j1_eta,j1_phi,j1_mass,j2_pt,j2_eta,j2_phi,j2_mass)")



  columns = ROOT.std.vector("string")()
  for c in ('ttc_region','genweight','HT','j1_pt','j1_eta','j1_phi','j1_mass','j2_pt','j2_eta','j2_phi','j2_mass','j3_pt','j3_eta','j3_phi','j3_mass','j1_FlavB','j1_FlavCvB','j1_FlavCvL','j2_FlavB','j2_FlavCvB','j2_FlavCvL','j3_FlavB','j3_FlavCvB','j3_FlavCvL','PV_npvsGood','PV_x','PV_y','PV_z','nSV','ttc_l1_pt','ttc_l1_pt_muPtup','ttc_l1_pt_muPtdo','ttc_l1_eta','ttc_l1_phi','ttc_l1_mass','ttc_l2_pt','ttc_l2_pt_muPtup','ttc_l2_pt_muPtdo','ttc_l2_eta','ttc_l2_phi','ttc_l2_mass','ttc_met','ttc_met_phi','ttc_mll','ttc_mllj1','ttc_mllj2','ttc_mllj3','puWeight','puWeightUp','puWeightDown','ttc_met_jesup','ttc_met_jesdo','ttc_met_jerup','ttc_met_jerdo','ttc_met_unclusterEup','ttc_met_unclusterEdo','ttc_met_phi_jesup','ttc_met_phi_jesdo','ttc_met_phi_jerup','ttc_met_phi_jerdo','ttc_met_phi_unclusterEup','ttc_met_phi_unclusterEdo','dr_j1j2','dr_j1j3','dr_j2j3','HT_jesup','HT_jesdo','HT_jerup','HT_jerdo','ttc_mllj1_jesup','ttc_mllj1_jesdo','ttc_mllj1_jerup','ttc_mllj1_jerdo','ttc_mllj2_jesup','ttc_mllj2_jesdo','ttc_mllj2_jerup','ttc_mllj2_jerdo','ttc_mllj3_jesup','ttc_mllj3_jesdo','ttc_mllj3_jerup','ttc_mllj3_jerdo','ttc_mllj1_muPtup','ttc_mllj2_muPtup','ttc_mllj3_muPtup','ttc_mllj1_muPtdo','ttc_mllj2_muPtdo','ttc_mllj3_muPtdo','ttc_mll_muPtup','ttc_mll_muPtdo','mjj'):
    columns.push_back(c)
  dOut.Snapshot(treeOut,fileOut,columns)

if __name__ == "__main__":
  start = time.time()
  start1 = time.clock()

  usage = 'usage: %prog [options]'
  parser = optparse.OptionParser(usage)
  parser.add_option('-e','--era', dest='era', help='era: [2016apv/2016postapv/2017/2018]', default='2018', type='string')
  parser.add_option('-t','--train', dest='train', help='file used for training or not', default=1, type=int)
  parser.add_option('-i','--iin',   dest='iin',   help='input file name', default=None, type='string')
  parser.add_option('-f','--flag',  dest='flag',  help='flag',            default='dummy', type='string')

  (args,opt) = parser.parse_args()


  era = args.era
  istrain = args.train
  iin = args.iin
  flag = args.flag

  path = str(inputFile_path_skim[era])

  iin  = TransFileName(iin, True, era, None, flag)

  print('Processing ',path+iin)
  ftemp=ROOT.TFile.Open(path+iin, 'READ')
  ttemp=ftemp.Get('Events')
  ntemp=ttemp.GetEntriesFast()
  # Samples used for BDT training only leaves half of the events in the application while others use full events
  ntrain = ntemp*0.5 if istrain else ntemp
  Slim_module(iin,ntrain,flag,era)
  ftemp.Close()


  end = time.time()
  end1 = time.clock()
  print( "wall time:", end-start)
  print( "process time:", end1-start1)
