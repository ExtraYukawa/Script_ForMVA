#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "TCanvas.h"
#include "TH1D.h"
#include "TLatex.h"
#include "Math/Vector4D.h"
#include "Math/Vector4Dfwd.h"
#include "TStyle.h"
#include "TString.h"

using namespace ROOT;
using namespace std;
using namespace ROOT::VecOps;

TString era = "EraToBeReplaced";

TFile*f_mu=TFile::Open("../../data/fr_data_mu_"+era+".root");
TFile*f_ele=TFile::Open("../../data/fr_data_ele_"+era+".root");


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

TFile*f_chargeflip=TFile::Open("../../data/ChargeFlipProbability_"+era+"_MLE.root");
TH2D*Prob_data=(TH2D*)f_chargeflip->Get("data_CFRate");
TH2D*Prob_mc=(TH2D*)f_chargeflip->Get("MC_CFRate");
TH2D*Cov_data=(TH2D*)f_chargeflip->Get("data_CovMatrix");
TH2D*Cov_MC=(TH2D*)f_chargeflip->Get("MC_CovMatrix");
TH1D*Chaflip_unc=(TH1D*)f_chargeflip->Get("overall_sys");
float Chaflip_unc_num=Chaflip_unc->GetBinContent(1);

TFile*f_sigunc=TFile::Open("../../data/signalunc.root");
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

    int pt1_index  = ((Prob_data->FindBin(lep1_pt,abs(lep1_eta)))%(Prob_data->GetNbinsX()+2))-1;
    int pt2_index  = ((Prob_data->FindBin(lep2_pt,abs(lep2_eta)))%(Prob_data->GetNbinsX()+2))-1;
    int eta1_index = ((Prob_data->FindBin(lep1_pt,abs(lep1_eta)))/(Prob_data->GetNbinsX()+2))-1;
    int eta2_index = ((Prob_data->FindBin(lep2_pt,abs(lep2_eta)))/(Prob_data->GetNbinsX()+2))-1;
    int index1     = pt1_index*(Prob_data->GetNbinsY()) + eta1_index + 1;
    int index2     = pt2_index*(Prob_data->GetNbinsY()) + eta2_index + 1;
    float data_error2_p1   = Cov_data->GetBinContent(index1,index1);
    float data_error2_p2   = Cov_data->GetBinContent(index2,index2);
    float data_error2_p1p2 = Cov_data->GetBinContent(index1,index2);
    float data_error2      = ((1.-2.*prob2_data)*(1.-2.*prob2_data))*data_error2_p1 + ((1.-2.*prob1_data)*(1.-2.*prob1_data))*data_error2_p2 + 2.*(1.-2.*prob1_data)*(1.-2.*prob2_data)*data_error2_p1p2;
    float MC_error2_p1     = Cov_MC->GetBinContent(index1,index1);
    float MC_error2_p2     = Cov_MC->GetBinContent(index2,index2);
    float MC_error2_p1p2   = Cov_MC->GetBinContent(index1,index2);
    float MC_error2        = ((1.-2.*prob2_mc)*(1.-2.*prob2_mc))*MC_error2_p1 + ((1.-2.*prob1_mc)*(1.-2.*prob1_mc))*MC_error2_p2 + 2.*(1.-2.*prob1_mc)*(1.-2.*prob2_mc)*MC_error2_p1p2;
    
    float prob_data = prob1_data + prob2_data - 2*prob1_data*prob2_data;
    float prob_MC   = prob1_mc   + prob2_mc   - 2*prob1_mc*prob2_mc;

    sf=prob_data/prob_MC;

    float sf_stat_error    = sqrt((data_error2/(prob_data*prob_data)) + (MC_error2/(prob_MC*prob_MC)))*sf;
    if(iw==0) return sf;
    if(iw==1) return (sf*(1.+Chaflip_unc_num)); //SystUp
    if(iw==2) return (sf*(1.-Chaflip_unc_num)); //SystDown
    if(iw==3) return (sf+sf_stat_error);        //StatUp
    if(iw==4){                                  //StatDown
      if((sf-sf_stat_error) > 0) return sf-sf_stat_error;
      else                       return 0.;
    }
  }
  else {return 1.;}
}

TFile*f_eleSF=TFile::Open("../../data/EleIDSF_"+era+".root");
TH2D *eleSF=(TH2D*)f_eleSF->Get("EleIDSF");
TFile*f_muSF=TFile::Open("../../data/muonIdSF_"+era+"UL.root");
TH2D *muSF=(TH2D*)f_muSF->Get("muIdSF");
TH2D *muSF_sys=(TH2D*)f_muSF->Get("muIdSF_syst");
TH2D *muSF_stat=(TH2D*)f_muSF->Get("muIdSF_stat");

TFile*f_trigger=TFile::Open("../../data/TriggerSF_"+era+"UL.root");
TH2D *diele_trigger=(TH2D*)f_trigger->Get("h2D_SF_ee_SF_l1l2pt");
TH2D *dimu_trigger=(TH2D*)f_trigger->Get("h2D_SF_mumu_SF_l1l2pt");
TH2D *muele_trigger=(TH2D*)f_trigger->Get("h2D_SF_emu_SF_l1l2pt");

TFile*f_ctag=TFile::Open("../../data/DeepJet_ctagSF_Summer"+era+"UL.root");
TH2F *SFb_hist=(TH2F*)f_ctag->Get("SFb_hist");
TH2F *SFc_hist=(TH2F*)f_ctag->Get("SFc_hist");
TH2F *SFl_hist=(TH2F*)f_ctag->Get("SFl_hist");
TH2F *SFb_hist_StatUp=(TH2F*)f_ctag->Get("SFb_hist_StatUp");
TH2F *SFb_hist_StatDo=(TH2F*)f_ctag->Get("SFb_hist_StatDown");
TH2F *SFc_hist_StatUp=(TH2F*)f_ctag->Get("SFc_hist_StatUp");
TH2F *SFc_hist_StatDo=(TH2F*)f_ctag->Get("SFc_hist_StatDown");
TH2F *SFl_hist_StatUp=(TH2F*)f_ctag->Get("SFl_hist_StatUp");
TH2F *SFl_hist_StatDo=(TH2F*)f_ctag->Get("SFl_hist_StatDown");
TH2F *SFb_hist_ExtrapUp=(TH2F*)f_ctag->Get("SFb_hist_ExtrapUp");
TH2F *SFb_hist_ExtrapDo=(TH2F*)f_ctag->Get("SFb_hist_ExtrapDown");
TH2F *SFc_hist_ExtrapUp=(TH2F*)f_ctag->Get("SFc_hist_ExtrapUp");
TH2F *SFc_hist_ExtrapDo=(TH2F*)f_ctag->Get("SFc_hist_ExtrapDown");
TH2F *SFl_hist_ExtrapUp=(TH2F*)f_ctag->Get("SFl_hist_ExtrapUp");
TH2F *SFl_hist_ExtrapDo=(TH2F*)f_ctag->Get("SFl_hist_ExtrapDown");
TH2F *SFb_hist_InterpUp=(TH2F*)f_ctag->Get("SFb_hist_InterpUp");
TH2F *SFb_hist_InterpDo=(TH2F*)f_ctag->Get("SFb_hist_InterpDown");
TH2F *SFc_hist_InterpUp=(TH2F*)f_ctag->Get("SFc_hist_InterpUp");
TH2F *SFc_hist_InterpDo=(TH2F*)f_ctag->Get("SFc_hist_InterpDown");
TH2F *SFl_hist_InterpUp=(TH2F*)f_ctag->Get("SFl_hist_InterpUp");
TH2F *SFl_hist_InterpDo=(TH2F*)f_ctag->Get("SFl_hist_InterpDown");
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
TH2F *SFb_hist_PSWeightFSRUp=(TH2F*)f_ctag->Get("SFb_hist_PSWeightFSRFixedUp");
TH2F *SFb_hist_PSWeightFSRDo=(TH2F*)f_ctag->Get("SFb_hist_PSWeightFSRFixedDown");
TH2F *SFc_hist_PSWeightFSRUp=(TH2F*)f_ctag->Get("SFc_hist_PSWeightFSRFixedUp");
TH2F *SFc_hist_PSWeightFSRDo=(TH2F*)f_ctag->Get("SFc_hist_PSWeightFSRFixedDown");
TH2F *SFl_hist_PSWeightFSRUp=(TH2F*)f_ctag->Get("SFl_hist_PSWeightFSRFixedUp");
TH2F *SFl_hist_PSWeightFSRDo=(TH2F*)f_ctag->Get("SFl_hist_PSWeightFSRFixedDown");
TH2F *SFb_hist_PSWeightISRUp=(TH2F*)f_ctag->Get("SFb_hist_PSWeightISRFixedUp");
TH2F *SFb_hist_PSWeightISRDo=(TH2F*)f_ctag->Get("SFb_hist_PSWeightISRFixedDown");
TH2F *SFc_hist_PSWeightISRUp=(TH2F*)f_ctag->Get("SFc_hist_PSWeightISRFixedUp");
TH2F *SFc_hist_PSWeightISRDo=(TH2F*)f_ctag->Get("SFc_hist_PSWeightISRFixedDown");
TH2F *SFl_hist_PSWeightISRUp=(TH2F*)f_ctag->Get("SFl_hist_PSWeightISRFixedUp");
TH2F *SFl_hist_PSWeightISRDo=(TH2F*)f_ctag->Get("SFl_hist_PSWeightISRFixedDown");
TH2F *SFb_hist_PUWeightUp=(TH2F*)f_ctag->Get("SFb_hist_PUWeightUp");
TH2F *SFb_hist_PUWeightDo=(TH2F*)f_ctag->Get("SFb_hist_PUWeightDown");
TH2F *SFc_hist_PUWeightUp=(TH2F*)f_ctag->Get("SFc_hist_PUWeightUp");
TH2F *SFc_hist_PUWeightDo=(TH2F*)f_ctag->Get("SFc_hist_PUWeightDown");
TH2F *SFl_hist_PUWeightUp=(TH2F*)f_ctag->Get("SFl_hist_PUWeightUp");
TH2F *SFl_hist_PUWeightDo=(TH2F*)f_ctag->Get("SFl_hist_PUWeightDown");
TH2F *SFb_hist_XSec_BRUnc_DYJets_bUp=(TH2F*)f_ctag->Get("SFb_hist_XSec_BRUnc_DYJets_bUp");
TH2F *SFb_hist_XSec_BRUnc_DYJets_bDo=(TH2F*)f_ctag->Get("SFb_hist_XSec_BRUnc_DYJets_bDown");
TH2F *SFc_hist_XSec_BRUnc_DYJets_bUp=(TH2F*)f_ctag->Get("SFc_hist_XSec_BRUnc_DYJets_bUp");
TH2F *SFc_hist_XSec_BRUnc_DYJets_bDo=(TH2F*)f_ctag->Get("SFc_hist_XSec_BRUnc_DYJets_bDown");
TH2F *SFl_hist_XSec_BRUnc_DYJets_bUp=(TH2F*)f_ctag->Get("SFl_hist_XSec_BRUnc_DYJets_bUp");
TH2F *SFl_hist_XSec_BRUnc_DYJets_bDo=(TH2F*)f_ctag->Get("SFl_hist_XSec_BRUnc_DYJets_bDown");
TH2F *SFb_hist_XSec_BRUnc_DYJets_cUp=(TH2F*)f_ctag->Get("SFb_hist_XSec_BRUnc_DYJets_cUp");
TH2F *SFb_hist_XSec_BRUnc_DYJets_cDo=(TH2F*)f_ctag->Get("SFb_hist_XSec_BRUnc_DYJets_cDown");
TH2F *SFc_hist_XSec_BRUnc_DYJets_cUp=(TH2F*)f_ctag->Get("SFc_hist_XSec_BRUnc_DYJets_cUp");
TH2F *SFc_hist_XSec_BRUnc_DYJets_cDo=(TH2F*)f_ctag->Get("SFc_hist_XSec_BRUnc_DYJets_cDown");
TH2F *SFl_hist_XSec_BRUnc_DYJets_cUp=(TH2F*)f_ctag->Get("SFl_hist_XSec_BRUnc_DYJets_cUp");
TH2F *SFl_hist_XSec_BRUnc_DYJets_cDo=(TH2F*)f_ctag->Get("SFl_hist_XSec_BRUnc_DYJets_cDown");
TH2F *SFb_hist_XSec_BRUnc_WJets_cUp=(TH2F*)f_ctag->Get("SFb_hist_XSec_BRUnc_WJets_cUp");
TH2F *SFb_hist_XSec_BRUnc_WJets_cDo=(TH2F*)f_ctag->Get("SFb_hist_XSec_BRUnc_WJets_cDown");
TH2F *SFc_hist_XSec_BRUnc_WJets_cUp=(TH2F*)f_ctag->Get("SFc_hist_XSec_BRUnc_WJets_cUp");
TH2F *SFc_hist_XSec_BRUnc_WJets_cDo=(TH2F*)f_ctag->Get("SFc_hist_XSec_BRUnc_WJets_cDown");
TH2F *SFl_hist_XSec_BRUnc_WJets_cUp=(TH2F*)f_ctag->Get("SFl_hist_XSec_BRUnc_WJets_cUp");
TH2F *SFl_hist_XSec_BRUnc_WJets_cDo=(TH2F*)f_ctag->Get("SFl_hist_XSec_BRUnc_WJets_cDown");
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
  int njet=jetid.size();
//  int njet = 3;
  if(iw==0){
  for (int i=0; i<njet; i++)
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
      if (jethadflav[id_temp]==4) sf*=SFc_hist_ExtrapUp->GetBinContent(SFc_hist_ExtrapUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else if (jethadflav[id_temp]==5) sf*=SFb_hist_ExtrapUp->GetBinContent(SFb_hist_ExtrapUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else sf*=SFl_hist_ExtrapUp->GetBinContent(SFl_hist_ExtrapUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
    }
  }
  else if(iw==4){
  for (int i=0; i<njet;i++)
    { int id_temp=jetid[i];
      if (jetpt[id_temp]<50 && jetpuID[id_temp]==0)continue;
      if (jethadflav[id_temp]==4) sf*=SFc_hist_ExtrapDo->GetBinContent(SFc_hist_ExtrapDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else if (jethadflav[id_temp]==5) sf*=SFb_hist_ExtrapDo->GetBinContent(SFb_hist_ExtrapDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else sf*=SFl_hist_ExtrapDo->GetBinContent(SFl_hist_ExtrapDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
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
      if (jethadflav[id_temp]==4) sf*=SFc_hist_InterpUp->GetBinContent(SFc_hist_InterpUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else if (jethadflav[id_temp]==5) sf*=SFb_hist_InterpUp->GetBinContent(SFb_hist_InterpUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else sf*=SFl_hist_InterpUp->GetBinContent(SFl_hist_InterpUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
    }
  }
  else if(iw==10){
  for (int i=0; i<njet;i++)
    { int id_temp=jetid[i];
      if (jetpt[id_temp]<50 && jetpuID[id_temp]==0)continue;
      if (jethadflav[id_temp]==4) sf*=SFc_hist_InterpDo->GetBinContent(SFc_hist_InterpDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else if (jethadflav[id_temp]==5) sf*=SFb_hist_InterpDo->GetBinContent(SFb_hist_InterpDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else sf*=SFl_hist_InterpDo->GetBinContent(SFl_hist_InterpDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
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
      if (jethadflav[id_temp]==4) sf*=SFc_hist_XSec_BRUnc_DYJets_bUp->GetBinContent(SFc_hist_XSec_BRUnc_DYJets_bUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else if (jethadflav[id_temp]==5) sf*=SFb_hist_XSec_BRUnc_DYJets_bUp->GetBinContent(SFb_hist_XSec_BRUnc_DYJets_bUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else sf*=SFl_hist_XSec_BRUnc_DYJets_bUp->GetBinContent(SFl_hist_XSec_BRUnc_DYJets_bUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
    }
  }
  else if(iw==18){
  for (int i=0; i<njet;i++)
    { int id_temp=jetid[i];
      if (jetpt[id_temp]<50 && jetpuID[id_temp]==0)continue;
      if (jethadflav[id_temp]==4) sf*=SFc_hist_XSec_BRUnc_DYJets_bDo->GetBinContent(SFc_hist_XSec_BRUnc_DYJets_bDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else if (jethadflav[id_temp]==5) sf*=SFb_hist_XSec_BRUnc_DYJets_bDo->GetBinContent(SFb_hist_XSec_BRUnc_DYJets_bDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else sf*=SFl_hist_XSec_BRUnc_DYJets_bDo->GetBinContent(SFl_hist_XSec_BRUnc_DYJets_bDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
    }
  }
  else if(iw==19){
  for (int i=0; i<njet;i++)
    { int id_temp=jetid[i];
      if (jetpt[id_temp]<50 && jetpuID[id_temp]==0)continue;
      if (jethadflav[id_temp]==4) sf*=SFc_hist_XSec_BRUnc_DYJets_cUp->GetBinContent(SFc_hist_XSec_BRUnc_DYJets_cUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else if (jethadflav[id_temp]==5) sf*=SFb_hist_XSec_BRUnc_DYJets_cUp->GetBinContent(SFb_hist_XSec_BRUnc_DYJets_cUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else sf*=SFl_hist_XSec_BRUnc_DYJets_cUp->GetBinContent(SFl_hist_XSec_BRUnc_DYJets_cUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
    }
  }
  else if(iw==20){
  for (int i=0; i<njet;i++)
    { int id_temp=jetid[i];
      if (jetpt[id_temp]<50 && jetpuID[id_temp]==0)continue;
      if (jethadflav[id_temp]==4) sf*=SFc_hist_XSec_BRUnc_DYJets_cDo->GetBinContent(SFc_hist_XSec_BRUnc_DYJets_cDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else if (jethadflav[id_temp]==5) sf*=SFb_hist_XSec_BRUnc_DYJets_cDo->GetBinContent(SFb_hist_XSec_BRUnc_DYJets_cDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else sf*=SFl_hist_XSec_BRUnc_DYJets_cDo->GetBinContent(SFl_hist_XSec_BRUnc_DYJets_cDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
    }
  }
  else if(iw==21){
  for (int i=0; i<njet;i++)
    { int id_temp=jetid[i];
      if (jetpt[id_temp]<50 && jetpuID[id_temp]==0)continue;
      if (jethadflav[id_temp]==4) sf*=SFc_hist_XSec_BRUnc_WJets_cUp->GetBinContent(SFc_hist_XSec_BRUnc_WJets_cUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else if (jethadflav[id_temp]==5) sf*=SFb_hist_XSec_BRUnc_WJets_cUp->GetBinContent(SFb_hist_XSec_BRUnc_WJets_cUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else sf*=SFl_hist_XSec_BRUnc_WJets_cUp->GetBinContent(SFl_hist_XSec_BRUnc_WJets_cUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
    }
  }
  else if(iw==22){
  for (int i=0; i<njet;i++)
    { int id_temp=jetid[i];
      if (jetpt[id_temp]<50 && jetpuID[id_temp]==0)continue;
      if (jethadflav[id_temp]==4) sf*=SFc_hist_XSec_BRUnc_WJets_cDo->GetBinContent(SFc_hist_XSec_BRUnc_WJets_cDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else if (jethadflav[id_temp]==5) sf*=SFb_hist_XSec_BRUnc_WJets_cDo->GetBinContent(SFb_hist_XSec_BRUnc_WJets_cDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else sf*=SFl_hist_XSec_BRUnc_WJets_cDo->GetBinContent(SFl_hist_XSec_BRUnc_WJets_cDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
    }
  }
  else if(iw==23){
  for (int i=0; i<njet;i++)
    { int id_temp=jetid[i];
      if (jetpt[id_temp]<50 && jetpuID[id_temp]==0)continue;
      if (jethadflav[id_temp]==4) sf*=SFc_hist_jerUp->GetBinContent(SFc_hist_jerUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else if (jethadflav[id_temp]==5) sf*=SFb_hist_jerUp->GetBinContent(SFb_hist_jerUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else sf*=SFl_hist_jerUp->GetBinContent(SFl_hist_jerUp->FindBin(cvfl[id_temp],cvfb[id_temp]));
    }
  }
  else if(iw==24){
  for (int i=0; i<njet;i++)
    { int id_temp=jetid[i];
      if (jetpt[id_temp]<50 && jetpuID[id_temp]==0)continue;
      if (jethadflav[id_temp]==4) sf*=SFc_hist_jerDo->GetBinContent(SFc_hist_jerDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else if (jethadflav[id_temp]==5) sf*=SFb_hist_jerDo->GetBinContent(SFb_hist_jerDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
      else sf*=SFl_hist_jerDo->GetBinContent(SFl_hist_jerDo->FindBin(cvfl[id_temp],cvfb[id_temp]));
    }
  }
  else if(iw==25){
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

  if (lep1_pt>119.) lep1_pt=119.;
  if (lep2_pt>119.) lep2_pt=119.;

  float sf=1.;
  if(channel==1)
  { 
    sf*=muSF->GetBinContent(muSF->FindBin(abs(lep1_eta), lep1_pt));
    sf*=muSF->GetBinContent(muSF->FindBin(abs(lep2_eta), lep2_pt));
    return sf;
  }
  if(channel==2)
  {
    return muSF->GetBinContent(muSF->FindBin(abs(lep1_eta), lep1_pt));
  }
  if(channel==3) return 1.;
}

float muid_sysup(float lep1_pt, float lep1_eta, float lep2_pt, float lep2_eta, int channel){

  if (lep1_pt>119.) lep1_pt=119.;
  if (lep2_pt>119.) lep2_pt=119.;

  float sf=1.;
  if(channel==1)
  {
    sf*=(muSF_sys->GetBinError(muSF_sys->FindBin(abs(lep1_eta), lep1_pt))+muSF->GetBinContent(muSF->FindBin(abs(lep1_eta), lep1_pt)));
    sf*=(muSF_sys->GetBinError(muSF_sys->FindBin(abs(lep2_eta), lep2_pt))+muSF->GetBinContent(muSF->FindBin(abs(lep2_eta), lep2_pt)));
    return sf;
  }
  if(channel==2)
  {
    return (muSF_sys->GetBinError(muSF_sys->FindBin(abs(lep1_eta), lep1_pt))+muSF->GetBinContent(muSF->FindBin(abs(lep1_eta), lep1_pt)));
  }
  if(channel==3) return 1.;
}

float muid_sysdo(float lep1_pt, float lep1_eta, float lep2_pt, float lep2_eta, int channel){

  if (lep1_pt>119.) lep1_pt=119.;
  if (lep2_pt>119.) lep2_pt=119.;

  float sf=1.;
  if(channel==1)
  { 
    sf*=(muSF->GetBinContent(muSF->FindBin(abs(lep1_eta), lep1_pt)) - muSF_sys->GetBinError(muSF_sys->FindBin(abs(lep1_eta), lep1_pt)));
    sf*=(muSF->GetBinContent(muSF->FindBin(abs(lep2_eta), lep2_pt)) - muSF_sys->GetBinError(muSF_sys->FindBin(abs(lep2_eta), lep2_pt)));
    return sf;
  }
  if(channel==2)
  {
    return (muSF->GetBinContent(muSF->FindBin(abs(lep1_eta), lep1_pt)) - muSF_sys->GetBinError(muSF_sys->FindBin(abs(lep1_eta), lep1_pt)));
  }
  if(channel==3) return 1.;
}

float muid_statup(float lep1_pt, float lep1_eta, float lep2_pt, float lep2_eta, int channel){

  if (lep1_pt>119.) lep1_pt=119.;
  if (lep2_pt>119.) lep2_pt=119.;

  float sf=1.;
  if(channel==1)
  {
    sf*=(muSF->GetBinContent(muSF->FindBin(abs(lep1_eta), lep1_pt)) + muSF_stat->GetBinError(muSF_stat->FindBin(abs(lep1_eta), lep1_pt)));
    sf*=(muSF->GetBinContent(muSF->FindBin(abs(lep2_eta), lep2_pt)) + muSF_stat->GetBinError(muSF_stat->FindBin(abs(lep2_eta), lep2_pt)));
    return sf;
  }
  if(channel==2)
  {
    return (muSF->GetBinContent(muSF->FindBin(abs(lep1_eta), lep1_pt)) + muSF_stat->GetBinError(muSF_stat->FindBin(abs(lep1_eta), lep1_pt)));
  }
  if(channel==3) return 1.;

}

float muid_statdo(float lep1_pt, float lep1_eta, float lep2_pt, float lep2_eta, int channel){

  if (lep1_pt>119.) lep1_pt=119.;
  if (lep2_pt>119.) lep2_pt=119.;

  float sf=1.;
  if(channel==1)
  {
    sf*=(muSF->GetBinContent(muSF->FindBin(abs(lep1_eta), lep1_pt)) - muSF_stat->GetBinError(muSF_stat->FindBin(abs(lep1_eta), lep1_pt)));
    sf*=(muSF->GetBinContent(muSF->FindBin(abs(lep2_eta), lep2_pt)) - muSF_stat->GetBinError(muSF_stat->FindBin(abs(lep2_eta), lep2_pt)));
    return sf;
  }
  if(channel==2)
  {
    return (muSF->GetBinContent(muSF->FindBin(abs(lep1_eta), lep1_pt)) - muSF_stat->GetBinError(muSF_stat->FindBin(abs(lep1_eta), lep1_pt)));
  }
  if(channel==3) return 1.;

}

//channel 3 is ee, 2 is me, 1 is mm, in me channel, the leading lepton is always muon
float eleid(float lep1_pt, float lep1_eta, float lep2_pt, float lep2_eta, int channel){

  if (lep1_pt>499.) lep1_pt = 499.;
  if (lep2_pt>499.) lep2_pt = 499.;  

  if(channel==1)return 1.0;
  if(channel==2) return eleSF->GetBinContent(eleSF->FindBin(lep2_pt, abs(lep2_eta)));
  if(channel==3) return eleSF->GetBinContent(eleSF->FindBin(lep1_pt, abs(lep1_eta)))*eleSF->GetBinContent(eleSF->FindBin(lep2_pt, abs(lep2_eta)));
}

float eleid_sysup(float lep1_pt, float lep1_eta, float lep2_pt, float lep2_eta, int channel){

  if (lep1_pt>499.) lep1_pt = 499.;
  if (lep2_pt>499.) lep2_pt = 499.;

  if(channel==1)return 1.0;
  if(channel==2) return eleSF->GetBinContent(eleSF->FindBin(lep2_pt, abs(lep2_eta)))+eleSF->GetBinError(eleSF->FindBin(lep2_pt, abs(lep2_eta)));
  if(channel==3) return (eleSF->GetBinContent(eleSF->FindBin(lep1_pt, abs(lep1_eta)))+eleSF->GetBinError(eleSF->FindBin(lep1_pt, abs(lep1_eta))))*(eleSF->GetBinContent(eleSF->FindBin(lep2_pt, abs(lep2_eta)))+eleSF->GetBinError(eleSF->FindBin(lep2_pt, abs(lep2_eta))));
}

float eleid_sysdo(float lep1_pt, float lep1_eta, float lep2_pt, float lep2_eta, int channel){

  if (lep1_pt>499.) lep1_pt = 499.;
  if (lep2_pt>499.) lep2_pt = 499.;

  if(channel==1)return 1.0;
  if(channel==2) return eleSF->GetBinContent(eleSF->FindBin(lep2_pt, abs(lep2_eta)))-eleSF->GetBinError(eleSF->FindBin(lep2_pt, abs(lep2_eta)));
  if(channel==3) return (eleSF->GetBinContent(eleSF->FindBin(lep1_pt, abs(lep1_eta)))-eleSF->GetBinError(eleSF->FindBin(lep1_pt, abs(lep1_eta))))*(eleSF->GetBinContent(eleSF->FindBin(lep2_pt, abs(lep2_eta)))-eleSF->GetBinError(eleSF->FindBin(lep2_pt, abs(lep2_eta))));
}

float eleid_statup(float lep1_pt, float lep1_eta, float lep2_pt, float lep2_eta, int channel){

  if (lep1_pt>499.) lep1_pt = 499.;
  if (lep2_pt>499.) lep2_pt = 499.;

  if(channel==1)return 1.0;
  if(channel==2) return eleSF->GetBinContent(eleSF->FindBin(lep2_pt, abs(lep2_eta)))+0.001;
  if(channel==3) return (eleSF->GetBinContent(eleSF->FindBin(lep1_pt, abs(lep1_eta)))+0.001)*(eleSF->GetBinContent(eleSF->FindBin(lep2_pt, abs(lep2_eta)))+0.001);
}

float eleid_statdo(float lep1_pt, float lep1_eta, float lep2_pt, float lep2_eta, int channel){

  if(lep1_pt>499.) lep1_pt = 499.;
  if(lep2_pt>499.) lep2_pt = 499.;

  if(channel==1)return 1.0;
  if(channel==2) return eleSF->GetBinContent(eleSF->FindBin(lep2_pt, abs(lep2_eta)))-0.001;
  if(channel==3) return (eleSF->GetBinContent(eleSF->FindBin(lep1_pt, abs(lep1_eta)))-0.001)*(eleSF->GetBinContent(eleSF->FindBin(lep2_pt, abs(lep2_eta)))-0.001);
}

float lep_trigger(float pt1, float pt2, int channel)
{

  if(pt1>199.) pt1 = 199.
  if(pt2>199.) pt2 = 199.

  if(channel==3) return diele_trigger->GetBinContent(diele_trigger->FindBin(pt1,pt2));
  if(channel==1) return dimu_trigger->GetBinContent(dimu_trigger->FindBin(pt1,pt2));
  if(channel==2) return muele_trigger->GetBinContent(muele_trigger->FindBin(pt1,pt2));
}

float lep_triggerup(float pt1, float pt2, int channel)
{

  if(pt1>199.) pt1 = 199.
  if(pt2>199.) pt2 = 199.

  if(channel==3) return (diele_trigger->GetBinContent(diele_trigger->FindBin(pt1,pt2))+diele_trigger->GetBinError(diele_trigger->FindBin(pt1,pt2)));
  if(channel==1) return (dimu_trigger->GetBinContent(dimu_trigger->FindBin(pt1,pt2))+dimu_trigger->GetBinError(dimu_trigger->FindBin(pt1,pt2)));
  if(channel==2) return (muele_trigger->GetBinContent(muele_trigger->FindBin(pt1,pt2))+muele_trigger->GetBinError(muele_trigger->FindBin(pt1,pt2)));
}

float lep_triggerdown(float pt1, float pt2, int channel)
{
  if(pt1>199.) pt1 = 199.
  if(pt2>199.) pt2 = 199.

  if(channel==3) return (diele_trigger->GetBinContent(diele_trigger->FindBin(pt1,pt2))-diele_trigger->GetBinError(diele_trigger->FindBin(pt1,pt2)));
  if(channel==1) return (dimu_trigger->GetBinContent(dimu_trigger->FindBin(pt1,pt2))-dimu_trigger->GetBinError(dimu_trigger->FindBin(pt1,pt2)));
  if(channel==2) return (muele_trigger->GetBinContent(muele_trigger->FindBin(pt1,pt2))-muele_trigger->GetBinError(muele_trigger->FindBin(pt1,pt2)));
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

float mll(float l1_pt, float l1_eta, float l1_phi, float l1_mass, float l2_pt, float l2_eta, float l2_phi, float l2_mass){
  float inv_mass = 0.;
  ROOT::Math::PtEtaPhiMVector l1(l1_pt, l1_eta, l1_phi, l1_mass);
  ROOT::Math::PtEtaPhiMVector l2(l2_pt, l2_eta, l2_phi, l2_mass);
  inv_mass = (l1+l2).M();
  return inv_mass;
}

float muPtcorr(float lep_pt, int lep_id, int lep_pdgid, ROOT::VecOps::RVec<float> mu_corrPt_variated){
  float pt = lep_pt;
  if(abs(lep_pdgid)==13) pt = mu_corrPt_variated[lep_id];
  return pt;
}
