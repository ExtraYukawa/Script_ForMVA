#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "TCanvas.h"
#include "TH1D.h"
#include "TLatex.h"
#include "Math/Vector4D.h"
#include "TStyle.h"

using namespace ROOT;
using namespace std;
using namespace ROOT::VecOps;

float deltaR_jet( ROOT::VecOps::RVec<float> jet_pt, ROOT::VecOps::RVec<float> jet_eta, ROOT::VecOps::RVec<float> jet_phi, ROOT::VecOps::RVec<float> jet_mass, ROOT::VecOps::RVec<Int_t> jet_id, int id)
{
  float deltar=0.;
  ROOT::Math::PtEtaPhiMVector j1(jet_pt[jet_id[0]],jet_eta[jet_id[0]],jet_phi[jet_id[0]],jet_mass[jet_id[0]]);
  ROOT::Math::PtEtaPhiMVector j2(jet_pt[jet_id[1]],jet_eta[jet_id[1]],jet_phi[jet_id[1]],jet_mass[jet_id[1]]);
  ROOT::Math::PtEtaPhiMVector j3(jet_pt[jet_id[2]],jet_eta[jet_id[2]],jet_phi[jet_id[2]],jet_mass[jet_id[2]]);
  if(id==1) deltar= ROOT::Math::VectorUtil::DeltaR(j1,j2);
  if(id==2) deltar= ROOT::Math::VectorUtil::DeltaR(j1,j3);
  if(id==3) deltar= ROOT::Math::VectorUtil::DeltaR(j2,j3);
  return deltar;
}

float HT_jesr(ROOT::VecOps::RVec<Int_t> jetid, ROOT::VecOps::RVec<float> jetpt_jesUp, ROOT::VecOps::RVec<float> jetpt_jesDo, ROOT::VecOps::RVec<float> jetpt_jerUp, ROOT::VecOps::RVec<float> jetpt_jerDo, int op, int njet)
{
  float ht=0.;
  if (op==0){
    for (int i=0;i<njet;i++)
     {if(jetid[i]<0) continue;
      ht+=jetpt_jesUp[jetid[i]];
     }
  }
  if (op==1){
    for (int i=0;i<njet;i++)
     {if(jetid[i]<0) continue;
      ht+=jetpt_jesDo[jetid[i]];
     }
  }
  if (op==2){
    for (int i=0;i<njet;i++)
     {if(jetid[i]<0) continue;
      ht+=jetpt_jerUp[jetid[i]];
     }
  }
  if (op==3){
    for (int i=0;i<njet;i++)
     {if(jetid[i]<0) continue;
      ht+=jetpt_jerDo[jetid[i]];
     }
  }
  return ht;
}

float mllj_jesr(float l1_pt, float l1_eta, float l1_phi, float l1_mass, float l2_pt, float l2_eta, float l2_phi, float l2_mass, ROOT::VecOps::RVec<float> jet_pt, ROOT::VecOps::RVec<float> jet_eta, ROOT::VecOps::RVec<float> jet_phi, ROOT::VecOps::RVec<float> jet_mass, ROOT::VecOps::RVec<Int_t> jet_id, int id)
{
  float mllj=0.;
  ROOT::Math::PtEtaPhiMVector l1(l1_pt,l1_eta,l1_phi,l1_mass);
  ROOT::Math::PtEtaPhiMVector l2(l2_pt,l2_eta,l2_phi,l2_mass);
  ROOT::Math::PtEtaPhiMVector j1(jet_pt[jet_id[0]],jet_eta[jet_id[0]],jet_phi[jet_id[0]],jet_mass[jet_id[0]]);
  ROOT::Math::PtEtaPhiMVector j2(jet_pt[jet_id[1]],jet_eta[jet_id[1]],jet_phi[jet_id[1]],jet_mass[jet_id[1]]);
  ROOT::Math::PtEtaPhiMVector j3(jet_pt[jet_id[2]],jet_eta[jet_id[2]],jet_phi[jet_id[2]],jet_mass[jet_id[2]]);
  if(id==1) mllj= (l1+l2+j1).M();
  if(id==2) mllj= (l1+l2+j2).M();
  if(id==3) mllj= (l1+l2+j3).M();
  return mllj;
}
