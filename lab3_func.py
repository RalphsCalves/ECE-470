import os
import argparse
import copy
import time
import rospy
import rospkg
import numpy as np
import yaml
import sys
from math import pi

# for UR3 Robot
def Get_MS():

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

def get_S(w, v):
    return np.array([[      0, -1*w[2],    w[1], v[0]],
                     [   w[2],       0, -1*w[0], v[1]],
                     [-1*w[1],    w[0],       0, v[2]],
                     [      0,       0,       0,    0]
                     ])

def lab_fk(theta1, theta2, theta3, theta4, theta5, theta6):

    # Initialize the return_value
    return_value = [None, None, None, None, None, None]
    print("Foward kinematics calculated:\n")

    M, S = Get_MS()
    T = M
    theta = [theta1, theta2, theta3, theta4, theta5, theta6]
    for i in range(5,-1,-1):
        T = np.matmul(expm(S[i]*theta[i]),T)

    print(str(T) + "\n")

    return_value[0] = theta1 + PI
    return_value[1] = theta2
    return_value[2] = theta3
    return_value[3] = theta4 - (0.5*PI)
    return_value[4] = theta5
    return_value[5] = theta6

    return return_value

def main():

	global home

	# Initialize ROS node
	rospy.init_node('lab3node')

    # Initialize publisher for ur3/command with buffer size of 10
	pub_command = rospy.Publisher('ur3/command', command, queue_size=10)

	# Initialize subscriber to ur3/position & ur3/gripper_input and callback fuction
	# each time data is published
	sub_position = rospy.Subscriber('ur3/position', position, position_callback)
	sub_input = rospy.Subscriber('ur3/gripper_input', gripper_input, input_callback)

	new_dest = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

	if(len(sys.argv) != 7):
		print("\n")
		print("Command should be entered in degrees with format: \n")
		print("rosrun lab3pkg_py lab3_exec.py theta1 theta2 theta3 theta4 theta5 theta6 \n")
	else:
		print("\ntheta1: " + sys.argv[1] + ", theta2: " + sys.argv[2] + \
			  ", theta3: " + sys.argv[3] + ", theta4: " + sys.argv[4] + \
			  ", theta5: " + sys.argv[5] + ", theta6: " + sys.argv[6] + "\n")

	new_dest = lab_fk(float(sys.argv[1])*PI/180.0, float(sys.argv[2])*PI/180.0, \
		              float(sys.argv[3])*PI/180.0, float(sys.argv[4])*PI/180.0, \
		              float(sys.argv[5])*PI/180.0, float(sys.argv[6])*PI/180.0,)


	vel = 4.0
	accel = 4.0

	# Check if ROS is ready for operation
	while(rospy.is_shutdown()):
		print("ROS is shutdown!")

	# Initialize the rate to publish to ur3/command
	loop_rate = rospy.Rate(SPIN_RATE)

	move_arm(pub_command, loop_rate, new_dest, vel, accel)

	rospy.loginfo("Destination is reached!")



if __name__ == '__main__':

	try:
		main()
    # When Ctrl+C is executed, it catches the exception
	except rospy.ROSInterruptException:
		pass
