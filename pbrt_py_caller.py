# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os
import math  
import re
import csv
import numpy as np
from tqdm import tqdm
import random

def materialGenerator():
    Kd1 = [0, .3, .6, .95]
    Kd2 = [0, .3, .6, .95]
    Kd3 = [0, .3, .6, .95]
    Ks = [0, .33, .66, 1]
    Kr = [0, .33, .66, 1]
    Kt = [0, .33, .66, 1]
    roughness = [0.01, 0.05, 0.2 , 0.75]
    
    materials_list = []
    
    for p in Kd1:
        for q in Kd2:
            for r in Kd3:
                for s in Kr:
                    for t in Ks:
                        for u in Kt:
                            for v in roughness:            
                                materials_list.append([
                                    p, q, r, 
                                    s+np.random.uniform(low=-.1,high=.1), s+np.random.uniform(low=-.1,high=.1),
                                    s+np.random.uniform(low=-.1,high=.1), t+np.random.uniform(low=-.1,high=.1), 
                                    t+np.random.uniform(low=-.1,high=.1), t+np.random.uniform(low=-.1,high=.1),
                                    u+np.random.uniform(low=-.1,high=.1), u+np.random.uniform(low=-.1,high=.1), 
                                    u+np.random.uniform(low=-.1,high=.1), 
                                    v])
    
    materials_list = np.array(materials_list)
    
    return np.clip(materials_list, 0, 1)


 
def materialGenerator2():
    arr = np.random.rand(20000, 13)
    return arr


def materialFileWriter(filename, materials):
   with open(filename, 'w+') as f:
       f.write('MakeNamedMaterial \"custommaterial\" \"string type\" \"uber\"\n' + '\n\"rgb Kd\" [' + str(materials[0]) + ' ' + str(materials[1]) + ' ' + str(materials[2]) +' \n\"rgb Kr\" [' + str(materials[3]) + ' ' + str(materials[4]) + ' ' + str(materials[5]) + '] ' + '\n\"rgb Ks\" [' + str(materials[6]) + ' ' + str(materials[7]) + ' ' + str(materials[8]) + '] ' + '\n\"rgb Kt\" [' + str(materials[9]) + ' ' + str(materials[10]) + ' ' + str(materials[11]) + '] '+ '\n\"float roughness\" [' + str(materials[12]) + ']\n')
       f.close()

def getPhi(x, y, z):
    return math.atan2(math.sqrt(x*x + z * z), y)

def getTheta(x, y, z):
    return math.atan2(x, -z)


def getRadius(x, y, z):
    return math.sqrt(x*x + y * y + z * z)

def getX(radius, theta, phi):
    #std::cout << std::endl << std::endl << radius * sin(phi*0.01745) * cos(theta*0.01745) << " ::: theta is " << theta << "phi is" << phi << "radius is " << radius << std::endl;
    return radius * math.sin(phi*0.01745) * math.cos(theta*0.01745);


def getY(radius, theta, phi):
    return radius * math.sin(phi*0.01745) * math.sin(theta*0.01745);


def getZ(radius, theta, phi):
    return radius * math.cos(phi*0.01745);

def generateCameraPoses():
    radius = 2
    camera_poses = []
    for phi in range(20, 90, 30):
        for theta in range(1, 360, 45):
            camera_poses.append([getX(radius, theta, phi), getY(radius, theta, phi),getZ(radius, theta, phi), phi, theta])
    return camera_poses            
    

def main():
    materials_set = np.loadtxt('materials.txt', delimiter=', ')
    material_index = 1

    for counter in tqdm(range(len(materials_set))):
        materials = materials_set[counter]
        mf = open("materials.pbrt", "w+")
        mf.write('MakeNamedMaterial \"custommaterial\" \"string type\" \"uber\"\n' + '\n\"rgb Kd\" [' + str(materials[0]) + ' ' + str(materials[1]) + ' ' + str(materials[2]) + ']'+ '\n\"rgb Ks\" [' + str(materials[3]) + ' ' + str(materials[4]) + ' ' + str(materials[5]) + '] ' + '\n\"float roughness\" [' + str(materials[6]) + ']\n')
        mf.close()
                
        if((material_index-1)%500==0):
            directory = 'data_'+str(1+(material_index//500))
            if not os.path.exists(directory):
                os.mkdir(directory)
        
        cam_poses = generateCameraPoses()

        for cam_pos in cam_poses:
            cf = open("camera.pbrt", "w+")
            ff = open("film.pbrt", "w+")
            cf.write("LookAt ")
            cf.write("\n%f %f %f\n0 0 0\n0 1 0" % (cam_pos[0], cam_pos[2], cam_pos[1]))
            ff.write("Film \"image\" \"string filename\" \"%s_%s_%s.png\" \"integer xresolution\" [128] \"integer yresolution\" [128]" %  (str(directory) +"/"+ str(material_index), str(cam_pos[3]), str(cam_pos[4])) )
            cf.close()
            ff.close()
            os.system(r"/home/farhan/Farhan_Thesis_Codes/pbrt-v3/cmake-build-release/pbrt --quiet --nthreads=128 scene.pbrt")
            #os.rename("/home/farhan/Farhan_Thesis_Codes/pbrt_experiments/kitchen/materials_props.txt", "materials_phi_%s_theta_%s.txt" %  (str(cam_pos[3]), str(cam_pos[4])))
        
        material_index += 1

    #np_cam = np.asarray(all_camera, dtype=np.float32)
    #np.savetxt('/home/farhan/Farhan_Thesis_Codes/pbrt_experiments/spheres-final/camera_poses.txt', all_camera, delimiter=', ', fmt='%.4f')

main()



