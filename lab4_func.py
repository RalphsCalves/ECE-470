#!/usr/bin/env python
import numpy as np
from scipy.linalg import expm
from lab4_header import *
import math

"""
Use 'expm' for matrix exponential.
Angles are in radian, distance are in meters.
"""
def Get_MS():
    # =================== Your code starts here ====================#
    # Fill in the correct values for a1~6 and q1~6, as well as the M matrix
    #M = np.eye(4)
    #S = np.zeros((6,6))

    w_1 = np.array([0,0,1]).T
    w_2 = np.array([0,1,0]).T
    w_3 = np.array([0,1,0]).T
    w_4 = np.array([0,1,0]).T
    w_5 = np.array([1,0,0]).T
    w_6 = np.array([0,1,0]).T

    q_1 = np.array([-0.150, 0.150, 0.162]).T
    q_2 = np.array([-0.150, 0.270, 0.162]).T
    q_3 = np.array([ 0.094, 0.270, 0.162]).T
    q_4 = np.array([ 0.307, 0.177, 0.162]).T
    q_5 = np.array([ 0.307, 0.260, 0.162]).T
    q_6 = np.array([ 0.390, 0.260, 0.162]).T

    v_1 = np.cross(w_1, (-1*q_1))
    v_2 = np.cross(w_2, (-1*q_2))
    v_3 = np.cross(w_3, (-1*q_3))
    v_4 = np.cross(w_4, (-1*q_4))
    v_5 = np.cross(w_5, (-1*q_5))
    v_6 = np.cross(w_6, (-1*q_6))

    S_1 = get_S(w_1.T,v_1.T)
    S_2 = get_S(w_2.T,v_2.T)
    S_3 = get_S(w_3.T,v_3.T)
    S_4 = get_S(w_4.T,v_4.T)
    S_5 = get_S(w_5.T,v_5.T)
    S_6 = get_S(w_6.T,v_6.T)

    S = np.array([S_1,S_2,S_3,S_4,S_5,S_6])

    M = np.array([[0, -1, 0, 0.390],
    [0, 0, -1, 0.402],
    [1, 0, 0, 0.220],
    [0, 0, 0, 1]])

    return M, S
    # ==============================================================#
    

def get_S(w, v):
    return np.array([[      0, -1*w[2],    w[1], v[0]],
                     [   w[2],       0, -1*w[0], v[1]],
                     [-1*w[1],    w[0],       0, v[2]],
                     [      0,       0,       0,    0]])


"""
Function that calculates encoder numbers for each motor
"""
def lab_fk(theta1, theta2, theta3, theta4, theta5, theta6):

    # Initialize the return_value
    return_value = [None, None, None, None, None, None]

    print("Foward kinematics calculated:\n")

    # =================== Your code starts here ====================#
    theta = np.array([theta1,theta2,theta3,theta4,theta5,theta6])
    T = np.eye(4)

    M, S = Get_MS()
    T = M
    
    for i in range(5,-1,-1):
      T = np.matmul(expm(S[i]*theta[i]),T)
      
    return_value[0] = theta1 + PI
    return_value[1] = theta2
    return_value[2] = theta3
    return_value[3] = theta4 - (0.5*PI)
    return_value[4] = theta5
    return_value[5] = theta6

    return return_value


# ==============================================================#




"""
Function that calculates an elbow up Inverse Kinematic solution for the UR3
"""
def lab_invk(xWgrip, yWgrip, zWgrip, yaw_WgripDegree):
    # =================== Your code starts here ====================#
    # get theta 5
    theta_5 = -1*(np.pi/2)
    # Convert Yaw angle from degree to radian
    yaw_rad = deg_to_rad(yaw_WgripDegree)
    # Convert gripper's frame from base frame to frame zero
    x_grip, y_grip, z_grip = base_to_zero(xWgrip, yWgrip, zWgrip)
    # Get the center point
    x_cen, y_cen, z_cen = get_xyz_center(x_grip, y_grip, z_grip, yaw_rad)

    theta_1 = get_theta_1(x_cen, y_cen, z_cen)

    theta_6 = get_theta_6(theta_1, yaw_rad)

    x_3end, y_3end, z_3end = get_xyz_3end(theta_1, x_cen, y_cen, z_cen)

    theta_2, theta_3, theta_4 = get_theta_2_3_4(x_3end, y_3end, z_3end)

    return lab_fk(theta_1, theta_2, theta_3, theta_4, theta_5, theta_6)



# ==============================================================#
def deg_to_rad(degree):
    return np.radians(degree)

def base_to_zero(xWgrip, yWgrip, zWgrip):
    x_grip = xWgrip + 0.150
    y_grip = yWgrip - 0.150
    z_grip = zWgrip - 0.010

    return x_grip, y_grip, z_grip

def get_xyz_center(x_grip, y_grip, z_grip, yaw_rad):
    x_cen = x_grip - np.cos(yaw_rad)*0.0535
    y_cen = y_grip - np.sin(yaw_rad)*0.0535
    z_cen = z_grip

    return x_cen, y_cen, z_cen

def get_theta_1(x_cen, y_cen, z_cen):
    return math.atan2(y_cen, x_cen) - np.arcsin((0.11)/(np.sqrt((x_cen**2)+(y_cen**2))))

def get_theta_6(theta_1, yaw_rad):
    return np.pi/2 + theta_1 - yaw_rad

def get_xyz_3end(theta_1, x_cen, y_cen, z_cen):
    x_3end = x_cen - 0.083*np.cos(theta_1) + 0.083*np.sin(theta_1) + 0.027*np.sin(theta_1)
    y_3end = y_cen - 0.083*np.sin(theta_1) - 0.083*np.cos(theta_1) - 0.027*np.cos(theta_1)
    z_3end = 0.059 + 0.082 + z_cen

    return x_3end, y_3end, z_3end

def get_theta_2_3_4(x_3end, y_3end, z_3end):
    norm = np.sqrt(x_3end**2 + y_3end**2 + (z_3end-0.152)**2)

    theta_2 = -1*(np.arccos((0.244**2 + norm**2 - 0.213**2)/(2*0.244*norm)) + math.atan2(np.sqrt((z_3end-0.152)**2), np.sqrt((x_3end**2+y_3end**2))))
    theta_3 = np.pi - np.arccos((0.213**2 + 0.244**2 - norm**2)/(2*0.213*0.244))
    theta_4 = -1*theta_2 - theta_3
    
    return theta_2, theta_3, theta_4
