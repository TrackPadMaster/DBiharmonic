#!/bin/bash


GAMMA="2.0 3.0 4.0 5.0 7.5 10.0 12.5 15.0 17.5 20.0 25.0"

for gamma in $GAMMA; do
	echo "Now running gamma=$gamma"
	awk -v gamma=$gamma '{if($3=="gammaP") {print gamma" ! gammaP"} else {print $0}}' inputstart > ./input0

	./FortranRunner.sh
	
	./DataCollector.sh > ${gamma}Gam.dat
	


done
