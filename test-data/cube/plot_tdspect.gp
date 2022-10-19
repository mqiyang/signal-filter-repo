set term pngcairo enhanced size 1200, 960 square

unset key

set output "vals_alongx.png"
set pm3d map 
set mxtics 1
set xrange [-1:2]
set cbrange [-0.002:0.002]
set yrange[0:0.06*800]
# unset cbrange
splot "td_xfil_dpdt.dat" matrix u ((-2.5+$1*0.07)):($2*0.06):3


# set output "vals_alongx.png"
# set pm3d map 
# set size 0.9, 1
# unset xrange
# unset yrange
# set palette defined (-0.03 "blue", 0 "white", 0.03 "red")
# set xtics ("-0.5" -0.5, "H" -0.3306292207, "O" 0, "C" 1.3626150697, "H" 1.4892309327, "H" 1.5407431623, "C" 2.0418068713, "C" 2.0590797360, "C"  3.4389159956, "C" 3.4573836308, "H" 3.9590876682, "H" 3.9967231013, "C" 4.1598046373, "N" 5.5414526820, "H" 6.0481831800, "H" 6.0653068925 )  
# set ytics 200
# set yrange [0:3500]
# set mytics 100
# set mxtics 1
# set xrange [-3:8]
# set cbrange [-0.02:0.02]
# # unset cbrange
# splot "td_xdpdt.dat" matrix u ((-5.66917838+$1*0.20786987)*0.529177249 ):($2*4+1):3


# # set output "filter_cm.png"
# # set pm3d map interpolate 0,0
# # unset xrange
# # unset yrange
# # set palette defined (0 "blue", 0.15 "white", 0.3 "red")
# # set xtics ('-3' -3, '-2' -2, '-1' -1,'Br' 0, '1' 1,'C' 1.90015880, 'C' 3.10009804, 'C' 4.632, 'C' 5.8, 'H' 6.8)  
# # set xrange [-3:8]
# # set ytics 200
# # set yrange [0:2500]
# # set mytics 10
# # set mxtics 1
# # # set cbrange [0:0.5]
# # set cbrange [-0.08:0.08]
# # # unset cbrange
# # splot "td_fil_holez.dat" matrix u ((-1.88972612e+01+$1*0.31495435)*0.529177249 ):($2+1):(-1*$3)
