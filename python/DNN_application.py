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
                               float l1_pt, \n\
                               float l1_eta, \n\
                               float l1_phi, \n\
                               float l1_mass, \n\
                               float l2_pt, \n\
                               float l2_eta, \n\
                               float l2_phi, \n\
                               float l2_mass, \n\
                               float met, \n\
                               float met_phi \n\
                               ){{ \n\
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
    input[0] = jet_pt[comb_[0]];\n\
    input[1] = jet_eta[comb_[0]];\n\
    input[2] = jet_phi[comb_[0]];\n\
    input[3] = jet_mass[comb_[0]];\n\
    input[4] = jet_CvB[comb_[0]];\n\
    input[5] = jet_CvL[comb_[0]];\n\
    input[6] = jet_FlavB[comb_[0]];\n\
    input[7] = jet_pt[comb_[1]];\n\
    input[8] = jet_eta[comb_[1]];\n\
    input[9] = jet_phi[comb_[1]];\n\
    input[10]= jet_mass[comb_[1]];\n\
    input[11]= jet_CvB[comb_[1]];\n\
    input[12]= jet_CvL[comb_[1]];\n\
    input[13]= jet_FlavB[comb_[1]];\n\
    ROOT::Math::PtEtaPhiMVector j1(jet_pt[comb_[0]],jet_eta[comb_[0]],jet_phi[comb_[0]],jet_mass[comb_[0]]);\n\
    ROOT::Math::PtEtaPhiMVector j2(jet_pt[comb_[1]],jet_eta[comb_[1]],jet_phi[comb_[1]],jet_mass[comb_[1]]);\n\
    ROOT::Math::PtEtaPhiMVector j3(jet_pt[comb_[2]],jet_eta[comb_[2]],jet_phi[comb_[2]],jet_mass[comb_[2]]);\n\
    ROOT::Math::PtEtaPhiMVector l1(l1_pt,l1_eta,l1_phi,l1_mass);\n\
    ROOT::Math::PtEtaPhiMVector l2(l2_pt,l2_eta,l2_phi,l2_mass);\n\
    input[14] = ROOT::Math::VectorUtil::DeltaR(j1,j2);\n\
    input[15] = ROOT::Math::VectorUtil::DeltaR(j1,l1);\n\
    input[16] = ROOT::Math::VectorUtil::DeltaR(j1,l2);\n\
    input[17] = ROOT::Math::VectorUtil::DeltaR(j2,l1);\n\
    input[18] = ROOT::Math::VectorUtil::DeltaR(j2,l2);\n\
    input[19] = (j1+j2).M();\n\
    input[20] = l1_pt;\n\
    input[21] = l1_eta;\n\
    input[22] = l1_phi;\n\
    input[23] = l1_mass;\n\
    input[24] = l2_pt;\n\
    input[25] = l2_eta;\n\
    input[26] = l2_phi;\n\
    input[27] = l2_mass;\n\
    input[28] = jet_pt[comb_[2]];\n\
    input[29] = jet_eta[comb_[2]];\n\
    input[30] = jet_phi[comb_[2]];\n\
    input[31] = jet_mass[comb_[2]];\n\
    input[32] = jet_CvB[comb_[2]];\n\
    input[33] = jet_CvL[comb_[2]];\n\
    input[34] = jet_FlavB[comb_[2]];\n\
    if(comb_[3] > -1){{\n\
      input[35] = jet_pt[comb_[3]];\n\
      input[36] = jet_eta[comb_[3]];\n\
      input[37] = jet_phi[comb_[3]];\n\
      input[38] = jet_mass[comb_[3]];\n\
      input[39] = jet_CvB[comb_[3]];\n\
      input[40] = jet_CvL[comb_[3]];\n\
      input[41] = jet_FlavB[comb_[3]];\n\
    }}\n\
    else{{\n\
      input[35] = -9.0;\n\
      input[36] = -9.0;\n\
      input[37] = -9.0;\n\
      input[38] = -9.0;\n\
      input[39] = -9.0;\n\
      input[40] = -9.0;\n\
      input[41] = -9.0;\n\
    }}\n\
    input[42] = met;\n\
    input[43] = met_phi;\n\
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
'.format(input_dim = len(col_names), model_name=model_name, mean_array = mean_array_str, std_array=std_array_str)
  #print(command)
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
