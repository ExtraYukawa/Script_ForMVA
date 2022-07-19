PWd=`pwd`
cps=("rtc01" "rtc04" "rtc08" "rtc10" "rtu01" "rtu04" "rtu08" "rtu10")
mass=(200 300 350 400 500 600 700)

#for TA submission
for j in ${cps[*]}
do
  for i in ${mass[*]}
  do
  cd ttc_a_${j}_MA$i
  echo $PWD
  tar xf output.tar.gz
  rm output.tar.gz
  cd $PWd
  done
done

#for TS0 submission
for j in ${cps[*]}
do
  for i in ${mass[*]}
  do
  cd ttc_s0_${j}_MS0$i
  echo $PWD
  tar xf output.tar.gz
  rm output.tar.gz
  cd $PWd
  done
done
