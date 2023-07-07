import ROOT
#import time
import os, sys
import math
import json
import optparse
from collections import OrderedDict
from math import sqrt
from common import inputFile_path
from common import GetTrigger_MC, GetMETFilter_MC
from DNN_application import Build_DNN_Command 

ROOT.gSystem.Load("libGenVector.so")


def Slim_module(filein,nin,mass_flag,era):

  TTC_header_path = os.path.join("script/slim_"+era+".h")
  pyTorch_header_path = os.path.join("script/","DNN_Flav_MET_threeJet_model.hxx")
  #ROOT.gInterpreter.Declare('#include "{}"'.format(pyTorch_header_path))
#  ROOT.gSystem.AddIncludePath(' -I{}'.format(os.getcwd()))
  ROOT.gInterpreter.Declare('#include "{}"'.format(TTC_header_path))
  path = str(inputFile_path[era])


  filters="(((ttc_region==1 || ttc_region==3) && ttc_l1_pt>30) || (ttc_region==2 && (ttc_l1_pt>30 || ttc_l2_pt>30))) && ttc_jets && ttc_met>30 && ttc_mll>20 && ttc_drll>0.3 && nHad_tau==0 && ttc_2P0F"

  Trigger      = GetTrigger_MC(era)
  MET_filters  = GetMETFilter_MC(era, filein)

  filters      = str("(" + filters + ") && (" + MET_filters + ")")

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
      print ("Interference samples")
      df_filein_tree_temp = ROOT.RDataFrame("Events",path+filein)
      df_filein_tree = df_filein_tree_temp.Range(int(nevent))
    elif "highmass.root" in filein.split('_'):
      print ("===> highmass samples <===")
      fileOut = filein.split('_')[0]+'_'+filein.split('_')[1]+'_'+filein.split('_')[3]+'_M'+filein.split('_')[1].upper()+filein.split('_')[2]+".root"
      fileOut = "sample/" + era + "/" + fileOut
      print ("Output filename changed to: ", fileOut)
      df_filein_tree_temp = ROOT.RDataFrame("Events",path+filein)
      df_filein_tree = df_filein_tree_temp.Range(int(nevent))
    else:
      print ("normal samples")
      fileOut = filein.split('.')[0]+'_'+mass_flag.split('_')[2]+mass_flag.split('_')[3]+".root"
      fileOut = "sample/" + era + "/" + fileOut
      print ("Output filename changed to: ", fileOut)
      df_filein_tree_temp = ROOT.RDataFrame("Events",path+filein)
      df_filein_tree_temp2 = df_filein_tree_temp.Filter(mass_flag)
      df_filein_tree = df_filein_tree_temp2.Range(int(nevent))
  else:
    df_filein_tree_temp = ROOT.RDataFrame("Events",path+filein)
    df_filein_tree = df_filein_tree_temp.Range(int(nevent))

  df_filein_tree = df_filein_tree.Define("genweight","puWeight*genWeight/abs(genWeight)")
  df_filein = df_filein_tree.Filter(filters)
  dOut = df_filein.Filter(Trigger)
  # JetMatchIdx 
  dOut = Build_DNN_Command('Flav_MET_threeJet_model_v2',dOut) #JetMatched_idx is defined in this function
  dOut = dOut.Define("j1_pt_DNN",   "Jet_pt[JetMatched_idx[0]]")\
             .Define("j1_eta_DNN",  "Jet_eta[JetMatched_idx[0]]")\
             .Define("j1_phi_DNN",  "Jet_phi[JetMatched_idx[0]]")\
             .Define("j1_mass_DNN", "Jet_mass[JetMatched_idx[0]]")\
             .Define("j1_FlavB_DNN","Jet_btagDeepFlavB[JetMatched_idx[0]]")\
             .Define("j1_FlavCvB_DNN","Jet_btagDeepFlavCvB[JetMatched_idx[0]]")\
             .Define("j1_FlavCvL_DNN","Jet_btagDeepFlavCvL[JetMatched_idx[0]]")\
             .Define("j2_pt_DNN",   "Jet_pt[JetMatched_idx[1]]")\
             .Define("j2_eta_DNN",  "Jet_eta[JetMatched_idx[1]]")\
             .Define("j2_phi_DNN",  "Jet_phi[JetMatched_idx[1]]")\
             .Define("j2_mass_DNN", "Jet_mass[JetMatched_idx[1]]")\
             .Define("j2_FlavB_DNN","Jet_btagDeepFlavB[JetMatched_idx[1]]")\
             .Define("j2_FlavCvB_DNN","Jet_btagDeepFlavCvB[JetMatched_idx[1]]")\
             .Define("j2_FlavCvL_DNN","Jet_btagDeepFlavCvL[JetMatched_idx[1]]")\
             .Define("j3_pt_DNN",   "Jet_pt[JetMatched_idx[2]]")\
             .Define("j3_eta_DNN",  "Jet_eta[JetMatched_idx[2]]")\
             .Define("j3_phi_DNN",  "Jet_phi[JetMatched_idx[2]]")\
             .Define("j3_mass_DNN", "Jet_mass[JetMatched_idx[2]]")\
             .Define("j3_FlavB_DNN","Jet_btagDeepFlavB[JetMatched_idx[2]]")\
             .Define("j3_FlavCvB_DNN","Jet_btagDeepFlavCvB[JetMatched_idx[2]]")\
             .Define("j3_FlavCvL_DNN","Jet_btagDeepFlavCvL[JetMatched_idx[2]]")\
             .Define("dr_j1j2_DNN","deltaR_jet(Jet_pt,Jet_eta,Jet_phi,Jet_mass,JetMatched_idx,1)")\
             .Define("dr_j1j3_DNN","deltaR_jet(Jet_pt,Jet_eta,Jet_phi,Jet_mass,JetMatched_idx,2)")\
             .Define("dr_j2j3_DNN","deltaR_jet(Jet_pt,Jet_eta,Jet_phi,Jet_mass,JetMatched_idx,3)")\
             .Define("m_j1j2_DNN","mjj(Jet_pt,Jet_eta,Jet_phi,Jet_mass,JetMatched_idx,1)")\
             .Define("m_j1j3_DNN","mjj(Jet_pt,Jet_eta,Jet_phi,Jet_mass,JetMatched_idx,2)")\
             .Define("m_j2j3_DNN","mjj(Jet_pt,Jet_eta,Jet_phi,Jet_mass,JetMatched_idx,3)")\
             .Define("m_j1l1_DNN","mll(j1_pt_DNN, j1_eta_DNN, j1_phi_DNN, j1_mass_DNN, ttc_l1_pt, ttc_l1_eta, ttc_l1_phi, ttc_l1_mass)")\
             .Define("m_j1l2_DNN","mll(j1_pt_DNN, j1_eta_DNN, j1_phi_DNN, j1_mass_DNN, ttc_l2_pt, ttc_l2_eta, ttc_l2_phi, ttc_l2_mass)")\
             .Define("m_j2l1_DNN","mll(j2_pt_DNN, j2_eta_DNN, j2_phi_DNN, j2_mass_DNN, ttc_l1_pt, ttc_l1_eta, ttc_l1_phi, ttc_l1_mass)")\
             .Define("m_j2l2_DNN","mll(j2_pt_DNN, j2_eta_DNN, j2_phi_DNN, j2_mass_DNN, ttc_l2_pt, ttc_l2_eta, ttc_l2_phi, ttc_l2_mass)")\
             .Define("m_j3l1_DNN","mll(j3_pt_DNN, j3_eta_DNN, j3_phi_DNN, j3_mass_DNN, ttc_l1_pt, ttc_l1_eta, ttc_l1_phi, ttc_l1_mass)")\
             .Define("m_j3l2_DNN","mll(j3_pt_DNN, j3_eta_DNN, j3_phi_DNN, j3_mass_DNN, ttc_l2_pt, ttc_l2_eta, ttc_l2_phi, ttc_l2_mass)")\
             .Define("m_j1j2l1_DNN", "inv_mass(j1_pt_DNN, j1_eta_DNN, j1_phi_DNN, j1_mass_DNN, j2_pt_DNN, j2_eta_DNN, j2_phi_DNN, j2_mass_DNN, ttc_l1_pt, ttc_l1_eta, ttc_l1_phi, ttc_l1_mass)")\
             .Define("m_j1j2l2_DNN", "inv_mass(j1_pt_DNN, j1_eta_DNN, j1_phi_DNN, j1_mass_DNN, j2_pt_DNN, j2_eta_DNN, j2_phi_DNN, j2_mass_DNN, ttc_l2_pt, ttc_l2_eta, ttc_l2_phi, ttc_l2_mass)")\
             .Define("m_j1j3l1_DNN", "inv_mass(j1_pt_DNN, j1_eta_DNN, j1_phi_DNN, j1_mass_DNN, j3_pt_DNN, j3_eta_DNN, j3_phi_DNN, j3_mass_DNN, ttc_l1_pt, ttc_l1_eta, ttc_l1_phi, ttc_l1_mass)")\
             .Define("m_j1j3l2_DNN", "inv_mass(j1_pt_DNN, j1_eta_DNN, j1_phi_DNN, j1_mass_DNN, j3_pt_DNN, j3_eta_DNN, j3_phi_DNN, j3_mass_DNN, ttc_l2_pt, ttc_l2_eta, ttc_l2_phi, ttc_l2_mass)")\
             .Define("m_j2j3l1_DNN", "inv_mass(j2_pt_DNN, j2_eta_DNN, j2_phi_DNN, j2_mass_DNN, j3_pt_DNN, j3_eta_DNN, j3_phi_DNN, j3_mass_DNN, ttc_l1_pt, ttc_l1_eta, ttc_l1_phi, ttc_l1_mass)")\
             .Define("m_j2j3l2_DNN", "inv_mass(j2_pt_DNN, j2_eta_DNN, j2_phi_DNN, j2_mass_DNN, j3_pt_DNN, j3_eta_DNN, j3_phi_DNN, j3_mass_DNN, ttc_l2_pt, ttc_l2_eta, ttc_l2_phi, ttc_l2_mass)")\
             .Define("dr_j1l1_DNN", "deltaR(j1_pt_DNN, j1_eta_DNN, j1_phi_DNN, j1_mass_DNN, ttc_l1_pt, ttc_l1_eta, ttc_l1_phi, ttc_l1_mass)")\
             .Define("dr_j1l2_DNN", "deltaR(j1_pt_DNN, j1_eta_DNN, j1_phi_DNN, j1_mass_DNN, ttc_l2_pt, ttc_l2_eta, ttc_l2_phi, ttc_l2_mass)")\
             .Define("dr_j2l1_DNN", "deltaR(j2_pt_DNN, j2_eta_DNN, j2_phi_DNN, j2_mass_DNN, ttc_l1_pt, ttc_l1_eta, ttc_l1_phi, ttc_l1_mass)")\
             .Define("dr_j2l2_DNN", "deltaR(j2_pt_DNN, j2_eta_DNN, j2_phi_DNN, j2_mass_DNN, ttc_l2_pt, ttc_l2_eta, ttc_l2_phi, ttc_l2_mass)")\
             .Define("dr_j3l1_DNN", "deltaR(j3_pt_DNN, j3_eta_DNN, j3_phi_DNN, j3_mass_DNN, ttc_l1_pt, ttc_l1_eta, ttc_l1_phi, ttc_l1_mass)")\
             .Define("dr_j3l2_DNN", "deltaR(j3_pt_DNN, j3_eta_DNN, j3_phi_DNN, j3_mass_DNN, ttc_l2_pt, ttc_l2_eta, ttc_l2_phi, ttc_l2_mass)")\
             .Define("ttc_mllj1_DNN","mllj_jesr(ttc_l1_pt,ttc_l1_eta,ttc_l1_phi,ttc_l1_mass,ttc_l2_pt,ttc_l2_eta,ttc_l2_phi,ttc_l2_mass,Jet_pt_nom,Jet_eta,Jet_phi,Jet_mass_nom,JetMatched_idx,1)")\
             .Define("ttc_mllj2_DNN","mllj_jesr(ttc_l1_pt,ttc_l1_eta,ttc_l1_phi,ttc_l1_mass,ttc_l2_pt,ttc_l2_eta,ttc_l2_phi,ttc_l2_mass,Jet_pt_nom,Jet_eta,Jet_phi,Jet_mass_nom,JetMatched_idx,2)")\
             .Define("ttc_mllj3_DNN","mllj_jesr(ttc_l1_pt,ttc_l1_eta,ttc_l1_phi,ttc_l1_mass,ttc_l2_pt,ttc_l2_eta,ttc_l2_phi,ttc_l2_mass,Jet_pt_nom,Jet_eta,Jet_phi,Jet_mass_nom,JetMatched_idx,3)")
  # Pt ordering (Default)
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
             .Define("m_j2j3","mjj(Jet_pt,Jet_eta,Jet_phi,Jet_mass,tightJets_id_in24,3)")\
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
             .Define("dr_j3l2", "deltaR(j3_pt, j3_eta, j3_phi, j3_mass, ttc_l2_pt, ttc_l2_eta, ttc_l2_phi, ttc_l2_mass)")


  columns = ROOT.std.vector("string")()
  for c in ('ttc_region','genweight','HT','j1_pt','j1_eta','j1_phi','j1_mass','j2_pt','j2_eta','j2_phi','j2_mass','j3_pt','j3_eta','j3_phi','j3_mass','j1_FlavB','j1_FlavCvB','j1_FlavCvL','j2_FlavB','j2_FlavCvB','j2_FlavCvL','j3_FlavB','j3_FlavCvB','j3_FlavCvL','PV_npvsGood','PV_x','PV_y','PV_z','nSV','ttc_l1_pt','ttc_l1_eta','ttc_l1_phi','ttc_l1_mass','ttc_l2_pt','ttc_l2_eta','ttc_l2_phi','ttc_l2_mass','ttc_met','ttc_met_phi','ttc_mll','ttc_mllj1','ttc_mllj2','ttc_mllj3','puWeight','dr_j1j2','dr_j1j3','dr_j2j3','m_j1j2','m_j1j3','m_j2j3','m_j1l1','m_j1l2','m_j2l1', 'm_j2l2', 'm_j3l1', 'm_j3l2', 'm_j1j2l1', 'm_j1j2l2', 'm_j2j3l1', 'm_j2j3l2', 'm_j1j3l1', 'm_j1j3l2', 'dr_j1l1','dr_j1l2','dr_j2l1','dr_j2l2','dr_j3l1','dr_j3l2','tightJets_id_in24',\
'j1_pt_DNN', 'j1_eta_DNN', 'j1_phi_DNN', 'j1_mass_DNN', 'j2_pt_DNN', 'j2_eta_DNN', 'j2_phi_DNN', 'j2_mass_DNN', 'j3_pt_DNN', 'j3_eta_DNN', 'j3_phi_DNN', 'j3_mass_DNN', 'j1_FlavB_DNN', 'j1_FlavCvB_DNN', 'j1_FlavCvL_DNN', 'j2_FlavB_DNN', 'j2_FlavCvB_DNN', 'j2_FlavCvL_DNN', 'j3_FlavB_DNN', 'j3_FlavCvB_DNN', 'j3_FlavCvL_DNN', 'ttc_mllj1_DNN', 'ttc_mllj2_DNN', 'ttc_mllj3_DNN', 'dr_j1j2_DNN', 'dr_j1j3_DNN', 'dr_j2j3_DNN', 'm_j1j2_DNN', 'm_j1j3_DNN', 'm_j2j3_DNN', 'm_j1l1_DNN', 'm_j1l2_DNN', 'm_j2l1_DNN', 'm_j2l2_DNN', 'm_j3l1_DNN', 'm_j3l2_DNN', 'm_j1j2l1_DNN', 'm_j1j2l2_DNN', 'm_j2j3l1_DNN', 'm_j2j3l2_DNN', 'm_j1j3l1_DNN', 'm_j1j3l2_DNN', 'dr_j1l1_DNN', 'dr_j1l2_DNN', 'dr_j2l1_DNN', 'dr_j2l2_DNN', 'dr_j3l1_DNN', 'dr_j3l2_DNN','JetMatched_idx'):
    columns.push_back(c)
  dOut.Snapshot(treeOut,fileOut,columns)

if __name__ == "__main__":
#  start = time.time()
#  start1 = time.clock()

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

  path = str(inputFile_path[era])

  print('Processing ',path+iin)
  ftemp=ROOT.TFile.Open(path+iin)
  ttemp=ftemp.Get('Events')
  if flag=='dummy':
    ntemp=ttemp.GetEntriesFast()
  else:
    ntemp=ttemp.GetEntries(flag)
  # Samples used for BDT training only leaves half of the events in the application while others use full events
  ntrain = ntemp*0.5 if istrain else ntemp
  Slim_module(iin,ntrain,flag,era)
  ftemp.Close()


#  end = time.time()
#  end1 = time.clock()
#  print( "wall time:", end-start)
#  print( "process time:", end1-start1)
