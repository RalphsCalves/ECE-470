#!/usr/bin/env python

'''
We get inspirations of Tower of Hanoi algorithm from the website below.
This is also on the lab manual.
Source: https://www.cut-the-knot.org/recurrence/hanoi.shtml
'''

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
from lab2_header import *

# 20Hz
SPIN_RATE = 20

# UR3 home location
home = np.radians([159.45, -67.17, 90.18, -113.04, -90.17, 39.38])

# Hanoi tower location 1
Q11 = [145.76*pi/180.0, -54.86*pi/180.0, 91.51*pi/180.0, -126.67*pi/180.0, -90.23*pi/180.0, 25.62*pi/180.0]
Q12 = [145.76*pi/180.0, -49.64*pi/180.0, 93.6*pi/180.0, -133.98*pi/180.0, -90.25*pi/180.0, 25.59*pi/180.0]
Q13 = [146*pi/180.0, -44.43*pi/180.0, 94.59*pi/180.0, -140.18*pi/180.0, -90.27*pi/180.0, 25.80*pi/180.0]
Q21 = [159.46*pi/180.0, -59.52*pi/180.0, 99.74*pi/180.0, -130.25*pi/180.0, -90.21*pi/180.0, 39.36*pi/180.0]
Q22 = [159.48*pi/180.0, -53.41*pi/180.0, 100.40*pi/180.0, -137.03*pi/180.0, -90.23*pi/180.0, 39.33*pi/180.0]
Q23 = [159.49*pi/180.0, -48.12*pi/180.0, 102.67*pi/180.0, -144.58*pi/180.0, -90.25*pi/180.0, 39.32*pi/180.0]
Q31 = [171.41*pi/180.0, -57.51*pi/180.0, 96.60*pi/180.0, -129.13*pi/180.0, -90.23*pi/180.0, 51.68*pi/180.0]
Q32 = [171.75*pi/180.0, -52.35*pi/180.0, 98.58*pi/180.0, -136.27*pi/180.0, -90.25*pi/180.0, 51.61*pi/180.0]
Q33 = [171.77*pi/180.0, -46.29*pi/180.0, 99.43*pi/180.0, -143.18*pi/180.0, -90.28*pi/180.0, 51.58*pi/180.0]

thetas = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

digital_in_0 = 0
analog_in_0 = 0

suction_on = True
suction_off = False
current_io_0 = False
current_position_set = False

# UR3 current position, using home position for initialization
current_position = copy.deepcopy(home)

############## Your Code Start Here ##############
"""
TODO: Initialize Q matrix
"""

Q = [ [Q11, Q12, Q13], \
      [Q21, Q22, Q23], \
      [Q31, Q32, Q33] ]
############### Your Code End Here ###############

############## Your Code Start Here ##############

"""
TODO: define a ROS topic callback funtion for getting the state of suction cup
Whenever ur3/gripper_input publishes info this callback function is called.
"""
def gripped_callback(msg):

    global digital_in_0
    global analog_in_0

    digital_in_0 = msg.DIGIN
    analog_in_0 = msg.AIN0




############### Your Code End Here ###############


"""
Whenever ur3/position publishes info, this callback function is called.
"""
def position_callback(msg):

    global thetas
    global current_position
    global current_position_set
    
    thetas[0] = msg.position[0]
    thetas[1] = msg.position[1]
    thetas[2] = msg.position[2]
    thetas[3] = msg.position[3]
    thetas[4] = msg.position[4]
    thetas[5] = msg.position[5]

    current_position[0] = thetas[0]
    current_position[1] = thetas[1]
    current_position[2] = thetas[2]
    current_position[3] = thetas[3]
    current_position[4] = thetas[4]
    current_position[5] = thetas[5]

    current_position_set = True


def gripper(pub_cmd, loop_rate, io_0):

    global SPIN_RATE
    global thetas
    global current_io_0
    global current_position

    error = 0
    spin_count = 0
    at_goal = 0

    current_io_0 = io_0

    driver_msg = command()
    driver_msg.destination = current_position
    driver_msg.v = 1.0
    driver_msg.a = 1.0
    driver_msg.io_0 = io_0
    pub_cmd.publish(driver_msg)

    while(at_goal == 0):

        if( abs(thetas[0]-driver_msg.destination[0]) < 0.0005 and \
            abs(thetas[1]-driver_msg.destination[1]) < 0.0005 and \
            abs(thetas[2]-driver_msg.destination[2]) < 0.0005 and \
            abs(thetas[3]-driver_msg.destination[3]) < 0.0005 and \
            abs(thetas[4]-driver_msg.destination[4]) < 0.0005 and \
            abs(thetas[5]-driver_msg.destination[5]) < 0.0005 ):

            at_goal = 1

        loop_rate.sleep()

        if(spin_count >  SPIN_RATE*5):

            pub_cmd.publish(driver_msg)
            rospy.loginfo("Just published again driver_msg")
            spin_count = 0

        spin_count = spin_count + 1

    return error


def move_arm(pub_cmd, loop_rate, dest, vel, accel):

    global thetas
    global SPIN_RATE

    error = 0
    spin_count = 0
    at_goal = 0

    driver_msg = command()
    driver_msg.destination = dest
    driver_msg.v = vel
    driver_msg.a = accel
    driver_msg.io_0 = current_io_0
    pub_cmd.publish(driver_msg)

    loop_rate.sleep()

    while(at_goal == 0):

        if( abs(thetas[0]-driver_msg.destination[0]) < 0.0005 and \
            abs(thetas[1]-driver_msg.destination[1]) < 0.0005 and \
            abs(thetas[2]-driver_msg.destination[2]) < 0.0005 and \
            abs(thetas[3]-driver_msg.destination[3]) < 0.0005 and \
            abs(thetas[4]-driver_msg.destination[4]) < 0.0005 and \
            abs(thetas[5]-driver_msg.destination[5]) < 0.0005 ):

            at_goal = 1
            rospy.loginfo("Goal is reached!")

        loop_rate.sleep()

        if(spin_count >  SPIN_RATE*5):

            pub_cmd.publish(driver_msg)
            rospy.loginfo("Just published again driver_msg")
            spin_count = 0

        spin_count = spin_count + 1

    return error


############## Your Code Start Here ##############

def move_block(pub_cmd, loop_rate, start_loc, start_height, \
               end_loc, end_height):
    global Q
    global home
    global digital_in_0

    ### Hint: Use the Q array to map out your towers by location and "height".

    error = 0
    rospy.loginfo("Moving to start location: " + str(start_loc) + " " + str(start_height))
    move_arm(pub_cmd,loop_rate,Q[start_loc-1][start_height-1],4.0,4.0)
    rospy.loginfo("Gripping")
    gripper(pub_cmd,loop_rate,suction_on)
    time.sleep(1.0)
    if digital_in_0 == False:
        rospy.loginfo("Block Missing; Moving back to home ...")
        move_arm(pub_cmd,loop_rate,home,4.0,4.0)
        rospy.loginfo("Ungripping")
        gripper(pub_cmd,loop_rate,suction_off)
        sys.exit()
    rospy.loginfo("Moving to home location")
    move_arm(pub_cmd,loop_rate,home,4.0,4.0)
    rospy.loginfo("Moving to end location: " + str(end_loc) + " " + str(end_height))
    move_arm(pub_cmd,loop_rate,Q[end_loc-1][end_height-1],4.0,4.0)
    rospy.loginfo("Ungripping")
    gripper(pub_cmd,loop_rate,suction_off)
    rospy.loginfo("Last: Moving to home location")
    move_arm(pub_cmd,loop_rate,home,4.0,4.0)



    return error


############### Your Code End Here ###############


def main():

    global home
    global Q
    global SPIN_RATE

    # Initialize ROS node
    rospy.init_node('lab2node')

    # Initialize publisher for ur3/command with buffer size of 10
    pub_command = rospy.Publisher('ur3/command', command, queue_size=10)

    # Initialize subscriber to ur3/position and callback fuction
    # each time data is published
    sub_position = rospy.Subscriber('ur3/position', position, position_callback)

    ############## Your Code Start Here ##############
    # TODO: define a ROS subscriber for ur3/gripper_input message and corresponding callback function
    sub_gripped = rospy.Subscriber('ur3/gripper_input', gripper_input, gripped_callback)

    ############### Your Code End Here ###############


    ############## Your Code Start Here ##############
    # TODO: modify the code below so that program can get user input

    input_done = 0
    loop_count = 0

    while(not input_done):
        start_loc = raw_input("Enter the Start Location <Either 1 2 3 or 0 to quit> ")
        print("Entered Start Location: " + start_loc + "\n")

        if(int(start_loc) == 1 or int(start_loc) == 2 or int(start_loc) == 3):
            input_done = 1
            start_loc = int(start_loc)
        elif (int(start_loc) == 0):
            print("Quitting... ")
            sys.exit()
        else:
            print("Please just enter the character 1 2 3 for the Start Location or 0 to quit \n\n")

    input_done = 0
    while(not input_done):
        end_loc = raw_input("Enter the End Location <Either 1 2 3 or 0 to quit>")
        print("Entered End Location: " + end_loc + "\n")

        if(int(end_loc) == start_loc):
            print("Overlap with the Start Location; Please choose another End Location \n\n")
        elif((int(end_loc) == 1 or int(end_loc) == 2 or int(end_loc) == 3) and int(end_loc) != start_loc):
            input_done = 1
            end_loc = int(end_loc)
        elif (int(end_loc) == 0):
            print("Quitting... ")
            sys.exit()
        else:
            print("Please just enter the character 1 2 3 for the End Location or 0 to quit \n\n")

    buffer_loc = 1
    if (start_loc == 1 and end_loc == 2) or (start_loc == 2 and end_loc == 1):
        buffer_loc = 3
    elif (start_loc == 1 and end_loc == 3) or (start_loc == 3 and end_loc == 1):
        buffer_loc = 2



    ############### Your Code End Here ###############

    # Check if ROS is ready for operation
    while(rospy.is_shutdown()):
        print("ROS is shutdown!")

    rospy.loginfo("Sending Goals ...")

    loop_rate = rospy.Rate(SPIN_RATE)

    ############## Your Code Start Here ##############
    # TODO: modify the code so that UR3 can move tower accordingly from user input

    not_gripped = False

    rospy.loginfo("Home Movement ...")
    move_arm(pub_command,loop_rate,home,4.0,4.0)

    rospy.loginfo("First Movement ...")
    move_block(pub_command, loop_rate, start_loc, 1, end_loc, 3)

    rospy.loginfo("Second Movement ...")
    move_block(pub_command, loop_rate, start_loc, 2, buffer_loc, 3)

    rospy.loginfo("Third Movement ...")
    move_block(pub_command, loop_rate, end_loc, 3, buffer_loc, 2)

    rospy.loginfo("Fourth Movement ...")
    move_block(pub_command, loop_rate, start_loc, 3, end_loc, 3)

    rospy.loginfo("Fifth Movement ...")
    move_block(pub_command, loop_rate, buffer_loc, 2, start_loc, 3)

    rospy.loginfo("Sixth Movement ...")
    move_block(pub_command, loop_rate, buffer_loc, 3, end_loc, 2)

    rospy.loginfo("Seventh Movement ...")
    move_block(pub_command, loop_rate, start_loc, 3, end_loc, 1)

    rospy.loginfo("Finished")


    ############### Your Code End Here ###############



if __name__ == '__main__':

    try:
        main()
    # When Ctrl+C is executed, it catches the exception
    except rospy.ROSInterruptException:
        pass
