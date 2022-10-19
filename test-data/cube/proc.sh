for i in {1..9}
do
    awk '{ printf $2"\t"} END{printf "\n"}' x_fil_dpdt.000000000$i.dat >> td_xfil_dpdt.dat
done

for i in {10..99}
do
    awk '{ printf $2"\t"} END{printf "\n"}' x_fil_dpdt.00000000$i.dat >> td_xfil_dpdt.dat
done

for i in {100..800}
do
    awk '{ printf $2"\t"} END{printf "\n"}' x_fil_dpdt.0000000$i.dat >> td_xfil_dpdt.dat
done
