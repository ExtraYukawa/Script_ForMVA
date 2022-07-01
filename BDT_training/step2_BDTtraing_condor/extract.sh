PWd=`pwd`
cps=("rtc01" "rtu01")
mass=(200 300 350 400 500 600 700)
syss=(0 1 2 3 4 5 6)

#for TA submission
for j in ${cps[*]}
do
  for i in ${mass[*]}
  do
  cd ttc_a_${j}_MA$i
  PWdd=`pwd`
  for s in ${syss[*]}
  do
    cd ttc_a_${j}_MA${i}_$s
    echo $PWD
    tar xf aa.tar.gz
    cd $PWdd
  done
  cd $PWd
  done
done

#for TS0 submission
for j in ${cps[*]}
do
  for i in ${mass[*]}
  do
  cd ttc_s0_${j}_MS0$i
  PWdd=`pwd`
  for s in ${syss[*]}
  do
    cd ttc_s0_${j}_MS0${i}_$s
    echo $PWD
    tar xf aa.tar.gz
    cd $PWdd
  done
  cd $PWd
  done
done
