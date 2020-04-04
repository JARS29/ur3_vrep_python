#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 11:58:37 2020
03
36
@author: jars
"""


import sys
import sim, simConst
import time
from operator import add
import numpy as np

opmode=sim.simx_opmode_oneshot_wait
def get_joint_handle(clientID, object_type=simConst.sim_object_joint_type, mode=opmode):
    UR3_joints={} 
    _, ids,_,_,names= sim.simxGetObjectGroupData(clientID,object_type, 0,mode)
    #_, ids,_,rot,_= sim.simxGetObjectGroupData(clientID,object_type, 5,mode)
    c=0
    #d=0
    for i in names:
        UR3_joints[i]=[ids[c]]
        #UR3_joints[i]=[ids[c], rot[d:d+3]]
        c=c+1    
        #d=d+3
    return UR3_joints

def get_joint_orientation(ClientID,JointID, relativeTo=-1, mode= opmode):
    return sim.simxGetObjectOrientation(ClientID, JointID, relativeTo, mode)[1]
    

def set_joint_orientation(ClientID, JointID, angle, mode=opmode):
    sim.simxSetJointTargetPosition(clientID, JointID, np.deg2rad(angle), mode)
    print('La junta ' + str(JointID) + ' se ha configurado en la siguiente orientacion ' + str(angle))
    return 0

def set_joint_velocity(clientID, JointID, targetVelocity, mode=opmode):
    return 0


try:
    
    sim.simxFinish(-1) #Terminar todas las conexiones
    clientID=sim.simxStart('127.0.0.1',19997,True,True,5000,5) # Connect to CoppeliaSim 
    if clientID!=-1:
        print ('Conexion establecida')
    else:
        sys.exit("Error: no se puede conectar") #Terminar este script
except:
    print('Check if CoppeliaSim is open')


UR3_joints_IP=get_joint_handle(clientID) #Getting the reference
for i in UR3_joints_IP:
    UR3_joints_IP[i].append(get_joint_orientation(clientID, UR3_joints_IP[i][0]))
    #print(get_joint_orientation(clientID, UR3_joints_IP[i]))

         
#J1z,J2z,J3Z
#Practica 30 grados j1, 15 grados j2, 30 grados j3, 20 grados j4, 15 grados j5, 10 grados j6
new_angles=[60,25,10,30,15,50]

c=0

sim.simxSynchronous(clientID,True)
sim.simxSynchronousTrigger(clientID) 
sim.simxStartSimulation(clientID, sim.simx_opmode_blocking)


for i in UR3_joints_IP:
    set_joint_orientation(clientID, UR3_joints_IP[i][0],new_angles[c], mode=sim.simx_opmode_blocking) #Todas las juntas posicion inicial
    c=c+1

time.sleep(5)
sim.simxStopSimulation(clientID, sim.simx_opmode_blocking)

sim.simxFinish(clientID)
