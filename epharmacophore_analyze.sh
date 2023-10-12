#!/bin/bash
./art.py
read -p "Please Give the path of your MD output file : " -r r1
parent=$r1
cp featureFromRMSD.py ePharm.sh grid_Gen.sh quotes.sh split.sh art.py backbone_align.sh trjwrite.sh $parent/
cd $parent
echo $parent
#./art.py
echo "Your MD out-cms file aligned on backbone of frame 0 ..."
./backbone_align.sh
echo "All your trajectories are write in individual files ... "
./trjwrite.sh
mkdir TRJ/
mv *.maegz TRJ/
cp featureFromRMSD.py ePharm.sh grid_Gen.sh quotes.sh split.sh art.py TRJ/
cd TRJ/
./quotes.sh
./grid_Gen.sh
./quotes.sh
./split.sh
./quotes.sh
./ePharm.sh
python ./featureFromRMSD.py

echo "█▄█ █▀█ █░█ █▀█   ░░█ █▀█ █▄▄   █ █▀   █▀▀ █▀█ █▀▄▀█ █▀█ █░░ █▀▀ ▀█▀ █▀▀ "
echo "░█░ █▄█ █▄█ █▀▄   █▄█ █▄█ █▄█   █ ▄█   █▄▄ █▄█ █░▀░█ █▀▀ █▄▄ ██▄ ░█░ ██▄ "

echo "ᴀɴᴀʟʏᴢᴇ ɪs ᴄᴏᴍᴘʟᴇᴛᴇ ᴀɴᴅ ʏᴏᴜ ᴄᴀɴ ғɪɴᴅ ʀᴇsᴜʟᴛ ɪɴ ᴛʜᴇ ᴘᴀᴛʜ ʏᴏᴜ ɢɪᴠᴇ ᴛᴏ sᴀᴠᴇ ғɪɢᴜʀᴇs"
