//==============
// Last used:
//root -l -b plot_TMVA_customROC.C\(\"200\"\)
//==============

#include "TH1F.h"
#include <cmath>
#include <string>

void plot_TMVA_customROC(TString mass){
  bool compute_optBDT = true;
  TCanvas *c1 = new TCanvas("c1","ROC "+mass,150,10,990,660);
  c1->SetGridx(1);
  c1->SetGridy(1);
  TLegend*leg = new TLegend(0.1,0.4,0.40,0.48);

  if(compute_optBDT) {
    //use BDT score distributions to set optimal categorisation
    TString file_name = "TMVA_ttc_a_rtc04_MA"+mass+"_central.root";
    TFile *f_tmva = new TFile(file_name,"READ");
    //TH1F *h_test_signal;
    //TH1F *h_test_bkg;
    //h_test_signal = (TH1F*)f->Get("BDTdecision_signal"+category);
    //h_test_bkg = (TH1F*)f->Get("BDTdecision_data_obs"+category);

    //BDTcut BDTcutvalues = Get_BDT_cut(category, h_test_signal, h_test_bkg, false);
    //cout<<"BDT cut set based on S and B distribution in "<<file_name<<endl;
    
    TTree *tTrain = (TTree*)f_tmva->Get("dataset_ttc_a_rtc04_MA"+mass+"_central/TrainTree");
    TTreeReader reader (tTrain);

    TTreeReaderValue<float> reader_bdt (reader, "BDTG");
    TTreeReaderValue<int> reader_classid (reader, "classID");

    int nentries = tTrain->GetEntries();
    int signal_class = 0;
    double n_a_true_positive = 0;
    double n_a_false_positive = 0;
    double n_a_true_negative_rej = 0;
    double n_a_false_negative_rej = 0;
    double bdt_cut = -0.6; // BDT cut value (change it here)

    TH1F *ROC;
    ROC = (TH1F*)f_tmva->Get("dataset_ttc_a_rtc04_MA"+mass+"_central/Method_BDTG/BDTG/MVA_BDTG_rejBvsS");
    ROC->SetLineColor(2);
    ROC->SetLineWidth(2);
    
    gStyle->SetOptStat(0);
    leg->AddEntry(ROC, "m_{A}="+mass+" GeV, #rho_{tc}=0.4","l");
    ROC->Draw("hist");

    // when "classID==0 that means <signal>" check for example TestTree->Draw("className","classID==1")
    
    while (reader.Next()) {
      if ((*reader_bdt) >= bdt_cut and (*reader_classid) == 0) {
	n_a_true_positive += 1.;
      } else if((*reader_bdt) >= bdt_cut and (*reader_classid) == 1){
	n_a_false_positive += 1.;
      }

      if ((*reader_bdt) < bdt_cut and (*reader_classid) == 1) {
	n_a_true_negative_rej += 1.;
      } else if ((*reader_bdt) < bdt_cut and (*reader_classid) == 0) {
	n_a_false_negative_rej += 1.;
      }
    }
    cout<<"-------\nBDT working point a "<<bdt_cut<<endl;
    cout<<"n_a_true_positive "<<n_a_true_positive<<" n_a_false_positive "<<n_a_false_positive<<endl;
    cout<<"n_a_true_negative_rej "<<n_a_true_negative_rej<<" n_a_false_negative_rej "<<n_a_false_negative_rej<<endl;
    cout<<"signal efficiency = TP/P "<<n_a_true_positive/(n_a_true_positive+n_a_false_negative_rej)<<endl;
    cout<<"bkg rejection = TN_rej/N "<<n_a_true_negative_rej/(n_a_false_positive+n_a_true_negative_rej)<<endl;
    Double_t x[1], y[1];
    x[0] = n_a_true_positive/(n_a_true_positive+n_a_false_negative_rej);
    y[0] = n_a_true_negative_rej/(n_a_false_positive+n_a_true_negative_rej);
    TGraph* gr = new TGraph(1,x,y);
    TLatex *l = new TLatex(0.5, 0.5, "label");
    l->SetTextSize(0.025);
    l->SetTextFont(42);
    l->SetTextAlign(21);
    l->SetTextColor(kBlue);
    l->DrawLatex(x[0],y[0]+0.01,Form("bdt_cut > %4.2f",bdt_cut));
    gr->Draw("same *p");
  }
  
  leg->Draw();
  gPad->Modified();
  c1->Update();
  c1->SaveAs("customROC_M"+mass+".png");
  c1->SaveAs("customROC_M"+mass+".pdf");
  
}
