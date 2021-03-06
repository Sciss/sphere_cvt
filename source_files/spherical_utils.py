import numpy as np
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from math import *

########################################################################
########################################################################
def get_lat_long(x):
     """ Calculates the latitude and longitude of a cartesian point.
          
     This is the geocentric latitude and longitude, i.e. the polar and
     aximuth angles.
     
     Args
          x -- a point on the surface in cartesian coordinates

     Returns
          latitude -- the latitude of the point (polar angle)
          longitude -- the longitude of the point (azimuth angle)
     """
     
     r = sqrt(x[0]**2 + x[1]**2 + x[2]**2)
     longitude = degrees(atan2(x[1],x[0]))
     latitude = degrees(asin(x[2]/r))
     
     #wrap latitude to [-90,90)
     #latitude = latitude - 90
     
     return latitude, longitude

def get_cartesian(lat, lon):
    lat=radians(lat)
    lon=radians(lon)
    x = np.cos(lat) * np.cos(lon)
    y = np.cos(lat) * np.sin(lon)
    z = np.sin(lat)
    
    return np.array([x, y, z])
    
########################################################################
########################################################################
def distance_euclidean(x, y):
     """ Returns the Euclidean distance between two points
     
     Args
          x, y -- two numpy arrays representing points in R^3
          
     Returns
          d -- the Euclidean distance between x and y
          
     """
     
     return sqrt((x[0]-y[0])**2 + (x[1]-y[1])**2 + (x[2]-y[2])**2)
     
########################################################################
########################################################################
def project_to_unit_sphere(x):
     """ Projects a point inside the unit sphere to a point on the 
     surface.
     
     Args
          x -- a numpy array representing the cartesian coordinates of 
               a point inside the unit sphere
               
     Returns
          p -- the projection on x onto the surface of the unit sphere
          
     """
     
     # compute spherical coordinates of x
     r = sqrt(x[0]**2 + x[1]**2 + x[2]**2)
     azimuth = atan2(x[1],x[0])
     polar = acos(x[2]/r)
     
     # compute cartesian coordinates of a point p with same azimuth and
     # polar angles as x, but with radius 1
     x1 = cos(azimuth)*sin(polar)
     y1 = sin(azimuth)*sin(polar)
     z1 = cos(polar)
     
     p = np.array([x1,y1,z1])
     
     return p

def project_onto_lower_plane(x):
    t = np.array([0,0,-1])
    
    s = 2 / np.dot(t, x + t)
    
    p = (s * x + (s - 1) * t)[:2]

    return p

def project_onto_lower_sphere(e):
    n = np.array([0,0,1])
    e = np.array([e[0],e[1],-1])
    return 1 / (4 + np.dot(e, e)) * (4*e - (4 - np.dot(e, e))*n)
    
def project_onto_upper_plane(x):
    t = np.array([0,0,1])
    
    s = 2 / np.dot(t, x + t)
    
    p = (s * x + (s - 1) * t )[:2]
    
    return p
    
def project_onto_upper_sphere(e):
    n = np.array([0,0,-1])
    e = np.array([e[0],e[1],1])
    return 1 / (4 + np.dot(e, e)) * (4*e - (4 - np.dot(e, e))*n)
   
def cir_rad_center(p1, p2, p3):
    p1_p2 = np.linalg.norm(p1 - p2)
    p2_p3 = np.linalg.norm(p2 - p3)
    p3_p1 = np.linalg.norm(p3 - p1)
    p1_p3 = np.linalg.norm(p1 - p3)
    
    rad_den = 2 * np.linalg.norm(np.cross(p1 - p2, p2 - p3))
    
    radius = p1_p2 * p2_p3 * p3_p1 / rad_den
    
    cen_den = 2 * np.linalg.norm(np.cross(p1 - p2, p2 - p3)) ** 2
    
    al = p2_p3 ** 2 * np.dot(p1 - p2, p1 - p3) / cen_den
    be = p1_p3 ** 2 * np.dot(p2 - p1, p2 - p3) / cen_den
    ga = p1_p2 ** 2 * np.dot(p3 - p1, p3 - p2) / cen_den
    
    center = al * p1 + be * p2 + ga * p3    
    
    return radius, center

def init_sphere():
     phi, theta = np.mgrid[0.0:pi:10j, 0.0:2.0*pi:25j]
     xx = np.sin(phi)*np.cos(theta)
     yy = np.sin(phi)*np.sin(theta)
     zz = np.cos(phi)
     
     fig = plt.figure()
     ax = fig.add_subplot(111, projection='3d')
     ax.plot_surface(
          xx, yy, zz,  rstride=1, cstride=1, color='c', alpha=0.3, linewidth=0)
     
     return ax
     
"""Clears Sphere"""
def disp_sphere(ax): 
     ax.set_xlim([-1,1])
     ax.set_ylim([-1,1])
     ax.set_zlim([-1,1])
     ax.set_aspect("equal")
     #plt.tight_layout()
     plt.show()
         
########################################################################
########################################################################
def sphere_points(ax, x):   
     for xi in x:
          ax.scatter(xi[0],xi[1],xi[2],color="k",s=20)
   
def sphere_line(ax, u, v, c = 'k'):
    #Makes parameterized line between points  
    r = 20
    
    t = np.linspace(0, 1, r)      
    w = v - u        
    x = u[0] + t*w[0]
    y = u[1] + t*w[1]
    z = u[2] + t*w[2]

    #Projects points on line onto unit sphere
    for i in range(r):
        pt1 = np.array([x[i],y[i],z[i]])
        new_pt1 = project_to_unit_sphere(pt1)
    
        x[i] = new_pt1[0]
        y[i] = new_pt1[1]
        z[i] = new_pt1[2]
    
    ax.plot(x, y, z, color=c)
    
def sphere_line2(ax, u, v, c = 'k'):
    #Makes parameterized line between points  
    r = 20
    
    t = np.linspace(0, 1, r)      
    w = np.cross(np.cross(u,v),u)     
    x = u[0] + t*w[0]
    y = u[1] + t*w[1]
    z = u[2] + t*w[2]

    #Projects points on line onto unit sphere
    for i in range(r):
        pt1 = np.array([x[i],y[i],z[i]])
        new_pt1 = project_to_unit_sphere(pt1)
    
        x[i] = new_pt1[0]
        y[i] = new_pt1[1]
        z[i] = new_pt1[2]
    
    ax.plot(x, y, z, color=c)


    
def project_onto_tan_sphere(e, t):
    t = np.asarray(t)    
    e = np.array([e[0],e[1],1])
    return 1 / (4 + np.dot(e, e)) * (4*e - (4 - np.dot(e, e))*t)
    
def project_onto_tan_plane(x, t):
    t = np.asarray(t)
    s = 2 / np.dot(t, x + t)
        
    return (s * x + (s - 1) * t )[:2]
