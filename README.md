# Instruction to run Script_ForMVA 

```
cmsrel CMSSW_10_6_29
cd CMSSW_10_6_29/src
source script/env.sh # DO NOT run cmsenv
git clone git@github.com:ExtraYukawa/Script_ForMVA.git (one time setup)
cd Script_ForMVA
```

## (Optional) Produce C++ code for DNN model
The DNN model and corresponding preprocessor (`.pt` and `.onnx` files) are trained in other code `HiggsReco` and imported to the `data` directory here. To automatically produce C++ code for DNN model(`.dat` and `.hxx`), please follow the steps below (not needed for standard DNN model, already produced for you)
```
cd data
root -l -b ../script/TMVA_SOFIE_ONNX.C\(\"data/DNN_Flav_MET_threeJet_model_v2.onnx\"\)
```
## Then for Training and Application goto sub-directories
