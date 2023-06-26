import ROOT
import time
import os
import math
import optparse
from math import sqrt
from common import inputFile_path, inputFile_path_skim
from common import GetTrainingFile, GetTrigger_MC, GetMETFilter_MC


def Slim_module(filein,nin,mass_flag, use_fortraining, channel, era):


  ROOT.gSystem.Load("libGenVector.so")
  TTC_header_path = os.path.join("script/slim_"+era+".h")
  ROOT.gInterpreter.Declare('#include "{}"'.format(TTC_header_path))


  path = str(inputFile_path_skim[era])

  if channel == "DoubleMuon":

    filters="ttc_region==1 && ttc_jets && ttc_l1_pt>30 && ttc_met>30 && ttc_mll>20 && ttc_drll>0.3 && nHad_tau==0 && (ttc_1P1F || ttc_0P2F) && (nGenDressedLepton>1 || lhe_nlepton >1)"
    fakeweight_definition = "fake_weight(ttc_region,ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,muon_conePt[ttc_l1_id],ttc_l1_eta,muon_conePt[ttc_l2_id],ttc_l2_eta,0)"
    fakeweight_ele_statUp_definition = "fake_weight(ttc_region,ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,muon_conePt[ttc_l1_id],ttc_l1_eta,muon_conePt[ttc_l2_id],ttc_l2_eta,1)"
    fakeweight_ele_statDo_definition = "fake_weight(ttc_region,ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,muon_conePt[ttc_l1_id],ttc_l1_eta,muon_conePt[ttc_l2_id],ttc_l2_eta,2)"
    fakeweight_mu_statUp_definition = "fake_weight(ttc_region,ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,muon_conePt[ttc_l1_id],ttc_l1_eta,muon_conePt[ttc_l2_id],ttc_l2_eta,3)"
    fakeweight_mu_statDo_definition = "fake_weight(ttc_region,ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,muon_conePt[ttc_l1_id],ttc_l1_eta,muon_conePt[ttc_l2_id],ttc_l2_eta,4)"

    channel_name = 'mm'

  elif channel == "DoubleElectron":

    filters="ttc_region==3 && ttc_jets && ttc_l1_pt>30 && ttc_met>30 && ttc_mll>20 && ttc_drll>0.3 && nHad_tau==0 && (ttc_1P1F || ttc_0P2F) && (nGenDressedLepton>1 || lhe_nlepton>1) && (ttc_mll<60 || ttc_mll>120)"
    fakeweight_definition = "fake_weight(ttc_region,ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,electron_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta,0)"
    fakeweight_ele_statUp_definition = "fake_weight(ttc_region,ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,electron_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta,1)"
    fakeweight_ele_statDo_definition = "fake_weight(ttc_region,ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,electron_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta,2)"
    fakeweight_mu_statUp_definition = "fake_weight(ttc_region,ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,electron_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta,3)"
    fakeweight_mu_statDo_definition = "fake_weight(ttc_region,ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,electron_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta,4)"


    channel_name = 'ee'

  elif channel == "ElectronMuon":
    filters="ttc_region==2 && ttc_jets && (ttc_l1_pt>30 || ttc_l2_pt>30) && ttc_met>30 && ttc_mll>20 && ttc_drll>0.3 && nHad_tau==0 && (ttc_1P1F || ttc_0P2F) && (nGenDressedLepton>1 || lhe_nlepton>1)"
    fakeweight_definition = "fake_weight(ttc_region,ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,muon_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta,0)"
    fakeweight_ele_statUp_definition = "fake_weight(ttc_region,ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,muon_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta,1)"
    fakeweight_ele_statDo_definition = "fake_weight(ttc_region,ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,muon_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta,2)"
    fakeweight_mu_statUp_definition = "fake_weight(ttc_region,ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,muon_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta,3)"
    fakeweight_mu_statDo_definition = "fake_weight(ttc_region,ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,muon_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta,4)"


    channel_name = 'em'

  fileOut = filein.split('.')[0]+"_fake_" + channel_name + ".root"
  fileOut = "sample/" + era + "/" + fileOut

  treeOut = "SlimTree"
  nevent=nin

  if use_fortraining:
    df_filein_tree_temp = ROOT.RDataFrame("Events",path+filein)
    print(df_filein_tree_temp, path+filein)
    df_filein_tree = df_filein_tree_temp.Range(int(nevent),0)
  else:
    df_filein_tree_temp = ROOT.RDataFrame("Events",path+filein)
    df_filein_tree = df_filein_tree_temp.Range(int(nevent))

  print ("Final Filters: ", filters)
  filters      = str("(" + filters + ")")

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
             .Define("dr_j1j2","deltaR_jet(Jet_pt,Jet_eta,Jet_phi,Jet_mass,JetMatched_idx,1)")\
             .Define("dr_j1j3","deltaR_jet(Jet_pt,Jet_eta,Jet_phi,Jet_mass,JetMatched_idx,2)")\
             .Define("dr_j2j3","deltaR_jet(Jet_pt,Jet_eta,Jet_phi,Jet_mass,JetMatched_idx,3)")\
             .Define("ttc_mllj1","mllj_jesr(ttc_l1_pt,ttc_l1_eta,ttc_l1_phi,ttc_l1_mass,ttc_l2_pt,ttc_l2_eta,ttc_l2_phi,ttc_l2_mass,Jet_pt_nom,Jet_eta,Jet_phi,Jet_mass_nom,JetMatched_idx,1)")\
             .Define("ttc_mllj2","mllj_jesr(ttc_l1_pt,ttc_l1_eta,ttc_l1_phi,ttc_l1_mass,ttc_l2_pt,ttc_l2_eta,ttc_l2_phi,ttc_l2_mass,Jet_pt_nom,Jet_eta,Jet_phi,Jet_mass_nom,JetMatched_idx,2)")\
             .Define("ttc_mllj3","mllj_jesr(ttc_l1_pt,ttc_l1_eta,ttc_l1_phi,ttc_l1_mass,ttc_l2_pt,ttc_l2_eta,ttc_l2_phi,ttc_l2_mass,Jet_pt_nom,Jet_eta,Jet_phi,Jet_mass_nom,JetMatched_idx,3)")\
             .Define("m_j1j2","mjj(Jet_pt,Jet_eta,Jet_phi,Jet_mass,JetMatched_idx,1)")\
             .Define("m_j1j3","mjj(Jet_pt,Jet_eta,Jet_phi,Jet_mass,JetMatched_idx,2)")\
             .Define("m_j2j3","mjj(Jet_pt,Jet_eta,Jet_phi,Jet_mass,JetMatched_idx,3)")\
             .Define("m_j1l1","mll(j1_pt, j1_eta, j1_phi, j1_mass, ttc_l1_pt, ttc_l1_eta, ttc_l1_phi, ttc_l1_mass)")\
             .Define("m_j1l2","mll(j1_pt, j1_eta, j1_phi, j1_mass, ttc_l2_pt, ttc_l2_eta, ttc_l2_phi, ttc_l2_mass)")\
             .Define("m_j2l1","mll(j2_pt, j2_eta, j2_phi, j2_mass, ttc_l1_pt, ttc_l1_eta, ttc_l1_phi, ttc_l1_mass)")\
             .Define("m_j2l2","mll(j2_pt, j2_eta, j2_phi, j2_mass, ttc_l2_pt, ttc_l2_eta, ttc_l2_phi, ttc_l2_mass)")\
             .Define("m_j3l1","mll(j3_pt, j3_eta, j3_phi, j3_mass, ttc_l1_pt, ttc_l1_eta, ttc_l1_phi, ttc_l1_mass)")\
             .Define("m_j3l2","mll(j3_pt, j3_eta, j3_phi, j3_mass, ttc_l2_pt, ttc_l2_eta, ttc_l2_phi, ttc_l2_mass)")\
             .Define("m_j1j2l1", "inv_mass(j1_pt, j1_eta, j1_phi, j1_mass, j2_pt, j2_eta, j2_phi, j2_mass, ttc_l1_pt, ttc_l1_eta, ttc_l1_phi, ttc_l1_mass)")\
             .Define("m_j1j2l2", "inv_mass(j1_pt, j1_eta, j1_phi, j1_mass, j2_pt, j2_eta, j2_phi, j2_mass, ttc_l2_pt, ttc_l2_eta, ttc_l2_phi, ttc_l2_mass)")\
             .Define("m_j1j3l1", "inv_mass(j1_pt, j1_eta, j1_phi, j1_mass, j3_pt, j3_eta, j3_phi, j3_mass, ttc_l1_pt, ttc_l1_eta, ttc_l1_phi, ttc_l1_mass)")\
             .Define("m_j1j3l2", "inv_mass(j1_pt, j1_eta, j1_phi, j1_mass, j3_pt, j3_eta, j3_phi, j3_mass, ttc_l2_pt, ttc_l2_eta, ttc_l2_phi, ttc_l2_mass)")\
             .Define("m_j2j3l1", "inv_mass(j2_pt, j2_eta, j2_phi, j2_mass, j3_pt, j3_eta, j3_phi, j3_mass, ttc_l1_pt, ttc_l1_eta, ttc_l1_phi, ttc_l1_mass)")\
             .Define("m_j2j3l2", "inv_mass(j2_pt, j2_eta, j2_phi, j2_mass, j3_pt, j3_eta, j3_phi, j3_mass, ttc_l2_pt, ttc_l2_eta, ttc_l2_phi, ttc_l2_mass)")\
             .Define("dr_j1l1", "deltaR(j1_pt, j1_eta, j1_phi, j1_mass, ttc_l1_pt, ttc_l1_eta, ttc_l1_phi, ttc_l1_mass)")\
             .Define("dr_j1l2", "deltaR(j1_pt, j1_eta, j1_phi, j1_mass, ttc_l2_pt, ttc_l2_eta, ttc_l2_phi, ttc_l2_mass)")\
             .Define("dr_j2l1", "deltaR(j2_pt, j2_eta, j2_phi, j2_mass, ttc_l1_pt, ttc_l1_eta, ttc_l1_phi, ttc_l1_mass)")\
             .Define("dr_j2l2", "deltaR(j2_pt, j2_eta, j2_phi, j2_mass, ttc_l2_pt, ttc_l2_eta, ttc_l2_phi, ttc_l2_mass)")\
             .Define("dr_j3l1", "deltaR(j3_pt, j3_eta, j3_phi, j3_mass, ttc_l1_pt, ttc_l1_eta, ttc_l1_phi, ttc_l1_mass)")\
             .Define("dr_j3l2", "deltaR(j3_pt, j3_eta, j3_phi, j3_mass, ttc_l2_pt, ttc_l2_eta, ttc_l2_phi, ttc_l2_mass)")\
             .Define("mu_id","muid(ttc_l1_pt,ttc_l1_eta,ttc_l2_pt,ttc_l2_eta,ttc_region)")\
             .Define("ele_id","eleid(ttc_l1_pt,ttc_l1_eta,ttc_l2_pt,ttc_l2_eta,ttc_region)")\
             .Define("trig_SF","lep_trigger(ttc_l1_pt,ttc_l2_pt,ttc_region)")\
             .Define("ctag_SF","ctagSF(tightJets_id_in24,Jet_puId,Jet_pt_nom,Jet_hadronFlavour,Jet_btagDeepFlavCvB,Jet_btagDeepFlavCvL,0)")\
             .Define("fakeweight",str(fakeweight_definition))\
             .Define("fakeweight_ele_statUp",str(fakeweight_ele_statUp_definition))\
             .Define("fakeweight_ele_statDo",str(fakeweight_ele_statDo_definition))\
             .Define("fakeweight_mu_statUp",str(fakeweight_mu_statUp_definition))\
             .Define("fakeweight_mu_statDo",str(fakeweight_mu_statDo_definition))
  columns = ROOT.std.vector("string")()
  for c in ('ttc_region','genweight','HT','j1_pt','j1_eta','j1_phi','j1_mass','j2_pt','j2_eta','j2_phi','j2_mass','j3_pt','j3_eta','j3_phi','j3_mass','j1_FlavB','j1_FlavCvB','j1_FlavCvL','j2_FlavB','j2_FlavCvB','j2_FlavCvL','j3_FlavB','j3_FlavCvB','j3_FlavCvL','PV_npvsGood','PV_x','PV_y','PV_z','nSV','ttc_l1_pt','ttc_l1_eta','ttc_l1_phi','ttc_l1_mass','ttc_l2_pt','ttc_l2_eta','ttc_l2_phi','ttc_l2_mass','ttc_met','ttc_met_phi','ttc_mll','ttc_mllj1','ttc_mllj2','ttc_mllj3','puWeight','dr_j1j2','dr_j1j3','dr_j2j3','m_j1j2','m_j1j3','m_j2j3','mu_id','ele_id','trig_SF','ctag_SF','fakeweight','fakeweight_ele_statUp','fakeweight_ele_statDo','fakeweight_mu_statUp','fakeweight_mu_statDo', 'm_j1l1','m_j1l2','m_j2l1', 'm_j2l2', 'm_j3l1', 'm_j3l2', 'm_j1j2l1', 'm_j1j2l2', 'm_j2j3l1', 'm_j2j3l2', 'm_j1j3l1', 'm_j1j3l2', 'dr_j1l1','dr_j1l2','dr_j2l1','dr_j2l2','dr_j3l1','dr_j3l2'):
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
  parser.add_option('-c','--channel',dest='channel', help='[DoubleElectron/DoubleMuon/ElectronMuon]')

  (args,opt) = parser.parse_args()

  iin = args.iin
  istrain = args.train
  flag = args.flag
  channel = args.channel
  era = args.era
  
  path = str(inputFile_path_skim[era])

  print('Processing ',path+iin)
  ftemp=ROOT.TFile.Open(path+iin)
  ttemp=ftemp.Get('Events')
  ntemp=ttemp.GetEntriesFast()
  if istrain:
    ntemp = ntemp*0.5
  #those samples are used for BDT training, so only half of the events will be used in the application
  Slim_module(iin,ntemp,flag,istrain, channel, era)
  ftemp.Close()

  end = time.time()
  end1 = time.clock()
  print "wall time:", end-start
  print "process time:", end1-start1
