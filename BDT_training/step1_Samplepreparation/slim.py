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

def Slim_module(filein,nin,mass_flag):

  filters="ttc_jets && ttc_l1_pt>30 && ttc_met>30 && ttc_mll>20 && ttc_drll>0.3 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && nHad_tau==0 && ttc_2P0F"

  fileOut = filein.split('.')[0]+".root"
  treeOut = "SlimTree"
  nevent=nin
  if 'TTTo1L' in filein:
    nevent=2*nin

  if 'ttc_a' in filein or 'ttc_s0' in filein:
     fileOut = filein.split('.')[0]+'_'+mass_flag.split('_')[2]+mass_flag.split('_')[3]+".root"
     df_filein_tree_temp = ROOT.RDataFrame("Events",path+filein)
     df_filein_tree_temp2 = df_filein_tree_temp.Filter(mass_flag)
     df_filein_tree = df_filein_tree_temp2.Range(int(nevent))
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
             .Define("ttc_mllj3_jerdo","mllj_jesr(ttc_l1_pt,ttc_l1_eta,ttc_l1_phi,ttc_l1_mass,ttc_l2_pt,ttc_l2_eta,ttc_l2_phi,ttc_l2_mass,Jet_pt_jerDown,Jet_eta,Jet_phi,Jet_mass_jerDown,tightJets_id_in24,3)")

  columns = ROOT.std.vector("string")()
  for c in ('ttc_region','genweight','HT','j1_pt','j1_eta','j1_phi','j1_mass','j2_pt','j2_eta','j2_phi','j2_mass','j3_pt','j3_eta','j3_phi','j3_mass','j1_FlavB','j1_FlavCvB','j1_FlavCvL','j2_FlavB','j2_FlavCvB','j2_FlavCvL','j3_FlavB','j3_FlavCvB','j3_FlavCvL','PV_npvsGood','PV_x','PV_y','PV_z','nSV','ttc_region','ttc_l1_pt','ttc_l1_eta','ttc_l1_phi','ttc_l1_mass','ttc_l2_pt','ttc_l2_eta','ttc_l2_phi','ttc_l2_mass','ttc_met','ttc_met_phi','ttc_mll','ttc_mllj1','ttc_mllj2','ttc_mllj3','puWeight','puWeightUp','puWeightDown','ttc_met_jesup','ttc_met_jesdo','ttc_met_jerup','ttc_met_jerdo','ttc_met_unclusterEup','ttc_met_unclusterEdo','ttc_met_phi_jesup','ttc_met_phi_jesdo','ttc_met_phi_jerup','ttc_met_phi_jerdo','ttc_met_phi_unclusterEup','ttc_met_phi_unclusterEdo','dr_j1j2','dr_j1j3','dr_j2j3','HT_jesup','HT_jesdo','HT_jerup','HT_jerdo','ttc_mllj1_jesup','ttc_mllj1_jesdo','ttc_mllj1_jerup','ttc_mllj1_jerdo','ttc_mllj2_jesup','ttc_mllj2_jesdo','ttc_mllj2_jerup','ttc_mllj2_jerdo','ttc_mllj3_jesup','ttc_mllj3_jesdo','ttc_mllj3_jerup','ttc_mllj3_jerdo'):
    columns.push_back(c)
  dOut.Snapshot(treeOut,fileOut,columns)

if __name__ == "__main__":
  start = time.time()
  start1 = time.clock()
  for iin in ['ttWtoLNu.root','ttWtoQQ.root','ttZ.root','ttZtoQQ.root','ttWW.root','ttWZ.root','ttZZ.root','TTTo1L.root','TTTo2L.root','WZ.root','WWZ.root','WZZ.root','WWW.root','ZZZ.root','osWW.root','tzq.root','tttt.root','tttJ.root','tttW.root']:
    print('Processing ',iin)
    ftemp=ROOT.TFile.Open(path+iin)
    ttemp=ftemp.Get('Events')
    ntemp=ttemp.GetEntriesFast()
    Slim_module(iin,ntemp*0.5,'dummy')
    ftemp.Close()

  coups=['rtc01','rtu01']
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
        Slim_module('ttc_'+cps[ic].lower()+'_'+coups[icp]+'.root',ntemp*0.5, flag)
      ftemp.Close()
  end = time.time()
  end1 = time.clock()
  print( "wall time:", end-start)
  print( "process time:", end1-start1)
