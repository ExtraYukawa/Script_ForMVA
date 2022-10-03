PWd=`pwd`
cps=("rtc01" "rtc04" "rtc08" "rtc10" "rtu01" "rtu04" "rtu08" "rtu10")
#cps=("rtc01")
mass=(200 300 350 400 500 600 700)
#mass=(200)
#era=("2016apv" "2016postapv" "2017" "2018")
era=("2016postapv")

#for TA extration
for k in ${era[*]}
do
    for j in ${cps[*]}
    do
	for i in ${mass[*]}
	do
	cd ${k}/ttc_a_${j}_MA$i
	echo -e "\033[0;32m $PWD \033[0m"
	tar xf output.tar.gz
	rm output.tar.gz
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
	echo -e "\033[0;32m $PWD \033[0m"
	tar xf output.tar.gz
	rm output.tar.gz
	cd $PWd
	done
    done
done
