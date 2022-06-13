#!/bin/bash

#Simulations list
Sims=("5-Series5" "6-Series6" "8-Series8" "9-Series9")
Scripts=("BrokenMF.py")

for sim in "${Sims[@]}"
do
	for script in "${Scripts[@]}"
	do
		cp $script $sim/dump/z-cId
	done
done

for sim in "${Sims[@]}"
do
	cd $sim/dump/z-cId
	./$script &
	cd ../../../
done
wait

./BrokenMFallSims.py


