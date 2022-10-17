PWd=`pwd`
cps=("rtc01" "rtu01")
##cps=("rtc04" "rtu04")
mass=(200 300 350 400 500 600 700)

#test
#cps=("rtc01")
##mass=(200)

#inteference samples
#cps=("rtc04" "rtu04")
#masses = ['250','300','350','400','550','700'] # asume this A mass
#mass=(250) # asume this A mass 

#highmass samples
#cps=("rtc04" "rtu04")
#mass=(800 900 1000)

#systematic variations
syss=(0 1 2 3 4 5 6 7 8)
#era=("2016apv" "2016postapv" "2017" "2018")
#era=("2016apv")
#era=("2016postapv")
#era=("2017")
era=("2018")

##for TA extration
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

##for TS0 extration
#for k in ${era[*]}
#do
#    for j in ${cps[*]}
#    do
#	for i in ${mass[*]}
#	do
#	cd ${k}/ttc_s0_${j}_MS0$i
#	PWdd=`pwd`
#	for s in ${syss[*]}
#	do
#	    cd ttc_s0_${j}_MS0${i}_$s
#	    echo -e "\033[0;32m $PWD \033[0m"
#	    tar xf aa.tar.gz
#	    cd $PWdd
#	done
#	cd $PWd
#	done
#    done
#done

#for inteterference samples extration
#for k in ${era[*]}
#do
#    for j in ${cps[*]}
#    do
#	for i in ${mass[*]}
#	do
#	cd ${k}/ttc_a_${i}_s_$(($i-50))_${j}
#	PWdd=`pwd`
#	for s in ${syss[*]}
#	do
#	    cd ttc_a_${i}_s_$(($i-50))_${j}_$s
#	    echo -e "\033[0;32m $PWD \033[0m"
#	    tar xf aa.tar.gz
#	    cd $PWdd
#	done
#	cd $PWd
#	done
#    done
#done
