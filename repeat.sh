#!/bin/bash
set -x
for i in {1..5}
do
   python generate_pci_input.py > result$i.txt
   
   PRIME=$(tail -1 result$i.txt 2>&1)
   ./compile.py --prime $PRIME tanegotiation

   Scripts/mascot.sh tanegotiation > resultmpc$i.txt
   # Scripts/mama.sh tanegotiation > resultmpc$i.txt
done


set +x

for i in {1..5}
do
   python process_output.py resultmpc$i.txt
   # tail -3 resultmpc$i.txt
   # echo ""
done
