# https://github.com/KIT-CMS/gc_configs_for_embedding/blob/4e87c9a166a2d117f586ef290d4442ad56fcf6c0/scripts/read_filelist_from_das.py
# Last used:
# python read_filelist_from_das.py --nick TAToTTQ_MA-200to700GeV_rtc04 --query /TAToTTQ_MA-200to700GeV_TuneCP5_13TeV_G2HDM-rtc04-madgraphMLM-pythia8/RunIISummer20UL17NanoAODv9-rp_106X_mc2017_realistic_v9-v2/NANOAODSIM --outputfile test2.txt
# chmod a+x test2.txt 
# ./test2.txt 
# cd /tmp/$USER/TAToTTQ_MA-200to700GeV_rtc04

#***************
# hadd all the files
#***************
# wget https://github.com/ExtraYukawa/ttc_bar/blob/lxplus-9/scripts/haddnano.py (with raw link from web)
# python haddnano.py output.root *.root 
# root -l output.root
# if you want only interactively the do in the following way:
# Events->GetEntries("GenModel_TAToTTQ_MA_200_TuneCP5_13TeV_G2HDM_rtc04_madgraphMLM_pythia8")
# (long long) 521871

# OR
# run the script https://github.com/ExtraYukawa/Script_ForMVA/blob/main/script/print_branch_entries.py



############

import argparse
import json
import subprocess
import os, sys
import getpass

xootd_prefix = "root://cms-xrd-global.cern.ch/"
parser = argparse.ArgumentParser(
    description="This scipt can be used, to generate a grid control compatible filelist from das"
)

parser.add_argument("--nick", required=True, help="Name of the dataset")
parser.add_argument("--query", required=True, help="DAS query of the dataset")
parser.add_argument(
    "--phys03",
    action="store_true",
    help="If set, phys03 instance is used instead of global",
)
parser.add_argument(
    "--gridka-red",
    action="store_true",
    help="If set, the gridka redicator root://cmsxrootd-redirectors.gridka.de/ is used directly. Default: {}".format(
        xootd_prefix
    ),
)
parser.add_argument("--outputfile", help="output file")


def read_filelist_from_das(nick, query, outputfile, phys03, xootd_prefix):
    print("Getting filelist for \n  Nick: {}".format(nick))
    filedict = {}
    das_query = "file dataset={}".format(query)
    if phys03:
        das_query += " instance=prod/phys03"
    else:
        das_query += " instance=prod/global"
    print("  DAS Query: {}".format(das_query))
    # cmd = "/cvmfs/cms.cern.ch/common/dasgoclient --query '{}' --json".format(das_query)
    cmd = "dasgoclient --query '{}' --json".format(das_query)
    output = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE)
    jsonS = output.communicate()[0]
    filelist = json.loads(jsonS)
    for file in filelist:
        filedict[file["file"][0]["name"]] = file["file"][0]["nevents"]
    print(
        "  Total files:  {} \n  Total events: {}".format(
            len(filedict.keys()), sum(filedict.values())
        )
    )
    outfile = open(outputfile, "w")
    #outfile.write("[{}] \n".format(nick))
    #outfile.write("nickname = {} \n".format(nick))
    #for file in filedict.keys():
    #    outfile.write(
    #        "{prefix}/{path} = {nevents} \n".format(
    #            prefix=xootd_prefix, path=file, nevents=filedict[file]
    #        )
    #    )
    
    # requested format for next step to copy root files to my lxplus tmp area
    path = "/tmp/%s/%s"%(getpass.getuser(), nick)
    if not os.path.isdir(path):
        os.mkdir(path)
    count = 1
    for file in filedict.keys():

        outfile.write(
            "xrdcp -f {prefix}/{path} /tmp/{username}/{name}/{count}.root \n".format(
                prefix=xootd_prefix, path=file, username=getpass.getuser(), name=nick, count=int(count)
            )
        )
        count = count+1
    outfile.close()

    # get entries with flag
    #for file in filedict.keys():
    #    cmdd = "root -l {prefix}/{path}".format(prefix=xootd_prefix, path=file)
    #    outputt = subprocess.Popen([cmdd], shell=True, stdout=subprocess.PIPE)
    #    jsonSS = outputt.communicate()[0]
    #    print jsonSS

if __name__ == "__main__":
    args = parser.parse_args()
    if args.gridka_red:
        xootd_prefix = "root://cmsxrootd-redirectors.gridka.de/"
    read_filelist_from_das(
        args.nick, args.query, args.outputfile, args.phys03, xootd_prefix
    )
