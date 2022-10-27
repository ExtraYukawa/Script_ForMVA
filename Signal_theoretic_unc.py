import ROOT
from array import array

ptbin=array('d',[20.0, 35.0, 50.0, 80.0, 120.0, 160.0, 200.0, 260.0, 320.0])
pdf_unc=array('d',[0.0027, 0.0060, 0.0064, 0.0071, 0.0073, 0.0105, 0.0132, 0.0161])
scale_unc=array('d',[0.0989, 0.0951, 0.0979, 0.1058, 0.1136, 0.1282, 0.1376, 0.1467])
ps_unc=array('d',[0.14212, 0.0492, 0.0387, 0.0163, 0.0378, 0.0192, 0.0691, 0.03185])

hist_pdf = ROOT.TH1D('pdf_unc','pdf_unc',8,ptbin)
hist_scale = ROOT.TH1D('scale_unc','scale_unc',8,ptbin)
hist_ps = ROOT.TH1D('ps_unc','ps_unc',8,ptbin)

for i in range(0,8):
  hist_pdf.SetBinContent(i+1,pdf_unc[i])
  hist_scale.SetBinContent(i+1,scale_unc[i])
  hist_ps.SetBinContent(i+1,ps_unc[i])

fout=ROOT.TFile.Open('signalunc.root','recreate')
fout.cd()
hist_pdf.Write()
hist_scale.Write()
hist_ps.Write()
fout.Close()
