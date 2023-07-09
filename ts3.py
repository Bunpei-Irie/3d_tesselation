# -*- coding: utf-8 -*-
"""
Created on Mon May 29 08:36:35 2023

@author: fhm22672
"""
import argparse
import math

parser = argparse.ArgumentParser() # create a parser
# parser.add_argument('-v','--verbose',help='verbose level', action='store_true')
parser.add_argument('-l','--lazy', action='store_true', help='plot half of the triangles')
parser.add_argument('-v', '--verbose', type=int, default = 0, help='debug level')
parser.add_argument('-p', '--point', type=int, default = 10, help='number of sampling points')
parser.add_argument('-m', '--multi', type=int, default = 1, help='number of repetition')
args = parser.parse_args() # parse
N = args.point
if N < 2:
    print("N must be >= 2 !")
    exit(1)
id = 1
v = [[[0 for i in range(N)] for j in range(N)] for k in range(3)]
w = [[[0 for i in range(N)] for j in range(N)] for k in range(3)]
radius = [] # distance of the current point from z-axis
suf = [] # suf[]=0,1,2,...,N-1,N-2,...,0
for k in range(N):
    suf.append(k)
    radius.append(math.sqrt(math.tan(math.pi * k / 4.0 / (N - 1))**2 + 1))
for k in range(N,N*2-1):
      suf.append((N-1)*2-k)
if args.verbose:
      print("suf=",suf)
      print("radius=",radius)

class vertex():
#%%
    def __init__(self, coord):
        global id
        self.coord = (coord)
        self.id = id
        if args.verbose:
            print("v %f %f %f #%d"%(self.coord[0],self.coord[1],self.coord[2],id))
        else:
            print("v %f %f %f"%(self.coord[0],self.coord[1],self.coord[2]))
        id+=1
        
#%%
    def set_faces(x0, y0, z0, sgnx, sgny, sgnz):
        for i in range(N):
            angle = float(i) *math.pi / 4.0 / float(N - 1) # angle as to x-y plane
            if N - i - 1 > 0:
                step = math.pi / 2.0 / float(N - 1)
            if args.verbose:
                print("i=%d angle=%fπ step=%fπ"%(i,angle/math.pi,step/math.pi))
            for j in range(N-i):
                k = suf[i]
                l = radius[k] # distance of the current point from z-axis
                x = l * math.cos(angle) # x-xoordinate of the current point
                y = l * math.sin(angle) # y-xoordinate of the current point
                z = 2.0 - math.tan( float(i) * math.pi / 4.0 / (N - 1))
                if args.verbose:
                    print("i=%d j=%d theta=%f*pi l=%f (x,y,z)=(%f,%f,%f)"%(i,j,angle/math.pi,l,x,y,z))
                v[0][i][j] = vertex((sgnx*x + x0, sgny*y + y0, sgnz*z + z0))
                v[1][i][j] = vertex((sgnx*y + x0, sgny*z + y0, sgnz*x + z0))
                v[2][i][j] = vertex((sgnx*z + x0, sgny*x + y0, sgnz*y + z0))
                p = - z + 2
                q = - y + 2
                r = - x + 2
                w[0][i][j] = vertex((sgnx*p + x0, sgny*q + y0, sgnz*r + z0))
                w[1][i][j] = vertex((sgnx*q + x0, sgny*r + y0, sgnz*p + z0))
                w[2][i][j] = vertex((sgnx*r + x0, sgny*p + y0, sgnz*q + z0))
                angle += step

        for k in range(3):
            if args.verbose:
                print("k=%d"%k)
            for i in range(N-1):
                if args.verbose:
                    print("i=%d"%i)
                for j in range(N-1-i):
                    if args.verbose:
                        print("j=%d"%j)
                    if args.verbose < 2:
                        print("f %d %d %d"%(v[k][i][j].id, v[k][i+1][j].id, v[k][i][j+1].id))
                        if args.lazy == False:
                            print("f %d %d %d"%(w[k][i][j].id, w[k][i+1][j].id, w[k][i][j+1].id))
                        if j < N-2-i:
                            if args.lazy == False:
                                print("f %d %d %d"%(v[k][i][j+1].id, v[k][i+1][j].id, v[k][i+1][j+1].id))                        
                            print("f %d %d %d"%(w[k][i][j+1].id, w[k][i+1][j].id, w[k][i+1][j+1].id))                        

#%%
def set_data(x0, y0, z0):
    vertex.set_faces(x0, y0, z0, +1.0, +1.0, +1.0)
    vertex.set_faces(x0, y0, z0, +1.0, +1.0, -1.0)
    vertex.set_faces(x0, y0, z0, +1.0, -1.0, +1.0)
    vertex.set_faces(x0, y0, z0, +1.0, -1.0, -1.0)
    vertex.set_faces(x0, y0, z0, -1.0, +1.0, +1.0)
    vertex.set_faces(x0, y0, z0, -1.0, +1.0, -1.0)
    vertex.set_faces(x0, y0, z0, -1.0, -1.0, +1.0)
    vertex.set_faces(x0, y0, z0, -1.0, -1.0, -1.0)
    
#%%
if __name__ == '__main__':
    for i in range(-2 * (args.multi - 1), 2 * (args.multi + 1), 4):
        for j in range(-2 * (args.multi - 1), 2 * (args.multi + 1), 4):
            for k in range(-2 * (args.multi - 1), 2 * (args.multi + 1), 4):
                set_data(i, j, k)
