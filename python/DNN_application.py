import ROOT
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
import torch

def Build_DNN_Command(model_name="", df=None):
  ROOT.gInterpreter.Declare('#include "DNN_{}.hxx"'.format(model_name))
  PreProcessor = torch.load('../../data/PreProcessor_{}.pt'.format(model_name), map_location=torch.device('cpu'))
  _,_,col_names = PreProcessor.transformers_[0]
  transformer = PreProcessor.named_transformers_['StandardScaler']
  mean, std = transformer.mean_, transformer.scale_
  mean_str = [str(x) for x in mean]
  std_str = [str(x) for x in std]
  mean_array_str = '{' + ', '.join(mean_str) + '}'
  std_array_str = '{' + ', '.join(std_str) + '}'
  var_dict = {'bmatched_jet_pt':'jet_pt[comb_[0]]',
              'lmatched_jet_pt':'jet_pt[comb_[1]]',
              'jet3_pt': 'jet_pt[comb_[2]]',
              'jet4_pt': '(comb_[3] > -1) ? jet_pt[comb_[3]] : -9.0',
              'bmatched_jet_eta':'jet_eta[comb_[0]]',
              'lmatched_jet_eta':'jet_eta[comb_[1]]',
              'jet3_eta': 'jet_eta[comb_[2]]',
              'jet4_eta': '(comb_[3] > -1) ? jet_eta[comb_[3]] : -9.0',
              'bmatched_jet_phi':'jet_phi[comb_[0]]',
              'lmatched_jet_phi':'jet_phi[comb_[1]]',
              'jet3_phi': 'jet_phi[comb_[2]]',
              'jet4_phi': '(comb_[3] > -1) ? jet_phi[comb_[3]] : -9.0',
              'bmatched_jet_mass':'jet_mass[comb_[0]]',
              'lmatched_jet_mass':'jet_mass[comb_[1]]',
              'jet3_mass': 'jet_mass[comb_[2]]',
              'jet4_mass': '(comb_[3] > -1) ? jet_mass[comb_[3]] : -9.0',
              'bmatched_jet_CvB': 'jet_CvB[comb_[0]]',
              'lmatched_jet_CvB': 'jet_CvB[comb_[1]]',
              'jet3_CvB': 'jet_CvB[comb_[2]]',
              'jet4_CvB': '(comb_[3] > -1) ? jet_CvB[comb_[3]] : -9.0',
              'bmatched_jet_CvL': 'jet_CvL[comb_[0]]',
              'lmatched_jet_CvL': 'jet_CvL[comb_[1]]',
              'jet3_CvL': 'jet_CvL[comb_[2]]',
              'jet4_CvL': '(comb_[3] > -1) ? jet_CvL[comb_[3]] : -9.0',
              'bmatched_jet_FlavB': 'jet_FlavB[comb_[0]]',
              'lmatched_jet_FlavB': 'jet_FlavB[comb_[1]]',
              'jet3_FlavB': 'jet_FlavB[comb_[2]]',
              'jet4_FlavB': '(comb_[3] > -1) ? jet_FlavB[comb_[3]] : -9.0',
              'lep1_pt': 'l1_pt',
              'lep2_pt': 'l2_pt',
              'lep1_eta': 'l1_eta',
              'lep2_eta': 'l2_eta',
              'lep1_phi': 'l1_phi',
              'lep2_phi': 'l2_phi',
              'lep1_mass': 'l1_mass',
              'lep2_mass': 'l2_mass',
              'dR_bmatched_lmatched_jets': 'ROOT::Math::VectorUtil::DeltaR(j1,j2)',
              'dR_bmatched_jet_lep1': 'ROOT::Math::VectorUtil::DeltaR(j1,l1)',
              'dR_bmatched_jet_lep2': 'ROOT::Math::VectorUtil::DeltaR(j1,l2)',
              'dR_lmatched_jet_lep1': 'ROOT::Math::VectorUtil::DeltaR(j2,l1)',
              'dR_lmatched_jet_lep2': 'ROOT::Math::VectorUtil::DeltaR(j2,l2)',
              'invmass_bjlj': '(j1+j2).M()',
              'met':'met',
              'met_phi':'met_phi'
               }
  input_def = ''
  for idx,col_name in enumerate(col_names):
    input_def += 'input[{idx}] = {def_};\n'.format(idx=idx,def_=var_dict[col_name])
  command = '\
  #include "ROOT/RDataFrame.hxx"\n\
  #include "ROOT/RVec.hxx"\n\
  #include "Math/Vector4D.h"\n\
  #include "Math/Vector4Dfwd.h"\n\
  #include "TString.h"\n\
  #include <vector>\n\
  #include <algorithm>\n\
  \n\
  TMVA_SOFIE_DNN_{model_name}::Session model("DNN_{model_name}.dat");\n\
  float Preprocessor_mean[{input_dim}] = {mean_array};\n\
  float Preprocessor_std[{input_dim}] = {std_array};\n\
  std::vector<int> Jet_reindex(ROOT::RVec<Int_t> jet_id,\n\
                               ROOT::RVec<Float_t> jet_pt,\n\
                               ROOT::RVec<Float_t> jet_eta, \n\
                               ROOT::RVec<Float_t> jet_phi, \n\
                               ROOT::RVec<Float_t> jet_mass, \n\
                               ROOT::RVec<Float_t> jet_CvL, \n\
                               ROOT::RVec<Float_t> jet_CvB, \n\
                               ROOT::RVec<Float_t> jet_FlavB, \n\
                               float ttc_l1_pt, \n\
                               float ttc_l1_eta, \n\
                               float ttc_l1_phi, \n\
                               float ttc_l1_mass, \n\
                               float ttc_l2_pt, \n\
                               float ttc_l2_eta, \n\
                               float ttc_l2_phi, \n\
                               float ttc_l2_mass, \n\
                               float met, \n\
                               float met_phi \n\
                               ){{ \n\
  float l1_pt, l1_eta, l1_phi, l1_mass, l2_pt, l2_eta, l2_phi, l2_mass;\n\
  if(ttc_l1_pt < ttc_l2_pt){{\n\
    l1_pt  = ttc_l2_pt;\n\
    l1_eta = ttc_l2_eta;\n\
    l1_phi = ttc_l2_phi;\n\
    l1_mass= ttc_l2_mass;\n\
    l2_pt  = ttc_l1_pt;\n\
    l2_eta = ttc_l1_eta;\n\
    l2_phi = ttc_l1_phi;\n\
    l2_mass= ttc_l1_mass;\n\
  }}\n\
  else{{\n\
    l1_pt  = ttc_l1_pt;\n\
    l1_eta = ttc_l1_eta;\n\
    l1_phi = ttc_l1_phi;\n\
    l1_mass= ttc_l1_mass;\n\
    l2_pt  = ttc_l2_pt;\n\
    l2_eta = ttc_l2_eta;\n\
    l2_phi = ttc_l2_phi;\n\
    l2_mass= ttc_l2_mass;\n\
  }}\n\
  int njet = std::min(6,static_cast<int>(jet_id.size()));\n\
  std::vector<std::vector<int>> combination;\n\
  for(int first_idx = 0; first_idx < njet; first_idx++){{ \n\
    for(int second_idx = 0; second_idx < njet; second_idx++){{\n\
      if(first_idx == second_idx) continue; \n\
      std::vector<int> comb_;\n\
      comb_.reserve(4);\n\
      comb_.push_back(jet_id[first_idx]);\n\
      comb_.push_back(jet_id[second_idx]);\n\
      for(int extra_idx = 0; extra_idx < std::min(4,njet); extra_idx++){{\n\
        if(!(extra_idx == first_idx) && !(extra_idx == second_idx) && (comb_.size()<4)){{\n\
          comb_.push_back(jet_id[extra_idx]);\n\
        }}\n\
      }}\n\
      if(comb_.size()<4) comb_.push_back(-1);\n\
      combination.push_back(comb_);\n\
    }}\n\
  }}\n\
  float best_score = -999.;\n\
  std::vector<int> best_index;\n\
  for(int comb_idx = 0; comb_idx < combination.size(); comb_idx++){{\n\
    std::vector<int> comb_; \n\
    comb_ = combination[comb_idx];\n\
    float input[{input_dim}];\n\
    ROOT::Math::PtEtaPhiMVector j1(jet_pt[comb_[0]],jet_eta[comb_[0]],jet_phi[comb_[0]],jet_mass[comb_[0]]);\n\
    ROOT::Math::PtEtaPhiMVector j2(jet_pt[comb_[1]],jet_eta[comb_[1]],jet_phi[comb_[1]],jet_mass[comb_[1]]);\n\
    ROOT::Math::PtEtaPhiMVector j3(jet_pt[comb_[2]],jet_eta[comb_[2]],jet_phi[comb_[2]],jet_mass[comb_[2]]);\n\
    ROOT::Math::PtEtaPhiMVector l1(l1_pt,l1_eta,l1_phi,l1_mass);\n\
    ROOT::Math::PtEtaPhiMVector l2(l2_pt,l2_eta,l2_phi,l2_mass);\n\
    {input_def}\n\
    for(int input_idx; input_idx < {input_dim}; input_idx++){{\n\
      input[input_idx] = (input[input_idx]-Preprocessor_mean[input_idx])/Preprocessor_std[input_idx];\n\
    }}\n\
    float tmp_score = model.infer(input)[0];\n\
    if(tmp_score > best_score){{\n\
      best_score = tmp_score;\n\
      best_index = comb_;\n\
    }}\n\
  }}\n\
  return best_index;\n\
 }}\
'.format(input_dim = len(col_names), model_name=model_name, mean_array = mean_array_str, std_array=std_array_str, input_def=input_def)
  print(command)
  ROOT.gInterpreter.Declare(str(command))
  if df:
    df = df.Define('JetMatched_idx','Jet_reindex(tightJets_id_in24,\
                                         Jet_pt,\
                                         Jet_eta,\
                                         Jet_phi,\
                                         Jet_mass,\
                                         Jet_btagDeepFlavCvL,\
                                         Jet_btagDeepFlavCvB,\
                                         Jet_btagDeepFlavB,\
                                         ttc_l1_pt,\
                                         ttc_l1_eta,\
                                         ttc_l1_phi,\
                                         ttc_l1_mass,\
                                         ttc_l2_pt,\
                                         ttc_l2_eta,\
                                         ttc_l2_phi,\
                                         ttc_l2_mass,\
                                         ttc_met,\
                                         ttc_met_phi)')
  return df

if __name__ == '__main__':
  Build_DNN_Command(model_name="Flav_MET_threeJet_model_v2", df=None)
