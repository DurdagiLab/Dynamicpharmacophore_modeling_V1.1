#!/bin/bash

for z in structure_*.maegz;do
        st=${z%.maegz}
        $SCHRODINGER18/run pv_convert.py -mode split_receptor $st.maegz -o structure-$st.maegz
        $SCHRODINGER18/run pv_convert.py -mode split_ligand $st.maegz -o ligand-$st.maegz
done

