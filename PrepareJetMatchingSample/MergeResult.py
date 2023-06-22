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
from common import store_place, TransFileName
import h5py
import os


skimstore_place = store_place + "ntuple_skim/"
h5py_place      = store_place + "dataframe/"
output_place    = store_place + "ntuple_reindex/"

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

def AddEntry(fin_name, era):

  # Reference ROOT file
  fin  = ROOT.TFile(os.path.join(skimstore_place, era, fin_name), 'READ')
  fOut = ROOT.TFile(os.path.join(output_place, era, fin_name), 'RECREATE')
  tree_name = 'Events'
  t    = fin.Get(tree_name)
  tOut = t.CloneTree()
  tOut.SetDirectory(0)
  matched_idx = array('i',[-1,-1,-1,-1])
  Branch_idx  = tOut.Branch("JetMatched_idx",matched_idx,"JetMatched_idx[4]/I")
  nentries    = t.GetEntries()
  run_event   = nentries


  # Load DNN
  input_columns_ = [
    'bmatched_jet_pt','bmatched_jet_eta','bmatched_jet_phi','bmatched_jet_mass', 'bmatched_jet_CvB', 'bmatched_jet_CvL', 'bmatched_jet_FlavB',
    'lmatched_jet_pt','lmatched_jet_eta','lmatched_jet_phi','lmatched_jet_mass', 'lmatched_jet_CvB', 'lmatched_jet_CvL', 'lmatched_jet_FlavB',
    'dR_bmatched_lmatched_jets','dR_bmatched_jet_lep1','dR_bmatched_jet_lep2','dR_lmatched_jet_lep1','dR_lmatched_jet_lep2',
    'invmass_bjlj',
    'lep1_pt','lep1_eta','lep1_phi','lep1_mass',
    'lep2_pt','lep2_eta','lep2_phi','lep2_mass',
    'jet3_pt','jet3_eta','jet3_phi','jet3_mass', 'jet3_CvB', 'jet3_CvL', 'jet3_FlavB',
    'jet4_pt','jet4_eta','jet4_phi','jet4_mass', 'jet4_CvB', 'jet4_CvL', 'jet4_FlavB'
    
  ] 
  model = NeuralNetwork(len(input_columns_))
  model.load_state_dict(torch.load('../data/DNN_Flav_model.pt', map_location=torch.device('cpu')))
  model.eval()

  df = []
  # Scan target file
  FileList = os.listdir(os.path.join(h5py_place,era))
  for f in FileList:
    if (fin_name.split('.')[0] == '_'.join(f.split('.')[0].split('_')[:-1])):
      print(f)
      df_ = pd.read_hdf(os.path.join(h5py_place,era,f))
      df.append(df_)
  # Prepare dataframe

  df = pd.concat(df)
  print(df)

  print(df.keys())
  # Data Preprocessing
  colnames = list(df.keys())
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
  source_combs = transformed_df[input_columns_].values
  X_input      = torch.tensor(source_combs, dtype=torch.float32, device=torch.device('cpu'))
  predicted    = torch.sigmoid(model(X_input)).detach().numpy()
  predicted    = np.array(predicted.reshape(len(predicted)))
  transformed_df.insert(1, "predicted", predicted)
  print(transformed_df)
  idx = transformed_df.groupby(['Entry'])['predicted'].transform(max) == transformed_df['predicted']
  df = transformed_df[idx]
  print(df)
  if not (nentries == len(df)):
    idx2 = df.groupby(['Entry'])['bmatched_jet_index'].transform(min) == df['bmatched_jet_index']
    df = df[idx2]
    if not (nentries == len(df)):
      idx3 = df.groupby(['Entry'])['lmatched_jet_index'].transform(min) == df['lmatched_jet_index']
      df = df[idx3]
      if not (nentries == len(df)):
        idx4 = df.groupby(['Entry'])['jet3_index'].transform(min) == df['jet3_index']
        df = df[idx4]


  df = df.sort_values(by=['Entry'])
  df = df.set_index("Entry")  

  print(df)

  # Check
  if not (nentries == len(df)):
    raise Exception("Sorry, root file and h5py file do not match")
  for entry in range(run_event):
    matched_idx[0] = df['bmatched_jet_index'][entry]
    matched_idx[1] = df['lmatched_jet_index'][entry]
    matched_idx[2] = df['jet3_index'][entry]
    matched_idx[3] = df['jet4_index'][entry]
    Branch_idx.Fill()

  fOut.cd()
  tOut.Write()
  fOut.Close()
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
  mass_flag = args.flag
  isMC = (args.Type == "MC")
  channel = args.channel
  iin = TransFileName(args.iin, isMC, era, channel,mass_flag)

  fileIn = iin

  print ("Input file: ", fileIn)
  AddEntry(fileIn, era)

  end = time.time()
  print( "wall time:", end-start)

