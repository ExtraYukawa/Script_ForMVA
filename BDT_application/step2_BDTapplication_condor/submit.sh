PWd=`pwd`
#cps=("rtc01" "rtc04" "rtc08" "rtc10" "rtu01" "rtu04" "rtu08" "rtu10")
cps=("rtc04" "rtu04") # Efe proved that other coupling can derived from this
#mass=(200 300 350 400 500 600 700)
#mass=(800 900 1000)
mass=(200 300 350 400 500 600 700 800 900 1000)
#era=("2016apv" "2016postapv" "2017" "2018")
era=("2016apv")
#era=("2016postapv")
#era=("2017")
#era=("2018")

#for TA submission
for k in ${era[*]}
do
    for j in ${cps[*]}
    do
	for i in ${mass[*]}
	do
	cd ${k}/ttc_a_${j}_MA$i
	echo $PWD
	echo -e "\033[0;32m Evaluating for ttc_a_${j}_MA$i in ${k} era \033[0m"
	condor_submit sub.jdl
	cd $PWd
	done
    done
done

##for TS0 submission
#for k in ${era[*]}
#do
#    for j in ${cps[*]}
#    do
#	for i in ${mass[*]}
#	do
#	cd ${k}/ttc_s0_${j}_MS0$i
#	echo $PWD
#	echo -e "\033[0;32m Evaluating for ttc_s0_${j}_MS0$i in ${k} era \033[0m"
#	condor_submit sub.jdl
#	cd $PWd
#	done
#    done
#done
