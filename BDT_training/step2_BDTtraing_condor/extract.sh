PWd=`pwd`
cps=("rtc01" "rtu01")
#mass=(200 300 350 400 500 600 700)
mass=(200 700)
syss=(0 1 2 3 4 5 6)
#era=("2016apv" "2016postapv" "2017" "2018")
era=("2018")

#for TA extration
for k in ${era[*]}
do
    for j in ${cps[*]}
    do
	for i in ${mass[*]}
	do
	cd ${k}/ttc_a_${j}_MA$i
	PWdd=`pwd`
	for s in ${syss[*]}
	do
	    cd ttc_a_${j}_MA${i}_$s
	    echo -e "\033[0;32m $PWD \033[0m"
	    tar xf aa.tar.gz
	    cd $PWdd
	done
	cd $PWd
	done
    done
done

#for TS0 extration
for k in ${era[*]}
do
    for j in ${cps[*]}
    do
	for i in ${mass[*]}
	do
	cd ${k}/ttc_s0_${j}_MS0$i
	PWdd=`pwd`
	for s in ${syss[*]}
	do
	    cd ttc_s0_${j}_MS0${i}_$s
	    echo -e "\033[0;32m $PWD \033[0m"
	    tar xf aa.tar.gz
	    cd $PWdd
	done
	cd $PWd
	done
    done
done
