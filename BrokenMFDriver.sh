#!/bin/bash

#Simulations list
Sims=("1-Series1" "2-Series2" "3-Series3" "4-Series4" "5-Series5")
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
