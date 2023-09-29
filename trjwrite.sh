#!/bin/bash
for f in *_backbone-out.cms;
do
name=$f

for i in *_backbone_trj;do
trj=$i

read -p "What is your Ligand ID? " -r r1
parent=$r1
$SCHRODINGER/run trj2mae.py  -extract-asl "((res.ptype '$parent ' )) or ((protein))" $name $trj structure -s ::1 -separate -out-format MAE
done
done
