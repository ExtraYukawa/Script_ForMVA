import ROOT
import time
import os
import math
from math import sqrt

TTC_header_path = os.path.join("slim.h")
ROOT.gInterpreter.Declare('#include "{}"'.format(TTC_header_path))

def all_trigger(df):
  all_trigger = df.Filter("HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8 || HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ || HLT_IsoMu27 || HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL || HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ || HLT_passEle32WPTight || HLT_Ele35_WPTight_Gsf")
  return all_trigger

def for_diele_trigger(df):
  ditri_ele_trigger = df.Filter("HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL || HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ")
  return ditri_ele_trigger

def for_singleele_trigger_eechannel(df):
  sin_ele_trigger = df.Filter("!(HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL) && !(HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ) && (HLT_passEle32WPTight || HLT_Ele35_WPTight_Gsf)")
  return sin_ele_trigger

def for_dimuon_trigger(df):
  ditri_mu_trigger = df.Filter("(HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8)")
  return ditri_mu_trigger

def for_singlemuon_trigger_mumuchannel(df):
  single_mu_trigger = df.Filter("!(HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8) && HLT_IsoMu27")
  return single_mu_trigger

def for_singlemuon_trigger_emuchannel(df):
  single_mu_trigger = df.Filter("!(HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ) && HLT_IsoMu27")
  return single_mu_trigger

def for_cross_trigger(df):
  x_trigger = df.Filter("(HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ)")
  return x_trigger

path='/eos/cms/store/group/phys_top/ExtraYukawa/2018/'

def Slim_module(filein,nin,mass_flag, use_fortraining):

  filters="ttc_jets && ttc_l1_pt>30 && ttc_met>30 && ttc_mll>20 && ttc_drll>0.3 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && nHad_tau==0 && ttc_2P0F"

  # flag for TTto2L and DY for chargeflip SF
  if 'TTTo2L' in filein or 'DY' in filein:
    OS_flag=1
  else:
    OS_flag=0

  fileOut = filein.split('.')[0]+".root"
  treeOut = "SlimTree"
  nevent=nin
  if 'TTTo1L' in filein:
    nevent=2*nin

  if 'ttc_a' in filein or 'ttc_s0' in filein:
     fileOut = filein.split('.')[0]+'_'+mass_flag.split('_')[2]+mass_flag.split('_')[3]+".root"
     df_filein_tree_temp = ROOT.RDataFrame("Events",path+filein)
     df_filein_tree_temp2 = df_filein_tree_temp.Filter(mass_flag)
     df_filein_tree = df_filein_tree_temp2.Range(int(nevent),0)
  elif 'TTTo1L' in filein:
    df_filein_tree_temp = ROOT.RDataFrame("Events",path+filein)
    df_filein_tree = df_filein_tree_temp.Range(int(nevent))
  elif use_fortraining:
    df_filein_tree_temp = ROOT.RDataFrame("Events",path+filein)
    df_filein_tree = df_filein_tree_temp.Range(int(nevent),0)
  else:
    df_filein_tree_temp = ROOT.RDataFrame("Events",path+filein)
    df_filein_tree = df_filein_tree_temp.Range(int(nevent))

  df_filein_tree = df_filein_tree.Define("genweight","puWeight*genWeight/abs(genWeight)")
  df_filein = df_filein_tree.Filter(filters)
  dOut = all_trigger(df_filein)
  dOut = dOut.Define("j1_FlavB","Jet_btagDeepFlavB[tightJets_id_in24[0]]")\
             .Define("j1_FlavCvB","Jet_btagDeepFlavCvB[tightJets_id_in24[0]]")\
             .Define("j1_FlavCvL","Jet_btagDeepFlavCvL[tightJets_id_in24[0]]")\
             .Define("j2_FlavB","Jet_btagDeepFlavB[tightJets_id_in24[1]]")\
             .Define("j2_FlavCvB","Jet_btagDeepFlavCvB[tightJets_id_in24[1]]")\
             .Define("j2_FlavCvL","Jet_btagDeepFlavCvL[tightJets_id_in24[1]]")\
             .Define("j3_FlavB","Jet_btagDeepFlavB[tightJets_id_in24[2]]")\
             .Define("j3_FlavCvB","Jet_btagDeepFlavCvB[tightJets_id_in24[2]]")\
             .Define("j3_FlavCvL","Jet_btagDeepFlavCvL[tightJets_id_in24[2]]")\
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
             .Define("dr_j1j2","deltaR_jet(Jet_pt,Jet_eta,Jet_phi,Jet_mass,tightJets_id_in24,1)")\
             .Define("dr_j1j3","deltaR_jet(Jet_pt,Jet_eta,Jet_phi,Jet_mass,tightJets_id_in24,2)")\
             .Define("dr_j2j3","deltaR_jet(Jet_pt,Jet_eta,Jet_phi,Jet_mass,tightJets_id_in24,3)")\
             .Define("HT_jesup","HT_jesr(tightJets_id_in24, Jet_pt_jesTotalUp, Jet_pt_jesTotalDown, Jet_pt_jerUp, Jet_pt_jerDown, 0, nJet)")\
             .Define("HT_jesdo","HT_jesr(tightJets_id_in24, Jet_pt_jesTotalUp, Jet_pt_jesTotalDown, Jet_pt_jerUp, Jet_pt_jerDown, 1, nJet)")\
             .Define("HT_jerup","HT_jesr(tightJets_id_in24, Jet_pt_jesTotalUp, Jet_pt_jesTotalDown, Jet_pt_jerUp, Jet_pt_jerDown, 2, nJet)")\
             .Define("HT_jerdo","HT_jesr(tightJets_id_in24, Jet_pt_jesTotalUp, Jet_pt_jesTotalDown, Jet_pt_jerUp, Jet_pt_jerDown, 3, nJet)")\
             .Define("ttc_mllj1_jesup","mllj_jesr(ttc_l1_pt,ttc_l1_eta,ttc_l1_phi,ttc_l1_mass,ttc_l2_pt,ttc_l2_eta,ttc_l2_phi,ttc_l2_mass,Jet_pt_jesTotalUp,Jet_eta,Jet_phi,Jet_mass_jesTotalUp,tightJets_id_in24,1)")\
             .Define("ttc_mllj2_jesup","mllj_jesr(ttc_l1_pt,ttc_l1_eta,ttc_l1_phi,ttc_l1_mass,ttc_l2_pt,ttc_l2_eta,ttc_l2_phi,ttc_l2_mass,Jet_pt_jesTotalUp,Jet_eta,Jet_phi,Jet_mass_jesTotalUp,tightJets_id_in24,2)")\
             .Define("ttc_mllj3_jesup","mllj_jesr(ttc_l1_pt,ttc_l1_eta,ttc_l1_phi,ttc_l1_mass,ttc_l2_pt,ttc_l2_eta,ttc_l2_phi,ttc_l2_mass,Jet_pt_jesTotalUp,Jet_eta,Jet_phi,Jet_mass_jesTotalUp,tightJets_id_in24,3)")\
             .Define("ttc_mllj1_jesdo","mllj_jesr(ttc_l1_pt,ttc_l1_eta,ttc_l1_phi,ttc_l1_mass,ttc_l2_pt,ttc_l2_eta,ttc_l2_phi,ttc_l2_mass,Jet_pt_jesTotalDown,Jet_eta,Jet_phi,Jet_mass_jesTotalDown,tightJets_id_in24,1)")\
             .Define("ttc_mllj2_jesdo","mllj_jesr(ttc_l1_pt,ttc_l1_eta,ttc_l1_phi,ttc_l1_mass,ttc_l2_pt,ttc_l2_eta,ttc_l2_phi,ttc_l2_mass,Jet_pt_jesTotalDown,Jet_eta,Jet_phi,Jet_mass_jesTotalDown,tightJets_id_in24,2)")\
             .Define("ttc_mllj3_jesdo","mllj_jesr(ttc_l1_pt,ttc_l1_eta,ttc_l1_phi,ttc_l1_mass,ttc_l2_pt,ttc_l2_eta,ttc_l2_phi,ttc_l2_mass,Jet_pt_jesTotalDown,Jet_eta,Jet_phi,Jet_mass_jesTotalDown,tightJets_id_in24,3)")\
             .Define("ttc_mllj1_jerup","mllj_jesr(ttc_l1_pt,ttc_l1_eta,ttc_l1_phi,ttc_l1_mass,ttc_l2_pt,ttc_l2_eta,ttc_l2_phi,ttc_l2_mass,Jet_pt_jerUp,Jet_eta,Jet_phi,Jet_mass_jerUp,tightJets_id_in24,1)")\
             .Define("ttc_mllj2_jerup","mllj_jesr(ttc_l1_pt,ttc_l1_eta,ttc_l1_phi,ttc_l1_mass,ttc_l2_pt,ttc_l2_eta,ttc_l2_phi,ttc_l2_mass,Jet_pt_jerUp,Jet_eta,Jet_phi,Jet_mass_jerUp,tightJets_id_in24,2)")\
             .Define("ttc_mllj3_jerup","mllj_jesr(ttc_l1_pt,ttc_l1_eta,ttc_l1_phi,ttc_l1_mass,ttc_l2_pt,ttc_l2_eta,ttc_l2_phi,ttc_l2_mass,Jet_pt_jerUp,Jet_eta,Jet_phi,Jet_mass_jerUp,tightJets_id_in24,3)")\
             .Define("ttc_mllj1_jerdo","mllj_jesr(ttc_l1_pt,ttc_l1_eta,ttc_l1_phi,ttc_l1_mass,ttc_l2_pt,ttc_l2_eta,ttc_l2_phi,ttc_l2_mass,Jet_pt_jerDown,Jet_eta,Jet_phi,Jet_mass_jerDown,tightJets_id_in24,1)")\
             .Define("ttc_mllj2_jerdo","mllj_jesr(ttc_l1_pt,ttc_l1_eta,ttc_l1_phi,ttc_l1_mass,ttc_l2_pt,ttc_l2_eta,ttc_l2_phi,ttc_l2_mass,Jet_pt_jerDown,Jet_eta,Jet_phi,Jet_mass_jerDown,tightJets_id_in24,2)")\
             .Define("ttc_mllj3_jerdo","mllj_jesr(ttc_l1_pt,ttc_l1_eta,ttc_l1_phi,ttc_l1_mass,ttc_l2_pt,ttc_l2_eta,ttc_l2_phi,ttc_l2_mass,Jet_pt_jerDown,Jet_eta,Jet_phi,Jet_mass_jerDown,tightJets_id_in24,3)")\
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
             .Define("trig_SF","lep_trigger(ttc_l1_eta,ttc_l2_eta,ttc_region)")\
             .Define("trig_SFup","lep_triggerup(ttc_l1_eta,ttc_l2_eta,ttc_region)")\
             .Define("trig_SFdo","lep_triggerdown(ttc_l1_eta,ttc_l2_eta,ttc_region)")\
             .Define("ctag_SF","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,0)")\
             .Define("ctag_SF_statup","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,1)")\
             .Define("ctag_SF_statdo","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,2)")\
             .Define("ctag_SF_EleIDup","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,3)")\
             .Define("ctag_SF_EleIDdo","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,4)")\
             .Define("ctag_SF_LHEScaleWeightmuFup","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,5)")\
             .Define("ctag_SF_LHEScaleWeightmuFdo","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,6)")\
             .Define("ctag_SF_LHEScaleWeightmuRup","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,7)")\
             .Define("ctag_SF_LHEScaleWeightmuRdo","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,8)")\
             .Define("ctag_SF_MuIDup","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,9)")\
             .Define("ctag_SF_MuIDdo","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,10)")\
             .Define("ctag_SF_PSWeightFSRup","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,11)")\
             .Define("ctag_SF_PSWeightFSRdo","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,12)")\
             .Define("ctag_SF_PSWeightISRup","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,13)")\
             .Define("ctag_SF_PSWeightISRdo","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,14)")\
             .Define("ctag_SF_PUWeightup","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,15)")\
             .Define("ctag_SF_PUWeightdo","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,16)")\
             .Define("ctag_SF_XSec_DYJetsup","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,17)")\
             .Define("ctag_SF_XSec_DYJetsdo","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,18)")\
             .Define("ctag_SF_XSec_STup","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,19)")\
             .Define("ctag_SF_XSec_STdo","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,20)")\
             .Define("ctag_SF_XSec_VVup","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,21)")\
             .Define("ctag_SF_XSec_VVdo","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,22)")\
             .Define("ctag_SF_XSec_WJetsup","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,23)")\
             .Define("ctag_SF_XSec_WJetsdo","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,24)")\
             .Define("ctag_SF_XSec_ttbarup","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,25)")\
             .Define("ctag_SF_XSec_ttbardo","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,26)")\
             .Define("ctag_SF_jerup","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,27)")\
             .Define("ctag_SF_jerdo","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,28)")\
             .Define("ctag_SF_jesTotalup","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,29)")\
             .Define("ctag_SF_jesTotaldo","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,30)")\
             .Define("sig_pdfup","signal_pdf(ttc_l1_pt,0)")\
             .Define("sig_pdfdo","signal_pdf(ttc_l1_pt,1)")\
             .Define("sig_scaleup","signal_scale(ttc_l1_pt,0)")\
             .Define("sig_scaledo","signal_scale(ttc_l1_pt,1)")\
             .Define("sig_psup","signal_ps(ttc_l1_pt,0)")\
             .Define("sig_psdo","signal_ps(ttc_l1_pt,1)")

  if OS_flag==1:
    dOut = dOut.Define("charFlip_SF","chargeflip_SF(1,ttc_l1_pt,ttc_l1_eta,ttc_l1_phi,ttc_l2_pt,ttc_l2_eta,ttc_l2_phi,ttc_region,0, GenDressedLepton_eta, GenDressedLepton_phi, GenDressedLepton_pdgId)")\
               .Define("charFlip_SFup","chargeflip_SF(1,ttc_l1_pt,ttc_l1_eta,ttc_l1_phi,ttc_l2_pt,ttc_l2_eta,ttc_l2_phi,ttc_region,1, GenDressedLepton_eta, GenDressedLepton_phi, GenDressedLepton_pdgId)")\
               .Define("charFlip_SFdo","chargeflip_SF(1,ttc_l1_pt,ttc_l1_eta,ttc_l1_phi,ttc_l2_pt,ttc_l2_eta,ttc_l2_phi,ttc_region,2, GenDressedLepton_eta, GenDressedLepton_phi, GenDressedLepton_pdgId)")
  else:
    dOut = dOut.Define("charFlip_SF","chargeflip_SF(0,ttc_l1_pt,ttc_l1_eta,ttc_l1_phi,ttc_l2_pt,ttc_l2_eta,ttc_l2_phi,ttc_region,0, GenDressedLepton_eta, GenDressedLepton_phi, GenDressedLepton_pdgId)")\
               .Define("charFlip_SFup","chargeflip_SF(0,ttc_l1_pt,ttc_l1_eta,ttc_l1_phi,ttc_l2_pt,ttc_l2_eta,ttc_l2_phi,ttc_region,1, GenDressedLepton_eta, GenDressedLepton_phi, GenDressedLepton_pdgId)")\
               .Define("charFlip_SFdo","chargeflip_SF(0,ttc_l1_pt,ttc_l1_eta,ttc_l1_phi,ttc_l2_pt,ttc_l2_eta,ttc_l2_phi,ttc_region,2, GenDressedLepton_eta, GenDressedLepton_phi, GenDressedLepton_pdgId)")


  columns = ROOT.std.vector("string")()
  for c in ('ttc_region','genweight','HT','j1_pt','j1_eta','j1_phi','j1_mass','j2_pt','j2_eta','j2_phi','j2_mass','j3_pt','j3_eta','j3_phi','j3_mass','j1_FlavB','j1_FlavCvB','j1_FlavCvL','j2_FlavB','j2_FlavCvB','j2_FlavCvL','j3_FlavB','j3_FlavCvB','j3_FlavCvL','PV_npvsGood','PV_x','PV_y','PV_z','nSV','ttc_l1_pt','ttc_l1_eta','ttc_l1_phi','ttc_l1_mass','ttc_l2_pt','ttc_l2_eta','ttc_l2_phi','ttc_l2_mass','ttc_met','ttc_met_phi','ttc_mll','ttc_mllj1','ttc_mllj2','ttc_mllj3','puWeight','puWeightUp','puWeightDown','ttc_met_jesup','ttc_met_jesdo','ttc_met_jerup','ttc_met_jerdo','ttc_met_unclusterEup','ttc_met_unclusterEdo','ttc_met_phi_jesup','ttc_met_phi_jesdo','ttc_met_phi_jerup','ttc_met_phi_jerdo','ttc_met_phi_unclusterEup','ttc_met_phi_unclusterEdo','dr_j1j2','dr_j1j3','dr_j2j3','HT_jesup','HT_jesdo','HT_jerup','HT_jerdo','ttc_mllj1_jesup','ttc_mllj1_jesdo','ttc_mllj1_jerup','ttc_mllj1_jerdo','ttc_mllj2_jesup','ttc_mllj2_jesdo','ttc_mllj2_jerup','ttc_mllj2_jerdo','ttc_mllj3_jesup','ttc_mllj3_jesdo','ttc_mllj3_jerup','ttc_mllj3_jerdo','mu_id','mu_id_sysup','mu_id_sysdo','mu_id_statup','mu_id_statdo','ele_id','ele_id_sysup','ele_id_sysdo','ele_id_statup','ele_id_statdo','trig_SF','trig_SFup','trig_SFdo','ctag_SF','ctag_SF_statup','ctag_SF_statdo','ctag_SF_EleIDup','ctag_SF_EleIDdo','ctag_SF_LHEScaleWeightmuFup','ctag_SF_LHEScaleWeightmuFdo','ctag_SF_LHEScaleWeightmuRup','ctag_SF_LHEScaleWeightmuRdo','ctag_SF_MuIDup','ctag_SF_MuIDdo','ctag_SF_PSWeightFSRup','ctag_SF_PSWeightFSRdo','ctag_SF_PUWeightup','ctag_SF_PUWeightdo','ctag_SF_XSec_DYJetsup','ctag_SF_XSec_DYJetsdo','ctag_SF_XSec_STup','ctag_SF_XSec_STdo','ctag_SF_XSec_VVup','ctag_SF_XSec_VVdo','ctag_SF_XSec_WJetsup','ctag_SF_XSec_WJetsdo','ctag_SF_XSec_ttbarup','ctag_SF_XSec_ttbardo','ctag_SF_jerup','ctag_SF_jerdo','ctag_SF_jesTotalup','ctag_SF_jesTotaldo','charFlip_SF','charFlip_SFup','charFlip_SFdo','sig_pdfup','sig_pdfdo','sig_scaleup','sig_scaledo','sig_psup','sig_psdo'):
    columns.push_back(c)
  dOut.Snapshot(treeOut,fileOut,columns)

if __name__ == "__main__":
  start = time.time()
  start1 = time.clock()
  for iin in ['ttWtoLNu.root','ttWtoQQ.root','ttZ.root','ttZtoQQ.root','ttWW.root','ttWZ.root','ttZZ.root','TTTo1L.root','TTTo2L.root','WZ.root','WWZ.root','WZZ.root','WWW.root','ZZZ.root','osWW.root','tzq.root','tttt.root','tttJ.root','tttW.root']:
    if not iin=='TTTo2L.root':continue
    print('Processing ',iin)
    ftemp=ROOT.TFile.Open(path+iin)
    ttemp=ftemp.Get('Events')
    ntemp=ttemp.GetEntriesFast()
    #those samples are used for BDT training, so only half of the events will be used in the application
    Slim_module(iin,ntemp*0.5,'dummy',True)
    ftemp.Close()

  for iin in ['DYnlo.root','WWdps.root','tW.root','tbarW.root','ttH.root','ttZH.root','ttWH.root','zz2l.root']:
    print('Processing ',iin)
    ftemp=ROOT.TFile.Open(path+iin)
    ttemp=ftemp.Get('Events')
    ntemp=ttemp.GetEntriesFast()
    #those samples are not used for BDT training, so all of the events will be used in the application
    Slim_module(iin,ntemp,'dummy', False)
    ftemp.Close()

  coups=['rtc01','rtc04','rtc08','rtc10','rtu01','rtu04','rtu08','rtu10']
  cps=['A','S0']
  masses=['200','300','350','400','500','600','700']
  for ic in range(0,len(cps)):
    continue
    for icp in range(0,len(coups)):
      ftemp=ROOT.TFile.Open(path+'ttc_'+cps[ic].lower()+'_'+coups[icp]+'.root')
      ttemp=ftemp.Get('Events')
      for im in range(0,len(masses)):
        flag='GenModel_T'+cps[ic]+'ToTTQ_M'+cps[ic]+'_'+masses[im]+'_TuneCP5_13TeV_G2HDM_'+coups[icp]+'_madgraphMLM_pythia8'
        ntemp=ttemp.GetEntries(flag)
        print('flag ',flag,' has event number:',ntemp)
        Slim_module('ttc_'+cps[ic].lower()+'_'+coups[icp]+'.root',ntemp*0.5, flag, True)
      ftemp.Close()

  end = time.time()
  end1 = time.clock()
  print "wall time:", end-start
  print "process time:", end1-start1
