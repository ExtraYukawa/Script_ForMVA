PWd=`pwd`

#cps=("rtc04" "rtu04")
#mass=(200 300 350 400 500 600 700)

#highmass samples
#cps=("rtc04" "rtu04")
#mass=(800 900 1000)


#inteference samples
cps=("rtc04" "rtu04")
#mass=(250 300 350 400 550 700 800 900 1000) # asume this A mass
mass=(800 900 1000) # asume this A mass
#mass=(250) # asume this A mass 


#era=("2016apv" "2016postapv" "2017" "2018")
era=("2016apv")
#era=("2016postapv")
#era=("2017")
#era=("2018")

#for TA submission
#for k in ${era[*]}
#do
#    for j in ${cps[*]}
#    do
#	for i in ${mass[*]}
#	do
#	cd ${k}/ttc_a_${j}_MA$i
#	echo $PWD
#	echo -e "\033[0;32m Submitting for ttc_a_${j}_MA$i in ${k} era \033[0m"
#	condor_submit sub.jdl
#	cd $PWd
#	done
#    done
#done

###for TS0 submission
##for k in ${era[*]}
##do
##    for j in ${cps[*]}
##    do
##	for i in ${mass[*]}
##	do
##	cd ${k}/ttc_s0_${j}_MS0$i
##	echo $PWD
##	echo -e "\033[0;32m Submitting for ttc_s0_${j}_MS0$i in ${k} era \033[0m"
##	condor_submit sub.jdl
##	cd $PWd
##	done
##    done
##done

#for inteterference samples extration
for k in ${era[*]}
do
    for j in ${cps[*]}
    do
	for i in ${mass[*]}
	do
	cd ${k}/ttc_a_${i}_s_$(($i-50))_${j}
	echo $PWD
	echo -e "\033[0;32m Submitting for ttc_a_${i}_s_$(($i-50))_${j} in ${k} era \033[0m"
	condor_submit sub.jdl 
	cd $PWd
	done
    done
done
