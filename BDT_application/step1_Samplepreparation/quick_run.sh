for ERA in 2016apv 2016postapv 2017 2018
do
  python runCondor.py --era $ERA 
  python runCondor.py --era $ERA -s highmass
  python runCondor.py --era $ERA -s interference
done
