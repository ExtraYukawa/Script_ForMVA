PWd=`pwd`
#cps=("rtc01" "rtc04" "rtc08" "rtc10" "rtu01" "rtu04" "rtu08" "rtu10")
#cps=("rtc04" "rtu04")
#cps=("rtc01" "rtc04" "rtc08" "rtc10")
#mass=(200 300 350 400 500 600 700)
#mass=(800 900 1000)
#mass=(200 300 350 400 500 600 700 800 900 1000)

#inteference samples
cps=("rtc04" "rtu04") # Efe proved that other coupling can derived from this 
mass=(250 300 350 400 550 700) # asume this A mass
#mass=(250) # asume this A mass 

#era=("2016apv" "2016postapv" "2017" "2018")
era=("2016apv")
#era=("2016postapv")
#era=("2017")
#era=("2018")

##for TA extration
#for k in ${era[*]}
#do
#    for j in ${cps[*]}
#    do
#	for i in ${mass[*]}
#	do
#	cd ${k}/ttc_a_${j}_MA$i
#	echo -e "\033[0;32m $PWD \033[0m"
#	tar xf output.tar.gz
#	rm output.tar.gz
#	cd $PWd
#	done
#    done
#done

##for TS0 extration
#for k in ${era[*]}
#do
#    for j in ${cps[*]}
#    do
#	for i in ${mass[*]}
#	do
#	cd ${k}/ttc_s0_${j}_MS0$i
#	echo -e "\033[0;32m $PWD \033[0m"
#	tar xf output.tar.gz
#	rm output.tar.gz
#	cd $PWd
#	done
#    done
#done


#for inteterference samples extration
for k in ${era[*]}
do
    for j in ${cps[*]}
    do
	for i in ${mass[*]}
	do
	cd ${k}/ttc_a_${i}_s_$(($i-50))_${j}
	echo -e "\033[0;32m $PWD \033[0m"
	tar xf output.tar.gz 
	rm output.tar.gz
	cd $PWd
	done
    done
done
