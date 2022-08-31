PWd=`pwd`
cps=("rtc01" "rtu01")
mass=(200) # 300 350 400 500 600 700)
era=("2016apv") # "2016postapv" "2017" "2018")

#for TA submission
for k in ${era[*]}
do
    for j in ${cps[*]}
    do
	for i in ${mass[*]}
	do
	cd ${k}/ttc_a_${j}_MA$i
	echo $PWD
	condor_submit sub.jdl
	cd $PWd
	done
    done
done

#for TS0 submission
for k in ${era[*]}
do
    for j in ${cps[*]}
    do
	for i in ${mass[*]}
	do
	cd ${k}/ttc_s0_${j}_MS0$i
	echo $PWD
	condor_submit sub.jdl
	cd $PWd
	done
    done
done
