/// \file
/// \ingroup tutorial_tmva
/// \notebook -nodraw
/// This macro provides a simple example on how to use the trained classifiers
/// within an analysis module
/// - Project   : TMVA - a Root-integrated toolkit for multivariate data analysis
/// - Package   : TMVA
/// - Executable: TMVAClassificationApplication
///
/// \macro_output
/// \macro_code
/// \author Andreas Hoecker

#include <cstdlib>
#include <vector>
#include <iostream>
#include <map>
#include <string>

#include "TFile.h"
#include "TTree.h"
#include "TString.h"
#include "TSystem.h"
#include "TROOT.h"
#include "TStopwatch.h"

#include "TMVA/Tools.h"
#include "TMVA/Reader.h"
#include "TMVA/MethodCuts.h"

using namespace TMVA;
using namespace std;

// Signal cross-section is taken from https://gist.github.com/efeyazgan/b5926ba4e2f60ef198592872e79c622c

float Get_signalXS(std::string signal_name=""){
  if (signal_name.find("s0")!= string::npos || signal_name.find("MS0")!= string::npos){
    if (signal_name.find("200")!= string::npos){
      if (signal_name.find("rtc01")!= string::npos) return 2.338e-04;
      if (signal_name.find("rtc04")!= string::npos) return 4.040e-03;
      if (signal_name.find("rtc08")!= string::npos) return 2.043e-02;
      if (signal_name.find("rtc10")!= string::npos) return 3.413e-02;
      if (signal_name.find("rtu01")!= string::npos) return 2.250e-03;
      if (signal_name.find("rtu04")!= string::npos) return 4.334e-02;
      if (signal_name.find("rtu08")!= string::npos) return 2.659e-01;
      if (signal_name.find("rtu10")!= string::npos) return 3.904e-01;
    }
    if (signal_name.find("300")!= string::npos){
      if (signal_name.find("rtc01")!= string::npos) return 2.848e-04;
      if (signal_name.find("rtc04")!= string::npos) return 4.421e-03;
      if (signal_name.find("rtc08")!= string::npos) return 2.022e-02;
      if (signal_name.find("rtc10")!= string::npos) return 4.135e-02;
      if (signal_name.find("rtu01")!= string::npos) return 3.337e-03;
      if (signal_name.find("rtu04")!= string::npos) return 4.025e-02;
      if (signal_name.find("rtu08")!= string::npos) return 2.308e-01;
      if (signal_name.find("rtu10")!= string::npos) return 4.656e-01;
    }
    if (signal_name.find("350")!= string::npos){
      if (signal_name.find("rtc01")!= string::npos) return 2.695e-04;
      if (signal_name.find("rtc04")!= string::npos) return 3.468e-03;
      if (signal_name.find("rtc08")!= string::npos) return 1.379e-02;
      if (signal_name.find("rtc10")!= string::npos) return 2.354e-02;
      if (signal_name.find("rtu01")!= string::npos) return 1.970e-03;
      if (signal_name.find("rtu04")!= string::npos) return 3.287e-02;
      if (signal_name.find("rtu08")!= string::npos) return 1.890e-01;
      if (signal_name.find("rtu10")!= string::npos) return 2.823e-01;
    }
    if (signal_name.find("400")!= string::npos){
      if (signal_name.find("rtc01")!= string::npos) return 1.602e-04;
      if (signal_name.find("rtc04")!= string::npos) return 2.288e-03;
      if (signal_name.find("rtc08")!= string::npos) return 9.202e-03;
      if (signal_name.find("rtc10")!= string::npos) return 1.299e-02;
      if (signal_name.find("rtu01")!= string::npos) return 1.315e-03;
      if (signal_name.find("rtu04")!= string::npos) return 2.609e-02;
      if (signal_name.find("rtu08")!= string::npos) return 1.018e-01;
      if (signal_name.find("rtu10")!= string::npos) return 2.706e-01;
    }
    if (signal_name.find("500")!= string::npos){
      if (signal_name.find("rtc01")!= string::npos) return 6.756e-05;
      if (signal_name.find("rtc04")!= string::npos) return 1.297e-03;
      if (signal_name.find("rtc08")!= string::npos) return 4.955e-03;
      if (signal_name.find("rtc10")!= string::npos) return 1.059e-02;
      if (signal_name.find("rtu01")!= string::npos) return 9.176e-04;
      if (signal_name.find("rtu04")!= string::npos) return 1.740e-02;
      if (signal_name.find("rtu08")!= string::npos) return 6.560e-02;
      if (signal_name.find("rtu10")!= string::npos) return 1.227e-01;
    }
    if (signal_name.find("600")!= string::npos){
      if (signal_name.find("rtc01")!= string::npos) return 3.676e-05;
      if (signal_name.find("rtc04")!= string::npos) return 7.525e-04;
      if (signal_name.find("rtc08")!= string::npos) return 3.227e-03;
      if (signal_name.find("rtc10")!= string::npos) return 5.353e-03;
      if (signal_name.find("rtu01")!= string::npos) return 4.966e-04;
      if (signal_name.find("rtu04")!= string::npos) return 8.251e-03;
      if (signal_name.find("rtu08")!= string::npos) return 5.711e-02;
      if (signal_name.find("rtu10")!= string::npos) return 8.863e-02;
    }
    if (signal_name.find("700")!= string::npos){
      if (signal_name.find("rtc01")!= string::npos) return 2.703e-05;
      if (signal_name.find("rtc04")!= string::npos) return 4.038e-04;
      if (signal_name.find("rtc08")!= string::npos) return 1.783e-03;
      if (signal_name.find("rtc10")!= string::npos) return 2.823e-03;
      if (signal_name.find("rtu01")!= string::npos) return 2.770e-04;
      if (signal_name.find("rtu04")!= string::npos) return 5.630e-03;
      if (signal_name.find("rtu08")!= string::npos) return 3.088e-02;
      if (signal_name.find("rtu10")!= string::npos) return 5.702e-02;
    }
    if (signal_name.find("800")!= string::npos){
      if (signal_name.find("rtc01")!= string::npos) return 8.899e-07;
      if (signal_name.find("rtc04")!= string::npos) return 2.360e-04;
      if (signal_name.find("rtc08")!= string::npos) return 3.731e-03;
      if (signal_name.find("rtc10")!= string::npos) return 1.000e-02;
      if (signal_name.find("rtu01")!= string::npos) return 2.497e-04;
      if (signal_name.find("rtu04")!= string::npos) return 5.328e-02;
      if (signal_name.find("rtu08")!= string::npos) return 8.240e-01;
      if (signal_name.find("rtu10")!= string::npos) return 1.995e+00;
    }
    if (signal_name.find("900")!= string::npos){
      if (signal_name.find("rtc01")!= string::npos) return 5.376e-07;
      if (signal_name.find("rtc04")!= string::npos) return 1.416e-04;
      if (signal_name.find("rtc08")!= string::npos) return 2.457e-03;
      if (signal_name.find("rtc10")!= string::npos) return 6.227e-03;
      if (signal_name.find("rtu01")!= string::npos) return 1.694e-04;
      if (signal_name.find("rtu04")!= string::npos) return 3.188e-02;
      if (signal_name.find("rtu08")!= string::npos) return 4.489e-01;
      if (signal_name.find("rtu10")!= string::npos) return 1.510e+00;
    }
    if (signal_name.find("1000")!= string::npos){
      if (signal_name.find("rtc01")!= string::npos) return 3.682e-07;
      if (signal_name.find("rtc04")!= string::npos) return 1.182e-04 ;
      if (signal_name.find("rtc08")!= string::npos) return 1.538e-03;
      if (signal_name.find("rtc10")!= string::npos) return 3.420e-03;
      if (signal_name.find("rtu01")!= string::npos) return 1.173e-04;
      if (signal_name.find("rtu04")!= string::npos) return 3.220e-02;
      if (signal_name.find("rtu08")!= string::npos) return 3.270e-01;
      if (signal_name.find("rtu10")!= string::npos) return 9.636e-01;
    }
  }
  else{
    if (signal_name.find("200")!= string::npos){
      if (signal_name.find("rtc01")!= string::npos) return 2.712e-04;
      if (signal_name.find("rtc04")!= string::npos) return 4.790e-03;
      if (signal_name.find("rtc08")!= string::npos) return 1.896e-02;
      if (signal_name.find("rtc10")!= string::npos) return 3.186e-02;
      if (signal_name.find("rtu01")!= string::npos) return 2.043e-03;
      if (signal_name.find("rtu04")!= string::npos) return 3.625e-02;
      if (signal_name.find("rtu08")!= string::npos) return 1.904e-01;
      if (signal_name.find("rtu10")!= string::npos) return 3.698e-01;
    }
    if (signal_name.find("300")!= string::npos){
      if (signal_name.find("rtc01")!= string::npos) return 2.633e-04;
      if (signal_name.find("rtc04")!= string::npos) return 4.866e-03;
      if (signal_name.find("rtc08")!= string::npos) return 2.319e-02;
      if (signal_name.find("rtc10")!= string::npos) return 3.105e-02;
      if (signal_name.find("rtu01")!= string::npos) return 2.795e-03;
      if (signal_name.find("rtu04")!= string::npos) return 3.991e-02;
      if (signal_name.find("rtu08")!= string::npos) return 2.283e-01;
      if (signal_name.find("rtu10")!= string::npos) return 3.484e-01;
    }
    if (signal_name.find("350")!= string::npos){
      if (signal_name.find("rtc01")!= string::npos) return 2.101e-04;
      if (signal_name.find("rtc04")!= string::npos) return 3.674e-03;
      if (signal_name.find("rtc08")!= string::npos) return 1.341e-02;
      if (signal_name.find("rtc10")!= string::npos) return 2.447e-02;
      if (signal_name.find("rtu01")!= string::npos) return 2.742e-03;
      if (signal_name.find("rtu04")!= string::npos) return 3.649e-02;
      if (signal_name.find("rtu08")!= string::npos) return 1.845e-01;
      if (signal_name.find("rtu10")!= string::npos) return 2.592e-01;
    }
    if (signal_name.find("400")!= string::npos){
      if (signal_name.find("rtc01")!= string::npos) return 1.568e-04;
      if (signal_name.find("rtc04")!= string::npos) return 2.441e-03;
      if (signal_name.find("rtc08")!= string::npos) return 9.325e-03;
      if (signal_name.find("rtc10")!= string::npos) return 1.591e-02;
      if (signal_name.find("rtu01")!= string::npos) return 1.663e-03;
      if (signal_name.find("rtu04")!= string::npos) return 2.743e-02;
      if (signal_name.find("rtu08")!= string::npos) return 1.687e-01;
      if (signal_name.find("rtu10")!= string::npos) return 2.907e-01;
    }
    if (signal_name.find("500")!= string::npos){
      if (signal_name.find("rtc01")!= string::npos) return 7.746e-05;
      if (signal_name.find("rtc04")!= string::npos) return 1.453e-03;
      if (signal_name.find("rtc08")!= string::npos) return 6.101e-03;
      if (signal_name.find("rtc10")!= string::npos) return 7.720e-03;
      if (signal_name.find("rtu01")!= string::npos) return 9.412e-04;
      if (signal_name.find("rtu04")!= string::npos) return 1.201e-02;
      if (signal_name.find("rtu08")!= string::npos) return 6.306e-02;
      if (signal_name.find("rtu10")!= string::npos) return 1.199e-01;
    }
    if (signal_name.find("600")!= string::npos){
      if (signal_name.find("rtc01")!= string::npos) return 4.475e-05;
      if (signal_name.find("rtc04")!= string::npos) return 6.698e-04;
      if (signal_name.find("rtc08")!= string::npos) return 2.750e-03;
      if (signal_name.find("rtc10")!= string::npos) return 4.480e-03;
      if (signal_name.find("rtu01")!= string::npos) return 6.026e-04;
      if (signal_name.find("rtu04")!= string::npos) return 7.906e-03;
      if (signal_name.find("rtu08")!= string::npos) return 4.101e-02;
      if (signal_name.find("rtu10")!= string::npos) return 7.277e-02;
    }
    if (signal_name.find("700")!= string::npos){
      if (signal_name.find("rtc01")!= string::npos) return 2.230e-05;
      if (signal_name.find("rtc04")!= string::npos) return 4.640e-04;
      if (signal_name.find("rtc08")!= string::npos) return 1.610e-03;
      if (signal_name.find("rtc10")!= string::npos) return 3.237e-03;
      if (signal_name.find("rtu01")!= string::npos) return 4.158e-04;
      if (signal_name.find("rtu04")!= string::npos) return 6.228e-03;
      if (signal_name.find("rtu08")!= string::npos) return 3.282e-02;
      if (signal_name.find("rtu10")!= string::npos) return 6.658e-02;
    }
    if (signal_name.find("800")!= string::npos){
      if (signal_name.find("rtc01")!= string::npos) return 9.492e-07;
      if (signal_name.find("rtc04")!= string::npos) return 2.268e-04;
      if (signal_name.find("rtc08")!= string::npos) return 4.213e-03;
      if (signal_name.find("rtc10")!= string::npos) return 9.412e-03;
      if (signal_name.find("rtu01")!= string::npos) return 1.802e-04;
      if (signal_name.find("rtu04")!= string::npos) return 4.967e-02;
      if (signal_name.find("rtu08")!= string::npos) return 1.079e+00;
      if (signal_name.find("rtu10")!= string::npos) return 2.259e+00;
    }
    if (signal_name.find("900")!= string::npos){
      if (signal_name.find("rtc01")!= string::npos) return 5.747e-07;
      if (signal_name.find("rtc04")!= string::npos) return 1.880e-04;
      if (signal_name.find("rtc08")!= string::npos) return 1.689e-03;
      if (signal_name.find("rtc10")!= string::npos) return 4.029e-03;
      if (signal_name.find("rtu01")!= string::npos) return 1.806e-04;
      if (signal_name.find("rtu04")!= string::npos) return 3.852e-02;
      if (signal_name.find("rtu08")!= string::npos) return 8.218e-01;
      if (signal_name.find("rtu10")!= string::npos) return 1.572e+00;
    }
    if (signal_name.find("1000")!= string::npos){
      if (signal_name.find("rtc01")!= string::npos) return 4.063e-07;
      if (signal_name.find("rtc04")!= string::npos) return 1.247e-04;
      if (signal_name.find("rtc08")!= string::npos) return 1.750e-03;
      if (signal_name.find("rtc10")!= string::npos) return 3.420e-03;
      if (signal_name.find("rtu01")!= string::npos) return 1.049e-04;
      if (signal_name.find("rtu04")!= string::npos) return 2.410e-02;
      if (signal_name.find("rtu08")!= string::npos) return 4.255e-01;
      if (signal_name.find("rtu10")!= string::npos) return 1.158e+00;
    }
  } 
  return 1.0;
}


TH1F* Getoutput( TString myMethodList = "", std::string input_name="",float xs=1.0, float eff_N=1.0, std::string weight_name="", std::string system_unc="", string mass_scan="", string channel="", string type_="", string cp="", int sample_type=0)
{
   cout<<"start Getoutput!!"<<endl;
   //---------------------------------------------------------------
   // This loads the library
   TMVA::Tools::Instance();

   // Default MVA methods to be trained + tested
   std::map<std::string,int> Use;

   TH1F *histnull(0);
   float lumi=LUMI;
   float norm_scale=xs/eff_N;
   cout<<"norm_scale:"<<norm_scale<<", input_name:"<<input_name<<endl;
   cout<<"xs:"<<xs<<", eff_N:"<<eff_N<<endl;

   // Cut optimisation
   Use["Cuts"]            = 0;
   Use["CutsD"]           = 0;
   Use["CutsPCA"]         = 0;
   Use["CutsGA"]          = 0;
   Use["CutsSA"]          = 0;
   //
   // 1-dimensional likelihood ("naive Bayes estimator")
   Use["Likelihood"]      = 0;
   Use["LikelihoodD"]     = 0; // the "D" extension indicates decorrelated input variables (see option strings)
   Use["LikelihoodPCA"]   = 0; // the "PCA" extension indicates PCA-transformed input variables (see option strings)
   Use["LikelihoodKDE"]   = 0;
   Use["LikelihoodMIX"]   = 0;
   //
   // Mutidimensional likelihood and Nearest-Neighbour methods
   Use["PDERS"]           = 0;
   Use["PDERSD"]          = 0;
   Use["PDERSPCA"]        = 0;
   Use["PDEFoam"]         = 0;
   Use["PDEFoamBoost"]    = 0; // uses generalised MVA method boosting
   Use["KNN"]             = 0; // k-nearest neighbour method
   //
   // Linear Discriminant Analysis
   Use["LD"]              = 0; // Linear Discriminant identical to Fisher
   Use["Fisher"]          = 0;
   Use["FisherG"]         = 0;
   Use["BoostedFisher"]   = 0; // uses generalised MVA method boosting
   Use["HMatrix"]         = 0;
   //
   // Function Discriminant analysis
   Use["FDA_GA"]          = 0; // minimisation of user-defined function using Genetics Algorithm
   Use["FDA_SA"]          = 0;
   Use["FDA_MC"]          = 0;
   Use["FDA_MT"]          = 0;
   Use["FDA_GAMT"]        = 0;
   Use["FDA_MCMT"]        = 0;
   //
   // Neural Networks (all are feed-forward Multilayer Perceptrons)
   Use["MLP"]             = 0; // Recommended ANN
   Use["MLPBFGS"]         = 0; // Recommended ANN with optional training method
   Use["MLPBNN"]          = 0; // Recommended ANN with BFGS training method and bayesian regulator
   Use["CFMlpANN"]        = 0; // Depreciated ANN from ALEPH
   Use["TMlpANN"]         = 0; // ROOT's own ANN
   Use["DNN_CPU"] = 0;         // CUDA-accelerated DNN training.
   Use["DNN_GPU"] = 0;         // Multi-core accelerated DNN.
   //
   // Support Vector Machine
   Use["SVM"]             = 0;
   //
   // Boosted Decision Trees
   Use["BDT"]             = 0; // uses Adaptive Boost
   Use["BDTG"]            = 1; // uses Gradient Boost
   Use["BDTB"]            = 0; // uses Bagging
   Use["BDTD"]            = 0; // decorrelation + Adaptive Boost
   Use["BDTF"]            = 0; // allow usage of fisher discriminant for node splitting
   //
   // Friedman's RuleFit method, ie, an optimised series of cuts ("rules")
   Use["RuleFit"]         = 0;
   // ---------------------------------------------------------------
   Use["Plugin"]          = 0;
   Use["Category"]        = 0;
   Use["SVM_Gauss"]       = 0;
   Use["SVM_Poly"]        = 0;
   Use["SVM_Lin"]         = 0;

   std::cout << std::endl;
   std::cout << "==> Start TMVAClassificationApplication" << std::endl;
   std::cout << "++> Check myMethodList:"<< myMethodList << std::endl;

   // Select methods (don't look at this code - not of interest)
   if (myMethodList != "") {
      for (std::map<std::string,int>::iterator it = Use.begin(); it != Use.end(); it++) it->second = 0;

      std::vector<TString> mlist = gTools().SplitString( myMethodList, ',' );
      for (UInt_t i=0; i<mlist.size(); i++) {
         std::string regMethod(mlist[i]);

         if (Use.find(regMethod) == Use.end()) {
            std::cout << "Method \"" << regMethod
                      << "\" not known in TMVA under this name. Choose among the following:" << std::endl;
            for (std::map<std::string,int>::iterator it = Use.begin(); it != Use.end(); it++) {
               std::cout << it->first << " ";
            }
            std::cout << std::endl;
            return histnull;
         }
         Use[regMethod] = 1;
      }
   }

   // --------------------------------------------------------------------------------------------------

   // Create the Reader object

   TMVA::Reader *reader = new TMVA::Reader( "!Color:!Silent" );

   // Create a set of variables and declare them to the reader
   // - the variable names MUST corresponds in name and type to those given in the weight file(s) used
   Float_t HT, ttc_l1_pt, ttc_l2_pt, ttc_met, ttc_met_phi, ttc_mll, ttc_mllj1, ttc_mllj2, ttc_mllj3;
   Float_t dr_j1j2, dr_j1j3, dr_j2j3;
   Float_t ttc_l1_eta,ttc_l2_eta;
   Float_t j1_FlavCvB, j1_FlavCvL;
   Float_t j2_FlavCvB, j2_FlavCvL;
   Float_t j3_FlavCvB, j3_FlavCvL;
   Int_t ttc_region;

   if(system_unc=="central"){
     reader->AddVariable( "HT", &HT );
     reader->AddVariable( "j1_FlavCvB", &j1_FlavCvB );
     reader->AddVariable( "j1_FlavCvL", &j1_FlavCvL );
     reader->AddVariable( "j2_FlavCvB", &j2_FlavCvB );
     reader->AddVariable( "j2_FlavCvL", &j2_FlavCvL );
     reader->AddVariable( "j3_FlavCvB", &j3_FlavCvB );
     reader->AddVariable( "j3_FlavCvL", &j3_FlavCvL );
     reader->AddVariable( "dr_j1j2", &dr_j1j2);
     reader->AddVariable( "dr_j1j3", &dr_j1j3);
     reader->AddVariable( "dr_j2j3", &dr_j2j3);
     reader->AddVariable( "ttc_l1_pt", &ttc_l1_pt );
     reader->AddVariable( "ttc_l2_pt", &ttc_l2_pt);
     reader->AddVariable( "ttc_met", &ttc_met);
     reader->AddVariable( "ttc_met_phi", &ttc_met_phi);
     reader->AddVariable( "ttc_mll", &ttc_mll);
     reader->AddVariable( "ttc_mllj1", &ttc_mllj1);
     reader->AddVariable( "ttc_mllj2", &ttc_mllj2);
     reader->AddVariable( "ttc_mllj3", &ttc_mllj3);
   }
   if(system_unc=="jesup"){
     reader->AddVariable( "HT_jesup", &HT );
     reader->AddVariable( "j1_FlavCvB", &j1_FlavCvB );
     reader->AddVariable( "j1_FlavCvL", &j1_FlavCvL );
     reader->AddVariable( "j2_FlavCvB", &j2_FlavCvB );
     reader->AddVariable( "j2_FlavCvL", &j2_FlavCvL );
     reader->AddVariable( "j3_FlavCvB", &j3_FlavCvB );
     reader->AddVariable( "j3_FlavCvL", &j3_FlavCvL );
     reader->AddVariable( "dr_j1j2", &dr_j1j2);
     reader->AddVariable( "dr_j1j3", &dr_j1j3);
     reader->AddVariable( "dr_j2j3", &dr_j2j3);
     reader->AddVariable( "ttc_l1_pt", &ttc_l1_pt );
     reader->AddVariable( "ttc_l2_pt", &ttc_l2_pt);
     reader->AddVariable( "ttc_met_jesup", &ttc_met);
     reader->AddVariable( "ttc_met_phi_jesup", &ttc_met_phi);
     reader->AddVariable( "ttc_mll", &ttc_mll);
     reader->AddVariable( "ttc_mllj1_jesup", &ttc_mllj1);
     reader->AddVariable( "ttc_mllj2_jesup", &ttc_mllj2);
     reader->AddVariable( "ttc_mllj3_jesup", &ttc_mllj3);
   }
   if(system_unc=="jesdo"){
     reader->AddVariable( "HT_jesdo", &HT );
     reader->AddVariable( "j1_FlavCvB", &j1_FlavCvB );
     reader->AddVariable( "j1_FlavCvL", &j1_FlavCvL );
     reader->AddVariable( "j2_FlavCvB", &j2_FlavCvB );
     reader->AddVariable( "j2_FlavCvL", &j2_FlavCvL );
     reader->AddVariable( "j3_FlavCvB", &j3_FlavCvB );
     reader->AddVariable( "j3_FlavCvL", &j3_FlavCvL );
     reader->AddVariable( "dr_j1j2", &dr_j1j2);
     reader->AddVariable( "dr_j1j3", &dr_j1j3);
     reader->AddVariable( "dr_j2j3", &dr_j2j3);
     reader->AddVariable( "ttc_l1_pt", &ttc_l1_pt );
     reader->AddVariable( "ttc_l2_pt", &ttc_l2_pt);
     reader->AddVariable( "ttc_met_jesdo", &ttc_met);
     reader->AddVariable( "ttc_met_phi_jesdo", &ttc_met_phi);
     reader->AddVariable( "ttc_mll", &ttc_mll);
     reader->AddVariable( "ttc_mllj1_jesdo", &ttc_mllj1);
     reader->AddVariable( "ttc_mllj2_jesdo", &ttc_mllj2);
     reader->AddVariable( "ttc_mllj3_jesdo", &ttc_mllj3);
   }
   if(system_unc=="jerup"){
     reader->AddVariable( "HT_jerup", &HT );
     reader->AddVariable( "j1_FlavCvB", &j1_FlavCvB );
     reader->AddVariable( "j1_FlavCvL", &j1_FlavCvL );
     reader->AddVariable( "j2_FlavCvB", &j2_FlavCvB );
     reader->AddVariable( "j2_FlavCvL", &j2_FlavCvL );
     reader->AddVariable( "j3_FlavCvB", &j3_FlavCvB );
     reader->AddVariable( "j3_FlavCvL", &j3_FlavCvL );
     reader->AddVariable( "dr_j1j2", &dr_j1j2);
     reader->AddVariable( "dr_j1j3", &dr_j1j3);
     reader->AddVariable( "dr_j2j3", &dr_j2j3);
     reader->AddVariable( "ttc_l1_pt", &ttc_l1_pt );
     reader->AddVariable( "ttc_l2_pt", &ttc_l2_pt);
     reader->AddVariable( "ttc_met_jerup", &ttc_met);
     reader->AddVariable( "ttc_met_phi_jerup", &ttc_met_phi);
     reader->AddVariable( "ttc_mll", &ttc_mll);
     reader->AddVariable( "ttc_mllj1_jerup", &ttc_mllj1);
     reader->AddVariable( "ttc_mllj2_jerup", &ttc_mllj2);
     reader->AddVariable( "ttc_mllj3_jerup", &ttc_mllj3);
   }
   if(system_unc=="jerdo"){
     reader->AddVariable( "HT_jerdo", &HT );
     reader->AddVariable( "j1_FlavCvB", &j1_FlavCvB );
     reader->AddVariable( "j1_FlavCvL", &j1_FlavCvL );
     reader->AddVariable( "j2_FlavCvB", &j2_FlavCvB );
     reader->AddVariable( "j2_FlavCvL", &j2_FlavCvL );
     reader->AddVariable( "j3_FlavCvB", &j3_FlavCvB );
     reader->AddVariable( "j3_FlavCvL", &j3_FlavCvL );
     reader->AddVariable( "dr_j1j2", &dr_j1j2);
     reader->AddVariable( "dr_j1j3", &dr_j1j3);
     reader->AddVariable( "dr_j2j3", &dr_j2j3);
     reader->AddVariable( "ttc_l1_pt", &ttc_l1_pt );
     reader->AddVariable( "ttc_l2_pt", &ttc_l2_pt);
     reader->AddVariable( "ttc_met_jerdo", &ttc_met);
     reader->AddVariable( "ttc_met_phi_jerdo", &ttc_met_phi);
     reader->AddVariable( "ttc_mll", &ttc_mll);
     reader->AddVariable( "ttc_mllj1_jerdo", &ttc_mllj1);
     reader->AddVariable( "ttc_mllj2_jerdo", &ttc_mllj2);
     reader->AddVariable( "ttc_mllj3_jerdo", &ttc_mllj3);
   }
   if(system_unc=="unclusterEup"){
     reader->AddVariable( "HT", &HT );
     reader->AddVariable( "j1_FlavCvB", &j1_FlavCvB );
     reader->AddVariable( "j1_FlavCvL", &j1_FlavCvL );
     reader->AddVariable( "j2_FlavCvB", &j2_FlavCvB );
     reader->AddVariable( "j2_FlavCvL", &j2_FlavCvL );
     reader->AddVariable( "j3_FlavCvB", &j3_FlavCvB );
     reader->AddVariable( "j3_FlavCvL", &j3_FlavCvL );
     reader->AddVariable( "dr_j1j2", &dr_j1j2);
     reader->AddVariable( "dr_j1j3", &dr_j1j3);
     reader->AddVariable( "dr_j2j3", &dr_j2j3);
     reader->AddVariable( "ttc_l1_pt", &ttc_l1_pt );
     reader->AddVariable( "ttc_l2_pt", &ttc_l2_pt);
     reader->AddVariable( "ttc_met_unclusterEup", &ttc_met);
     reader->AddVariable( "ttc_met_phi_unclusterEup", &ttc_met_phi);
     reader->AddVariable( "ttc_mll", &ttc_mll);
     reader->AddVariable( "ttc_mllj1", &ttc_mllj1);
     reader->AddVariable( "ttc_mllj2", &ttc_mllj2);
     reader->AddVariable( "ttc_mllj3", &ttc_mllj3);
   }
   if(system_unc=="unclusterEdo"){
     reader->AddVariable( "HT", &HT );
     reader->AddVariable( "j1_FlavCvB", &j1_FlavCvB );
     reader->AddVariable( "j1_FlavCvL", &j1_FlavCvL );
     reader->AddVariable( "j2_FlavCvB", &j2_FlavCvB );
     reader->AddVariable( "j2_FlavCvL", &j2_FlavCvL );
     reader->AddVariable( "j3_FlavCvB", &j3_FlavCvB );
     reader->AddVariable( "j3_FlavCvL", &j3_FlavCvL );
     reader->AddVariable( "dr_j1j2", &dr_j1j2);
     reader->AddVariable( "dr_j1j3", &dr_j1j3);
     reader->AddVariable( "dr_j2j3", &dr_j2j3);
     reader->AddVariable( "ttc_l1_pt", &ttc_l1_pt );
     reader->AddVariable( "ttc_l2_pt", &ttc_l2_pt);
     reader->AddVariable( "ttc_met_unclusterEdo", &ttc_met);
     reader->AddVariable( "ttc_met_phi_unclusterEdo", &ttc_met_phi);
     reader->AddVariable( "ttc_mll", &ttc_mll);
     reader->AddVariable( "ttc_mllj1", &ttc_mllj1);
     reader->AddVariable( "ttc_mllj2", &ttc_mllj2);
     reader->AddVariable( "ttc_mllj3", &ttc_mllj3);
   }
   // Book the MVA methods

   TString dir    = "";
   if(system_unc=="central"){
     dir    = "./BDT_weights_0/";
   }
   if(system_unc=="jesup"){
     dir    = "./BDT_weights_1/";
   }
   if(system_unc=="jesdo"){
     dir    = "./BDT_weights_2/";
   }
   if(system_unc=="jerup"){
     dir    = "./BDT_weights_3/";
   }
   if(system_unc=="jerdo"){
     dir    = "./BDT_weights_4/";
   }
   if(system_unc=="unclusterEup"){
     dir    = "./BDT_weights_5/";
   }
   if(system_unc=="unclusterEdo"){
     dir    = "./BDT_weights_6/";
   }

   TString prefix = "TMVAClassification";

   // Book method(s)
   for (std::map<std::string,int>::iterator it = Use.begin(); it != Use.end(); it++) {
      if (it->second) {
         TString methodName = TString(it->first) + TString(" method");
         TString weightfile = dir + prefix + TString("_") + TString(it->first) + TString(".weights.xml");
         reader->BookMVA( methodName, weightfile );
      } 
   }

   // Book output histograms
   UInt_t nbin = 200;
   TH1F *histLk(0);
   TH1F *histLkD(0);
   TH1F *histLkPCA(0);
   TH1F *histLkKDE(0);
   TH1F *histLkMIX(0);
   TH1F *histPD(0);
   TH1F *histPDD(0);
   TH1F *histPDPCA(0);
   TH1F *histPDEFoam(0);
   TH1F *histPDEFoamErr(0);
   TH1F *histPDEFoamSig(0);
   TH1F *histKNN(0);
   TH1F *histHm(0);
   TH1F *histFi(0);
   TH1F *histFiG(0);
   TH1F *histFiB(0);
   TH1F *histLD(0);
   TH1F *histNn(0);
   TH1F *histNnbfgs(0);
   TH1F *histNnbnn(0);
   TH1F *histNnC(0);
   TH1F *histNnT(0);
   TH1F *histBdt(0);
   TH1F *histBdtG(0);
   TH1F *histBdtB(0);
   TH1F *histBdtD(0);
   TH1F *histBdtF(0);
   TH1F *histRf(0);
   TH1F *histSVMG(0);
   TH1F *histSVMP(0);
   TH1F *histSVML(0);
   TH1F *histFDAMT(0);
   TH1F *histFDAGA(0);
   TH1F *histCat(0);
   TH1F *histPBdt(0);
   TH1F *histDnnGpu(0);
   TH1F *histDnnCpu(0);

   if (Use["Likelihood"])    histLk      = new TH1F( "MVA_Likelihood",    "MVA_Likelihood",    nbin, -1, 1 );
   if (Use["LikelihoodD"])   histLkD     = new TH1F( "MVA_LikelihoodD",   "MVA_LikelihoodD",   nbin, -1, 0.9999 );
   if (Use["LikelihoodPCA"]) histLkPCA   = new TH1F( "MVA_LikelihoodPCA", "MVA_LikelihoodPCA", nbin, -1, 1 );
   if (Use["LikelihoodKDE"]) histLkKDE   = new TH1F( "MVA_LikelihoodKDE", "MVA_LikelihoodKDE", nbin,  -0.00001, 0.99999 );
   if (Use["LikelihoodMIX"]) histLkMIX   = new TH1F( "MVA_LikelihoodMIX", "MVA_LikelihoodMIX", nbin,  0, 1 );
   if (Use["PDERS"])         histPD      = new TH1F( "MVA_PDERS",         "MVA_PDERS",         nbin,  0, 1 );
   if (Use["PDERSD"])        histPDD     = new TH1F( "MVA_PDERSD",        "MVA_PDERSD",        nbin,  0, 1 );
   if (Use["PDERSPCA"])      histPDPCA   = new TH1F( "MVA_PDERSPCA",      "MVA_PDERSPCA",      nbin,  0, 1 );
   if (Use["KNN"])           histKNN     = new TH1F( "MVA_KNN",           "MVA_KNN",           nbin,  0, 1 );
   if (Use["HMatrix"])       histHm      = new TH1F( "MVA_HMatrix",       "MVA_HMatrix",       nbin, -0.95, 1.55 );
   if (Use["Fisher"])        histFi      = new TH1F( "MVA_Fisher",        "MVA_Fisher",        nbin, -4, 4 );
   if (Use["FisherG"])       histFiG     = new TH1F( "MVA_FisherG",       "MVA_FisherG",       nbin, -1, 1 );
   if (Use["BoostedFisher"]) histFiB     = new TH1F( "MVA_BoostedFisher", "MVA_BoostedFisher", nbin, -2, 2 );
   if (Use["LD"])            histLD      = new TH1F( "MVA_LD",            "MVA_LD",            nbin, -2, 2 );
   if (Use["MLP"])           histNn      = new TH1F( "MVA_MLP",           "MVA_MLP",           nbin, -1.25, 1.5 );
   if (Use["MLPBFGS"])       histNnbfgs  = new TH1F( "MVA_MLPBFGS",       "MVA_MLPBFGS",       nbin, -1.25, 1.5 );
   if (Use["MLPBNN"])        histNnbnn   = new TH1F( "MVA_MLPBNN",        "MVA_MLPBNN",        nbin, -1.25, 1.5 );
   if (Use["CFMlpANN"])      histNnC     = new TH1F( "MVA_CFMlpANN",      "MVA_CFMlpANN",      nbin,  0, 1 );
   if (Use["TMlpANN"])       histNnT     = new TH1F( "MVA_TMlpANN",       "MVA_TMlpANN",       nbin, -1.3, 1.3 );
   if (Use["DNN_GPU"]) histDnnGpu = new TH1F("MVA_DNN_GPU", "MVA_DNN_GPU", nbin, -0.1, 1.1);
   if (Use["DNN_CPU"]) histDnnCpu = new TH1F("MVA_DNN_CPU", "MVA_DNN_CPU", nbin, -0.1, 1.1);
   if (Use["BDT"])           histBdt     = new TH1F( "MVA_BDT",           "MVA_BDT",           nbin, -0.8, 0.8 );
   if (Use["BDTG"])          histBdtG    = new TH1F( input_name.c_str(),  input_name.c_str(),          nbin, -1.0, 1.0 );
   if (Use["BDTB"])          histBdtB    = new TH1F( "MVA_BDTB",          "MVA_BDTB",          nbin, -1.0, 1.0 );
   if (Use["BDTD"])          histBdtD    = new TH1F( "MVA_BDTD",          "MVA_BDTD",          nbin, -0.8, 0.8 );
   if (Use["BDTF"])          histBdtF    = new TH1F( "MVA_BDTF",          "MVA_BDTF",          nbin, -1.0, 1.0 );
   if (Use["RuleFit"])       histRf      = new TH1F( "MVA_RuleFit",       "MVA_RuleFit",       nbin, -2.0, 2.0 );
   if (Use["SVM_Gauss"])     histSVMG    = new TH1F( "MVA_SVM_Gauss",     "MVA_SVM_Gauss",     nbin,  0.0, 1.0 );
   if (Use["SVM_Poly"])      histSVMP    = new TH1F( "MVA_SVM_Poly",      "MVA_SVM_Poly",      nbin,  0.0, 1.0 );
   if (Use["SVM_Lin"])       histSVML    = new TH1F( "MVA_SVM_Lin",       "MVA_SVM_Lin",       nbin,  0.0, 1.0 );
   if (Use["FDA_MT"])        histFDAMT   = new TH1F( "MVA_FDA_MT",        "MVA_FDA_MT",        nbin, -2.0, 3.0 );
   if (Use["FDA_GA"])        histFDAGA   = new TH1F( "MVA_FDA_GA",        "MVA_FDA_GA",        nbin, -2.0, 3.0 );
   if (Use["Category"])      histCat     = new TH1F( "MVA_Category",      "MVA_Category",      nbin, -2., 2. );
   if (Use["Plugin"])        histPBdt    = new TH1F( "MVA_PBDT",          "MVA_BDT",           nbin, -0.8, 0.8 );

   // PDEFoam also returns per-event error, fill in histogram, and also fill significance
   if (Use["PDEFoam"]) {
      histPDEFoam    = new TH1F( "MVA_PDEFoam",       "MVA_PDEFoam",              nbin,  0, 1 );
      histPDEFoamErr = new TH1F( "MVA_PDEFoamErr",    "MVA_PDEFoam error",        nbin,  0, 1 );
      histPDEFoamSig = new TH1F( "MVA_PDEFoamSig",    "MVA_PDEFoam significance", nbin,  0, 10 );
   }

   // Book example histogram for probability (the other methods are done similarly)
   TH1F *probHistFi(0), *rarityHistFi(0);
   if (Use["Fisher"]) {
      probHistFi   = new TH1F( "MVA_Fisher_Proba",  "MVA_Fisher_Proba",  nbin, 0, 1 );
      rarityHistFi = new TH1F( "MVA_Fisher_Rarity", "MVA_Fisher_Rarity", nbin, 0, 1 );
   }

   // Prepare input tree (this must be replaced by your data source)
   // in this example, there is a toy tree with signal and one with background events
   // we'll later on use only the "signal" events for the test in this example.
   //
   TFile *input_f(0);
   cout<<"input file:"<<input_name<<endl;
   std::string filename="./"+input_name+".root";
   input_f=TFile::Open(filename.c_str());
   
   // Event loop

   // Prepare the event tree
   // - Here the variable names have to corresponds to your tree
   // - You can use the same variables as above which is slightly faster,
   //   but of course you can use different ones and copy the values inside the event loop
   //
   std::cout << "--- Select signal sample" << std::endl;
   TTree* theTree = (TTree*)input_f->Get("SlimTree");

   Float_t genweight, puWeight, puWeightUp, puWeightDown, trig_SF, trig_SFup, trig_SFdo, mu_id, mu_id_sysup, mu_id_sysdo, mu_id_statup, mu_id_statdo, ele_id, ele_id_sysup, ele_id_sysdo, ele_id_statup, ele_id_statdo;
   Float_t ctag_SF, ctag_SF_statup, ctag_SF_statdo, ctag_SF_Extrapup, ctag_SF_Extrapdo, ctag_SF_LHEScaleWeightmuFup, ctag_SF_LHEScaleWeightmuFdo, ctag_SF_LHEScaleWeightmuRup, ctag_SF_LHEScaleWeightmuRdo, ctag_SF_Interpup, ctag_SF_Interpdo, ctag_SF_PSWeightISRup, ctag_SF_PSWeightISRdo, ctag_SF_PSWeightFSRup, ctag_SF_PSWeightFSRdo, ctag_SF_PUWeightup, ctag_SF_PUWeightdo, ctag_SF_XSec_BRUnc_DYJets_bup, ctag_SF_XSec_BRUnc_DYJets_bdo, ctag_SF_XSec_BRUnc_DYJets_cup, ctag_SF_XSec_BRUnc_DYJets_cdo, ctag_SF_XSec_BRUnc_WJets_cup, ctag_SF_XSec_BRUnc_WJets_cdo, ctag_SF_jerup, ctag_SF_jerdo, ctag_SF_jesTotalup, ctag_SF_jesTotaldo, charFlip_SF, charFlip_SFstatup, charFlip_SFstatdo, charFlip_SFsystup, charFlip_SFsystdo, sig_pdfup, sig_pdfdo, sig_scaleup, sig_scaledo, sig_psup, sig_psdo, prefireWeight, prefireWeightup, prefireWeightdo;
   Float_t fakeweight;

   theTree->SetBranchAddress( "ttc_region", &ttc_region );
   theTree->SetBranchAddress( "j1_FlavCvB", &j1_FlavCvB );
   theTree->SetBranchAddress( "j1_FlavCvL", &j1_FlavCvL );
   theTree->SetBranchAddress( "j2_FlavCvB", &j2_FlavCvB );
   theTree->SetBranchAddress( "j2_FlavCvL", &j2_FlavCvL );
   theTree->SetBranchAddress( "j3_FlavCvB", &j3_FlavCvB );
   theTree->SetBranchAddress( "j3_FlavCvL", &j3_FlavCvL );
   theTree->SetBranchAddress( "dr_j1j2", &dr_j1j2);
   theTree->SetBranchAddress( "dr_j1j3", &dr_j1j3);
   theTree->SetBranchAddress( "dr_j2j3", &dr_j2j3);
   theTree->SetBranchAddress( "ttc_l1_pt", &ttc_l1_pt );
   theTree->SetBranchAddress( "ttc_l2_pt", &ttc_l2_pt);
   theTree->SetBranchAddress( "ttc_l1_eta", &ttc_l1_eta );
   theTree->SetBranchAddress( "ttc_l2_eta", &ttc_l2_eta);
   theTree->SetBranchAddress( "ttc_mll", &ttc_mll);
   if((sample_type==0) || (sample_type==1)){ // MC
     theTree->SetBranchAddress( "genweight", &genweight);
     theTree->SetBranchAddress( "puWeight", &puWeight);
     theTree->SetBranchAddress( "puWeightUp", &puWeightUp);
     theTree->SetBranchAddress( "puWeightDown", &puWeightDown);
     theTree->SetBranchAddress( "trig_SF", &trig_SF);
     theTree->SetBranchAddress( "trig_SFup", &trig_SFup);
     theTree->SetBranchAddress( "trig_SFdo", &trig_SFdo);
     theTree->SetBranchAddress( "mu_id", &mu_id);
     theTree->SetBranchAddress( "mu_id_sysup", &mu_id_sysup);
     theTree->SetBranchAddress( "mu_id_sysdo", &mu_id_sysdo);
     theTree->SetBranchAddress( "mu_id_statup", &mu_id_statup);
     theTree->SetBranchAddress( "mu_id_statdo", &mu_id_statdo);
     theTree->SetBranchAddress( "ele_id", &ele_id);
     theTree->SetBranchAddress( "ele_id_sysup", &ele_id_sysup);
     theTree->SetBranchAddress( "ele_id_sysdo", &ele_id_sysdo);
     theTree->SetBranchAddress( "ele_id_statup", &ele_id_statup);
     theTree->SetBranchAddress( "ele_id_statdo", &ele_id_statdo);
     theTree->SetBranchAddress( "ctag_SF", &ctag_SF);
     theTree->SetBranchAddress( "ctag_SF_statup", &ctag_SF_statup);    theTree->SetBranchAddress( "ctag_SF_statdo", &ctag_SF_statdo);
     theTree->SetBranchAddress( "ctag_SF_Extrapup", &ctag_SF_Extrapup);
     theTree->SetBranchAddress( "ctag_SF_Extrapdo", &ctag_SF_Extrapdo);
     theTree->SetBranchAddress( "ctag_SF_LHEScaleWeightmuFup", &ctag_SF_LHEScaleWeightmuFup);
     theTree->SetBranchAddress( "ctag_SF_LHEScaleWeightmuFdo", &ctag_SF_LHEScaleWeightmuFdo);
     theTree->SetBranchAddress( "ctag_SF_LHEScaleWeightmuRup", &ctag_SF_LHEScaleWeightmuRup);
     theTree->SetBranchAddress( "ctag_SF_LHEScaleWeightmuRdo", &ctag_SF_LHEScaleWeightmuRdo);
     theTree->SetBranchAddress( "ctag_SF_Interpup", &ctag_SF_Interpup);
     theTree->SetBranchAddress( "ctag_SF_Interpdo", &ctag_SF_Interpdo);
     theTree->SetBranchAddress( "ctag_SF_PSWeightFSRup", &ctag_SF_PSWeightFSRup);
     theTree->SetBranchAddress( "ctag_SF_PSWeightFSRdo", &ctag_SF_PSWeightFSRdo);
     theTree->SetBranchAddress( "ctag_SF_PSWeightISRup", &ctag_SF_PSWeightISRup);
     theTree->SetBranchAddress( "ctag_SF_PSWeightISRdo", &ctag_SF_PSWeightISRdo);
     theTree->SetBranchAddress( "ctag_SF_PUWeightup", &ctag_SF_PUWeightup);
     theTree->SetBranchAddress( "ctag_SF_PUWeightdo", &ctag_SF_PUWeightdo);
     theTree->SetBranchAddress( "ctag_SF_XSec_BRUnc_DYJets_bup", &ctag_SF_XSec_BRUnc_DYJets_bup);
     theTree->SetBranchAddress( "ctag_SF_XSec_BRUnc_DYJets_bdo", &ctag_SF_XSec_BRUnc_DYJets_bdo);
     theTree->SetBranchAddress( "ctag_SF_XSec_BRUnc_DYJets_cup", &ctag_SF_XSec_BRUnc_DYJets_cup);
     theTree->SetBranchAddress( "ctag_SF_XSec_BRUnc_DYJets_cdo", &ctag_SF_XSec_BRUnc_DYJets_cdo);
     theTree->SetBranchAddress( "ctag_SF_XSec_BRUnc_WJets_cup", &ctag_SF_XSec_BRUnc_WJets_cup);
     theTree->SetBranchAddress( "ctag_SF_XSec_BRUnc_WJets_cdo", &ctag_SF_XSec_BRUnc_WJets_cdo);
     theTree->SetBranchAddress( "ctag_SF_jerup", &ctag_SF_jerup);
     theTree->SetBranchAddress( "ctag_SF_jerdo", &ctag_SF_jerdo);
     theTree->SetBranchAddress( "ctag_SF_jesTotalup", &ctag_SF_jesTotalup);
     theTree->SetBranchAddress( "ctag_SF_jesTotaldo", &ctag_SF_jesTotaldo);
     theTree->SetBranchAddress( "charFlip_SF", &charFlip_SF);
     theTree->SetBranchAddress( "charFlip_SFstatup", &charFlip_SFstatup);
     theTree->SetBranchAddress( "charFlip_SFstatdo", &charFlip_SFstatdo);
     theTree->SetBranchAddress( "charFlip_SFsystup", &charFlip_SFsystup);
     theTree->SetBranchAddress( "charFlip_SFsystdo", &charFlip_SFsystdo);
     theTree->SetBranchAddress( "sig_pdfup", &sig_pdfup);
     theTree->SetBranchAddress( "sig_pdfdo", &sig_pdfdo);
     theTree->SetBranchAddress( "sig_scaleup", &sig_scaleup);
     theTree->SetBranchAddress( "sig_scaledo", &sig_scaledo);
     theTree->SetBranchAddress( "sig_psup", &sig_psup);
     theTree->SetBranchAddress( "sig_psdo", &sig_psdo);
     theTree->SetBranchAddress( "PrefireWeight", &prefireWeight);
     theTree->SetBranchAddress( "PrefireWeight_Up", &prefireWeightup);
     theTree->SetBranchAddress( "PrefireWeight_Down", &prefireWeightdo);
   }
   else if(sample_type==2){ //fakelep
     theTree->SetBranchAddress( "fakeweight", &fakeweight);
   }

   else if(sample_type==3){ //fakelep_mc
     theTree->SetBranchAddress( "genweight", &genweight);
     theTree->SetBranchAddress( "puWeight", &puWeight);
     theTree->SetBranchAddress( "PrefireWeight", &prefireWeight); // Not sure if needed (Terry).
     theTree->SetBranchAddress( "trig_SF", &trig_SF);
     theTree->SetBranchAddress( "mu_id", &mu_id);
     theTree->SetBranchAddress( "ele_id", &ele_id);
     theTree->SetBranchAddress( "ctag_SF", &ctag_SF);
     theTree->SetBranchAddress( "fakeweight", &fakeweight);
   }

   if(system_unc=="central"){
     theTree->SetBranchAddress( "HT", &HT );
     theTree->SetBranchAddress( "ttc_met", &ttc_met);
     theTree->SetBranchAddress( "ttc_met_phi", &ttc_met_phi);
     theTree->SetBranchAddress( "ttc_mllj1", &ttc_mllj1);
     theTree->SetBranchAddress( "ttc_mllj2", &ttc_mllj2);
     theTree->SetBranchAddress( "ttc_mllj3", &ttc_mllj3);
   }
   if(system_unc=="jesup"){
     theTree->SetBranchAddress( "HT_jesup", &HT );
     theTree->SetBranchAddress( "ttc_met_jesup", &ttc_met);
     theTree->SetBranchAddress( "ttc_met_phi_jesup", &ttc_met_phi);
     theTree->SetBranchAddress( "ttc_mllj1_jesup", &ttc_mllj1);
     theTree->SetBranchAddress( "ttc_mllj2_jesup", &ttc_mllj2);
     theTree->SetBranchAddress( "ttc_mllj3_jesup", &ttc_mllj3);
   }
   if(system_unc=="jesdo"){
     theTree->SetBranchAddress( "HT_jesdo", &HT );
     theTree->SetBranchAddress( "ttc_met_jesdo", &ttc_met);
     theTree->SetBranchAddress( "ttc_met_phi_jesdo", &ttc_met_phi);
     theTree->SetBranchAddress( "ttc_mllj1_jesdo", &ttc_mllj1);
     theTree->SetBranchAddress( "ttc_mllj2_jesdo", &ttc_mllj2);
     theTree->SetBranchAddress( "ttc_mllj3_jesdo", &ttc_mllj3);
   }
   if(system_unc=="jerup"){
     theTree->SetBranchAddress( "HT_jerup", &HT );
     theTree->SetBranchAddress( "ttc_met_jerup", &ttc_met);
     theTree->SetBranchAddress( "ttc_met_phi_jerup", &ttc_met_phi);
     theTree->SetBranchAddress( "ttc_mllj1_jerup", &ttc_mllj1);
     theTree->SetBranchAddress( "ttc_mllj2_jerup", &ttc_mllj2);
     theTree->SetBranchAddress( "ttc_mllj3_jerup", &ttc_mllj3);
   }
   if(system_unc=="jerdo"){
     theTree->SetBranchAddress( "HT_jerdo", &HT );
     theTree->SetBranchAddress( "ttc_met_jerdo", &ttc_met);
     theTree->SetBranchAddress( "ttc_met_phi_jerdo", &ttc_met_phi);
     theTree->SetBranchAddress( "ttc_mllj1_jerdo", &ttc_mllj1);
     theTree->SetBranchAddress( "ttc_mllj2_jerdo", &ttc_mllj2);
     theTree->SetBranchAddress( "ttc_mllj3_jerdo", &ttc_mllj3);
   }
   if(system_unc=="unclusterEup"){
     theTree->SetBranchAddress( "HT", &HT );
     theTree->SetBranchAddress( "ttc_met_unclusterEup", &ttc_met);
     theTree->SetBranchAddress( "ttc_met_phi_unclusterEup", &ttc_met_phi);
     theTree->SetBranchAddress( "ttc_mllj1", &ttc_mllj1);
     theTree->SetBranchAddress( "ttc_mllj2", &ttc_mllj2);
     theTree->SetBranchAddress( "ttc_mllj3", &ttc_mllj3);
   }
   if(system_unc=="unclusterEdo"){
     theTree->SetBranchAddress( "HT", &HT );
     theTree->SetBranchAddress( "ttc_met_unclusterEdo", &ttc_met);
     theTree->SetBranchAddress( "ttc_met_phi_unclusterEdo", &ttc_met_phi);
     theTree->SetBranchAddress( "ttc_mllj1", &ttc_mllj1);
     theTree->SetBranchAddress( "ttc_mllj2", &ttc_mllj2);
     theTree->SetBranchAddress( "ttc_mllj3", &ttc_mllj3);
   }

   // Efficiency calculator for cut method
   Int_t    nSelCutsGA = 0;
   Double_t effS       = 0.7;

   std::vector<Float_t> vecVar(4); // vector for EvaluateMVA tests

   std::cout << "--- Processing: " << theTree->GetEntries() << " events" << std::endl;
   TStopwatch sw;
   sw.Start();

   // store normalization for no ctag
   float ctag_norm=0.;

   for (Long64_t ievt=0; ievt<theTree->GetEntries();ievt++) {

      if (ievt%40000 == 0) std::cout << "--- ... Processing event: " << ievt << std::endl;

      theTree->GetEntry(ievt);
      if(channel=="mm" && ttc_region!=1) continue;
      if(channel=="em" && ttc_region!=2) continue;
      if(channel=="ee" && ttc_region!=3) continue;
      if(channel=="ee" && ttc_mll>60 && ttc_mll<120) continue;
      // Return the MVA outputs and fill into histograms

      if (input_name.find("DY")!= string::npos)cout<<"MENG:"<<genweight<<" "<<norm_scale<<" "<<mu_id<<" "<<ele_id<<" "<<trig_SF<<" "<<charFlip_SF<<" "<<lumi<<endl;

      if (Use["CutsGA"]) {
         // Cuts is a special case: give the desired signal efficiency
         Bool_t passed = reader->EvaluateMVA( "CutsGA method", effS );
         if (passed) nSelCutsGA++;
      }
      //chargeflip SF has already be taken care of in step1 to set to be 1. in em & mm channel.
     if (input_name.find("ttc_a")!= string::npos || input_name.find("ttc_s0")!= string::npos){
        charFlip_SF=1.0;
      }//Should be done in step1// Fix me, Terry


      if (Use["Likelihood"   ])   histLk     ->Fill( reader->EvaluateMVA( "Likelihood method"    ) );
      if (Use["LikelihoodD"  ])   histLkD    ->Fill( reader->EvaluateMVA( "LikelihoodD method"   ) );
      if (Use["LikelihoodPCA"])   histLkPCA  ->Fill( reader->EvaluateMVA( "LikelihoodPCA method" ) );
      if (Use["LikelihoodKDE"])   histLkKDE  ->Fill( reader->EvaluateMVA( "LikelihoodKDE method" ) );
      if (Use["LikelihoodMIX"])   histLkMIX  ->Fill( reader->EvaluateMVA( "LikelihoodMIX method" ) );
      if (Use["PDERS"        ])   histPD     ->Fill( reader->EvaluateMVA( "PDERS method"         ) );
      if (Use["PDERSD"       ])   histPDD    ->Fill( reader->EvaluateMVA( "PDERSD method"        ) );
      if (Use["PDERSPCA"     ])   histPDPCA  ->Fill( reader->EvaluateMVA( "PDERSPCA method"      ) );
      if (Use["KNN"          ])   histKNN    ->Fill( reader->EvaluateMVA( "KNN method"           ) );
      if (Use["HMatrix"      ])   histHm     ->Fill( reader->EvaluateMVA( "HMatrix method"       ) );
      if (Use["Fisher"       ])   histFi     ->Fill( reader->EvaluateMVA( "Fisher method"        ) );
      if (Use["FisherG"      ])   histFiG    ->Fill( reader->EvaluateMVA( "FisherG method"       ) );
      if (Use["BoostedFisher"])   histFiB    ->Fill( reader->EvaluateMVA( "BoostedFisher method" ) );
      if (Use["LD"           ])   histLD     ->Fill( reader->EvaluateMVA( "LD method"            ) );
      if (Use["MLP"          ])   histNn     ->Fill( reader->EvaluateMVA( "MLP method"           ) );
      if (Use["MLPBFGS"      ])   histNnbfgs ->Fill( reader->EvaluateMVA( "MLPBFGS method"       ) );
      if (Use["MLPBNN"       ])   histNnbnn  ->Fill( reader->EvaluateMVA( "MLPBNN method"        ) );
      if (Use["CFMlpANN"     ])   histNnC    ->Fill( reader->EvaluateMVA( "CFMlpANN method"      ) );
      if (Use["TMlpANN"      ])   histNnT    ->Fill( reader->EvaluateMVA( "TMlpANN method"       ) );
      if (Use["DNN_GPU"]) histDnnGpu->Fill(reader->EvaluateMVA("DNN_GPU method"));
      if (Use["DNN_CPU"]) histDnnCpu->Fill(reader->EvaluateMVA("DNN_CPU method"));
      if (Use["BDT"          ])   histBdt    ->Fill( reader->EvaluateMVA( "BDT method"           ) );
      if (Use["BDTG"         ])
       { 
         if(weight_name=="data")  histBdtG->Fill( reader->EvaluateMVA( "BDTG method"), 1.0);
	 else if(weight_name=="nominal_noctag"){
	   histBdtG->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*charFlip_SF);
	 }
         else if(weight_name=="fakelep")   histBdtG->Fill( reader->EvaluateMVA( "BDTG method"), fakeweight);
         else if(weight_name=="fakelep_mc"){
           histBdtG->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*ctag_SF*fakeweight);
        ctag_norm+=genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*fakeweight;
         }
	 else if(weight_name=="central"){
	   histBdtG->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*charFlip_SF*ctag_SF);
	   ctag_norm+=genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*charFlip_SF;
	 }
	 else if(weight_name=="pileup_up"){
	   histBdtG->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*(puWeightUp/puWeight)*mu_id*ele_id*trig_SF*charFlip_SF*ctag_SF);
	   ctag_norm+=genweight*norm_scale*lumi*(puWeightUp/puWeight)*mu_id*ele_id*trig_SF*charFlip_SF;
	 }
	 else if(weight_name=="pileup_down"){
	   histBdtG->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*(puWeightDown/puWeight)*mu_id*ele_id*trig_SF*charFlip_SF*ctag_SF);
	   ctag_norm+=genweight*norm_scale*lumi*(puWeightDown/puWeight)*mu_id*ele_id*trig_SF*charFlip_SF;
	 }
         else if(weight_name=="prefire_up"){
           histBdtG->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*(prefireWeightup/prefireWeight)*mu_id*ele_id*trig_SF*charFlip_SF*ctag_SF);
           ctag_norm+=genweight*norm_scale*lumi*(prefireWeightup/prefireWeight)*mu_id*ele_id*trig_SF*charFlip_SF;
         }
         else if(weight_name=="prefire_down"){
           histBdtG->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*(prefireWeightdo/prefireWeight)*mu_id*ele_id*trig_SF*charFlip_SF*ctag_SF);
           ctag_norm+=genweight*norm_scale*lumi*(prefireWeightdo/prefireWeight)*mu_id*ele_id*trig_SF*charFlip_SF;
         }
	 else if(weight_name=="muID_sysup"){
	   histBdtG->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*mu_id_sysup*ele_id*trig_SF*charFlip_SF*ctag_SF);
	   ctag_norm+=genweight*norm_scale*lumi*mu_id_sysup*ele_id*trig_SF*charFlip_SF;
	 }
	 else if(weight_name=="muID_sysdown"){
	   histBdtG->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*mu_id_sysdo*ele_id*trig_SF*charFlip_SF*ctag_SF);
	   ctag_norm+=genweight*norm_scale*lumi*mu_id_sysdo*ele_id*trig_SF*charFlip_SF;
	 }
	 else if(weight_name=="muID_statup"){
	   histBdtG->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*mu_id_statup*ele_id*trig_SF*charFlip_SF*ctag_SF);
	   ctag_norm+=genweight*norm_scale*lumi*mu_id_statup*ele_id*trig_SF*charFlip_SF;
	 }
	 else if(weight_name=="muID_statdown"){
	   histBdtG->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*mu_id_statdo*ele_id*trig_SF*charFlip_SF*ctag_SF);
	   ctag_norm+=genweight*norm_scale*lumi*mu_id_statdo*ele_id*trig_SF*charFlip_SF;
	 }
	 else if(weight_name=="eleID_sysup"){
	   histBdtG->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*mu_id*ele_id_sysup*trig_SF*charFlip_SF*ctag_SF);
	   ctag_norm+=genweight*norm_scale*lumi*mu_id*ele_id_sysup*trig_SF*charFlip_SF;
	 }
	 else if(weight_name=="eleID_sysdown"){
	   histBdtG->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*mu_id*ele_id_sysdo*trig_SF*charFlip_SF*ctag_SF);
	   ctag_norm+=genweight*norm_scale*lumi*mu_id*ele_id_sysdo*trig_SF*charFlip_SF;
	 }
	 else if(weight_name=="eleID_statup"){
	   histBdtG->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*mu_id*ele_id_statup*trig_SF*charFlip_SF*ctag_SF);
	   ctag_norm+=genweight*norm_scale*lumi*mu_id*ele_id_statup*trig_SF*charFlip_SF;
	 }
	 else if(weight_name=="eleID_statdown"){
	   histBdtG->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*mu_id*ele_id_statdo*trig_SF*charFlip_SF*ctag_SF);
	   ctag_norm+=genweight*norm_scale*lumi*mu_id*ele_id_statdo*trig_SF*charFlip_SF;
	 }
	 else if(weight_name=="prefire_up"){
	   histBdtG->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*charFlip_SF*ctag_SF);
	   ctag_norm+=genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*charFlip_SF;
	 }
	 else if(weight_name=="prefire_down"){
	   histBdtG->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*charFlip_SF*ctag_SF);
	   ctag_norm+=genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*charFlip_SF;
	 }
	 else if(weight_name=="trigger_up"){
	   histBdtG->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*mu_id*ele_id*trig_SFup*charFlip_SF*ctag_SF);
	   ctag_norm+=genweight*norm_scale*lumi*mu_id*ele_id*trig_SFup*charFlip_SF;
	 }
	 else if(weight_name=="trigger_down"){
	   histBdtG->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*mu_id*ele_id*trig_SFdo*charFlip_SF*ctag_SF);
	   ctag_norm+=genweight*norm_scale*lumi*mu_id*ele_id*trig_SFdo*charFlip_SF;
	 }
	 else if(weight_name=="lumi_up"){
	   histBdtG->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*1.025*charFlip_SF*ctag_SF);
	   ctag_norm+=genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*1.025*charFlip_SF;
	 }
	 else if(weight_name=="lumi_down"){
	   histBdtG->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*0.975*charFlip_SF*ctag_SF);
	   ctag_norm+=genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*0.975*charFlip_SF;
	 }
	 else if(weight_name=="charFlip_SFstatup"){
	   histBdtG->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*charFlip_SFstatup*ctag_SF);
	   ctag_norm+=genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*charFlip_SFstatup;
	 }
	 else if(weight_name=="charFlip_SFstatdo"){
	   histBdtG->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*charFlip_SFstatdo*ctag_SF);
	   ctag_norm+=genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*charFlip_SFstatdo;
	 }
         else if(weight_name=="charFlip_SFsystup"){
           histBdtG->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*charFlip_SFsystup*ctag_SF);
           ctag_norm+=genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*charFlip_SFsystup;
         }
         else if(weight_name=="charFlip_SFsystdo"){
           histBdtG->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*charFlip_SFsystdo*ctag_SF);
           ctag_norm+=genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*charFlip_SFsystdo;
         }
	 else if(weight_name=="sig_pdfup"){
	   histBdtG->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*charFlip_SF*sig_pdfup*ctag_SF);
	   ctag_norm+=genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*charFlip_SF*sig_pdfup;
	 }
	 else if(weight_name=="sig_pdfdo"){
	   histBdtG->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*charFlip_SF*sig_pdfdo*ctag_SF);
	   ctag_norm+=genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*charFlip_SF*sig_pdfdo;
	 }
	 else if(weight_name=="sig_scaleup"){
	   histBdtG->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*charFlip_SF*sig_scaleup*ctag_SF);
	   ctag_norm+=genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*charFlip_SF*sig_scaleup;
	 }
	 else if(weight_name=="sig_scaledo"){
	   histBdtG->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*charFlip_SF*sig_scaledo*ctag_SF);
	   ctag_norm+=genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*charFlip_SF*sig_scaledo;
	 }
	 else if(weight_name=="sig_psup"){
	   histBdtG->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*charFlip_SF*sig_psup*ctag_SF);
	   ctag_norm+=genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*charFlip_SF*sig_psup;
	 }
	 else if(weight_name=="sig_psdo"){
	   histBdtG->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*charFlip_SF*sig_psdo*ctag_SF);
	   ctag_norm+=genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*charFlip_SF*sig_psdo;
         }
	 // ctag uncertainty
	 else if(weight_name=="ctag_statup")histBdtG   ->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*charFlip_SF*ctag_SF_statup);
	 else if(weight_name=="ctag_statdo")histBdtG   ->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*charFlip_SF*ctag_SF_statdo);
	 else if(weight_name=="ctag_Extrapup")histBdtG   ->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*charFlip_SF*ctag_SF_Extrapup);
	 else if(weight_name=="ctag_Extrapdo")histBdtG   ->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*charFlip_SF*ctag_SF_Extrapdo);
	 else if(weight_name=="ctag_LHEScaleWeightmuFup")histBdtG   ->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*charFlip_SF*ctag_SF_LHEScaleWeightmuFup);
	 else if(weight_name=="ctag_LHEScaleWeightmuFdo")histBdtG   ->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*charFlip_SF*ctag_SF_LHEScaleWeightmuFdo);
	 else if(weight_name=="ctag_LHEScaleWeightmuRup")histBdtG   ->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*charFlip_SF*ctag_SF_LHEScaleWeightmuRup);
	 else if(weight_name=="ctag_LHEScaleWeightmuRdo")histBdtG   ->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*charFlip_SF*ctag_SF_LHEScaleWeightmuRdo);
	 else if(weight_name=="ctag_Interpup")histBdtG   ->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*charFlip_SF*ctag_SF_Interpup);
	 else if(weight_name=="ctag_Interpdo")histBdtG   ->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*charFlip_SF*ctag_SF_Interpdo);
	 else if(weight_name=="ctag_PSWeightFSRup")histBdtG   ->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*charFlip_SF*ctag_SF_PSWeightFSRup);
	 else if(weight_name=="ctag_PSWeightFSRdo")histBdtG   ->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*charFlip_SF*ctag_SF_PSWeightFSRdo);
         else if(weight_name=="ctag_PSWeightISRup")histBdtG   ->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*charFlip_SF*ctag_SF_PSWeightISRup);
         else if(weight_name=="ctag_PSWeightISRdo")histBdtG   ->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*charFlip_SF*ctag_SF_PSWeightISRdo);
	 else if(weight_name=="ctag_PUWeightup")histBdtG   ->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*charFlip_SF*ctag_SF_PUWeightup);
	 else if(weight_name=="ctag_PUWeightdo")histBdtG   ->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*charFlip_SF*ctag_SF_PUWeightdo);
	 else if(weight_name=="ctag_XSec_BRUnc_DYJets_bup")histBdtG   ->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*charFlip_SF*ctag_SF_XSec_BRUnc_DYJets_bup);
	 else if(weight_name=="ctag_XSec_BRUnc_DYJets_bdo")histBdtG   ->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*charFlip_SF*ctag_SF_XSec_BRUnc_DYJets_bdo);
	 else if(weight_name=="ctag_XSec_BRUnc_DYJets_cup")histBdtG   ->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*charFlip_SF*ctag_SF_XSec_BRUnc_DYJets_cup);
	 else if(weight_name=="ctag_XSec_BRUnc_DYJets_cdo")histBdtG   ->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*charFlip_SF*ctag_SF_XSec_BRUnc_DYJets_cdo);
	 else if(weight_name=="ctag_XSec_BRUnc_WJets_cup")histBdtG   ->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*charFlip_SF*ctag_SF_XSec_BRUnc_WJets_cup);
	 else if(weight_name=="ctag_XSec_BRUnc_WJets_cdo")histBdtG   ->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*charFlip_SF*ctag_SF_XSec_BRUnc_WJets_cdo);
	 else if(weight_name=="ctag_jerup")histBdtG   ->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*charFlip_SF*ctag_SF_jerup);
	 else if(weight_name=="ctag_jerdo")histBdtG   ->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*charFlip_SF*ctag_SF_jerdo);
	 else if(weight_name=="ctag_jesTotalup")histBdtG   ->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*charFlip_SF*ctag_SF_jesTotalup);
	 else histBdtG   ->Fill( reader->EvaluateMVA( "BDTG method"), genweight*norm_scale*lumi*mu_id*ele_id*trig_SF*charFlip_SF*ctag_SF_jesTotaldo);
	}
      if (Use["BDTB"         ])   histBdtB   ->Fill( reader->EvaluateMVA( "BDTB method"          ) );
      if (Use["BDTD"         ])   histBdtD   ->Fill( reader->EvaluateMVA( "BDTD method"          ) );
      if (Use["BDTF"         ])   histBdtF   ->Fill( reader->EvaluateMVA( "BDTF method"          ) );
      if (Use["RuleFit"      ])   histRf     ->Fill( reader->EvaluateMVA( "RuleFit method"       ) );
      if (Use["SVM_Gauss"    ])   histSVMG   ->Fill( reader->EvaluateMVA( "SVM_Gauss method"     ) );
      if (Use["SVM_Poly"     ])   histSVMP   ->Fill( reader->EvaluateMVA( "SVM_Poly method"      ) );
      if (Use["SVM_Lin"      ])   histSVML   ->Fill( reader->EvaluateMVA( "SVM_Lin method"       ) );
      if (Use["FDA_MT"       ])   histFDAMT  ->Fill( reader->EvaluateMVA( "FDA_MT method"        ) );
      if (Use["FDA_GA"       ])   histFDAGA  ->Fill( reader->EvaluateMVA( "FDA_GA method"        ) );
      if (Use["Category"     ])   histCat    ->Fill( reader->EvaluateMVA( "Category method"      ) );
      if (Use["Plugin"       ])   histPBdt   ->Fill( reader->EvaluateMVA( "P_BDT method"         ) );

      // Retrieve also per-event error
      if (Use["PDEFoam"]) {
         Double_t val = reader->EvaluateMVA( "PDEFoam method" );
         Double_t err = reader->GetMVAError();
         histPDEFoam   ->Fill( val );
         histPDEFoamErr->Fill( err );
         if (err>1.e-50) histPDEFoamSig->Fill( val/err );
      }

      // Retrieve probability instead of MVA output
      if (Use["Fisher"])   {
         probHistFi  ->Fill( reader->GetProba ( "Fisher method" ) );
         rarityHistFi->Fill( reader->GetRarity( "Fisher method" ) );
      }
   }

   //normalize histo to value without ctag
   if ((!(weight_name.find("ctag")!= string::npos)) && (sample_type==0 || sample_type==1)){
     cout << "weight_name in normalized: " << weight_name << endl;
     if (fabs(histBdtG->Integral()) > 0.0) histBdtG->Scale(ctag_norm/histBdtG->Integral());
   }
   cout << "Final histBdtG->Integral(): " << histBdtG->Integral() << endl;


   // Get elapsed time
   sw.Stop();
   std::cout << "--- End of event loop: "; sw.Print();

   // Get efficiency for cuts classifier
   if (Use["CutsGA"]) std::cout << "--- Efficiency for CutsGA method: " << double(nSelCutsGA)/theTree->GetEntries()
                                << " (for a required signal efficiency of " << effS << ")" << std::endl;

   if (Use["CutsGA"]) {

      // test: retrieve cuts for particular signal efficiency
      // CINT ignores dynamic_casts so we have to use a cuts-specific Reader function to acces the pointer
      TMVA::MethodCuts* mcuts = reader->FindCutsMVA( "CutsGA method" ) ;

      if (mcuts) {
         std::vector<Double_t> cutsMin;
         std::vector<Double_t> cutsMax;
         mcuts->GetCuts( 0.7, cutsMin, cutsMax );
         std::cout << "--- -------------------------------------------------------------" << std::endl;
         std::cout << "--- Retrieve cut values for signal efficiency of 0.7 from Reader" << std::endl;
         for (UInt_t ivar=0; ivar<cutsMin.size(); ivar++) {
            std::cout << "... Cut: "
                      << cutsMin[ivar]
                      << " < \""
                      << mcuts->GetInputVar(ivar)
                      << "\" <= "
                      << cutsMax[ivar] << std::endl;
         }
         std::cout << "--- -------------------------------------------------------------" << std::endl;
      }
   }

   delete reader;

   std::cout << "==> TMVAClassificationApplication is done!" << std::endl << std::endl;
   string name_temp="";
   string name_wgt ="";
   string name_sys ="";
   if (weight_name=="nominal_noctag") name_wgt = "_nominal_noctag";
   if (weight_name=="central")        name_wgt = "";
   if (weight_name=="fakelep")        name_wgt = "";
   if (weight_name=="data")           name_wgt = "";
   if (weight_name=="fakelep_mc")     name_wgt = "_fake";
   if (weight_name=="pileup_up")      name_wgt = "_pileupUp";
   if (weight_name=="pileup_down")    name_wgt = "_pileupDown";
   if (weight_name=="prefire_up")     name_wgt = "_prefireUp";
   if (weight_name=="prefire_down")   name_wgt = "_prefireDown";
   if (weight_name=="muID_sysup")     name_wgt = "_muIDYEARsysUp";
   if (weight_name=="muID_sysdown")   name_wgt = "_muIDYEARsysDown";
   if (weight_name=="muID_statup")    name_wgt = "_muIDYEARstatUp";
   if (weight_name=="muID_statdown")  name_wgt = "_muIDYEARstatDown";
   if (weight_name=="eleID_sysup")    name_wgt = "_eleIDYEARsysUp";
   if (weight_name=="eleID_sysdown")  name_wgt = "_eleIDYEARsysDown";
   if (weight_name=="eleID_statup")   name_wgt = "_eleIDYEARstatUp";
   if (weight_name=="eleID_statdown") name_wgt = "_eleIDYEARstatDown";
   if (weight_name=="lumi_up")        name_wgt = "_lumiYEARUp";
   if (weight_name=="lumi_down")      name_wgt = "_lumiYEARDown";
   if (weight_name=="trigger_up")  
   {
    if(channel=="ee"){                name_wgt = "_dieleTriggerYEARUp";}
    if(channel=="em"){                name_wgt = "_elemuTriggerYEARUp";}
    if(channel=="mm"){                name_wgt = "_dimuTriggerYEARUp";}
   }
   if (weight_name=="trigger_down")
   {
    if(channel=="ee"){                name_wgt = "_dieleTriggerYEARDown";}
    if(channel=="em"){                name_wgt = "_elemuTriggerYEARDown";}
    if(channel=="mm"){                name_wgt = "_dimuTriggerYEARDown";}
   }
   if (weight_name=="charFlip_SFstatup")  name_wgt = "_chargeflipYEARstatUp";
   if (weight_name=="charFlip_SFstatdo")  name_wgt = "_chargeflipYEARstatDown";
   if (weight_name=="charFlip_SFsystup")  name_wgt = "_chargeflipYEARsystUp";
   if (weight_name=="charFlip_SFsystdo")  name_wgt = "_chargeflipYEARsystDown";
   if (weight_name=="sig_pdfup")      name_wgt = "_sigYEARpdfUp";
   if (weight_name=="sig_pdfdo")      name_wgt = "_sigYEARpdfDown";
   if (weight_name=="sig_scaleup")    name_wgt = "_sigYEARscaleUp";
   if (weight_name=="sig_scaledo")    name_wgt = "_sigYEARscaleDown";
   if (weight_name=="sig_psup")       name_wgt = "_sigYEARpsUp";
   if (weight_name=="sig_psdo")       name_wgt = "_sigYEARpsDown";
   //ctag
   if (weight_name=="ctag_statup")    name_wgt = "_ctagYEARstatUp";
   if (weight_name=="ctag_statdo")    name_wgt = "_ctagYEARstatDown";
   if (weight_name=="ctag_Extrapup")   name_wgt = "_ctagYEARExtrapUp";
   if (weight_name=="ctag_Extrapdo")   name_wgt = "_ctagYEARExtrapDown";
   if (weight_name=="ctag_LHEScaleWeightmuFup") name_wgt = "_ctagYEARLHEmuFUp";
   if (weight_name=="ctag_LHEScaleWeightmuFdo") name_wgt = "_ctagYEARLHEmuFDown";
   if (weight_name=="ctag_LHEScaleWeightmuRup") name_wgt = "_ctagYEARLHEmuRUp";
   if (weight_name=="ctag_LHEScaleWeightmuRdo") name_wgt = "_ctagYEARLHEmuRDown";
   if (weight_name=="ctag_Interpup")              name_wgt = "_ctagYEARInterpUp";
   if (weight_name=="ctag_Interpdo")              name_wgt = "_ctagYEARInterpDown";
   if (weight_name=="ctag_PSWeightFSRup")       name_wgt = "_ctagYEARPSFSRUp";
   if (weight_name=="ctag_PSWeightFSRdo")       name_wgt = "_ctagYEARPSFSRDown";
   if (weight_name=="ctag_PSWeightISRup")       name_wgt = "_ctagYEARPSISRUp";
   if (weight_name=="ctag_PSWeightISRdo")       name_wgt = "_ctagYEARPSISRDown";
   if (weight_name=="ctag_PUWeightup")          name_wgt = "_ctagYEARPUUp";
   if (weight_name=="ctag_PUWeightdo")          name_wgt = "_ctagYEARPUDown";
   if (weight_name=="ctag_XSec_BRUnc_DYJets_bup")       name_wgt = "_ctagDYXSbUp";
   if (weight_name=="ctag_XSec_BRUnc_DYJets_bdo")       name_wgt = "_ctagDYXSbDown";
   if (weight_name=="ctag_XSec_BRUnc_DYJets_cup")           name_wgt = "_ctagDYXScUp";
   if (weight_name=="ctag_XSec_BRUnc_DYJets_cdo")           name_wgt = "_ctagDYXScDown";
   if (weight_name=="ctag_XSec_BRUnc_WJets_cup")           name_wgt = "_ctagWJetsXScUp";
   if (weight_name=="ctag_XSec_BRUnc_WJets_cdo")           name_wgt = "_ctagWJetsXScDown";
   if (weight_name=="ctag_jerup")               name_wgt = "_ctagJERUp";
   if (weight_name=="ctag_jerdo")               name_wgt = "_ctagJERDown";
   if (weight_name=="ctag_jesTotalup")          name_wgt = "_ctagJESUp";
   if (weight_name=="ctag_jesTotaldo")          name_wgt = "_ctagJESDown";

   if (system_unc=="central")                   name_sys = "";
   if (system_unc=="jesup")                     name_sys = "_jesYEARUp";
   if (system_unc=="jesdo")                     name_sys = "_jesYEARDown";
   if (system_unc=="jerup")                     name_sys = "_jerYEARUp";
   if (system_unc=="jerdo")                     name_sys = "_jerYEARDown";
   if (system_unc=="unclusterEup")              name_sys = "_metYEARunclusterEUp";
   if (system_unc=="unclusterEdo")              name_sys = "_metYEARunclusterEDown";

   name_temp = "ttcYEAR_" + input_name + name_wgt + name_sys;
   if (input_name.find("ttc_a")!= string::npos) name_temp.replace(REPLACEINDEX,5,"TAToTTQ");
   if (input_name.find("ttc_s0")!= string::npos) name_temp.replace(REPLACEINDEX,6,"TS0ToTTQ");
   histBdtG->SetNameTitle(name_temp.c_str(),name_temp.c_str());

   input_f->Close();
   return histBdtG;
}

int TMVAClassificationApplication()
{
   std::cout<<"START!"<<std::endl;
   string sample_path = "SAMPLE_PATH";

   string type_="CSIGTYPE"; 
   string cp="COUPLING";
   string mass="MASS";

   float eff_N_signal;
   string flags="GenModel_T"+type_+"ToTTQ_M"+type_+"_MASS_TuneCP5_13TeV_G2HDM_"+cp+"_madgraphMLM_pythia8";

   string ntemp_signal=sample_path;
   ntemp_signal=ntemp_signal+"SIGNAL_EOS_INPUT";
   TFile*ftemp_signal=TFile::Open(ntemp_signal.c_str());
   TH1D*htemp_signal=(TH1D*)ftemp_signal->Get("nEventsGenWeighted");
   TTree*ttemp_signal=(TTree*)ftemp_signal->Get("Events");
   int nsignal_total=ttemp_signal->GetEntriesFast();

   SIGNAL_EFF_COMMAND
   ftemp_signal->Close();

   vector<std::string> samples;
   LOADSAMPLE

   vector<float> xss;
   LOADXSEC
  
   vector<bool> is_train;
   LOAD_ISTRAIN
 
   vector<float> eff_N;
   for(int i=0;i<samples.size();i++){
     string ntemp=sample_path+samples[i]+".root";
//     if(i==11)ntemp=sample_path+"DYnlo.root";
     TFile*ftemp=TFile::Open(ntemp.c_str());
     TH1D*ttemp=(TH1D*)ftemp->Get("nEventsGenWeighted");
     if (is_train[i]) eff_N.push_back(0.5*ttemp->GetBinContent(1));//half of the events are used for BDT training
     else eff_N.push_back(ttemp->GetBinContent(1));
     ftemp->Close();
   }
   //   eff_N.push_back(3.4087701e+08);
   //   eff_N.push_back(349000.);
   //   eff_N.push_back(175000.);
   //   eff_N.push_back(1935527);
   //   eff_N.push_back(3455733.0);
   
  std::vector<string> weights{"nominal_noctag","central","pileup_up","pileup_down","muID_sysup","muID_sysdown","muID_statup","muID_statdown","eleID_sysup","eleID_sysdown","eleID_statup","eleID_statdown","trigger_up","trigger_down","lumi_up","lumi_down","ctag_statup","ctag_statdo","ctag_Extrapup","ctag_Extrapdo","ctag_LHEScaleWeightmuFup","ctag_LHEScaleWeightmuFdo","ctag_LHEScaleWeightmuRup","ctag_LHEScaleWeightmuRdo","ctag_Interpup","ctag_Interpdo","ctag_PSWeightFSRup","ctag_PSWeightFSRdo","ctag_PSWeightISRup","ctag_PSWeightISRdo","ctag_PUWeightup","ctag_PUWeightdo","ctag_XSec_BRUnc_DYJets_bup","ctag_XSec_BRUnc_DYJets_bdo","ctag_XSec_BRUnc_DYJets_cup","ctag_XSec_BRUnc_DYJets_cdo","ctag_XSec_BRUnc_WJets_cup","ctag_XSec_BRUnc_WJets_cdo","ctag_jerup","ctag_jerdo","ctag_jesTotalup","ctag_jesTotaldo","charFlip_SFstatup","charFlip_SFstatdo","charFlip_SFsystup","charFlip_SFsystdo","sig_pdfup","sig_pdfdo","sig_scaleup","sig_scaledo","sig_psup","sig_psdo","prefire_up","prefire_down"};

  string system_unc[6]={"jesup","jesdo","jerup","jerdo","unclusterEup","unclusterEdo"};
  string channels[3]={"ee","em","mm"};

  for (int ic=0;ic<3;ic++){
    string output_name="TMVApp_"+mass+"_"+channels[ic]+".root";
    TFile *target  = new TFile( output_name.c_str(),"RECREATE" );
    string signal_input="";
    if(type_=="A")signal_input=signal_input+"ttc_a_"+cp+"_M"+type_+mass;
    if(type_=="S0")signal_input=signal_input+"ttc_s0_"+cp+"_M"+type_+mass;
    if (type_=="a_s"){
     if (mass=="250_200"){
       signal_input=signal_input+"ttc_a_250_s_200_"+cp;
     }else{
       signal_input=signal_input+"ttc_a_250_s_200_"+cp;
     }
    }
    TH1F*htemp;
    TH1F*hfake_no_mcsubtraction;
    TH1F*hfake;
    TH1F*hfake_up;
    TH1F*hfake_down;
    
    // add signal cross-section
    float signal_xs=Get_signalXS(signal_input);
    cout << "Signal cross-section -->" << signal_xs << endl;

    std::vector<float> ctagnorms_beforecalibrated;
    std::vector<float> ctagnorms_aftercalibrated;
    std::cout<<"start looping weights"<<std::endl;
    for(int iw=0;iw<weights.size();iw++){
      // signal don't need charge flip SF (Should be dropped since we take care of it in step1)
      if(!(weights[iw].find("charFlip")!= string::npos))
      {
        htemp=Getoutput("",signal_input,signal_xs,eff_N_signal,weights[iw],"central",mass,channels[ic],type_, cp, 0);
        if(iw == 0)ctagnorms_beforecalibrated.push_back(htemp->Integral());
        if(iw == 1)ctagnorms_aftercalibrated.push_back(htemp->Integral());
        if(iw>0 && weights[iw].find("ctag")!= string::npos){
	  if (fabs(htemp->Integral()) > 0.0) htemp->Scale(ctagnorms_beforecalibrated[0]/ctagnorms_aftercalibrated[0]); // Use nominal normalization factor
	}
        target->cd();
        htemp->Write();
      }
      //for bkgs, no need of signal theoretic uncertainty
      if(weights[iw].find("sig")!= string::npos)continue;
      for(int is=0;is<samples.size();is++){
        cout<<"start loop process:"<<samples[is]<<endl;
        htemp=Getoutput("",samples[is],xss[is],eff_N[is],weights[iw],"central",mass,channels[ic],type_, cp, 0);
        if(iw == 0)ctagnorms_beforecalibrated.push_back(htemp->Integral());
        if(iw == 1)ctagnorms_aftercalibrated.push_back(htemp->Integral());
        if(iw>0 && weights[iw].find("ctag")!= string::npos){ // after BTV meeting we should fix this as well
	  if (fabs(htemp->Integral()) > 0.0) htemp->Scale(ctagnorms_beforecalibrated[is+1]/ctagnorms_aftercalibrated[is+1]);
	}
        target->cd();
        htemp->Write();
     }
   }

   std::cout<<"start looping systematics"<<std::endl;
   for(int isys=0;isys<6;isys++){
      htemp = Getoutput("", signal_input,signal_xs, eff_N_signal,"central",system_unc[isys], mass, channels[ic], type_, cp, 1);
      target->cd();
      htemp->Write();
      for(int is=0;is<samples.size();is++){
        htemp = Getoutput("", samples[is], xss[is], eff_N[is],"central",system_unc[isys], mass, channels[ic], type_, cp, 1);
        target->cd();
        htemp->Write();
     }
   }
  
   std::cout<<"start looping fake"<<std::endl;
   if(ic==0) {
     hfake_no_mcsubtraction=Getoutput("", "fakelep_ee", 1., 1,"fakelep","central", mass, channels[ic], type_, cp, 2);
   }
   if(ic==1) {
     hfake_no_mcsubtraction=Getoutput("", "fakelep_em", 1., 1,"fakelep","central", mass, channels[ic], type_, cp, 2);
   }
   if(ic==2) {
     hfake_no_mcsubtraction=Getoutput("", "fakelep_mm", 1., 1,"fakelep","central", mass, channels[ic], type_, cp, 2);
   }

   hfake=(TH1F*)hfake_no_mcsubtraction->Clone();

   std::cout<<"start looping fake mc"<<std::endl;
   for(int is=0;is<samples.size();is++){
     htemp=Getoutput("",samples[is]+"_fake_"+channels[ic],xss[is],eff_N[is],"fakelep_mc","central",mass,channels[ic],type_,cp,3);
     hfake->Add(htemp);
   }

   hfake_up=(TH1F*)hfake->Clone();
   hfake_up->Scale(1.3);
   hfake_down=(TH1F*)hfake->Clone();
   hfake_down->Scale(0.7);

   hfake_no_mcsubtraction->SetNameTitle("ttcYEAR_TTTo1L_noMCsub","ttcYEAR_TTTo1L_noMCsub");
   hfake->SetNameTitle("ttcYEAR_TTTo1L","ttcYEAR_TTTo1L");
   hfake_up->SetNameTitle("ttcYEAR_TTTo1L_fakeUp","ttcYEAR_TTTo1L_fakeUp");
   hfake_down->SetNameTitle("ttcYEAR_TTTo1L_fakeDown","ttcYEAR_TTTo1L_fakeDown");
   target->cd();
   hfake->Write();
   hfake_up->Write();
   hfake_down->Write();

   // check fake subtraction of MC
   std::cout<<"WITHOUT subtraction"<<hfake_no_mcsubtraction->Integral()<<std::endl;
   std::cout<<"WITH subtractiob"<<hfake->Integral()<<std::endl;

   TH1F*hdata;
   std::cout<<"start looping data"<<std::endl;
   if(ic==0) {
     hdata=Getoutput("","data_ee",1.,1,"data","central",mass,channels[ic],type_,cp,4);
   }
   if(ic==1) {
     hdata=Getoutput("","data_em",1.,1,"data","central",mass,channels[ic],type_,cp,4);
   }
   if(ic==2) {
     hdata=Getoutput("","data_mm",1.,1,"data","central",mass,channels[ic],type_,cp,4);
   }
   hdata->SetNameTitle("ttcYEAR_data_obs","ttcYEAR_data_obs");
   target->cd();
   hdata->Write();
   target->Close();
  }
  
  return 0;
}
