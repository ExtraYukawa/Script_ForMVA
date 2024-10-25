# Last used:
# python print_branch_entries.py
#example output: https://gist.github.com/gourangakole/cc5d1c4274268989b31b42efef527229
import ROOT
import itertools  # To generate combinations of rhott and rhotc values

# Specify the path to your ROOT file
file_path = "/tmp/gkole/CGToBHpm_MH-300_all_coupling/output.root"  # Replace this with your actual file path

# Load the ROOT file and retrieve the TTree
file = ROOT.TFile.Open(file_path)
tree = file.Get("Events")  # Replace "Events" with your actual TTree name if different

# Define possible values for `rhott` and `rhotc` variations
rhott_values = ['rhott01', 'rhott04', 'rhott06', 'rhott10']  # Example values, adjust as needed
rhotc_values = ['rhotc01', 'rhotc04', 'rhotc06', 'rhotc10']  # Example values, adjust as needed

# Generate all combinations of rhott and rhotc
combinations = itertools.product(rhott_values, rhotc_values)

total_events = 0
# Loop over each combination to generate branch names
for rhott, rhotc in combinations:
        branch_name = f"GenModel_CGToBHpm_MH_300_{rhott}_{rhotc}_TuneCP5_13TeV_G2HDM_madgraphMLM_pythia8"
        print(f"Processing branch: {branch_name}")

        print ("print entries")
        total_events = total_events + tree.GetEntries(branch_name)
        # Events->GetEntries("GenModel_CGToBHpm_MH_300_rhott01_rhotc01_TuneCP5_13TeV_G2HDM_madgraphMLM_pythia8")
        print (tree.GetEntries(branch_name))
        print("\n" + "="*50 + "\n")  # Separator between branches

print ("total_events", total_events)
# Close the ROOT file
file.Close()
                                                                
