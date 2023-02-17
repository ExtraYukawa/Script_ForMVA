import ROOT
import time
import os,sys
import math
import json
import optparse
from collections import OrderedDict
from math import sqrt
from common import inputFile_path, inputFile_path_skim
from common import GetTrainingFile, GetTrigger_MC, GetMETFilter_MC, DefinePrefireWeight, TransFileName


def Slim_module(filein,nin,mass_flag, use_fortraining, era):

  ROOT.gSystem.Load("libGenVector.so")
  TTC_header_path = os.path.join("script/slim_"+era+".h")
  ROOT.gInterpreter.Declare('#include "{}"'.format(TTC_header_path))


  path = str(inputFile_path_skim[era])

  if 'ttc_a' in filein or 'ttc_s0' in filein:
    filters      = "(((ttc_region==1 || ttc_region==3) && ttc_l1_pt>30) || (ttc_region==2 && (ttc_l1_pt>30 || ttc_l2_pt>30))) && ttc_jets && ttc_met > 30 && ttc_mll > 20 && ttc_drll > 0.3 && nHad_tau==0 && ttc_2P0F" # lhe_nlepton is 0 in randomized scan samples
  else:
    filters      = "(((ttc_region==1 || ttc_region==3) && ttc_l1_pt>30) || (ttc_region==2 && (ttc_l1_pt>30 || ttc_l2_pt>30))) && ttc_jets && ttc_met > 30 && ttc_mll > 20 && ttc_drll > 0.3 && (nGenDressedLepton > 1 || lhe_nlepton > 1) && nHad_tau==0 && ttc_2P0F"

  # Print filters
  print ("filters: ", filters)

  filters      = str("(" + filters + ")")

  # flag for TTto2L and DY for chargeflip SF
  if 'TTTo2L' in filein or 'DY' in filein:
    OS_flag=1
  else:
    OS_flag=0

  fileOut = filein.split('.')[0]+".root"
  fileOut = "sample/" + era + "/" + fileOut

  treeOut = "SlimTree"
  nevent  = nin
  if 'TTTo1L' in filein:
    nevent=2*nin

  if 'ttc_a' in filein or 'ttc_s0' in filein:
    if "a" in filein.split('_') and "s" in filein.split('_'):
      print ("Interference samples all events for evaluation")
      df_filein_tree_temp = ROOT.RDataFrame("Events",path+filein)
      df_filein_tree = df_filein_tree_temp.Range(int(nevent), 0)
    elif (("MA800" in filein) or ("MA900" in filein) or ("MA1000" in filein)):
      print ("===> highmass samples <===")
      df_filein_tree_temp = ROOT.RDataFrame("Events",path+filein)
      df_filein_tree = df_filein_tree_temp.Range(int(nevent), 0)
    else:
      print ("normal samples")
      df_filein_tree_temp = ROOT.RDataFrame("Events",path+filein)
      print(mass_flag)
      df_filein_tree = df_filein_tree_temp.Range(int(nevent),0)
  elif 'TTTo1L' in filein:
    df_filein_tree_temp = ROOT.RDataFrame("Events",path+filein)
    df_filein_tree = df_filein_tree_temp.Range(int(nevent))
  elif use_fortraining:
    df_filein_tree_temp = ROOT.RDataFrame("Events",path+filein)
    print(df_filein_tree_temp,path+filein)
    df_filein_tree = df_filein_tree_temp.Range(int(nevent),0)
  else:
    df_filein_tree_temp = ROOT.RDataFrame("Events",path+filein)
    df_filein_tree = df_filein_tree_temp.Range(int(nevent))

  df_filein_tree = DefinePrefireWeight(df_filein_tree, era)

  df_filein_tree = df_filein_tree.Define("genweight","PrefireWeight*puWeight*genWeight/abs(genWeight)")
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
             .Define("ttc_l1_pt_muPtup", "muPtcorr(ttc_l1_pt, ttc_l1_id, ttc_l1_pdgid, Muon_correctedUp_pt)")\
             .Define("ttc_l1_pt_muPtdo", "muPtcorr(ttc_l1_pt, ttc_l1_id, ttc_l1_pdgid, Muon_correctedDown_pt)")\
             .Define("ttc_l2_pt_muPtup", "muPtcorr(ttc_l2_pt, ttc_l2_id, ttc_l2_pdgid, Muon_correctedUp_pt)")\
             .Define("ttc_l2_pt_muPtdo", "muPtcorr(ttc_l2_pt, ttc_l2_id, ttc_l2_pdgid, Muon_correctedDown_pt)")\
             .Define("ttc_mllj1_muPtup","mllj_jesr(ttc_l1_pt_muPtup,ttc_l1_eta,ttc_l1_phi,ttc_l1_mass,ttc_l2_pt_muPtup,ttc_l2_eta,ttc_l2_phi,ttc_l2_mass,Jet_pt_nom,Jet_eta,Jet_phi,Jet_mass_nom,JetMatched_idx,1)")\
             .Define("ttc_mllj2_muPtup","mllj_jesr(ttc_l1_pt_muPtup,ttc_l1_eta,ttc_l1_phi,ttc_l1_mass,ttc_l2_pt_muPtup,ttc_l2_eta,ttc_l2_phi,ttc_l2_mass,Jet_pt_nom,Jet_eta,Jet_phi,Jet_mass_nom,JetMatched_idx,2)")\
             .Define("ttc_mllj3_muPtup","mllj_jesr(ttc_l1_pt_muPtup,ttc_l1_eta,ttc_l1_phi,ttc_l1_mass,ttc_l2_pt_muPtup,ttc_l2_eta,ttc_l2_phi,ttc_l2_mass,Jet_pt_nom,Jet_eta,Jet_phi,Jet_mass_nom,JetMatched_idx,3)")\
             .Define("ttc_mllj1_muPtdo","mllj_jesr(ttc_l1_pt_muPtdo,ttc_l1_eta,ttc_l1_phi,ttc_l1_mass,ttc_l2_pt_muPtdo,ttc_l2_eta,ttc_l2_phi,ttc_l2_mass,Jet_pt_nom,Jet_eta,Jet_phi,Jet_mass_nom,JetMatched_idx,1)")\
             .Define("ttc_mllj2_muPtdo","mllj_jesr(ttc_l1_pt_muPtdo,ttc_l1_eta,ttc_l1_phi,ttc_l1_mass,ttc_l2_pt_muPtdo,ttc_l2_eta,ttc_l2_phi,ttc_l2_mass,Jet_pt_nom,Jet_eta,Jet_phi,Jet_mass_nom,JetMatched_idx,2)")\
             .Define("ttc_mllj3_muPtdo","mllj_jesr(ttc_l1_pt_muPtdo,ttc_l1_eta,ttc_l1_phi,ttc_l1_mass,ttc_l2_pt_muPtdo,ttc_l2_eta,ttc_l2_phi,ttc_l2_mass,Jet_pt_nom,Jet_eta,Jet_phi,Jet_mass_nom,JetMatched_idx,3)")\
             .Define("ttc_mll_muPtup","mll(ttc_l1_pt_muPtup,ttc_l1_eta,ttc_l1_phi,ttc_l1_mass,ttc_l2_pt_muPtup,ttc_l2_eta,ttc_l2_phi,ttc_l2_mass)")\
             .Define("ttc_mll_muPtdo","mll(ttc_l1_pt_muPtdo,ttc_l1_eta,ttc_l1_phi,ttc_l1_mass,ttc_l2_pt_muPtdo,ttc_l2_eta,ttc_l2_phi,ttc_l2_mass)")\
             .Define("mu_id","muid(ttc_l1_pt,ttc_l1_eta,ttc_l2_pt,ttc_l2_eta,ttc_region)")\
             .Define("mu_id_sysup","muid_sysup(ttc_l1_pt,ttc_l1_eta,ttc_l2_pt,ttc_l2_eta,ttc_region)")\
             .Define("mu_id_sysdo","muid_sysdo(ttc_l1_pt,ttc_l1_eta,ttc_l2_pt,ttc_l2_eta,ttc_region)")\
             .Define("mu_id_statup","muid_statup(ttc_l1_pt,ttc_l1_eta,ttc_l2_pt,ttc_l2_eta,ttc_region)")\
             .Define("mu_id_statdo","muid_statdo(ttc_l1_pt,ttc_l1_eta,ttc_l2_pt,ttc_l2_eta,ttc_region)")\
             .Define("ele_id","eleid(ttc_l1_pt,ttc_l1_eta,ttc_l2_pt,ttc_l2_eta,ttc_region)")\
             .Define("ele_id_sysup","eleid_sysup(ttc_l1_pt,ttc_l1_eta,ttc_l2_pt,ttc_l2_eta,ttc_region)")\
             .Define("ele_id_sysdo","eleid_sysdo(ttc_l1_pt,ttc_l1_eta,ttc_l2_pt,ttc_l2_eta,ttc_region)")\
             .Define("ele_id_statup","eleid_statup(ttc_l1_pt,ttc_l1_eta,ttc_l2_pt,ttc_l2_eta,ttc_region)")\
             .Define("ele_id_statdo","eleid_statdo(ttc_l1_pt,ttc_l1_eta,ttc_l2_pt,ttc_l2_eta,ttc_region)")\
             .Define("trig_SF","lep_trigger(ttc_l1_pt,ttc_l2_pt,ttc_region)")\
             .Define("trig_SFup","lep_triggerup(ttc_l1_pt,ttc_l2_pt,ttc_region)")\
             .Define("trig_SFdo","lep_triggerdown(ttc_l1_pt,ttc_l2_pt,ttc_region)")\
             .Define("ctag_SF","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,0)")\
             .Define("ctag_SF_statup","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,1)")\
             .Define("ctag_SF_statdo","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,2)")\
             .Define("ctag_SF_Extrapup","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,3)")\
             .Define("ctag_SF_Extrapdo","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,4)")\
             .Define("ctag_SF_LHEScaleWeightmuFup","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,5)")\
             .Define("ctag_SF_LHEScaleWeightmuFdo","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,6)")\
             .Define("ctag_SF_LHEScaleWeightmuRup","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,7)")\
             .Define("ctag_SF_LHEScaleWeightmuRdo","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,8)")\
             .Define("ctag_SF_Interpup","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,9)")\
             .Define("ctag_SF_Interpdo","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,10)")\
             .Define("ctag_SF_PSWeightFSRup","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,11)")\
             .Define("ctag_SF_PSWeightFSRdo","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,12)")\
             .Define("ctag_SF_PSWeightISRup","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,13)")\
             .Define("ctag_SF_PSWeightISRdo","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,14)")\
             .Define("ctag_SF_PUWeightup","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,15)")\
             .Define("ctag_SF_PUWeightdo","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,16)")\
             .Define("ctag_SF_XSec_BRUnc_DYJets_bup","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,17)")\
             .Define("ctag_SF_XSec_BRUnc_DYJets_bdo","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,18)")\
             .Define("ctag_SF_XSec_BRUnc_DYJets_cup","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,19)")\
             .Define("ctag_SF_XSec_BRUnc_DYJets_cdo","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,20)")\
             .Define("ctag_SF_XSec_BRUnc_WJets_cup","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,21)")\
             .Define("ctag_SF_XSec_BRUnc_WJets_cdo","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,22)")\
             .Define("ctag_SF_jerup","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,23)")\
             .Define("ctag_SF_jerdo","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,24)")\
             .Define("ctag_SF_jesTotalup","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,25)")\
             .Define("ctag_SF_jesTotaldo","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,26)")\
             .Define("sig_pdfup","signal_pdf(ttc_l1_pt,0)")\
             .Define("sig_pdfdo","signal_pdf(ttc_l1_pt,1)")\
             .Define("sig_scaleup","signal_scale(ttc_l1_pt,0)")\
             .Define("sig_scaledo","signal_scale(ttc_l1_pt,1)")\
             .Define("sig_psup","signal_ps(ttc_l1_pt,0)")\
             .Define("sig_psdo","signal_ps(ttc_l1_pt,1)")

  if OS_flag==1:
    dOut = dOut.Define("charFlip_SF","chargeflip_SF(1,ttc_l1_pt,ttc_l1_eta,ttc_l1_phi,ttc_l2_pt,ttc_l2_eta,ttc_l2_phi,ttc_region,0, GenDressedLepton_eta, GenDressedLepton_phi, GenDressedLepton_pdgId)")\
               .Define("charFlip_SFsystup","chargeflip_SF(1,ttc_l1_pt,ttc_l1_eta,ttc_l1_phi,ttc_l2_pt,ttc_l2_eta,ttc_l2_phi,ttc_region,1, GenDressedLepton_eta, GenDressedLepton_phi, GenDressedLepton_pdgId)")\
               .Define("charFlip_SFsystdo","chargeflip_SF(1,ttc_l1_pt,ttc_l1_eta,ttc_l1_phi,ttc_l2_pt,ttc_l2_eta,ttc_l2_phi,ttc_region,2, GenDressedLepton_eta, GenDressedLepton_phi, GenDressedLepton_pdgId)")\
               .Define("charFlip_SFstatup","chargeflip_SF(1,ttc_l1_pt,ttc_l1_eta,ttc_l1_phi,ttc_l2_pt,ttc_l2_eta,ttc_l2_phi,ttc_region,3, GenDressedLepton_eta, GenDressedLepton_phi, GenDressedLepton_pdgId)")\
               .Define("charFlip_SFstatdo","chargeflip_SF(1,ttc_l1_pt,ttc_l1_eta,ttc_l1_phi,ttc_l2_pt,ttc_l2_eta,ttc_l2_phi,ttc_region,4, GenDressedLepton_eta, GenDressedLepton_phi, GenDressedLepton_pdgId)")
  else:
    dOut = dOut.Define("charFlip_SF","chargeflip_SF(0,ttc_l1_pt,ttc_l1_eta,ttc_l1_phi,ttc_l2_pt,ttc_l2_eta,ttc_l2_phi,ttc_region,0, GenDressedLepton_eta, GenDressedLepton_phi, GenDressedLepton_pdgId)")\
               .Define("charFlip_SFsystup","chargeflip_SF(0,ttc_l1_pt,ttc_l1_eta,ttc_l1_phi,ttc_l2_pt,ttc_l2_eta,ttc_l2_phi,ttc_region,1, GenDressedLepton_eta, GenDressedLepton_phi, GenDressedLepton_pdgId)")\
               .Define("charFlip_SFsystdo","chargeflip_SF(0,ttc_l1_pt,ttc_l1_eta,ttc_l1_phi,ttc_l2_pt,ttc_l2_eta,ttc_l2_phi,ttc_region,2, GenDressedLepton_eta, GenDressedLepton_phi, GenDressedLepton_pdgId)")\
               .Define("charFlip_SFstatup","chargeflip_SF(0,ttc_l1_pt,ttc_l1_eta,ttc_l1_phi,ttc_l2_pt,ttc_l2_eta,ttc_l2_phi,ttc_region,3, GenDressedLepton_eta, GenDressedLepton_phi, GenDressedLepton_pdgId)")\
               .Define("charFlip_SFstatdo","chargeflip_SF(0,ttc_l1_pt,ttc_l1_eta,ttc_l1_phi,ttc_l2_pt,ttc_l2_eta,ttc_l2_phi,ttc_region,4, GenDressedLepton_eta, GenDressedLepton_phi, GenDressedLepton_pdgId)")



  columns = ROOT.std.vector("string")()
  for c in ('ttc_region','genweight','HT','j1_pt','j1_eta','j1_phi','j1_mass','j2_pt','j2_eta','j2_phi','j2_mass','j3_pt','j3_eta','j3_phi','j3_mass','j1_FlavB','j1_FlavCvB','j1_FlavCvL','j2_FlavB','j2_FlavCvB','j2_FlavCvL','j3_FlavB','j3_FlavCvB','j3_FlavCvL','PV_npvsGood','PV_x','PV_y','PV_z','nSV','ttc_l1_pt','ttc_l1_pt_muPtup','ttc_l1_pt_muPtdo','ttc_l1_eta','ttc_l1_phi','ttc_l1_mass','ttc_l2_pt','ttc_l2_pt_muPtup','ttc_l2_pt_muPtdo','ttc_l2_eta','ttc_l2_phi','ttc_l2_mass','ttc_met','ttc_met_phi','ttc_mll','ttc_mllj1','ttc_mllj2','ttc_mllj3','puWeight','puWeightUp','puWeightDown','ttc_met_jesup','ttc_met_jesdo','ttc_met_jerup','ttc_met_jerdo','ttc_met_unclusterEup','ttc_met_unclusterEdo','ttc_met_phi_jesup','ttc_met_phi_jesdo','ttc_met_phi_jerup','ttc_met_phi_jerdo','ttc_met_phi_unclusterEup','ttc_met_phi_unclusterEdo','dr_j1j2','dr_j1j3','dr_j2j3','HT_jesup','HT_jesdo','HT_jerup','HT_jerdo','ttc_mllj1_jesup','ttc_mllj1_jesdo','ttc_mllj1_jerup','ttc_mllj1_jerdo','ttc_mllj2_jesup','ttc_mllj2_jesdo','ttc_mllj2_jerup','ttc_mllj2_jerdo','ttc_mllj3_jesup','ttc_mllj3_jesdo','ttc_mllj3_jerup','ttc_mllj3_jerdo','mu_id','mu_id_sysup','mu_id_sysdo','mu_id_statup','mu_id_statdo','ele_id','ele_id_sysup','ele_id_sysdo','ele_id_statup','ele_id_statdo','trig_SF','trig_SFup','trig_SFdo','ctag_SF','ctag_SF_statup','ctag_SF_statdo','ctag_SF_Extrapup','ctag_SF_Extrapdo','ctag_SF_LHEScaleWeightmuFup','ctag_SF_LHEScaleWeightmuFdo','ctag_SF_LHEScaleWeightmuRup','ctag_SF_LHEScaleWeightmuRdo','ctag_SF_Interpup','ctag_SF_Interpdo','ctag_SF_PSWeightFSRup','ctag_SF_PSWeightFSRdo','ctag_SF_PSWeightISRup','ctag_SF_PSWeightISRdo','ctag_SF_PUWeightup','ctag_SF_PUWeightdo','ctag_SF_XSec_BRUnc_DYJets_bup','ctag_SF_XSec_BRUnc_DYJets_bdo','ctag_SF_XSec_BRUnc_DYJets_cup','ctag_SF_XSec_BRUnc_DYJets_cdo','ctag_SF_XSec_BRUnc_WJets_cup','ctag_SF_XSec_BRUnc_WJets_cdo','ctag_SF_jerup','ctag_SF_jerdo','ctag_SF_jesTotalup','ctag_SF_jesTotaldo','charFlip_SF','charFlip_SFsystup','charFlip_SFsystdo','charFlip_SFstatup','charFlip_SFstatdo','sig_pdfup','sig_pdfdo','sig_scaleup','sig_scaledo','sig_psup','sig_psdo','PrefireWeight','PrefireWeight_Up','PrefireWeight_Down','ttc_mllj1_muPtup','ttc_mllj2_muPtup','ttc_mllj3_muPtup','ttc_mllj1_muPtdo','ttc_mllj2_muPtdo','ttc_mllj3_muPtdo','ttc_mll_muPtup','ttc_mll_muPtdo'):
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
  flag = args.flag
  iin = TransFileName(args.iin, True, era, None, flag)

  path = str(inputFile_path_skim[era])

  print('Processing ',path+iin)
  ftemp=ROOT.TFile.Open(path+iin)   
  ttemp=ftemp.Get('Events')
  if flag=='dummy':
    ntemp=ttemp.GetEntriesFast()
  else:
    ntemp=ttemp.GetEntries(flag)
  # Samples used for BDT training only leaves half of the events in the application while others use full events
  ntrain = ntemp*0.5 if istrain else ntemp
  Slim_module(iin,ntrain,flag,istrain,era)
  ftemp.Close()

  end = time.time()
  end1 = time.clock()
  print "wall time:", end-start
  print "process time:", end1-start1
