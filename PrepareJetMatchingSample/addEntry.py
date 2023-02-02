import torch
import ROOT
import time
from array import array
import optparse
import numba as nb
import awkward as ak
import pandas as pd
import vector
import numpy as np
from torch import nn
from itertools import combinations, permutations
import uproot
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer


ROOT.gSystem.Load("libGenVector.so")
np.finfo(np.dtype("float32"))

class NeuralNetwork(nn.Module):
    def __init__(self,nvars):
        # return a temporary object of superclass so we can call superclass' methods
        super(NeuralNetwork, self).__init__()
        # Initialise layers
        self.linear_relu_stack = nn.Sequential(
            nn.Flatten(), #Flattens contiguous range of dimensions into a tensor
            nn.Linear(nvars,24),
            nn.ReLU(),
            nn.Linear(24,12),
            nn.ReLU(),
            nn.Linear(12,8),
            nn.ReLU(),
            nn.Linear(8,4),
            nn.ReLU(),
            nn.Linear(4,1),
        )
    # Method to implement operations on input data
    # Passing input data to model automatically executes models forward method
    def forward(self, x):
        logits = self.linear_relu_stack(x)
        return logits

#@nb.njit
def compute_di_mass(v1, v2):
    return (v1 + v2).mass

def AddEntry(fin_name):

  # Update ROOT file
  fin = ROOT.TFile(fin_name, 'update')
  tree_name = 'Events'
  t = fin.Get(tree_name)
  matched_idx = array('i',[-1,-1,-1,-1])
  Branch_idx  = t.Branch("JetMatched_idx",matched_idx,"JetMatched_idx[4]/I")
  nentries    = t.GetEntries()
  run_event   = nentries

  # Use uproot to process data
  try:
    events = uproot.open(fin_name + ":" + tree_name)
  except FileNotFoundError():
    raise FileNotFoundError('Input tree &s not found! ' % (fin_name + ":" + tree_name))
  
  # Create Jet 4-vectors
  Jet_pt         = events.arrays(['Jet_pt_nom'],   entry_stop=run_event)['Jet_pt_nom']
  Jet_eta        = events.arrays(['Jet_eta'],      entry_stop=run_event)['Jet_eta']
  Jet_phi        = events.arrays(['Jet_phi'],      entry_stop=run_event)['Jet_phi']
  Jet_mass       = events.arrays(['Jet_mass_nom'], entry_stop=run_event)['Jet_mass_nom']
  Jet_p4         = vector.zip({'pt':Jet_pt, 'eta':Jet_eta, 'phi':Jet_phi, 'mass':Jet_mass})
  tight_jet_id   = events.arrays(['tightJets_id_in24'], entry_stop=run_event)['tightJets_id_in24']
  n_tight_jet    = events.arrays(['n_tight_jet'],  entry_stop=run_event)['n_tight_jet']
  # Create lepton 4-vectors
  l1_pt          = events.arrays(['ttc_l1_pt'],   entry_stop=run_event)['ttc_l1_pt']
  l1_eta         = events.arrays(['ttc_l1_eta'],  entry_stop=run_event)['ttc_l1_eta']
  l1_phi         = events.arrays(['ttc_l1_phi'],  entry_stop=run_event)['ttc_l1_phi']
  l1_mass        = events.arrays(['ttc_l1_mass'], entry_stop=run_event)['ttc_l1_mass']
  l1_p4          = vector.zip({'pt':l1_pt, 'eta':l1_eta, 'phi':l1_phi, 'mass':l1_mass})
  l2_pt          = events.arrays(['ttc_l2_pt'],   entry_stop=run_event)['ttc_l2_pt']
  l2_eta         = events.arrays(['ttc_l2_eta'],  entry_stop=run_event)['ttc_l2_eta']
  l2_phi         = events.arrays(['ttc_l2_phi'],  entry_stop=run_event)['ttc_l2_phi']
  l2_mass        = events.arrays(['ttc_l2_mass'], entry_stop=run_event)['ttc_l2_mass']
  l2_p4          = vector.zip({'pt':l2_pt, 'eta':l2_eta, 'phi':l2_phi, 'mass':l2_mass})


  # Load DNN 
  model = NeuralNetwork(30)
  model.load_state_dict(torch.load('../../HiggsReco/training/model_1e-05_500_100/saved_model.pt'))
  model.eval()

  # Prepare dataframe
  df =[]
  for row in range(0, len(Jet_pt)):
    tight_jet_id_skim = tight_jet_id[row][:min(n_tight_jet[row],6)]
    combinations_list = list(combinations(tight_jet_id_skim, 2 ))

    bmatched_jet_pt = []
    bmatched_jet_eta = []
    bmatched_jet_phi = []
    bmatched_jet_mass = []
    bmatched_jet_index = []
    lmatched_jet_pt = []
    lmatched_jet_eta = []
    lmatched_jet_phi = []
    lmatched_jet_mass = []
    lmatched_jet_index = []
    dR_bmatched_lmatched_jets = []
    dR_bmatched_jet_lep1 = []
    dR_bmatched_jet_lep2 = []
    dR_lmatched_jet_lep1 = []
    dR_lmatched_jet_lep2 = []
    invmass_bjlj = []
    jet3_pt = []
    jet3_eta = []
    jet3_phi = []
    jet3_mass = []
    jet3_index = []
    jet4_pt = []
    jet4_eta = []
    jet4_phi = []
    jet4_mass = []
    jet4_index = []
    leading_lept_pt = []
    leading_lept_eta = []
    leading_lept_phi = []
    leading_lept_mass = []
    subleading_lept_pt = []
    subleading_lept_eta = []
    subleading_lept_phi = []
    subleading_lept_mass = []

    for comb_ in combinations_list:
      bmatched_jet_pt.append(Jet_pt[row][comb_[0]])
      bmatched_jet_eta.append(Jet_eta[row][comb_[0]])
      bmatched_jet_phi.append(Jet_phi[row][comb_[0]])
      bmatched_jet_mass.append(Jet_mass[row][comb_[0]])
      bmatched_jet_index.append(comb_[0])
      lmatched_jet_pt.append(Jet_pt[row][comb_[1]])
      lmatched_jet_eta.append(Jet_eta[row][comb_[1]])
      lmatched_jet_phi.append(Jet_phi[row][comb_[1]])
      lmatched_jet_mass.append(Jet_mass[row][comb_[1]])
      lmatched_jet_index.append(comb_[1])
      dR_bmatched_lmatched_jets.append(Jet_p4[row][comb_[0]].deltaR(Jet_p4[row][comb_[1]]))
      dR_bmatched_jet_lep1.append(Jet_p4[row][comb_[0]].deltaR(l1_p4[row]))
      dR_bmatched_jet_lep2.append(Jet_p4[row][comb_[0]].deltaR(l2_p4[row]))
      dR_lmatched_jet_lep1.append(Jet_p4[row][comb_[1]].deltaR(l1_p4[row]))
      dR_lmatched_jet_lep2.append(Jet_p4[row][comb_[1]].deltaR(l2_p4[row]))
      j1_p4 = vector.obj(pt=Jet_pt[row][comb_[0]], eta=Jet_eta[row][comb_[0]], phi=Jet_phi[row][comb_[0]], mass=Jet_mass[row][comb_[0]])
      j2_p4 = vector.obj(pt=Jet_pt[row][comb_[1]], eta=Jet_eta[row][comb_[1]], phi=Jet_phi[row][comb_[1]], mass=Jet_mass[row][comb_[1]])
      invmass_bjlj.append(compute_di_mass(j1_p4, j2_p4))
      
      jet3_index_ = -1
      jet4_index_ = -1
      for idx in tight_jet_id_skim:
        if idx not in [comb_[0], comb_[1]] and jet3_index_ == -1:
          jet3_index_ = idx
          jet3_pt.append(Jet_p4[row][idx].pt)
          jet3_eta.append(Jet_p4[row][idx].eta)
          jet3_phi.append(Jet_p4[row][idx].phi)
          jet3_mass.append(Jet_p4[row][idx].mass)
        elif idx not in [comb_[0], comb_[1], jet3_index_]:
          jet4_index_ = idx
          jet4_pt.append(Jet_p4[row][idx].pt)
          jet4_eta.append(Jet_p4[row][idx].eta)
          jet4_phi.append(Jet_p4[row][idx].phi)
          jet4_mass.append(Jet_p4[row][idx].mass)
          break
      if jet4_index_ == -1:
          jet4_pt.append(0)
          jet4_eta.append(0)
          jet4_phi.append(0)
          jet4_mass.append(0)
      jet3_index.append(jet3_index_)
      jet4_index.append(jet4_index_)

      leading_lept_pt.append(l1_pt[row])
      leading_lept_eta.append(l1_eta[row])
      leading_lept_phi.append(l1_phi[row])
      leading_lept_mass.append(l1_mass[row])
      subleading_lept_pt.append(l2_pt[row])
      subleading_lept_eta.append(l2_eta[row])
      subleading_lept_phi.append(l2_phi[row])
      subleading_lept_mass.append(l2_mass[row])


      

     # print(in_array)
     # with torch.no_grad():
     #   print(model(in_array)[0][0].item())
    d_entries = {
       'Entry': row,
       'bmatched_jet_index': bmatched_jet_index,
       'lmatched_jet_index': lmatched_jet_index,
       'jet3_index': jet3_index,
       'jet4_index': jet4_index,
       'bmatched_jet_pt': bmatched_jet_pt,
       'bmatched_jet_eta': bmatched_jet_eta,
       'bmatched_jet_phi': bmatched_jet_phi,
       'bmatched_jet_mass': bmatched_jet_mass,
       'lmatched_jet_pt': lmatched_jet_pt,
       'lmatched_jet_eta': lmatched_jet_eta,
       'lmatched_jet_phi': lmatched_jet_phi,
       'lmatched_jet_mass': lmatched_jet_mass,
       'dR_bmatched_lmatched_jets': dR_bmatched_lmatched_jets,
       'dR_bmatched_jet_lep1': dR_bmatched_jet_lep1,
       'dR_bmatched_jet_lep2': dR_bmatched_jet_lep2,
       'dR_lmatched_jet_lep1': dR_lmatched_jet_lep1,
       'dR_lmatched_jet_lep2': dR_lmatched_jet_lep2,
       'invmass_bjlj': invmass_bjlj,
       'lep1_pt': leading_lept_pt,
       'lep1_eta': leading_lept_eta,
       'lep1_phi': leading_lept_phi,
       'lep1_mass': leading_lept_mass,
       'lep2_pt': subleading_lept_pt,
       'lep2_eta': subleading_lept_eta,
       'lep2_phi': subleading_lept_phi,
       'lep2_mass': subleading_lept_mass,
       'jet3_pt': jet3_pt,
       'jet3_eta': jet3_eta,
       'jet3_phi': jet3_phi,
       'jet3_mass': jet3_mass,
       'jet4_pt': jet4_pt,
       'jet4_eta': jet4_eta,
       'jet4_phi': jet4_phi,
       'jet4_mass': jet4_mass
    }
    df_ = pd.DataFrame(data=d_entries)
    df.append(df_)
  df = pd.concat(df)
  # Data Preprocessing
  colnames = list(d_entries.keys())
  ct = ColumnTransformer(
  [('StandardScaler', StandardScaler(), colnames[5:] )],
      remainder='drop'# Drop nontransformed columns
  )
  index_ = df[colnames[:5]]
  result_ = ct.fit_transform(df)
  result_ = np.c_[index_, result_]
  transformed_df = pd.DataFrame(result_,columns=colnames)
  transformed_df = transformed_df.astype({'Entry':"int",'bmatched_jet_index':'int','lmatched_jet_index':'int','jet3_index':'int','jet4_index':'int'})
  print(transformed_df)
  input_columns_ = [
    'bmatched_jet_pt','bmatched_jet_eta','bmatched_jet_phi','bmatched_jet_mass',
    'lmatched_jet_pt','lmatched_jet_eta','lmatched_jet_phi','lmatched_jet_mass',
    'dR_bmatched_lmatched_jets','dR_bmatched_jet_lep1','dR_bmatched_jet_lep2','dR_lmatched_jet_lep1','dR_lmatched_jet_lep2',
    'invmass_bjlj',
    'lep1_pt','lep1_eta','lep1_phi','lep1_mass',
    'lep2_pt','lep2_eta','lep2_phi','lep2_mass',
    'jet3_pt','jet3_eta','jet3_phi','jet3_mass',
    'jet4_pt','jet4_eta','jet4_phi','jet4_mass'
  ]
  source_combs = transformed_df[input_columns_].values
  X_input      = torch.tensor(source_combs, dtype=torch.float32)
  predicted    = torch.sigmoid(model(X_input)).detach().numpy()
  predicted    = np.array(predicted.reshape(len(predicted)))
  transformed_df.insert(1, "predicted", predicted)
  idx = transformed_df.groupby(['Entry'])['predicted'].transform(max) == transformed_df['predicted']
  df = transformed_df[idx]
  df = df.set_index("Entry")
  
  print(df)

  for entry in range(run_event):
    t.GetEntry(entry)
    matched_idx[0] = df['bmatched_jet_index'][entry]
    matched_idx[1] = df['lmatched_jet_index'][entry]
    matched_idx[2] = df['jet3_index'][entry]
    matched_idx[3] = df['jet4_index'][entry]
    Branch_idx.Fill()

  t.Write()



  fin.Close()

  return 0
if __name__ == "__main__":
  start = time.time()

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
  mass_flag = args.flag
  isMC = (args.Type == "MC")
  channel = args.channel


  fileIn = iin.split('.')[0]+".root"

  if not isMC:
    if channel == 'DoubleMuon':
      channel_name = 'mm'
    elif channel == 'DoubleElectron':
      channel_name = 'ee'
    elif channel == 'ElectronMuon':
      channel_name = 'em'

    fileIn = iin.split('.')[0]+"_" + channel_name + ".root"
  fileIn = "/eos/user/t/tihsu/BDT/ntuple_skim/" + era + "/" + fileIn


  if 'ttc_a' in iin or 'ttc_s0' in iin:

    if "a" in iin.split('_') and "s" in iin.split('_'):
      print ("Interference samples")

    elif "highmass.root" in iin.split('_'):
      print ("===> highmass samples <===")
      fileIn = iin.split('_')[0]+'_'+iin.split('_')[1]+'_'+iin.split('_')[3]+'_M'+iin.split('_')[1].upper()+iin.split('_')[2]+".root"
      fileIn = "/eos/user/t/tihsu/BDT/ntuple_skim/" + era + "/" + fileIn
    else:
      print ("normal samples")
      fileIn = iin.split('.')[0]+'_'+mass_flag.split('_')[2]+mass_flag.split('_')[3]+".root"
      fileIn = "/eos/user/t/tihsu/BDT/ntuple_skim/" + era + "/" + fileIn

  print ("Input file: ", fileIn)
  AddEntry(fileIn)

  end = time.time()
  print( "wall time:", end-start)

