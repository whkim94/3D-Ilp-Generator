# Jonathan Kim
# Project
# Extending 2D ILP generator to handle 3D cases.
# December 14, 2017

import sys


arg1 = sys.argv[1]
arg2 = sys.argv[2]

INFILE = open(arg1, "r")  # open the file specified by the value of arg1, to read from the file.
OUT = open(arg2, "w")     # open the file specified by the value of arg2, to write to the file.

sequence = ""
constraints = "\n"  # assign the string `such that \n\n' to the variable `constraints'
objective = ""
Econstraints = ""
binaries = "binary \n"

for sequence in INFILE:
    sequence = sequence.rstrip()

n = len(sequence)
print('%s, %d' % (sequence,n))
diam = n - (int)(n*0.2)

print('diameter %d' % (diam))
diamsquared = diam**2
diamcubic = diam**3


# loop through the edges in the diam-by-diam grid to set up
# the objective function, and also set up the inequalities to count 
# the number of edges whose endpoints are both assigned a character whose
# value is 1.

k = 1
kp1 = 0

for z  in xrange(1, diam+1):
    for i  in xrange(1, diam+1):
        for j  in xrange(1, diam+1):
            if j < diam:
                kp1 = k + 1 # horizontal edges
                objective = objective + "+ C"+ str(k) + "," + str(kp1) + " "
                Econstraints = Econstraints + "I" + str(k) + " + I" + str(kp1) + " - 2 C" + str(k) + "," + str(kp1) + " >= 0\n"  # C can be set to 1 only if both endpoints are assigned 1s. 
                binaries = binaries + "C" + str(k) + "," + str(kp1) + "\n"

            if i < diam:
                kpn = k + diam # vertical edges
                objective = objective + "+ C" + str(k) + "," + str(kpn) + " "
                Econstraints = Econstraints + "I" + str(k) + " + I" + str(kpn) + " - 2 C" + str(k) + "," + str(kpn) + " >= 0\n"
                binaries = binaries + "C" + str(k) + "," + str(kpn) + "\n"

            if z < diam:
                kpz = k + diamsquared # z edges
                objective = objective + "+ C" + str(k) + "," + str(kpz) + " "
                Econstraints = Econstraints + "I" + str(k) + " + I" + str(kpz) + " - 2 C" + str(k) + "," + str(kpz) + " >= 0\n"
                binaries = binaries + "C" + str(k) + "," + str(kpz) + "\n"

            k += 1
    print('z: %d k: %d' % (z,k-1))
    #k += 1   # increment k to account for the last node in each row.


for i in xrange(1, n+1):   # set up inequalities to ensure each character is assigned to one position
    for pos in xrange(1, diamcubic+1):
        constraints = constraints + "+ X" + str(i) + "," + str(pos) + " "
        binaries = binaries + "X" + str(i) + "," + str(pos) + "\n"

    constraints = constraints + "=  1 \n"


for pos in xrange(1, diamcubic+1):   # set up inequalties to ensure each position is assigned at most one character
    for i in xrange (1, n+1):
        constraints = constraints + "+ X" + str(i) + "," + str(pos) + " "

    constraints = constraints + "<= 1 \n"


# create inequalities to ensure that chars i and i+1 are neighbors on the grid
# first takecare of the general cases, and then do the external rows and columns.  

gridbase = diamsquared + diam + 2 # second plane's second row's second point

for plane in xrange(2, diam):       # middle planes
    for row in xrange(2, diam):     # middle rows of middle planes 
        for offset in xrange(0, diam-2):
            point = gridbase + offset
            for i  in xrange(1, n):       # each char position i in sequence
                ip1 = i + 1               # the next char poistion
                pointp1 = point + 1          # right point
                pointn1 = point - 1          # left point
                pointpn = point + diam       # down point
                pointnn = point - diam       # up point
                pointpz = point + diamsquared # back point
                pointzz = point - diamsquared # front point


                constraints = constraints + "X" + str(i) + "," + str(point) + " "
                constraints = constraints + "- X" + str(ip1) + "," + str(pointp1) + " - X" + str(ip1) + "," + str(pointn1) + " - X" + str(ip1) + "," + str(pointpn) + " - X" + str(ip1) + "," + str(pointnn) + " - X" + str(ip1) + "," + str(pointpz) + " - X" + str(ip1) + "," + str(pointzz) + " <= 0\n"
        #constraints = constraints + "end of middle rows and first plane\n"        
        gridbase += diam
    gridbase += diamsquared


gridbase = diam + 2     # fisrt plane's second row's second point

for row in xrange(2, diam):     # middle rows of first plane
    for offset in xrange(0, diam-2):
        point = gridbase + offset
        for i  in xrange(1, n):       # each char position i in sequence
            ip1 = i + 1               # the next char poistion
            pointp1 = point + 1          # right point
            pointn1 = point - 1          # left point
            pointpn = point + diam       # down point
            pointnn = point - diam       # up point
            pointpz = point + diamsquared # back point
            pointzz = point - diamsquared # front point


            constraints = constraints + "X" + str(i) + "," + str(point) + " "
            constraints = constraints + "- X" + str(ip1) + "," + str(pointp1) + " - X" + str(ip1) + "," + str(pointn1) + " - X" + str(ip1) + "," + str(pointpn) + " - X" + str(ip1) + "," + str(pointnn) + " - X" + str(ip1) + "," + str(pointpz)+ " <= 0\n"
    #constraints = constraints + "end of middle rows and first plane\n"        
    gridbase += diam


gridbase = diamsquared * (diam - 1) + diam + 2    # last plane's second row's second point

for row in xrange(2, diam):     # middle rows of last plane
    for offset in xrange(0, diam-2):
        point = gridbase + offset
        for i  in xrange(1, n):       # each char position i in sequence
            ip1 = i + 1               # the next char poistion
            pointp1 = point + 1          # right point
            pointn1 = point - 1          # left point
            pointpn = point + diam       # down point
            pointnn = point - diam       # up point
            pointpz = point + diamsquared # back point
            pointzz = point - diamsquared # front point


            constraints = constraints + "X" + str(i) + "," + str(point) + " "
            constraints = constraints + "- X" + str(ip1) + "," + str(pointp1) + " - X" + str(ip1) + "," + str(pointn1) + " - X" + str(ip1) + "," + str(pointpn) + " - X" + str(ip1) + "," + str(pointnn) + " - X" + str(ip1) + "," + str(pointzz)+ " <= 0\n"
    #constraints = constraints + "end of middle rows of last plane\n"        
    gridbase += diam


#---------------------------------------

# middle planes' first rows, last rows care without corners

gridbase = diamsquared + 2
for plane in xrange(2, diam):       # middle planes
    for offset in xrange(0, diam-2):# take care of the middle plane's first rows of the grid, minus the points in the
                                    # first and last columns.
        point = gridbase + offset
        for i in xrange(1, n):
            ip1 = i + 1
            pointp1 = point + 1          # right point
            pointn1 = point - 1          # left point
            pointpn = point + diam       # down point
            pointnn = point - diam       # up point
            pointpz = point + diamsquared # back point
            pointzz = point - diamsquared # front point

            constraints = constraints + "X" + str(i) + "," + str(point) + " "
            constraints = constraints + "- X" + str(ip1) + "," + str(pointp1) + " - X" + str(ip1) + "," + str(pointn1) + " - X" + str(ip1) + "," + str(pointpn) + " - X" + str(ip1) + "," + str(pointpz) + " - X" + str(ip1) + "," + str(pointzz) + " <= 0\n"

            if pointn1 < 0:
                print("YIKES1.1\n")
    gridbase += diamsquared 
        #constraints = constraints + "end of first rows\n"


gridbase = diam * (diam - 1) + diamsquared + 2
for plane in xrange(2, diam):       # middle planes
    for offset in xrange(0, diam-2):# take care of the middle plane's last rows of the grid, minus the points in the
                                    # first and last columns.
        point = gridbase + offset
        for i in xrange(1, n):
            ip1 = i + 1
            pointp1 = point + 1          # right point
            pointn1 = point - 1          # left point
            pointpn = point + diam       # down point
            pointnn = point - diam       # up point
            pointpz = point + diamsquared # back point
            pointzz = point - diamsquared # front point

            constraints = constraints + "X" + str(i) + "," + str(point) + " "
            constraints = constraints + "- X" + str(ip1) + "," + str(pointp1) + " - X" + str(ip1) + "," + str(pointn1) + " - X" + str(ip1) + "," + str(pointnn) + " - X" + str(ip1) + "," + str(pointpz) + " - X" + str(ip1) + "," + str(pointzz) + " <= 0\n"

            if pointn1 < 0:
                print("YIKES1.2\n")
    gridbase += diamsquared 
        #constraints = constraints + "end of last rows\n"


#---------------------------------------

# middle planes' first cols, last cols care without corners 

gridbase = diamsquared + diam + 1
for plane in xrange(2, diam):       # middle planes
    for offset in xrange(0, diam-2):# take care of the middle plane's first colds of the grid, minus the points in the
                                    # first and last columns.
        point = gridbase + offset * diam
        for i in xrange(1, n):
            ip1 = i + 1
            pointp1 = point + 1          # right point
            pointn1 = point - 1          # left point
            pointpn = point + diam       # down point
            pointnn = point - diam       # up point
            pointpz = point + diamsquared # back point
            pointzz = point - diamsquared # front point

            constraints = constraints + "X" + str(i) + "," + str(point) + " "
            constraints = constraints + "- X" + str(ip1) + "," + str(pointp1) + " - X" + str(ip1) + "," + str(pointpn) + " - X" + str(ip1) + "," + str(pointnn) + " - X" + str(ip1) + "," + str(pointpz) + " - X" + str(ip1) + "," + str(pointzz) + " <= 0\n"

            if pointn1 < 0:
                print("YIKES1.1\n")
    gridbase += diamsquared 
        #constraints = constraints + "end of first rows\n"


gridbase = diamsquared + (diam*2)
for plane in xrange(2, diam):       # middle planes
    for offset in xrange(0, diam-2):# take care of the middle plane's last cols of the grid, minus the points in the
                                    # first and last rowss.
        point = gridbase + offset * diam
        for i in xrange(1, n):
            ip1 = i + 1
            pointp1 = point + 1          # right point
            pointn1 = point - 1          # left point
            pointpn = point + diam       # down point
            pointnn = point - diam       # up point
            pointpz = point + diamsquared # back point
            pointzz = point - diamsquared # front point

            constraints = constraints + "X" + str(i) + "," + str(point) + " "
            constraints = constraints + "- X" + str(ip1) + "," + str(pointn1) + " - X" + str(ip1) + "," + str(pointpn) + " - X" + str(ip1) + "," + str(pointnn) + " - X" + str(ip1) + "," + str(pointpz) + " - X" + str(ip1) + "," + str(pointzz) + " <= 0\n"

            if pointn1 < 0:
                print("YIKES1.2\n")
    gridbase += diamsquared 
       # constraints = constraints + "end of last rows\n"

#--------------------------------------------

# fisrt plane's row, col care without corners

gridbase = 2
for offset in xrange(0, diam-2):# take care of the fisrt plane's first row of the grid, minus the points in the
                                # first and last columns.
    point = gridbase + offset
    for i in xrange(1, n):
        ip1 = i + 1
        pointp1 = point + 1          # right point
        pointn1 = point - 1          # left point
        pointpn = point + diam       # down point
        pointnn = point - diam       # up point
        pointpz = point + diamsquared # back point
        pointzz = point - diamsquared # front point

        constraints = constraints + "X" + str(i) + "," + str(point) + " "
        constraints = constraints + "- X" + str(ip1) + "," + str(pointp1) + " - X" + str(ip1) + "," + str(pointn1) + " - X" + str(ip1) + "," + str(pointpn) + " - X" + str(ip1) + "," + str(pointpz) + " <= 0\n"

        if pointn1 < 0:
            print("YIKES1\n")
    #constraints = constraints + "end of first rows\n" 


gridbase = diam * (diam - 1) + 2
for offset in xrange(0, diam-2):# take care of the first plane's last row of the grid, minus the points in the
                                # first and last columns.
    point = gridbase + offset
    for i in xrange(1, n):
        ip1 = i + 1
        pointp1 = point + 1          # right point
        pointn1 = point - 1          # left point
        pointpn = point + diam       # down point
        pointnn = point - diam       # up point
        pointpz = point + diamsquared # back point
        pointzz = point - diamsquared # front point

        constraints = constraints + "X" + str(i) + "," + str(point) + " "
        constraints = constraints + "- X" + str(ip1) + "," + str(pointp1) + " - X" + str(ip1) + "," + str(pointn1) + " - X" + str(ip1) + "," + str(pointnn) + " - X" + str(ip1) + "," + str(pointpz) + " <= 0\n"

        if pointn1 < 0:
            print("YIKES2\n")


gridbase = diam  + 1
for offset in xrange (0, diam-2): # take care of the first plane's first column minus the corners.
    point = gridbase + offset * diam
    for i  in xrange (1, n):
        ip1 = i + 1
        pointp1 = point + 1          # right point
        pointn1 = point - 1          # left point
        pointpn = point + diam       # down point
        pointnn = point - diam       # up point
        pointpz = point + diamsquared # back point
        pointzz = point - diamsquared # front point

        constraints = constraints + "X" + str(i) + "," + str(point) + " "
        constraints = constraints + "- X" + str(ip1) + "," + str(pointp1) + " - X" + str(ip1) + "," + str(pointpn) + " - X" + str(ip1) + "," + str(pointnn) + " - X" + str(ip1) + "," + str(pointpz) + " <= 0\n"

        if pointn1 < 0:
            print("YIKES3")


gridbase = 2*diam
for offset in xrange(0, diam-2): # take care of the first planes' last column minus the corners.
    point = gridbase + offset * diam
    for i in xrange(1, n):
        ip1 = i + 1
        pointp1 = point + 1          # right point
        pointn1 = point - 1          # left point
        pointpn = point + diam       # down point
        pointnn = point - diam       # up point
        pointpz = point + diamsquared # back point
        pointzz = point - diamsquared # front point

        constraints = constraints + "X" + str(i) + "," + str(point) + " "
        constraints = constraints + "- X" + str(ip1) + "," + str(pointn1) + " - X" + str(ip1) + "," + str(pointpn) + " - X" + str(ip1) + "," + str(pointnn) + " - X" + str(ip1) + "," + str(pointpz) + " <= 0\n"

        if pointn1 < 0:
            print("YIKES4")
            #print("$i, $ip1, $gridbase, $offset, $point, $pointn1, $pointpn, $pointnn \n")
            print('%d, %d, %d, %d, %d, %d, %d, %d' % (i, ip1, gridbase, offset, point, pointn1, pointpn, pointnn))

#--------------------------------------------------------------


# last plane's row, col care without corners

gridbase = diamsquared * (diam - 1) + 2
for offset in xrange(0, diam-2):# take care of the last plane's first row of the grid, minus the points in the
                                # first and last columns.
    point = gridbase + offset
    for i in xrange(1, n):
        ip1 = i + 1
        pointp1 = point + 1          # right point
        pointn1 = point - 1          # left point
        pointpn = point + diam       # down point
        pointnn = point - diam       # up point
        pointpz = point + diamsquared # back point
        pointzz = point - diamsquared # front point

        constraints = constraints + "X" + str(i) + "," + str(point) + " "
        constraints = constraints + "- X" + str(ip1) + "," + str(pointp1) + " - X" + str(ip1) + "," + str(pointn1) + " - X" + str(ip1) + "," + str(pointpn) + " - X" + str(ip1) + "," + str(pointzz) + " <= 0\n"

        if pointn1 < 0:
            print("YIKES1\n")
    #constraints = constraints + "end of last plane's first rows\n" 


gridbase = (diamsquared * (diam - 1)) + (diam * (diam -1)) + 2
for offset in xrange(0, diam-2):# take care of the last plane's last row of the grid, minus the points in the
                                # first and last columns.
    point = gridbase + offset
    for i in xrange(1, n):
        ip1 = i + 1
        pointp1 = point + 1          # right point
        pointn1 = point - 1          # left point
        pointpn = point + diam       # down point
        pointnn = point - diam       # up point
        pointpz = point + diamsquared # back point
        pointzz = point - diamsquared # front point

        constraints = constraints + "X" + str(i) + "," + str(point) + " "
        constraints = constraints + "- X" + str(ip1) + "," + str(pointp1) + " - X" + str(ip1) + "," + str(pointn1) + " - X" + str(ip1) + "," + str(pointnn) + " - X" + str(ip1) + "," + str(pointzz) + " <= 0\n"

        if pointn1 < 0:
            print("YIKES2\n")


gridbase = diamsquared * (diam-1) + diam + 1
for offset in xrange (0, diam-2): # take care of the last plane's first column minus the corners.
    point = gridbase + offset * diam
    for i  in xrange (1, n):
        ip1 = i + 1
        pointp1 = point + 1          # right point
        pointn1 = point - 1          # left point
        pointpn = point + diam       # down point
        pointnn = point - diam       # up point
        pointpz = point + diamsquared # back point
        pointzz = point - diamsquared # front point

        constraints = constraints + "X" + str(i) + "," + str(point) + " "
        constraints = constraints + "- X" + str(ip1) + "," + str(pointp1) + " - X" + str(ip1) + "," + str(pointpn) + " - X" + str(ip1) + "," + str(pointnn) + " - X" + str(ip1) + "," + str(pointzz) + " <= 0\n"

        if pointn1 < 0:
            print("YIKES3")


gridbase = (diamsquared * (diam-1)) + (diam*2)
for offset in xrange(0, diam-2): # take care of the last planes' last column minus the corners.
    point = gridbase + offset * diam
    for i in xrange(1, n):
        ip1 = i + 1
        pointp1 = point + 1          # right point
        pointn1 = point - 1          # left point
        pointpn = point + diam       # down point
        pointnn = point - diam       # up point
        pointpz = point + diamsquared # back point
        pointzz = point - diamsquared # front point

        constraints = constraints + "X" + str(i) + "," + str(point) + " "
        constraints = constraints + "- X" + str(ip1) + "," + str(pointn1) + " - X" + str(ip1) + "," + str(pointpn) + " - X" + str(ip1) + "," + str(pointnn) + " - X" + str(ip1) + "," + str(pointzz) + " <= 0\n"

        if pointn1 < 0:
            print("YIKES4")
            print('%d, %d, %d, %d, %d, %d, %d, %d' % (i, ip1, gridbase, offset, point, pointn1, pointpn, pointnn))

#constraints += "Middle corner starts \n"
#--------------------------------------------------------------------

# take care of the middle corners

checker = [diamsquared + 1, diamsquared + diam, diam * (diam-1) + diamsquared + 1, diamsquared + diamsquared]
for plane  in  xrange(2, diam):
    for i  in xrange(1, n):
        for point in checker:  # take care of the corner cases
            ip1 = i + 1
            pointp1 = point + 1          # right point
            pointn1 = point - 1          # left point
            pointpn = point + diam       # down point
            pointnn = point - diam       # up point
            pointpz = point + diamsquared # back point
            pointzz = point - diamsquared # front point

              
            if point == checker[0]:
                constraints = constraints + "X" + str(i) + "," + str(point) + " "
                constraints = constraints + "- X" + str(ip1) + "," + str(pointp1) + " - X" + str(ip1) + "," + str(pointpn) + " - X" + str(ip1) + "," + str(pointpz) + " - X" + str(ip1) + "," + str(pointzz) + " <= 0\n"

                if pointn1 < 0:
                    print("YIKES5")

            if point == checker[2]:
                constraints = constraints + "X" + str(i) + "," + str(point) + " "
                constraints = constraints + "- X" + str(ip1) + "," + str(pointp1) + " - X" + str(ip1) + "," + str(pointnn) + " - X" + str(ip1) + "," + str(pointpz) + " - X" + str(ip1) + "," + str(pointzz) + " <= 0\n"


            if point == checker[1]:
                constraints = constraints + "X" + str(i) + "," + str(point) + " "
                constraints = constraints + "- X" + str(ip1) + "," + str(pointn1) + " - X" + str(ip1) + "," + str(pointpn) + " - X" + str(ip1) + "," + str(pointpz) + " - X" + str(ip1) + "," + str(pointzz) + " <= 0\n"


            if point == checker[3]:
                constraints = constraints + "X" + str(i) + "," + str(point) + " "
                constraints = constraints + "- X" + str(ip1) + "," + str(pointn1) + " - X" + str(ip1) + "," + str(pointnn) + " - X" + str(ip1) + "," + str(pointpz) + " - X" + str(ip1) + "," + str(pointzz) + " <= 0\n"

                if pointn1 < 0:
                    print("YIKES6")
    checker[0] += diamsquared
    checker[1] += diamsquared
    checker[2] += diamsquared
    checker[3] += diamsquared
    #print("%d %d %d %d" % (checker[0],checker[1],checker[2],checker[3]))

#constraints += "Only corner starts \n"
#------------------------------------------------------
# take care of the corners

checkers = [1, diam, diam * (diam-1) + 1, diamsquared, diamsquared*(diam-1)+1, diamsquared*(diam-1)+diam, (diamsquared*(diam-1)) + (diam * (diam-1) + 1), diamcubic]
for i  in xrange(1, n):
    for point in checkers:  # take care of the corner cases
        ip1 = i + 1
        pointp1 = point + 1          # right point
        pointn1 = point - 1          # left point
        pointpn = point + diam       # down point
        pointnn = point - diam       # up point
        pointpz = point + diamsquared # back point
        pointzz = point - diamsquared # front point

          
        if point == 1:
            constraints = constraints + "X" + str(i) + "," + str(point) + " "
            constraints = constraints + "- X" + str(ip1) + "," + str(pointp1) + " - X" + str(ip1) + "," + str(pointpn) + " - X" + str(ip1) + "," + str(pointpz) + " <= 0\n"

            if pointn1 < 0:
                print("YIKES5")

        if point == diam * (diam - 1) + 1:
            constraints = constraints + "X" + str(i) + "," + str(point) + " "
            constraints = constraints + "- X" + str(ip1) + "," + str(pointp1) + " - X" + str(ip1) + "," + str(pointnn) + " - X" + str(ip1) + "," + str(pointpz) + " <= 0\n"


        if point == diam:
            constraints = constraints + "X" + str(i) + "," + str(point) + " "
            constraints = constraints + "- X" + str(ip1) + "," + str(pointn1) + " - X" + str(ip1) + "," + str(pointpn) + " - X" + str(ip1) + "," + str(pointpz) + " <= 0\n"


        if point == diamsquared:
            constraints = constraints + "X" + str(i) + "," + str(point) + " "
            constraints = constraints + "- X" + str(ip1) + "," + str(pointn1) + " - X" + str(ip1) + "," + str(pointnn) + " - X" + str(ip1) + "," + str(pointpz) + " <= 0\n"

            if pointn1 < 0:
                print("YIKES6")

        if point == checkers[4]:
            constraints = constraints + "X" + str(i) + "," + str(point) + " "
            constraints = constraints + "- X" + str(ip1) + "," + str(pointp1) + " - X" + str(ip1) + "," + str(pointpn) + " - X" + str(ip1) + "," + str(pointzz) + " <= 0\n"

            if pointn1 < 0:
                print("YIKES5")

        if point == checkers[5]:
            constraints = constraints + "X" + str(i) + "," + str(point) + " "
            constraints = constraints + "- X" + str(ip1) + "," + str(pointp1) + " - X" + str(ip1) + "," + str(pointnn) + " - X" + str(ip1) + "," + str(pointzz) + " <= 0\n"


        if point == checkers[6]:
            constraints = constraints + "X" + str(i) + "," + str(point) + " "
            constraints = constraints + "- X" + str(ip1) + "," + str(pointn1) + " - X" + str(ip1) + "," + str(pointpn) + " - X" + str(ip1) + "," + str(pointzz) + " <= 0\n"


        if point == checkers[7]:
            constraints = constraints + "X" + str(i) + "," + str(point) + " "
            constraints = constraints + "- X" + str(ip1) + "," + str(pointn1) + " - X" + str(ip1) + "," + str(pointnn) + " - X" + str(ip1) + "," + str(pointzz) + " <= 0\n"

            if pointn1 < 0:
                print("YIKES6")


# Now we create the inequalities to determine if a point has been assigned a 1 or not. Assign I$i to 1 if and only if
# grid point $i has been assigned a 1

inputs  = list(sequence)
ones = {}
lastchar = 0
neighbors1 = 0

for char in xrange(0, n):        # use hash %ones to record the positions of the 1s in the sequence, and count
                               # the number of adjacent 1s. The objective function is reduced by that count.        
    print('%d %s' % (char,inputs[char])) 

    if inputs[char] == '1':
        if lastchar == 1:
            neighbors1 += 1   
        ones[char] = 1
        lastchar = 1

    else:
        lastchar = 0

print('Neighbor count: %d ' % neighbors1) 

# spiral way from center to outward



for pos in xrange(1, diamcubic+1):
    assigned1 = ""
    for char in sorted(ones.keys()):
        charp1 = char + 1
        assigned1 = assigned1 + "+ X" + str(charp1) + "," + str(pos) + " "

    binaries = binaries + "I" + str(pos) + " \n"
    constraints = constraints + assigned1 + "- I" + str(pos) + " = 0 \n"



INFILE.close()
OUT.write("Maximize \n")  # write to file the string (word) 'Maximize' and move to a new line (because of '\n')
OUT.write(objective + "- Offset \n\n")
OUT.write("subject to \n")
OUT.write("Offset = " + str(neighbors1) + "\n")
OUT.write(constraints + " \n\n")
OUT.write(Econstraints + " \n\n")
OUT.write(binaries + " \n")  # write to file the value of the variable 'binaries'
OUT.write("end")  # write to file the string (word) 'end'
OUT.close()


