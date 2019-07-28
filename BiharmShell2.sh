#!/bin/bash



GAMMA="2.0 3.0 4.0 5.0 6.0 7.5 9.0 11.0 15.0 20.0 25.0"
FF="250 300 350 400"
for ff in $FF; do
	echo "Starting F0 = "$ff
	newdir=$ff'Force_200Potential'
	mkdir $newdir
	awk -v F0=$ff '{if($3=="F_0") {print F0" 		! F_0 in units of Fr"} else {print $0}}' inputstart > ./inputstep
	for gamma in $GAMMA; do
		echo "Now running gamma=$gamma"
		awk -v gamma=$gamma '{if($3=="gammaP") {print gamma" ! gammaP"} else {print $0}}' inputstep > ./input0

		./FortranRunner.sh
	
		./DataCollector.sh > ./$newdir/${gamma}Gam.dat
	done
done
