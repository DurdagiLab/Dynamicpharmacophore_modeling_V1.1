#!/bin/bash
read -p "To generate grid of your Protein-Ligand complex i need to be sure about your Ligand ID, Can you write the ID again Please? " -r r1
parent=$r1
for i in *.maegz;do
        name=${i%.maegz}
        $SCHRODINGER/utilities/generate_glide_grids -rec_file $name.maegz -lig_asl "res.ptype $parent" -j $name -write_in
done
