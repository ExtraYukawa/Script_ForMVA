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
TFile*f_mu=TFile::Open("SFs/fr_data_mu.root");
TFile*f_ele=TFile::Open("SFs/fr_data_ele.root");

TH2D*h_m=(TH2D*)f_mu->Get("fakerate");
TH2D*h_e=(TH2D*)f_ele->Get("fakerate");

float fake_weight(int ttc_region, bool ttc_1P1F, bool ttc_0P2F, bool ttc_lep1_faketag, float l1_pt, float l1_eta, float l2_pt, float l2_eta){
  if (l1_pt>70.) l1_pt=70.;
  if (l2_pt>70.) l2_pt=70.;
  if (fabs(l1_eta)>2.3) l1_eta=2.3;
  if (fabs(l2_eta)>2.3) l2_eta=2.3;
  float w_temp=1.0;
  float fakerate1=1.0;
  float fakerate2=1.0;
  if (ttc_region==1){
    if(ttc_1P1F){
      if(ttc_lep1_faketag) fakerate1=h_m->GetBinContent(h_m->FindBin(fabs(l1_eta), l1_pt));
      else fakerate1=h_m->GetBinContent(h_m->FindBin(fabs(l2_eta), l2_pt));
      w_temp=-1*fakerate1/(1-fakerate1);
    }
    if(ttc_0P2F){
          fakerate1=h_m->GetBinContent(h_m->FindBin(fabs(l1_eta), l1_pt));
          fakerate2=h_m->GetBinContent(h_m->FindBin(fabs(l2_eta), l2_pt));
          w_temp=fakerate1*fakerate2/((1-fakerate1)*(1-fakerate2));
    }
  }
  if (ttc_region==2){
    if(ttc_1P1F){
      if(ttc_lep1_faketag) fakerate1=h_m->GetBinContent(h_m->FindBin(fabs(l1_eta), l1_pt));
      else fakerate1=h_e->GetBinContent(h_e->FindBin(fabs(l2_eta), l2_pt));
      w_temp=-1*fakerate1/(1-fakerate1);
    }
    if(ttc_0P2F){
          fakerate1=h_m->GetBinContent(h_m->FindBin(fabs(l1_eta), l1_pt));
          fakerate2=h_e->GetBinContent(h_e->FindBin(fabs(l2_eta), l2_pt));
          w_temp=fakerate1*fakerate2/((1-fakerate1)*(1-fakerate2));
    }
  }
  if (ttc_region==3){
    if(ttc_1P1F){
      if(ttc_lep1_faketag) fakerate1=h_e->GetBinContent(h_e->FindBin(fabs(l1_eta), l1_pt));
      else fakerate1=h_e->GetBinContent(h_e->FindBin(fabs(l2_eta), l2_pt));
      w_temp=-1*fakerate1/(1-fakerate1);
    }
    if(ttc_0P2F){
          fakerate1=h_e->GetBinContent(h_e->FindBin(fabs(l1_eta), l1_pt));
          fakerate2=h_e->GetBinContent(h_e->FindBin(fabs(l2_eta), l2_pt));
          w_temp=fakerate1*fakerate2/((1-fakerate1)*(1-fakerate2));
    }
  }
  return w_temp;
}

TFile*f_chargeflip=TFile::Open("SFs/ChargeFlipSF.root");
TH2D*Prob_data=(TH2D*)f_chargeflip->Get("data_CFRate");
TH2D*Prob_mc=(TH2D*)f_chargeflip->Get("MC_CFRate");
TH1D*Chaflip_unc=(TH1D*)f_chargeflip->Get("overall_sys");
float Chaflip_unc_num=Chaflip_unc->GetBinContent(1);

TFile*f_sigunc=TFile::Open("SFs/signalunc.root");
TH1D*sig_pdf=(TH1D*)f_sigunc->Get("pdf_unc");
TH1D*sig_scale=(TH1D*)f_sigunc->Get("scale_unc");
TH1D*sig_ps=(TH1D*)f_sigunc->Get("ps_unc");
float signal_pdf(float lep1_pt, int iw){
if(iw==0) return (1+sig_pdf->GetBinContent(sig_pdf->FindBin(lep1_pt)));
if(iw==1) return (1-sig_pdf->GetBinContent(sig_pdf->FindBin(lep1_pt)));
}
float signal_scale(float lep1_pt, int iw){
if(iw==0) return (1+sig_scale->GetBinContent(sig_scale->FindBin(lep1_pt)));
if(iw==1) return (1-sig_scale->GetBinContent(sig_scale->FindBin(lep1_pt)));
}
float signal_ps(float lep1_pt, int iw){
if(iw==0) return (1+sig_ps->GetBinContent(sig_ps->FindBin(lep1_pt)));
if(iw==1) return (1-sig_ps->GetBinContent(sig_ps->FindBin(lep1_pt)));
}

float dphi(float phi1, float phi2){
  if(abs(phi1-phi2)>3.1415926) return (6.2831852-abs(phi1-phi2));
  else return abs(phi1-phi2);
}

float chargeflip_SF(int OS_flag, float lep1_pt, float lep1_eta, float lep1_phi, float lep2_pt, float lep2_eta, float lep2_phi, int channel, int iw, ROOT::VecOps::RVec<float> genlep_eta, ROOT::VecOps::RVec<float> genlep_phi, ROOT::VecOps::RVec<int> genlep_id){

  // for DY and TTTo2L, no need to gen matching
  if(OS_flag==0){
    int ngenlep=genlep_id.size();
    if(ngenlep<2)return 1.;
    int l1_temp=-99;
    int l2_temp=-99;
    float dr1=100.;
    float dr1_temp=100.;
    float dr2=100.;
    float dr2_temp=100.;
    for(int iloop=0;iloop<ngenlep;iloop++){
      dr1_temp=sqrt((lep1_eta-genlep_eta[iloop])*(lep1_eta-genlep_eta[iloop]) + dphi(lep1_phi, genlep_phi[iloop])*dphi(lep1_phi, genlep_phi[iloop]));
      if (dr1_temp<dr1) {dr1=dr1_temp;l1_temp=iloop;}
    }
    for(int iloop=0;iloop<ngenlep;iloop++){
      dr2_temp=sqrt((lep2_eta-genlep_eta[iloop])*(lep2_eta-genlep_eta[iloop]) + dphi(lep2_phi, genlep_phi[iloop])*dphi(lep2_phi, genlep_phi[iloop]));
      if (dr2_temp<dr2) {dr2=dr2_temp;l2_temp=iloop;}
    }
    
    if(!(l1_temp>-1 && l2_temp>-1 && dr1<0.3 && dr2<0.3 && genlep_id[l1_temp]*genlep_id[l2_temp]<0 && (l1_temp!=l2_temp)))return 1.;
  }

  float sf=1.;
  if(lep1_pt>300.) lep1_pt=200.;
  if(lep2_pt>300.) lep2_pt=200.;
  if(abs(lep1_eta)>2.5) lep1_eta=2.0;
  if(abs(lep2_eta)>2.5) lep2_eta=2.0;
  if(channel==3){
    float prob1_data=Prob_data->GetBinContent(Prob_data->FindBin(lep1_pt,abs(lep1_eta)));
    float prob2_data=Prob_data->GetBinContent(Prob_data->FindBin(lep2_pt,abs(lep2_eta)));
    float prob1_mc=Prob_mc->GetBinContent(Prob_mc->FindBin(lep1_pt,abs(lep1_eta)));
    float prob2_mc=Prob_mc->GetBinContent(Prob_mc->FindBin(lep2_pt,abs(lep2_eta)));
    sf=(prob1_data+prob2_data-2*prob1_data*prob2_data)/(prob1_mc+prob2_mc-2*prob1_mc*prob2_mc);
    if(iw==0) return sf;
    if(iw==1) return (sf+Chaflip_unc_num);
    if(iw==2) return (sf-Chaflip_unc_num);
  }
  else {return 1.;}
}

TFile*f_eleSF=TFile::Open("SFs/ele.root");
TH2D *eleSF=(TH2D*)f_eleSF->Get("EleIDSF");
TFile*f_muSF=TFile::Open("SFs/muon.root");
TH2D *muSF=(TH2D*)f_muSF->Get("muIdSF");
TH2D *muSF_sys=(TH2D*)f_muSF->Get("sys_error");
TH2D *muSF_all=(TH2D*)f_muSF->Get("combined_error");

TFile*f_diele_trigger=TFile::Open("SFs/diEle_trigger.root");
TH2D *diele_trigger=(TH2D*)f_diele_trigger->Get("l1l2eta");
TFile*f_dimu_trigger=TFile::Open("SFs/diMuon_trigger.root");
TH2D *dimu_trigger=(TH2D*)f_dimu_trigger->Get("l1l2eta");
TFile*f_muele_trigger=TFile::Open("SFs/MuEle_trigger.root");
TH2D *muele_trigger=(TH2D*)f_muele_trigger->Get("l1l2eta");

TFile*f_ctag=TFile::Open("SFs/DeepJet_ctagSF.root");
TH2F *SFb_hist=(TH2F*)f_ctag->Get("SFb_hist");
TH2F *SFc_hist=(TH2F*)f_ctag->Get("SFc_hist");
TH2F *SFl_hist=(TH2F*)f_ctag->Get("SFl_hist");
TH2F *SFb_hist_StatUp=(TH2F*)f_ctag->Get("SFb_hist_StatUp");
TH2F *SFb_hist_StatDo=(TH2F*)f_ctag->Get("SFb_hist_StatDown");
TH2F *SFc_hist_StatUp=(TH2F*)f_ctag->Get("SFc_hist_StatUp");
TH2F *SFc_hist_StatDo=(TH2F*)f_ctag->Get("SFc_hist_StatDown");
TH2F *SFl_hist_StatUp=(TH2F*)f_ctag->Get("SFl_hist_StatUp");
TH2F *SFl_hist_StatDo=(TH2F*)f_ctag->Get("SFl_hist_StatDown");
TH2F *SFb_hist_EleIDSFUp=(TH2F*)f_ctag->Get("SFb_hist_EleIDSFUp");
TH2F *SFb_hist_EleIDSFDo=(TH2F*)f_ctag->Get("SFb_hist_EleIDSFDown");
TH2F *SFc_hist_EleIDSFUp=(TH2F*)f_ctag->Get("SFc_hist_EleIDSFUp");
TH2F *SFc_hist_EleIDSFDo=(TH2F*)f_ctag->Get("SFc_hist_EleIDSFDown");
TH2F *SFl_hist_EleIDSFUp=(TH2F*)f_ctag->Get("SFl_hist_EleIDSFUp");
TH2F *SFl_hist_EleIDSFDo=(TH2F*)f_ctag->Get("SFl_hist_EleIDSFDown");
TH2F *SFb_hist_LHEScaleWeight_muFUp=(TH2F*)f_ctag->Get("SFb_hist_LHEScaleWeight_muFUp");
TH2F *SFb_hist_LHEScaleWeight_muFDo=(TH2F*)f_ctag->Get("SFb_hist_LHEScaleWeight_muFDown");
TH2F *SFc_hist_LHEScaleWeight_muFUp=(TH2F*)f_ctag->Get("SFc_hist_LHEScaleWeight_muFUp");
TH2F *SFc_hist_LHEScaleWeight_muFDo=(TH2F*)f_ctag->Get("SFc_hist_LHEScaleWeight_muFDown");
TH2F *SFl_hist_LHEScaleWeight_muFUp=(TH2F*)f_ctag->Get("SFl_hist_LHEScaleWeight_muFUp");
TH2F *SFl_hist_LHEScaleWeight_muFDo=(TH2F*)f_ctag->Get("SFl_hist_LHEScaleWeight_muFDown");
TH2F *SFb_hist_LHEScaleWeight_muRUp=(TH2F*)f_ctag->Get("SFb_hist_LHEScaleWeight_muRUp");
TH2F *SFb_hist_LHEScaleWeight_muRDo=(TH2F*)f_ctag->Get("SFb_hist_LHEScaleWeight_muRDown");
TH2F *SFc_hist_LHEScaleWeight_muRUp=(TH2F*)f_ctag->Get("SFc_hist_LHEScaleWeight_muRUp");
TH2F *SFc_hist_LHEScaleWeight_muRDo=(TH2F*)f_ctag->Get("SFc_hist_LHEScaleWeight_muRDown");
TH2F *SFl_hist_LHEScaleWeight_muRUp=(TH2F*)f_ctag->Get("SFl_hist_LHEScaleWeight_muRUp");
TH2F *SFl_hist_LHEScaleWeight_muRDo=(TH2F*)f_ctag->Get("SFl_hist_LHEScaleWeight_muRDown");
TH2F *SFb_hist_MuIDSFUp=(TH2F*)f_ctag->Get("SFb_hist_MuIDSFUp");
TH2F *SFb_hist_MuIDSFDo=(TH2F*)f_ctag->Get("SFb_hist_MuIDSFDown");
TH2F *SFc_hist_MuIDSFUp=(TH2F*)f_ctag->Get("SFc_hist_MuIDSFUp");
TH2F *SFc_hist_MuIDSFDo=(TH2F*)f_ctag->Get("SFc_hist_MuIDSFDown");
TH2F *SFl_hist_MuIDSFUp=(TH2F*)f_ctag->Get("SFl_hist_MuIDSFUp");
TH2F *SFl_hist_MuIDSFDo=(TH2F*)f_ctag->Get("SFl_hist_MuIDSFDown");
TH2F *SFb_hist_PSWeightFSRUp=(TH2F*)f_ctag->Get("SFb_hist_PSWeightFSRUp");
TH2F *SFb_hist_PSWeightFSRDo=(TH2F*)f_ctag->Get("SFb_hist_PSWeightFSRDown");
TH2F *SFc_hist_PSWeightFSRUp=(TH2F*)f_ctag->Get("SFc_hist_PSWeightFSRUp");
TH2F *SFc_hist_PSWeightFSRDo=(TH2F*)f_ctag->Get("SFc_hist_PSWeightFSRDown");
TH2F *SFl_hist_PSWeightFSRUp=(TH2F*)f_ctag->Get("SFl_hist_PSWeightFSRUp");
TH2F *SFl_hist_PSWeightFSRDo=(TH2F*)f_ctag->Get("SFl_hist_PSWeightFSRDown");
TH2F *SFb_hist_PSWeightISRUp=(TH2F*)f_ctag->Get("SFb_hist_PSWeightISRUp");
TH2F *SFb_hist_PSWeightISRDo=(TH2F*)f_ctag->Get("SFb_hist_PSWeightISRDown");
TH2F *SFc_hist_PSWeightISRUp=(TH2F*)f_ctag->Get("SFc_hist_PSWeightISRUp");
TH2F *SFc_hist_PSWeightISRDo=(TH2F*)f_ctag->Get("SFc_hist_PSWeightISRDown");
TH2F *SFl_hist_PSWeightISRUp=(TH2F*)f_ctag->Get("SFl_hist_PSWeightISRUp");
TH2F *SFl_hist_PSWeightISRDo=(TH2F*)f_ctag->Get("SFl_hist_PSWeightISRDown");
TH2F *SFb_hist_PUWeightUp=(TH2F*)f_ctag->Get("SFb_hist_PUWeightUp");
TH2F *SFb_hist_PUWeightDo=(TH2F*)f_ctag->Get("SFb_hist_PUWeightDown");
TH2F *SFc_hist_PUWeightUp=(TH2F*)f_ctag->Get("SFc_hist_PUWeightUp");
TH2F *SFc_hist_PUWeightDo=(TH2F*)f_ctag->Get("SFc_hist_PUWeightDown");
TH2F *SFl_hist_PUWeightUp=(TH2F*)f_ctag->Get("SFl_hist_PUWeightUp");
TH2F *SFl_hist_PUWeightDo=(TH2F*)f_ctag->Get("SFl_hist_PUWeightDown");
TH2F *SFb_hist_XSec_DYJetsUp=(TH2F*)f_ctag->Get("SFb_hist_XSec_DYJetsUp");
TH2F *SFb_hist_XSec_DYJetsDo=(TH2F*)f_ctag->Get("SFb_hist_XSec_DYJetsDown");
TH2F *SFc_hist_XSec_DYJetsUp=(TH2F*)f_ctag->Get("SFc_hist_XSec_DYJetsUp");
TH2F *SFc_hist_XSec_DYJetsDo=(TH2F*)f_ctag->Get("SFc_hist_XSec_DYJetsDown");
TH2F *SFl_hist_XSec_DYJetsUp=(TH2F*)f_ctag->Get("SFl_hist_XSec_DYJetsUp");
TH2F *SFl_hist_XSec_DYJetsDo=(TH2F*)f_ctag->Get("SFl_hist_XSec_DYJetsDown");
TH2F *SFb_hist_XSec_STUp=(TH2F*)f_ctag->Get("SFb_hist_XSec_STUp");
TH2F *SFb_hist_XSec_STDo=(TH2F*)f_ctag->Get("SFb_hist_XSec_STDown");
TH2F *SFc_hist_XSec_STUp=(TH2F*)f_ctag->Get("SFc_hist_XSec_STUp");
TH2F *SFc_hist_XSec_STDo=(TH2F*)f_ctag->Get("SFc_hist_XSec_STDown");
TH2F *SFl_hist_XSec_STUp=(TH2F*)f_ctag->Get("SFl_hist_XSec_STUp");
TH2F *SFl_hist_XSec_STDo=(TH2F*)f_ctag->Get("SFl_hist_XSec_STDown");
TH2F *SFb_hist_XSec_VVUp=(TH2F*)f_ctag->Get("SFb_hist_XSec_VVUp");
TH2F *SFb_hist_XSec_VVDo=(TH2F*)f_ctag->Get("SFb_hist_XSec_VVDown");
TH2F *SFc_hist_XSec_VVUp=(TH2F*)f_ctag->Get("SFc_hist_XSec_VVUp");
TH2F *SFc_hist_XSec_VVDo=(TH2F*)f_ctag->Get("SFc_hist_XSec_VVDown");
TH2F *SFl_hist_XSec_VVUp=(TH2F*)f_ctag->Get("SFl_hist_XSec_VVUp");
TH2F *SFl_hist_XSec_VVDo=(TH2F*)f_ctag->Get("SFl_hist_XSec_VVDown");
TH2F *SFb_hist_XSec_WJetsUp=(TH2F*)f_ctag->Get("SFb_hist_XSec_WJetsUp");
TH2F *SFb_hist_XSec_WJetsDo=(TH2F*)f_ctag->Get("SFb_hist_XSec_WJetsDown");
TH2F *SFc_hist_XSec_WJetsUp=(TH2F*)f_ctag->Get("SFc_hist_XSec_WJetsUp");
TH2F *SFc_hist_XSec_WJetsDo=(TH2F*)f_ctag->Get("SFc_hist_XSec_WJetsDown");
TH2F *SFl_hist_XSec_WJetsUp=(TH2F*)f_ctag->Get("SFl_hist_XSec_WJetsUp");
TH2F *SFl_hist_XSec_WJetsDo=(TH2F*)f_ctag->Get("SFl_hist_XSec_WJetsDown");
TH2F *SFb_hist_XSec_ttbarUp=(TH2F*)f_ctag->Get("SFb_hist_XSec_ttbarUp");
TH2F *SFb_hist_XSec_ttbarDo=(TH2F*)f_ctag->Get("SFb_hist_XSec_ttbarDown");
TH2F *SFc_hist_XSec_ttbarUp=(TH2F*)f_ctag->Get("SFc_hist_XSec_ttbarUp");
TH2F *SFc_hist_XSec_ttbarDo=(TH2F*)f_ctag->Get("SFc_hist_XSec_ttbarDown");
TH2F *SFl_hist_XSec_ttbarUp=(TH2F*)f_ctag->Get("SFl_hist_XSec_ttbarUp");
TH2F *SFl_hist_XSec_ttbarDo=(TH2F*)f_ctag->Get("SFl_hist_XSec_ttbarDown");
TH2F *SFb_hist_jerUp=(TH2F*)f_ctag->Get("SFb_hist_jerUp");
TH2F *SFb_hist_jerDo=(TH2F*)f_ctag->Get("SFb_hist_jerDown");
TH2F *SFc_hist_jerUp=(TH2F*)f_ctag->Get("SFc_hist_jerUp");
TH2F *SFc_hist_jerDo=(TH2F*)f_ctag->Get("SFc_hist_jerDown");
TH2F *SFl_hist_jerUp=(TH2F*)f_ctag->Get("SFl_hist_jerUp");
TH2F *SFl_hist_jerDo=(TH2F*)f_ctag->Get("SFl_hist_jerDown");
TH2F *SFb_hist_jesTotalUp=(TH2F*)f_ctag->Get("SFb_hist_jesTotalUp");
TH2F *SFb_hist_jesTotalDo=(TH2F*)f_ctag->Get("SFb_hist_jesTotalDown");
TH2F *SFc_hist_jesTotalUp=(TH2F*)f_ctag->Get("SFc_hist_jesTotalUp");
TH2F *SFc_hist_jesTotalDo=(TH2F*)f_ctag->Get("SFc_hist_jesTotalDown");
TH2F *SFl_hist_jesTotalUp=(TH2F*)f_ctag->Get("SFl_hist_jesTotalUp");
TH2F *SFl_hist_jesTotalDo=(TH2F*)f_ctag->Get("SFl_hist_jesTotalDown");

float ctagSF(ROOT::VecOps::RVec<Int_t> jetid, ROOT::VecOps::RVec<Int_t> jetpuID, ROOT::VecOps::RVec<float> jetpt, ROOT::VecOps::RVec<Int_t> jethadflav, ROOT::VecOps::RVec<float> cvfb, ROOT::VecOps::RVec<float> cvfl, int iw)
{
  float sf=1.;
//  int njet=sizeof(jetid)/sizeof(jetid[0]);
  int njet=3;
  if(iw==0){
  for (int i=0; i<njet;i++)
    { int id_temp=jetid[i];
      if (jetpt[id_temp]<50 && jetpuID[id_temp]==0)continue;
      if (jethadflav[id_temp]==4) sf*=SFc_hist->GetBinContent(SFc_hist->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else if (jethadflav[id_temp]==5) sf*=SFb_hist->GetBinContent(SFb_hist->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else sf*=SFl_hist->GetBinContent(SFl_hist->FindBin(cvfl[id_temp],cvfb[id_temp]));
    }
  }
  else if(iw==1){
  for (int i=0; i<njet;i++)
    { int id_temp=jetid[i];
      if (jetpt[id_temp]<50 && jetpuID[id_temp]==0)continue;
      if (jethadflav[id_temp]==4) sf*=SFc_hist_StatUp->GetBinContent(SFc_hist_StatUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else if (jethadflav[id_temp]==5) sf*=SFb_hist_StatUp->GetBinContent(SFb_hist_StatUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else sf*=SFl_hist_StatUp->GetBinContent(SFl_hist_StatUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
    }
  }
  else if(iw==2){
  for (int i=0; i<njet;i++)
    { int id_temp=jetid[i];
      if (jetpt[id_temp]<50 && jetpuID[id_temp]==0)continue;
      if (jethadflav[id_temp]==4) sf*=SFc_hist_StatDo->GetBinContent(SFc_hist_StatDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else if (jethadflav[id_temp]==5) sf*=SFb_hist_StatDo->GetBinContent(SFb_hist_StatDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else sf*=SFl_hist_StatDo->GetBinContent(SFl_hist_StatDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
    }
  }
  else if(iw==3){
  for (int i=0; i<njet;i++)
    { int id_temp=jetid[i];
      if (jetpt[id_temp]<50 && jetpuID[id_temp]==0)continue;
      if (jethadflav[id_temp]==4) sf*=SFc_hist_EleIDSFUp->GetBinContent(SFc_hist_EleIDSFUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else if (jethadflav[id_temp]==5) sf*=SFb_hist_EleIDSFUp->GetBinContent(SFb_hist_EleIDSFUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else sf*=SFl_hist_EleIDSFUp->GetBinContent(SFl_hist_EleIDSFUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
    }
  }
  else if(iw==4){
  for (int i=0; i<njet;i++)
    { int id_temp=jetid[i];
      if (jetpt[id_temp]<50 && jetpuID[id_temp]==0)continue;
      if (jethadflav[id_temp]==4) sf*=SFc_hist_EleIDSFDo->GetBinContent(SFc_hist_EleIDSFDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else if (jethadflav[id_temp]==5) sf*=SFb_hist_EleIDSFDo->GetBinContent(SFb_hist_EleIDSFDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else sf*=SFl_hist_EleIDSFDo->GetBinContent(SFl_hist_EleIDSFDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
    }
  }
  else if(iw==5){
  for (int i=0; i<njet;i++)
    { int id_temp=jetid[i];
      if (jetpt[id_temp]<50 && jetpuID[id_temp]==0)continue;
      if (jethadflav[id_temp]==4) sf*=SFc_hist_LHEScaleWeight_muFUp->GetBinContent(SFc_hist_LHEScaleWeight_muFUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else if (jethadflav[id_temp]==5) sf*=SFb_hist_LHEScaleWeight_muFUp->GetBinContent(SFb_hist_LHEScaleWeight_muFUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else sf*=SFl_hist_LHEScaleWeight_muFUp->GetBinContent(SFl_hist_LHEScaleWeight_muFUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
    }
  }
  else if(iw==6){
  for (int i=0; i<njet;i++)
    { int id_temp=jetid[i];
      if (jetpt[id_temp]<50 && jetpuID[id_temp]==0)continue;
      if (jethadflav[id_temp]==4) sf*=SFc_hist_LHEScaleWeight_muFDo->GetBinContent(SFc_hist_LHEScaleWeight_muFDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else if (jethadflav[id_temp]==5) sf*=SFb_hist_LHEScaleWeight_muFDo->GetBinContent(SFb_hist_LHEScaleWeight_muFDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else sf*=SFl_hist_LHEScaleWeight_muFDo->GetBinContent(SFl_hist_LHEScaleWeight_muFDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
    }
  }
  else if(iw==7){
  for (int i=0; i<njet;i++)
    { int id_temp=jetid[i];
      if (jetpt[id_temp]<50 && jetpuID[id_temp]==0)continue;
      if (jethadflav[id_temp]==4) sf*=SFc_hist_LHEScaleWeight_muRUp->GetBinContent(SFc_hist_LHEScaleWeight_muRUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else if (jethadflav[id_temp]==5) sf*=SFb_hist_LHEScaleWeight_muRUp->GetBinContent(SFb_hist_LHEScaleWeight_muRUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else sf*=SFl_hist_LHEScaleWeight_muRUp->GetBinContent(SFl_hist_LHEScaleWeight_muRUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
    }
  }
  else if(iw==8){
  for (int i=0; i<njet;i++)
    { int id_temp=jetid[i];
      if (jetpt[id_temp]<50 && jetpuID[id_temp]==0)continue;
      if (jethadflav[id_temp]==4) sf*=SFc_hist_LHEScaleWeight_muRDo->GetBinContent(SFc_hist_LHEScaleWeight_muRDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else if (jethadflav[id_temp]==5) sf*=SFb_hist_LHEScaleWeight_muRDo->GetBinContent(SFb_hist_LHEScaleWeight_muRDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else sf*=SFl_hist_LHEScaleWeight_muRDo->GetBinContent(SFl_hist_LHEScaleWeight_muRDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
    }
  }
  else if(iw==9){
  for (int i=0; i<njet;i++)
    { int id_temp=jetid[i];
      if (jetpt[id_temp]<50 && jetpuID[id_temp]==0)continue;
      if (jethadflav[id_temp]==4) sf*=SFc_hist_MuIDSFUp->GetBinContent(SFc_hist_MuIDSFUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else if (jethadflav[id_temp]==5) sf*=SFb_hist_MuIDSFUp->GetBinContent(SFb_hist_MuIDSFUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else sf*=SFl_hist_MuIDSFUp->GetBinContent(SFl_hist_MuIDSFUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
    }
  }
  else if(iw==10){
  for (int i=0; i<njet;i++)
    { int id_temp=jetid[i];
      if (jetpt[id_temp]<50 && jetpuID[id_temp]==0)continue;
      if (jethadflav[id_temp]==4) sf*=SFc_hist_MuIDSFDo->GetBinContent(SFc_hist_MuIDSFDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else if (jethadflav[id_temp]==5) sf*=SFb_hist_MuIDSFDo->GetBinContent(SFb_hist_MuIDSFDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else sf*=SFl_hist_MuIDSFDo->GetBinContent(SFl_hist_MuIDSFDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
    }
  }
  else if(iw==11){
  for (int i=0; i<njet;i++)
    { int id_temp=jetid[i];
      if (jetpt[id_temp]<50 && jetpuID[id_temp]==0)continue;
      if (jethadflav[id_temp]==4) sf*=SFc_hist_PSWeightFSRUp->GetBinContent(SFc_hist_PSWeightFSRUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else if (jethadflav[id_temp]==5) sf*=SFb_hist_PSWeightFSRUp->GetBinContent(SFb_hist_PSWeightFSRUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else sf*=SFl_hist_PSWeightFSRUp->GetBinContent(SFl_hist_PSWeightFSRUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
    }
  }
  else if(iw==12){
  for (int i=0; i<njet;i++)
    { int id_temp=jetid[i];
      if (jetpt[id_temp]<50 && jetpuID[id_temp]==0)continue;
      if (jethadflav[id_temp]==4) sf*=SFc_hist_PSWeightFSRDo->GetBinContent(SFc_hist_PSWeightFSRDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else if (jethadflav[id_temp]==5) sf*=SFb_hist_PSWeightFSRDo->GetBinContent(SFb_hist_PSWeightFSRDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else sf*=SFl_hist_PSWeightFSRDo->GetBinContent(SFl_hist_PSWeightFSRDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
    }
  }
  else if(iw==13){
  for (int i=0; i<njet;i++)
    { int id_temp=jetid[i];
      if (jetpt[id_temp]<50 && jetpuID[id_temp]==0)continue;
      if (jethadflav[id_temp]==4) sf*=SFc_hist_PSWeightISRUp->GetBinContent(SFc_hist_PSWeightISRUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else if (jethadflav[id_temp]==5) sf*=SFb_hist_PSWeightISRUp->GetBinContent(SFb_hist_PSWeightISRUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else sf*=SFl_hist_PSWeightISRUp->GetBinContent(SFl_hist_PSWeightISRUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
    }
  }
  else if(iw==14){
  for (int i=0; i<njet;i++)
    { int id_temp=jetid[i];
      if (jetpt[id_temp]<50 && jetpuID[id_temp]==0)continue;
      if (jethadflav[id_temp]==4) sf*=SFc_hist_PSWeightISRDo->GetBinContent(SFc_hist_PSWeightISRDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else if (jethadflav[id_temp]==5) sf*=SFb_hist_PSWeightISRDo->GetBinContent(SFb_hist_PSWeightISRDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else sf*=SFl_hist_PSWeightISRDo->GetBinContent(SFl_hist_PSWeightISRDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
    }
  }
  else if(iw==15){
  for (int i=0; i<njet;i++)
    { int id_temp=jetid[i];
      if (jetpt[id_temp]<50 && jetpuID[id_temp]==0)continue;
      if (jethadflav[id_temp]==4) sf*=SFc_hist_PUWeightUp->GetBinContent(SFc_hist_PUWeightUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else if (jethadflav[id_temp]==5) sf*=SFb_hist_PUWeightUp->GetBinContent(SFb_hist_PUWeightUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else sf*=SFl_hist_PUWeightUp->GetBinContent(SFl_hist_PUWeightUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
    }
  }
  else if(iw==16){
  for (int i=0; i<njet;i++)
    { int id_temp=jetid[i];
      if (jetpt[id_temp]<50 && jetpuID[id_temp]==0)continue;
      if (jethadflav[id_temp]==4) sf*=SFc_hist_PUWeightDo->GetBinContent(SFc_hist_PUWeightDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else if (jethadflav[id_temp]==5) sf*=SFb_hist_PUWeightDo->GetBinContent(SFb_hist_PUWeightDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else sf*=SFl_hist_PUWeightDo->GetBinContent(SFl_hist_PUWeightDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
    }
  }
  else if(iw==17){
  for (int i=0; i<njet;i++)
    { int id_temp=jetid[i];
      if (jetpt[id_temp]<50 && jetpuID[id_temp]==0)continue;
      if (jethadflav[id_temp]==4) sf*=SFc_hist_XSec_DYJetsUp->GetBinContent(SFc_hist_XSec_DYJetsUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else if (jethadflav[id_temp]==5) sf*=SFb_hist_XSec_DYJetsUp->GetBinContent(SFb_hist_XSec_DYJetsUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else sf*=SFl_hist_XSec_DYJetsUp->GetBinContent(SFl_hist_XSec_DYJetsUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
    }
  }
  else if(iw==18){
  for (int i=0; i<njet;i++)
    { int id_temp=jetid[i];
      if (jetpt[id_temp]<50 && jetpuID[id_temp]==0)continue;
      if (jethadflav[id_temp]==4) sf*=SFc_hist_XSec_DYJetsDo->GetBinContent(SFc_hist_XSec_DYJetsDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else if (jethadflav[id_temp]==5) sf*=SFb_hist_XSec_DYJetsDo->GetBinContent(SFb_hist_XSec_DYJetsDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else sf*=SFl_hist_XSec_DYJetsDo->GetBinContent(SFl_hist_XSec_DYJetsDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
    }
  }
  else if(iw==19){
  for (int i=0; i<njet;i++)
    { int id_temp=jetid[i];
      if (jetpt[id_temp]<50 && jetpuID[id_temp]==0)continue;
      if (jethadflav[id_temp]==4) sf*=SFc_hist_XSec_STUp->GetBinContent(SFc_hist_XSec_STUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else if (jethadflav[id_temp]==5) sf*=SFb_hist_XSec_STUp->GetBinContent(SFb_hist_XSec_STUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else sf*=SFl_hist_XSec_STUp->GetBinContent(SFl_hist_XSec_STUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
    }
  }
  else if(iw==20){
  for (int i=0; i<njet;i++)
    { int id_temp=jetid[i];
      if (jetpt[id_temp]<50 && jetpuID[id_temp]==0)continue;
      if (jethadflav[id_temp]==4) sf*=SFc_hist_XSec_STDo->GetBinContent(SFc_hist_XSec_STDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else if (jethadflav[id_temp]==5) sf*=SFb_hist_XSec_STDo->GetBinContent(SFb_hist_XSec_STDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else sf*=SFl_hist_XSec_STDo->GetBinContent(SFl_hist_XSec_STDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
    }
  }
  else if(iw==21){
  for (int i=0; i<njet;i++)
    { int id_temp=jetid[i];
      if (jetpt[id_temp]<50 && jetpuID[id_temp]==0)continue;
      if (jethadflav[id_temp]==4) sf*=SFc_hist_XSec_VVUp->GetBinContent(SFc_hist_XSec_VVUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else if (jethadflav[id_temp]==5) sf*=SFb_hist_XSec_VVUp->GetBinContent(SFb_hist_XSec_VVUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else sf*=SFl_hist_XSec_VVUp->GetBinContent(SFl_hist_XSec_VVUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
    }
  }
  else if(iw==22){
  for (int i=0; i<njet;i++)
    { int id_temp=jetid[i];
      if (jetpt[id_temp]<50 && jetpuID[id_temp]==0)continue;
      if (jethadflav[id_temp]==4) sf*=SFc_hist_XSec_VVDo->GetBinContent(SFc_hist_XSec_VVDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else if (jethadflav[id_temp]==5) sf*=SFb_hist_XSec_VVDo->GetBinContent(SFb_hist_XSec_VVDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else sf*=SFl_hist_XSec_VVDo->GetBinContent(SFl_hist_XSec_VVDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
    }
  }
  else if(iw==23){
  for (int i=0; i<njet;i++)
    { int id_temp=jetid[i];
      if (jetpt[id_temp]<50 && jetpuID[id_temp]==0)continue;
      if (jethadflav[id_temp]==4) sf*=SFc_hist_XSec_WJetsUp->GetBinContent(SFc_hist_XSec_WJetsUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else if (jethadflav[id_temp]==5) sf*=SFb_hist_XSec_WJetsUp->GetBinContent(SFb_hist_XSec_WJetsUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else sf*=SFl_hist_XSec_WJetsUp->GetBinContent(SFl_hist_XSec_WJetsUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
    }
  }
  else if(iw==24){
  for (int i=0; i<njet;i++)
    { int id_temp=jetid[i];
      if (jetpt[id_temp]<50 && jetpuID[id_temp]==0)continue;
      if (jethadflav[id_temp]==4) sf*=SFc_hist_XSec_WJetsDo->GetBinContent(SFc_hist_XSec_WJetsDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else if (jethadflav[id_temp]==5) sf*=SFb_hist_XSec_WJetsDo->GetBinContent(SFb_hist_XSec_WJetsDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else sf*=SFl_hist_XSec_WJetsDo->GetBinContent(SFl_hist_XSec_WJetsDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
    }
  }
  else if(iw==25){
  for (int i=0; i<njet;i++)
    { int id_temp=jetid[i];
      if (jetpt[id_temp]<50 && jetpuID[id_temp]==0)continue;
      if (jethadflav[id_temp]==4) sf*=SFc_hist_XSec_ttbarUp->GetBinContent(SFc_hist_XSec_ttbarUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else if (jethadflav[id_temp]==5) sf*=SFb_hist_XSec_ttbarUp->GetBinContent(SFb_hist_XSec_ttbarUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else sf*=SFl_hist_XSec_ttbarUp->GetBinContent(SFl_hist_XSec_ttbarUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
    }
  }
  else if(iw==26){
  for (int i=0; i<njet;i++)
    { int id_temp=jetid[i];
      if (jetpt[id_temp]<50 && jetpuID[id_temp]==0)continue;
      if (jethadflav[id_temp]==4) sf*=SFc_hist_XSec_ttbarDo->GetBinContent(SFc_hist_XSec_ttbarDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else if (jethadflav[id_temp]==5) sf*=SFb_hist_XSec_ttbarDo->GetBinContent(SFb_hist_XSec_ttbarDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else sf*=SFl_hist_XSec_ttbarDo->GetBinContent(SFl_hist_XSec_ttbarDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
    }
  }
  else if(iw==27){
  for (int i=0; i<njet;i++)
    { int id_temp=jetid[i];
      if (jetpt[id_temp]<50 && jetpuID[id_temp]==0)continue;
      if (jethadflav[id_temp]==4) sf*=SFc_hist_jerUp->GetBinContent(SFc_hist_jerUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else if (jethadflav[id_temp]==5) sf*=SFb_hist_jerUp->GetBinContent(SFb_hist_jerUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else sf*=SFl_hist_jerUp->GetBinContent(SFl_hist_jerUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
    }
  }
  else if(iw==28){
  for (int i=0; i<njet;i++)
    { int id_temp=jetid[i];
      if (jetpt[id_temp]<50 && jetpuID[id_temp]==0)continue;
      if (jethadflav[id_temp]==4) sf*=SFc_hist_jerDo->GetBinContent(SFc_hist_jerDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else if (jethadflav[id_temp]==5) sf*=SFb_hist_jerDo->GetBinContent(SFb_hist_jerDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else sf*=SFl_hist_jerDo->GetBinContent(SFl_hist_jerDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
    }
  }
  else if(iw==29){
  for (int i=0; i<njet;i++)
    { int id_temp=jetid[i];
      if (jetpt[id_temp]<50 && jetpuID[id_temp]==0)continue;
      if (jethadflav[id_temp]==4) sf*=SFc_hist_jesTotalUp->GetBinContent(SFc_hist_jesTotalUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else if (jethadflav[id_temp]==5) sf*=SFb_hist_jesTotalUp->GetBinContent(SFb_hist_jesTotalUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else sf*=SFl_hist_jesTotalUp->GetBinContent(SFl_hist_jesTotalUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
    }
  }
  else {
  for (int i=0; i<njet;i++)
    { int id_temp=jetid[i];
      if (jetpt[id_temp]<50 && jetpuID[id_temp]==0)continue;
      if (jethadflav[id_temp]==4) sf*=SFc_hist_jesTotalDo->GetBinContent(SFc_hist_jesTotalDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else if (jethadflav[id_temp]==5) sf*=SFb_hist_jesTotalDo->GetBinContent(SFb_hist_jesTotalDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else sf*=SFl_hist_jesTotalDo->GetBinContent(SFl_hist_jesTotalDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
    }
  }
  return sf;
}

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


//channel 3 is ee, 2 is me, 1 is mm, in me channel, the leading lepton is always muon
float muid(float lep1_pt, float lep1_eta, float lep2_pt, float lep2_eta, int channel){
  float sf=1.;
  if(channel==1)
  { 
    sf*=muSF->GetBinContent(muSF->FindBin(lep1_pt, abs(lep1_eta)));
    sf*=muSF->GetBinContent(muSF->FindBin(lep2_pt, abs(lep2_eta)));
    return sf;
  }
  if(channel==2)
  {
    return muSF->GetBinContent(muSF->FindBin(lep1_pt, abs(lep1_eta)));
  }
  if(channel==3) return 1.;
}

float muid_sysup(float lep1_pt, float lep1_eta, float lep2_pt, float lep2_eta, int channel){
  float sf=1.;
  if(channel==1)
  {
    sf*=(muSF_sys->GetBinContent(muSF_sys->FindBin(lep1_pt, abs(lep1_eta)))+muSF->GetBinContent(muSF->FindBin(lep1_pt, abs(lep1_eta))));
    sf*=(muSF_sys->GetBinContent(muSF_sys->FindBin(lep2_pt, abs(lep2_eta)))+muSF->GetBinContent(muSF->FindBin(lep1_pt, abs(lep1_eta))));
    return sf;
  }
  if(channel==2)
  {
    return (muSF_sys->GetBinContent(muSF_sys->FindBin(lep1_pt, abs(lep1_eta)))+muSF->GetBinContent(muSF->FindBin(lep1_pt, abs(lep1_eta))));
  }
  if(channel==3) return 1.;
}

float muid_sysdo(float lep1_pt, float lep1_eta, float lep2_pt, float lep2_eta, int channel){
  float sf=1.;
  if(channel==1)
  { 
    sf*=(muSF->GetBinContent(muSF->FindBin(lep1_pt, abs(lep1_eta))) - muSF_sys->GetBinContent(muSF_sys->FindBin(lep1_pt, abs(lep1_eta))));
    sf*=(muSF->GetBinContent(muSF->FindBin(lep2_pt, abs(lep2_eta))) - muSF_sys->GetBinContent(muSF_sys->FindBin(lep1_pt, abs(lep1_eta))));
    return sf;
  }
  if(channel==2)
  {
    return (muSF->GetBinContent(muSF->FindBin(lep1_pt, abs(lep1_eta))) - muSF_sys->GetBinContent(muSF_sys->FindBin(lep1_pt, abs(lep1_eta))));
  }
  if(channel==3) return 1.;
}

float muid_statup(float lep1_pt, float lep1_eta, float lep2_pt, float lep2_eta, int channel){
  float sf=1.;
  float U_all1=0.;
  float U_sys1=0.;
  float U_stat1=0.;
  float U_all2=0.;
  float U_sys2=0.;
  float U_stat2=0.;
  if(channel==1)
  { 
    U_all1=muSF_all->GetBinContent(muSF_all->FindBin(lep1_pt, abs(lep1_eta)));
    U_sys1=muSF_sys->GetBinContent(muSF_sys->FindBin(lep1_pt, abs(lep1_eta)));
    U_stat1=sqrt(U_all1*U_all1-U_sys1*U_sys1);
    U_all2=muSF_all->GetBinContent(muSF_all->FindBin(lep2_pt, abs(lep2_eta)));
    U_sys2=muSF_sys->GetBinContent(muSF_sys->FindBin(lep2_pt, abs(lep2_eta)));
    U_stat2=sqrt(U_all2*U_all2-U_sys2*U_sys2);
    sf*=(muSF->GetBinContent(muSF->FindBin(lep1_pt, abs(lep1_eta)))+U_stat1);
    sf*=(muSF->GetBinContent(muSF->FindBin(lep2_pt, abs(lep2_eta)))+U_stat2);
    return sf;
  }
  if(channel==2)
  {
    U_all1=muSF_all->GetBinContent(muSF_all->FindBin(lep1_pt, abs(lep1_eta)));
    U_sys1=muSF_sys->GetBinContent(muSF_sys->FindBin(lep1_pt, abs(lep1_eta)));
    U_stat1=sqrt(U_all1*U_all1-U_sys1*U_sys1);
    sf*=(muSF->GetBinContent(muSF->FindBin(lep1_pt, abs(lep1_eta)))+U_stat1);
    return sf;
  }
  if(channel==3) return 1.;
}

float muid_statdo(float lep1_pt, float lep1_eta, float lep2_pt, float lep2_eta, int channel){
  float sf=1.;
  float U_all1=0.;
  float U_sys1=0.;
  float U_stat1=0.;
  float U_all2=0.;
  float U_sys2=0.;
  float U_stat2=0.;
  if(channel==1)
  { 
    U_all1=muSF_all->GetBinContent(muSF_all->FindBin(lep1_pt, abs(lep1_eta)));
    U_sys1=muSF_sys->GetBinContent(muSF_sys->FindBin(lep1_pt, abs(lep1_eta)));
    U_stat1=sqrt(U_all1*U_all1-U_sys1*U_sys1);
    U_all2=muSF_all->GetBinContent(muSF_all->FindBin(lep2_pt, abs(lep2_eta)));
    U_sys2=muSF_sys->GetBinContent(muSF_sys->FindBin(lep2_pt, abs(lep2_eta)));
    U_stat2=sqrt(U_all2*U_all2-U_sys2*U_sys2);
    sf*=(muSF->GetBinContent(muSF->FindBin(lep1_pt, abs(lep1_eta)))-U_stat1);
    sf*=(muSF->GetBinContent(muSF->FindBin(lep2_pt, abs(lep2_eta)))-U_stat2);
    return sf;
  }
  if(channel==2)
  {
    U_all1=muSF_all->GetBinContent(muSF_all->FindBin(lep1_pt, abs(lep1_eta)));
    U_sys1=muSF_sys->GetBinContent(muSF_sys->FindBin(lep1_pt, abs(lep1_eta)));
    U_stat1=sqrt(U_all1*U_all1-U_sys1*U_sys1);
    sf*=(muSF->GetBinContent(muSF->FindBin(lep1_pt, abs(lep1_eta)))-U_stat1);
    return sf;
  }
  if(channel==3) return 1.;
}

//channel 3 is ee, 2 is me, 1 is mm, in me channel, the leading lepton is always muon
float eleid(float lep1_pt, float lep1_eta, float lep2_pt, float lep2_eta, int channel){
  if(channel==1)return 1.0;
  if(channel==2) return eleSF->GetBinContent(eleSF->FindBin(lep2_pt, abs(lep2_eta)));
  if(channel==3) return eleSF->GetBinContent(eleSF->FindBin(lep1_pt, abs(lep1_eta)))*eleSF->GetBinContent(eleSF->FindBin(lep2_pt, abs(lep2_eta)));
}

float eleid_sysup(float lep1_pt, float lep1_eta, float lep2_pt, float lep2_eta, int channel){
  if(channel==1)return 1.0;
  if(channel==2) return eleSF->GetBinContent(eleSF->FindBin(lep2_pt, abs(lep2_eta)))+eleSF->GetBinError(eleSF->FindBin(lep2_pt, abs(lep2_eta)));
  if(channel==3) return (eleSF->GetBinContent(eleSF->FindBin(lep1_pt, abs(lep1_eta)))+eleSF->GetBinError(eleSF->FindBin(lep1_pt, abs(lep1_eta))))*(eleSF->GetBinContent(eleSF->FindBin(lep2_pt, abs(lep2_eta)))+eleSF->GetBinError(eleSF->FindBin(lep2_pt, abs(lep2_eta))));
}

float eleid_sysdo(float lep1_pt, float lep1_eta, float lep2_pt, float lep2_eta, int channel){
  if(channel==1)return 1.0;
  if(channel==2) return eleSF->GetBinContent(eleSF->FindBin(lep2_pt, abs(lep2_eta)))-eleSF->GetBinError(eleSF->FindBin(lep2_pt, abs(lep2_eta)));
  if(channel==3) return (eleSF->GetBinContent(eleSF->FindBin(lep1_pt, abs(lep1_eta)))-eleSF->GetBinError(eleSF->FindBin(lep1_pt, abs(lep1_eta))))*(eleSF->GetBinContent(eleSF->FindBin(lep2_pt, abs(lep2_eta)))-eleSF->GetBinError(eleSF->FindBin(lep2_pt, abs(lep2_eta))));
}

float eleid_statup(float lep1_pt, float lep1_eta, float lep2_pt, float lep2_eta, int channel){
  if(channel==1)return 1.0;
  if(channel==2) return eleSF->GetBinContent(eleSF->FindBin(lep2_pt, abs(lep2_eta)))+0.001;
  if(channel==3) return (eleSF->GetBinContent(eleSF->FindBin(lep1_pt, abs(lep1_eta)))+0.001)*(eleSF->GetBinContent(eleSF->FindBin(lep2_pt, abs(lep2_eta)))+0.001);
}

float eleid_statdo(float lep1_pt, float lep1_eta, float lep2_pt, float lep2_eta, int channel){
  if(channel==1)return 1.0;
  if(channel==2) return eleSF->GetBinContent(eleSF->FindBin(lep2_pt, abs(lep2_eta)))-0.001;
  if(channel==3) return (eleSF->GetBinContent(eleSF->FindBin(lep1_pt, abs(lep1_eta)))-0.001)*(eleSF->GetBinContent(eleSF->FindBin(lep2_pt, abs(lep2_eta)))-0.001);
}

float lep_trigger(float eta1, float eta2, int channel)
{
  if(channel==3) return diele_trigger->GetBinContent(diele_trigger->FindBin(abs(eta1),abs(eta2)));
  if(channel==1) return dimu_trigger->GetBinContent(dimu_trigger->FindBin(abs(eta1),abs(eta2)));
  if(channel==2) return muele_trigger->GetBinContent(muele_trigger->FindBin(abs(eta1),abs(eta2)));
}

float lep_triggerup(float eta1, float eta2, int channel)
{
  if(channel==3) return (diele_trigger->GetBinContent(diele_trigger->FindBin(abs(eta1),abs(eta2)))+diele_trigger->GetBinError(diele_trigger->FindBin(abs(eta1),abs(eta2))));
  if(channel==1) return (dimu_trigger->GetBinContent(dimu_trigger->FindBin(abs(eta1),abs(eta2)))+dimu_trigger->GetBinError(dimu_trigger->FindBin(abs(eta1),abs(eta2))));
  if(channel==2) return (muele_trigger->GetBinContent(muele_trigger->FindBin(abs(eta1),abs(eta2)))+muele_trigger->GetBinError(muele_trigger->FindBin(abs(eta1),abs(eta2))));
}

float lep_triggerdown(float eta1, float eta2, int channel)
{
  if(channel==3) return (diele_trigger->GetBinContent(diele_trigger->FindBin(abs(eta1),abs(eta2)))-diele_trigger->GetBinError(diele_trigger->FindBin(abs(eta1),abs(eta2))));
  if(channel==1) return (dimu_trigger->GetBinContent(dimu_trigger->FindBin(abs(eta1),abs(eta2)))-dimu_trigger->GetBinError(dimu_trigger->FindBin(abs(eta1),abs(eta2))));
  if(channel==2) return (muele_trigger->GetBinContent(muele_trigger->FindBin(abs(eta1),abs(eta2)))-muele_trigger->GetBinError(muele_trigger->FindBin(abs(eta1),abs(eta2))));
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
