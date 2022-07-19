import ROOT
import time
import os
import math
from math import sqrt

TTC_header_path = os.path.join("slim_fake.h")
ROOT.gInterpreter.Declare('#include "{}"'.format(TTC_header_path))

def all_trigger(df):
  all_trigger = df.Filter("HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8 || HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8 || HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL || HLT_Ele32_WPTight_Gsf || HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL || HLT_IsoMu27")
  return all_trigger

def for_diele_trigger(df):
  ditri_ele_trigger = df.Filter("HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL || HLT_Ele32_WPTight_Gsf")
  return ditri_ele_trigger

def for_singleele_trigger_emuchannel(df):
  sin_ele_trigger = df.Filter("!(HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL) && !(HLT_IsoMu27) &&  HLT_Ele32_WPTight_Gsf")
  return sin_ele_trigger

def for_dimuon_trigger(df):
  ditri_mu_trigger = df.Filter("HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8 || HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8")
  return ditri_mu_trigger

def for_singlemuon_trigger_mumuchannel(df):
  single_mu_trigger = df.Filter("!(HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8) &&!(HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8) && HLT_IsoMu27")
  return single_mu_trigger

def for_singlemuon_trigger_emuchannel(df):
  single_mu_trigger = df.Filter("!(HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL) && HLT_IsoMu27")
  return single_mu_trigger

def for_cross_trigger(df):
  x_trigger = df.Filter("(HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL)")
  return x_trigger

path='/eos/cms/store/group/phys_top/ExtraYukawa/2018/'

def Slim_module_mm(filein,nin,mass_flag):

  filters="ttc_jets && ttc_region==1 && ttc_l1_pt>30 && ttc_met>30 && ttc_mll>20 && ttc_drll>0.3 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && nHad_tau==0 && (ttc_1P1F || ttc_0P2F)"

  fileOut = filein.split('.')[0]+"_mm.root"
  treeOut = "SlimTree"
  nevent=nin

  df_filein_tree_temp = ROOT.RDataFrame("Events",path+filein)
  df_filein_tree = df_filein_tree_temp.Range(int(nevent))

  df_filein = df_filein_tree.Filter(filters)
  df_filein = df_filein.Define("fakeweight","fake_weight(ttc_region,ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,muon_conePt[ttc_l1_id],ttc_l1_eta,muon_conePt[ttc_l2_id],ttc_l2_eta)")

  if 'SingleMuon' in filein:
    print('single muon')
    dOut = for_singlemuon_trigger_mumuchannel(df_filein)
  if 'DoubleMuon' in filein:
    print('double muon')
    dOut = for_dimuon_trigger(df_filein)
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


  columns = ROOT.std.vector("string")()
  for c in ('ttc_region','HT','j1_pt','j1_eta','j1_phi','j1_mass','j2_pt','j2_eta','j2_phi','j2_mass','j3_pt','j3_eta','j3_phi','j3_mass','j1_FlavB','j1_FlavCvB','j1_FlavCvL','j2_FlavB','j2_FlavCvB','j2_FlavCvL','j3_FlavB','j3_FlavCvB','j3_FlavCvL','PV_npvsGood','PV_x','PV_y','PV_z','nSV','ttc_l1_pt','ttc_l1_eta','ttc_l1_phi','ttc_l1_mass','ttc_l2_pt','ttc_l2_eta','ttc_l2_phi','ttc_l2_mass','ttc_met','ttc_met_phi','ttc_mll','ttc_mllj1','ttc_mllj2','ttc_mllj3','dr_j1j2','dr_j1j3','dr_j2j3','fakeweight'):
    columns.push_back(c)
  dOut.Snapshot(treeOut,fileOut,columns)

def Slim_module_em(filein,nin,mass_flag):

  filters="ttc_jets && ttc_region==2 && (ttc_l1_pt>30 || ttc_l2_pt>30) && ttc_met>30 && ttc_mll>20 && ttc_drll>0.3 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && nHad_tau==0 && (ttc_1P1F || ttc_0P2F)"

  fileOut = filein.split('.')[0]+"_em.root"
  treeOut = "SlimTree"
  nevent=nin

  df_filein_tree_temp = ROOT.RDataFrame("Events",path+filein)
  df_filein_tree = df_filein_tree_temp.Range(int(nevent))

  df_filein = df_filein_tree.Filter(filters)
  df_filein = df_filein.Define("fakeweight","fake_weight(ttc_region,ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,muon_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta)")

  if 'SingleMuon' in filein:
    print('single muon')
    dOut = for_singlemuon_trigger_emuchannel(df_filein)
  if 'EGamma' in filein:
    print('egamma')
    dOut = for_singleele_trigger_emuchannel(df_filein)
  if 'MuonEG' in filein:
    print('muongamma')
    dOut = for_cross_trigger(df_filein)

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


  columns = ROOT.std.vector("string")()
  #for c in ('ttc_region','HT','j1_pt','j1_eta','j1_phi','j1_mass','j2_pt','j2_eta','j2_phi','j2_mass','j3_pt','j3_eta','j3_phi','j3_mass','j1_FlavB','j1_FlavCvB','j1_FlavCvL','j2_FlavB','j2_FlavCvB','j2_FlavCvL','j3_FlavB','j3_FlavCvB','j3_FlavCvL','PV_npvsGood','PV_x','PV_y','PV_z','nSV','ttc_l1_pt','ttc_l1_eta','ttc_l1_phi','ttc_l1_mass','ttc_l2_pt','ttc_l2_eta','ttc_l2_phi','ttc_l2_mass','ttc_met','ttc_met_phi','ttc_mll','ttc_mllj1','ttc_mllj2','ttc_mllj3','dr_j1j2','dr_j1j3','dr_j2j3','fakeweight','ttc_1P1F','ttc_0P2F'):
  for c in ('ttc_region','HT','j1_pt','j1_eta','j1_phi','j1_mass','j2_pt','j2_eta','j2_phi','j2_mass','j3_pt','j3_eta','j3_phi','j3_mass','j1_FlavB','j1_FlavCvB','j1_FlavCvL','j2_FlavB','j2_FlavCvB','j2_FlavCvL','j3_FlavB','j3_FlavCvB','j3_FlavCvL','PV_npvsGood','PV_x','PV_y','PV_z','nSV','ttc_l1_pt','ttc_l1_eta','ttc_l1_phi','ttc_l1_mass','ttc_l2_pt','ttc_l2_eta','ttc_l2_phi','ttc_l2_mass','ttc_met','ttc_met_phi','ttc_mll','ttc_mllj1','ttc_mllj2','ttc_mllj3','dr_j1j2','dr_j1j3','dr_j2j3','fakeweight'):
    columns.push_back(c)
  dOut.Snapshot(treeOut,fileOut,columns)

def Slim_module_ee(filein,nin,mass_flag):

  filters="ttc_jets && ttc_region==3 && ttc_l1_pt>30 && ttc_met>30 && ttc_mll>20 && ttc_drll>0.3 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && nHad_tau==0 && (ttc_1P1F || ttc_0P2F) && (ttc_mll<60 || ttc_mll>120)"

  fileOut = filein.split('.')[0]+"_ee.root"
  treeOut = "SlimTree"
  nevent=nin

  df_filein_tree_temp = ROOT.RDataFrame("Events",path+filein)
  df_filein_tree = df_filein_tree_temp.Range(int(nevent))

  df_filein = df_filein_tree.Filter(filters)
  df_filein = df_filein.Define("fakeweight","fake_weight(ttc_region,ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,electron_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta)")

  if 'EGamma' in filein:
    print('egamma')
    dOut = for_diele_trigger(df_filein)

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


  columns = ROOT.std.vector("string")()
  for c in ('ttc_region','HT','j1_pt','j1_eta','j1_phi','j1_mass','j2_pt','j2_eta','j2_phi','j2_mass','j3_pt','j3_eta','j3_phi','j3_mass','j1_FlavB','j1_FlavCvB','j1_FlavCvL','j2_FlavB','j2_FlavCvB','j2_FlavCvL','j3_FlavB','j3_FlavCvB','j3_FlavCvL','PV_npvsGood','PV_x','PV_y','PV_z','nSV','ttc_l1_pt','ttc_l1_eta','ttc_l1_phi','ttc_l1_mass','ttc_l2_pt','ttc_l2_eta','ttc_l2_phi','ttc_l2_mass','ttc_met','ttc_met_phi','ttc_mll','ttc_mllj1','ttc_mllj2','ttc_mllj3','dr_j1j2','dr_j1j3','dr_j2j3','fakeweight'):
    columns.push_back(c)
  dOut.Snapshot(treeOut,fileOut,columns)

if __name__ == "__main__":
  start = time.time()
  start1 = time.clock()

  # single/double muon
  for iin in ['SingleMuonA.root','SingleMuonB.root','SingleMuonC.root','SingleMuonD_0.root','SingleMuonD_1.root','DoubleMuonA.root','DoubleMuonB.root','DoubleMuonC.root','DoubleMuonD_0.root','DoubleMuonD_1.root']:
    continue
    print('Processing ',iin)
    ftemp=ROOT.TFile.Open(path+iin)
    ttemp=ftemp.Get('Events')
    ntemp=ttemp.GetEntriesFast()
    Slim_module_mm(iin,ntemp,'dummy')
    ftemp.Close()

  # muon egamma
 # for iin in ['MuonEGA.root','MuonEGB.root','MuonEGC.root','MuonEGD_0.root','MuonEGD_1.root','SingleMuonA.root','SingleMuonB.root','SingleMuonC.root','SingleMuonD_0.root','SingleMuonD_1.root','EGammaA.root','EGammaB.root','EGammaC.root','EGammaD_0.root','EGammaD_1.root']:
  for iin in ['MuonEGA.root','MuonEGB.root','MuonEGC.root','MuonEGD_0.root','MuonEGD_1.root','SingleMuonA.root','SingleMuonB.root','SingleMuonC.root','SingleMuonD_0.root','SingleMuonD_1.root','EGammaA.root','EGammaB.root','EGammaC.root','EGammaD_0.root','EGammaD_1.root']:
    print('Processing ',iin)
    ftemp=ROOT.TFile.Open(path+iin)
    ttemp=ftemp.Get('Events')
    ntemp=ttemp.GetEntriesFast()
    print(ntemp)
    Slim_module_em(iin,ntemp,'dummy')
    ftemp.Close()

  # double egamma
  for iin in ['EGammaA.root','EGammaB.root','EGammaC.root','EGammaD_0.root','EGammaD_1.root']:
    continue
    print('Processing ',iin)
    ftemp=ROOT.TFile.Open(path+iin)
    ttemp=ftemp.Get('Events')
    ntemp=ttemp.GetEntriesFast()
    Slim_module_ee(iin,ntemp,'dummy')
    ftemp.Close()

  end = time.time()
  end1 = time.clock()
  print "wall time:", end-start
  print "process time:", end1-start1
