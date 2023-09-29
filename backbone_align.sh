#!/bin/bash
for f in desmond_md*-out.cms;
do
name=$f

for i in desmond_md*_trj;do
trj=$i

$SCHRODINGER/run trj_align.py $name $trj ${trj}_aligned_backbone -s ::1 -asl '( backbone )' -ref-frame 0
done
done
