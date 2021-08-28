# Just documenting the problem setup.
print("N Lennard-Jones atoms are randomly places in a box.\n26 periodic images of each atom in this box are then generated.\nAverage distance and angle are calculated.\nFractional coordinate are used for distances and degress for angles.\nHopefully, this code means something!")

import numpy as n
import matplotlib.pyplot as p

N = int(input("Number of atoms you want to simulate: "))

# Generating random coordinates
r = n.random.rand(N, 3)

# A function that creates periodic images of each set of x-y-z coordinates
def PeriodicImages(R):
    a = []
    s = [-1, 0, 1] # Remeber, we are using fractional coordinates, so the length of the cubic box is 1.
    for i in s:
        x = R[0] + i
        for j in s:
            y = R[1] + j
            for k in s:
                z = R[2] + k
                a.append([x, y, z])
    coordinates = n.array(a)
    return coordinates

# Testing the function is working as intended
atom = PeriodicImages(r[0])
print(atom)
print("Shape:", n.shape(atom))

# Here, and before calculating distances and angles, pair potential shall be calculated and minimized. I have been trying to do this for two weeks but the algorithms are just too long (and Allen & Tildesley are awful writers).

# Putting all coordinates in one list in preparation of distance and angle calculations
AllCoordinates = []
for i in range(n.shape(r)[0]):
    AllCoordinates.extend(PeriodicImages(r[i]))

Distances = []
Angles = []
for i in AllCoordinates:
    for j in AllCoordinates:
        if (i != j).all(): # Doesn't calculate distances and angles for identical coordinates
            d = n.sqrt( (i[0]-j[0])**2 + (i[1]-j[1])**2 + (i[2]-j[2])**2 )
            Distances.append(d)
            if d <= 1.0:
                ang = n.degrees(n.arccos((n.dot(i, n.transpose(j))) / (n.linalg.norm(i)*n.linalg.norm(j)))) # Messy but correct
                Angles.append(ang)

AngleDist = n.array(Angles)

AverageDistance = sum(Distances)/len(Distances)
print("Average distance in fractional units =", AverageDistance)

AverageAngle = sum(Angles)/len(Angles)
print("Average angle in degrees =", AverageAngle)

p.hist(AngleDist, bins = 100, density = True, histtype = 'step')
p.xlabel("Angles in degrees")
p.ylabel("Normalized frequency distribution")
p.show()
