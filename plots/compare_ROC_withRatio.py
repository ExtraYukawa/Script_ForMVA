#==============
# Last used:
# python compare_ROC_withRatio.py
#==============

#!/usr/bin/env python

import sys
import os
import array
import shutil

thisdir = os.path.dirname(os.path.realpath(__file__))
basedir = os.path.dirname(thisdir)
sys.path.append(basedir)
print (thisdir)
#import config
#from datasets import allsamples
#from plotstyle import SimpleCanvas
from plotstyle import *

import ROOT
#from ROOT import *
ROOT.gROOT.SetBatch(True)

def makePlot(mass, hname, xmin, xmax, year="2018", isNorm=True):
    
    wRatio = True
    
    #Get histograms
    file_old = ROOT.TFile("/eos/user/g/gkole/database/ExtraYukawa_BDT_woMETPhi/BDT_weights/2018/ttc_a_rtc04_MA350_toStudy/ttc_a_rtc04_MA350_0/TMVA_ttc_a_rtc04_MA350_central.root")
    file_new = ROOT.TFile("/afs/cern.ch/work/g/gkole/TTC/InputForLimit/CMSSW_10_6_29/src/Script_ForMVA/BDT_training/step2_BDTtraing_condor/2018/ttc_a_rtc04_MA350_toStudy/ttc_a_rtc04_MA350_0/TMVA_ttc_a_rtc04_MA350_central.root")

    hold = file_old.Get("dataset_ttc_a_rtc04_MA350_central/Method_BDTG/BDTG/%s"%hname)
    hnew = file_new.Get("dataset_ttc_a_rtc04_MA350_central/Method_BDTG/BDTG/%s"%hname)
    
    
    hold.SetLineColor(ROOT.kRed)
    hnew.SetLineColor(ROOT.kBlue)
    
    # print "hmm.Integral(): ", hmm.Integral()

    if wRatio:
        canvas = RatioCanvas(" "," ",59000)
        canvas.ytitle = 'Background rejection (1-eff)'
        canvas.xtitle = 'Signal eff'
    else:
        canvas = SimpleCanvas(" "," ",59000)
    canvas.legend.setPosition(0.7, 0.7, 0.9, 0.9)
    canvas.legend.add('hold', title = 'approval', opt = 'LF', color = ROOT.kRed, fstyle = 3003, lwidth = 2)
    canvas.legend.add('hnew', title = 'new', opt = 'LF', color = ROOT.kBlue,  fstyle = 3003, lwidth = 2)
    
    canvas.addHistogram(hold, drawOpt = 'HIST')
    canvas.addHistogram(hnew, drawOpt = 'HIST')
    
    canvas.applyStyles()
    if wRatio:
        canvas.printWeb('ROC_compare_wRatio', hname+"_M"+mass, logy = True)
    else:
        canvas.printWeb('ROC_compare', hname+"_M"+mass, logy = True)

if __name__ == "__main__":
    makePlot("350","MVA_BDTG_rejBvsS",0.0,1.0)
    # makePlot("350","MVA_BDTG_invBeffvsSeff",0.0,1.0)
